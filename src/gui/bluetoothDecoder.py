from queue import Queue

MODES = {
	0: 'Voltmeter',
	1: 'Ammeter',
	2: 'Ohmmeter',
}

# Add dividers and max/min when available here
ATTENUATION = {
	'Voltmeter': (0.001,    40,     0),
	'Ammeter': (0.001,    40,     -40),
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
		data = int.from_bytes(newData[2:4], 'big')
		print(data)
		for i in range(0, 6, 2):
                        self.bufferValues.append(int.from_bytes(newData[i:i+2], 'little', signed=True))
		self._updateAll()
		self.bufferValues.clear()

	@staticmethod
	def _decodeByte(byte: bytearray):
		data = int.from_bytes(byte, 'big')
		return data >> 4, data & 15

	def _getValue(self, mode):
		return self.bufferValues[mode]

	def getNextPoint(self):
		if self.fake:
			return next(self.fakegen)
		if self.storedData.empty():
			return None
		return self.storedData.get_nowait()

	def _updateAll(self):
		data = []
		for m in range(0, 3):
                        mode = MODES[m]
                        attenuation = ATTENUATION.get(mode, DEFAULT_ATTENUATION)
                        value = self._getValue(m)
                        value = value * attenuation[0]
                        data.append({
                                "type": mode,
                                "max_y": attenuation[1],
                                "min_y": attenuation[2],
                                "value": value,
                        })
		self.storedData.put(data)

	def _fakeGenerator(self, starting_at):
		from random import randint
		current = starting_at
		while True:
			x = []
			for m in range(0, 3):
                                x.append({
                                        "type": MODES[m],
                                        "max_y": 40,
                                        "min_y": 40,
                                        "value": current,
                                })
			y = current + randint(-1,1)
			if -40 < y < 40:
				current = y
			yield x
