from queue import Queue

MODES = {
	0: 'Light Sensor',
	1: 'Temperature Sensor',
	2: 'Voltmeter',
	3: 'Ammeter',
	4: 'Ohmmeter',
}

# Add dividers and max/min when available here
ATTENUATION = {
	0: {'Voltmeter': (0.00001,  0.4,    -0.4),      'Ohmmeter': (.001,  400,        0)},
	1: {'Voltmeter': (0.0001,   4.0,    -4.0),      'Ohmmeter': (0.1,   4000,       0)},
	2: {'Voltmeter': (0.001,    40,     -40),       'Ohmmeter': (1,     40000,      0)},
	3: {'Voltmeter': (0.01,     400,    -400),      'Ohmmeter': (10,    400000,     0)},
	4: {'Voltmeter': (0.1,      4000,   -4000),     'Ohmmeter': (100,   4000000,    0)},
	5: {'Voltmeter': (1,        40000,  -40000),    'Ohmmeter': (1000,  40000000,   0)},
}

DEFAULT_ATTENUATION = (1, 40000, -40000)


class BluetoothDecoder:
	def __init__(self, fake=False):
		self.bufferValues = []
		self.storedData = Queue()
		self.fake = fake
		if fake:
			self.fakegen = self._fakeGenerator(10)

	def addNextByte(self, newData):
		if newData:
			code, meaning = self._decodeByte(newData)
			if code == len(self.bufferValues):
				self.bufferValues.append(meaning)
			elif code != len(self.bufferValues) - 1 or self.bufferValues[code] != meaning:
				self.bufferValues.clear()
			if len(self.bufferValues) == 7:
				self._updateAll()
				self.bufferValues.clear()

	@staticmethod
	def _decodeByte(byte: bytearray):
		data = int.from_bytes(byte, 'big')
		return data >> 4, data & 15

	def _getValue(self):
		value = 0
		digits = self.bufferValues[1:6]
		digits.reverse()
		for i, digit in enumerate(digits):
			value += digit * (10 ** i)
		value -= 100000 if value > 50000 else 0
		return value

	def getNextPoint(self):
		if self.fake:
			return next(self.fakegen)
		if self.storedData.empty():
			return None
		return self.storedData.get_nowait()

	def _updateAll(self):
		mode = MODES[self.bufferValues[0]]
		attenuation = ATTENUATION.get(
			self.bufferValues[6], DEFAULT_ATTENUATION).get(mode, DEFAULT_ATTENUATION)
		value = self._getValue()
		value = value * attenuation[0]
		self.storedData.put({
			"type": mode,
			"max_y": attenuation[1],
			"min_y": attenuation[2],
			"value": value,
		})

	def _fakeGenerator(self, starting_at):
		from random import randint
		current = starting_at
		while True:
			x = {
				"type": 'Voltmeter',
				"max_y": 40,
				"min_y": -40,
				"value": current,
			}
			y = current + randint(-1,1)
			if -40 < y < 40:
				current = y
			yield x