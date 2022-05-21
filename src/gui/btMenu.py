import asyncio
import threading

from bluetoothDecoder import BluetoothDecoder
from kivy .app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, ObjectProperty
from kivy.uix.recycleview import RecycleView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from BLE_Windows_Mac import BLE
import multiMeterGui
import time

bluetooth = BLE()
decoder=BluetoothDecoder(fake=False)

def close_application(self):
	bluetooth.disconnectFromDevice()
	App.get_running_app().stop()
	Window.close()


class DeviceCell(Button):

	device = ObjectProperty()

	def on_release(self):
		print(f'selected {self.device.name}')
		"""TODO: complete cell connect press"""
		# Disconnect and existing connections
		bluetooth.disconnectFromDevice()

		# Update status to trying to connect
		self.status_bar.text = f'Trying to connect to {self.device.name}'

		# Attempt to connect
		bluetooth.address = self.device.address
		x=threading.Thread(target=bluetooth.startBluetoothConnection, args=(decoder,), daemon=True)
		x.start()
		#asyncio.run(bluetooth.connectAndGetData())
		time.sleep(7)

		# if connection success
		if bluetooth.getConnectionStatus():
			# Update status to connected
			self.status_bar.text = f'Connected to {self.device.name}'

			# Assign device to bluetooth connceted device
			multiMeterGui.bluetooth.address = self.device.address

			# If device not on Mydevice list Add to list

			# Start BlueTooth
			bluetooth.disconnectFromDevice()
			App.get_running_app().stop()

		# if connection failed
		self.status_bar.text = f'Failed to connect to {self.device.name}'



class DeviceRecycleView(RecycleView):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.data = []


class BtMenu(BoxLayout):

	devices = ListProperty()

	def bt_search_event(self):
		self.devices = asyncio.run(bluetooth.scanForDevices())
		recycleView = self.ids.devices_recycle_list
		recycleView.data = [
			{
				'text': f"{device.name}: {device.address}",
				'device': device,
				'status_bar': self.ids.status_status
			}
			for device in self.devices
		]




class BtMenuApp(App):
	def build(self):
		return BtMenu()


if __name__ == '__main__':
	multiMeterGui.FAKE_DECODER = False
	BtMenuApp().run()
	multiMeterGui.MultiMeterApp().run()
