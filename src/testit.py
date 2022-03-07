import unittest
from bluetoothDecoder import BluetoothDecoder


class MyTestCase(unittest.TestCase):
	def test_something(self):
		btd = BluetoothDecoder()
		aBytes = [0x02, 0x16, 0x20, 0x30, 0x40, 0x50, 0x64]
		byteArrays = []
		for b in aBytes:
			t = bytearray()
			t.append(b)
			byteArrays.append(t)
		for byte in byteArrays:
			btd.addNextByte(byte)
		x = btd.getNextPoint()
		print(x)

		self.assertEqual(40.0, x['value'])

	def testinput(cls) -> None:
		btd = BluetoothDecoder()
		with open('logFile.txt', 'r') as f:
			data = f.read()
		data = [bytearray(x,'utf-8') for x in data]
		for d in data:
			btd.addNextByte(d)



if __name__ == '__main__':
	unittest.main()
