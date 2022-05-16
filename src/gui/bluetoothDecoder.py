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
	'Voltmeter': (0.001,    40,     -40),
	'Ohmmeter': (1,     40000,      0)
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
		data = int.from_bytes(newData, 'big')
		print(data)
		for i in range(0, 4):
                        self.bufferValues.append((data >> (8*i)) % 256)
		self._updateAll()
		self.bufferValues.clear()

	@staticmethod
	def _decodeByte(byte: bytearray):
		data = int.from_bytes(byte, 'big')
		return data >> 4, data & 15

	def _getValue(self):
		value = self.bufferValues[3]
		value += self.bufferValues[2] << 8
		return value

	def getNextPoint(self):
		if self.fake:
			return next(self.fakegen)
		if self.storedData.empty():
			return None
		return self.storedData.get_nowait()

	def _updateAll(self):
		print(self.bufferValues)
		mode = MODES[self.bufferValues[1]]
		attenuation = ATTENUATION.get(mode, DEFAULT_ATTENUATION)
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
				"min_y": 40,
				"value": current,
			}
			y = current + randint(-1,1)
			if -40 < y < 40:
				current = y
			yield x
