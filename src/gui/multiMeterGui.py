from bluetoothDecoder import BluetoothDecoder
from BLE_Windows_Mac import BLE
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from multiMeterGraph import GraphLayout
from multiMeterGraph import GraphProfile
import random
from kivy.core.window import Window
from kivy.uix.togglebutton import ToggleButton
from kivy.utils import get_color_from_hex as rgb
from digitalDisplay import DigitalLayout
import threading
import btMenu

ModeButtonsOptions = ['V~', 'V=', 'A', 'Ω', 'C/F', 'Light', '+']

testpoint = 80
FAKE_DECODER = False

# Starting Environment
# kivy_venv\Scripts\activate
# cd ECS193Project\btmultimeter\src\gui
# python MultiMeterGUI.py

class ModeButton(Widget):

	def __init__(self, text, **kwargs):
		super(ModeButton, self).__init__(**kwargs)
		button = Button()
		button.width = self.width
		button.height = self.height
		button.pos = self.pos
		button.color = "red"
		button.text = kwargs.get('text')
		self.add_widget(button)


def add_new_button(self):
	print("Creating a new Button")

	outer_menu = self.parent.parent
	menu = outer_menu.children[1].children[0]

	menu.button_count += 1

	new_button = Button(text='New Button', size_hint=(1, 0.15), background_normal='')
	new_button.bind(on_press=swap_main)

	new_button.btn_number = menu.button_count

	new_button.selected = True
	# Graph wil be loaded from the file

	GraphLayout.popUpLoad(new_button, menu)

	#GraphLayout.getTableFromFile('C:\\Users\\jdsba', new_button, menu, 'testData.graph')

	return


def swap_main(self):
	print("Swapping the main display")
	total_layout = self.parent.parent.parent.parent
	main_layout = total_layout.children[0].children[0]
	main_layout_top_bar = total_layout.children[0].children[1]

	total_layout.children[0].remove_widget(main_layout)
	new_layout = self.selected_display
	#new_layout = self.digital_display

	
	total_layout.children[0].add_widget(new_layout)

	for child in self.parent.children:
		child.background_color = rgb("#33B5E5")
		child.color = (1, 1, 1, 1)
		child.selected = False

	main_layout_top_bar.input_type_button.text = self.graph.graphProfile.input_type
	self.background_color = rgb('079163')
	self.color = (1, 1, 1, 1)
	self.selected = True
	if self.btn_number == 1:
		main_layout_top_bar.remove_button.text = "Delete Recording"
	else:
		main_layout_top_bar.remove_button.text = "Remove"

	total_layout.current_graph = self.selected_display

	return


def delete_button(self):
	print("Deleting button")
	total_layout = self.parent.parent.parent
	menu = total_layout.children[1].children[1].children[0]
	if len(menu.children) > 1:
		for child in menu.children:
			if child.selected:
				if child.btn_number != 1:
					menu.remove_widget(child)
					swap_main(menu.children[0])
					return
				else:
					child.graph = GraphLayout(GraphProfile)
					child.graph.padding = 3
					swap_main(child)
					return


def display_settings(self):
	# popup = Popup(title='File Saved',
	#    content=self.settings,
	#    size_hint=(None, None), si
	# ze=(200, 200))
	btMenu.bluetooth.disconnectFromDevice()
	#app = self.parent.parent.parent
	#app.open_settings()
	return


def close_application(self):
	btMenu.bluetooth.disconnectFromDevice()
	App.get_running_app().stop()
	Window.close()


class LeftMenu(BoxLayout):

	def __init__(self, **kwargs):
		super(LeftMenu, self).__init__(**kwargs)
		self.background_normal = ''
		self.background_color = rgb("#000000")
		scrolling_menu = ScrollView(size_hint=(1, 0.8))

		add_button_menu = BoxLayout(orientation='vertical', size_hint=(1, 0.2))
		menu = StackLayout(size_hint=(1, 0.8))
		menu.background_normal = ''
		menu.background_color = rgb("#000000")
		menu.padding = 3
		menu.spacing = 3
		menu.bind(minimum_height=menu.setter('height'))

		scrolling_menu.add_widget(menu)
		self.add_widget(scrolling_menu)
		self.add_widget(add_button_menu)
		add_button_menu.padding = 3

		scrolling_menu.size = (scrolling_menu.parent.width, scrolling_menu.parent.height)

		menu.button_count = 1
		btn1 = Button(text='Multimeter', size_hint=(1, 0.15), background_normal='')
		btn1.input_type = 'Voltage'
		btn1.btn_number = 1
		btn1.bind(on_press=swap_main)
		self.current_button = btn1
		
		self.multimeter_button = btn1
		btn1.graph = GraphLayout(GraphProfile)
		btn1.digital_display = DigitalLayout()
		btn1.digital_display.padding = 3
		btn1.selected_display = btn1.graph

		btn1.graph.padding = 3
		self.multimeter_graph = btn1.selected_display
		add_button_menu.add_button = Button(size_hint=(1, 1))
		add_button_menu.add_button.text = '+'
		add_button_menu.add_button.background_normal = ''
		add_button_menu.add_button.background_color = rgb("#33B5E5")
		menu.add_widget(btn1)

		add_button_menu.add_widget(add_button_menu.add_button)
		add_button_menu.add_button.bind(on_press=add_new_button)

class CenterTopMenu(StackLayout):
	def __init__(self, **kwargs):
		super(CenterTopMenu, self).__init__(**kwargs)
		self.spacing = 3

		self.input_type_button = Button(text="Input Type", size_hint=(0.2, 1), background_normal='',
		                       						background_color=rgb("#33B5E5"), disabled = True, background_disabled_normal = "",
							   						color = rgb("ffffff"))


		self.remove_button = Button(text="Delete Recording", size_hint=(0.2, 1), background_normal='',
		                       					background_color=rgb("#33B5E5"))
		self.remove_button.bind(on_press=delete_button)


		self.settings_button = Button(text="", size_hint=(0.2, 1), background_normal='',
		                         				background_color=rgb("#000000"), disabled = True)
		self.settings_button.bind(on_press=display_settings)


		self.display_selector = ToggleButton(text = "Display Mode",size_hint=(0.2, 1),background_normal='',
		                         				background_color=rgb("#33B5E5"))
		self.display_selector.bind(on_press = self.toggle_center_display)


		self.quit_button = Button(text="Quit", size_hint=(0.2, 1), background_normal='',
		                         			background_color=rgb("#33B5E5"))
		self.quit_button.bind(on_press = close_application)

		self.add_widget(self.input_type_button)
		self.add_widget(self.remove_button)
		self.add_widget(self.display_selector)
		self.add_widget(self.settings_button)
		self.add_widget(self.quit_button)

	def toggle_center_display(self, *args):
		state = self.display_selector.state
		multimeter_button = self.parent.parent.left_menu.multimeter_button
		if state == 'down':
			print("Button is Down")
			multimeter_button.selected_display = self.parent.parent.left_menu.multimeter_button.digital_display
		if state == 'normal':
			print("Button is Up")
			multimeter_button.selected_display = self.parent.parent.left_menu.multimeter_button.graph
		swap_main(multimeter_button)


class CenterLayout(BoxLayout):
	def __init__(self, **kwargs):
		super(CenterLayout, self).__init__(**kwargs)
		self.padding = 3

		self.top_menu = CenterTopMenu(size_hint=(1, 0.105))


		self.add_widget(self.top_menu)

	


class MutliMeterApp(BoxLayout):

	def __init__(self, **kwargs):
		super(MutliMeterApp, self).__init__(**kwargs)
		self.orientation = 'horizontal'
		self.left_menu = LeftMenu(orientation='vertical', size_hint=(0.2, 1))

		self.add_widget(self.left_menu, 0)

		self.center_layout = CenterLayout(orientation='vertical', size_hint=(1, 1))

		main_display = Button(text='Layout 0', size_hint=(1, 0.9))
		self.center_layout.add_widget(main_display)
		self.add_widget(self.center_layout)
		self.decoder = BluetoothDecoder(fake=FAKE_DECODER)
		self.multimeter_graph = self.children[1].multimeter_graph
		self.multimeter_button = self.children[1].multimeter_button
		self.queue = self.multimeter_graph.graph.queue
		
		Clock.schedule_interval(self.sendDataToQueue, 1 / 10)
		Clock.schedule_interval(self.add_to_graph, 1 / 10)
		swap_main(self.left_menu.current_button)
		#global bluetooth
		#bluetooth = BLE()
		x = threading.Thread(target=btMenu.bluetooth.startBluetoothConnection, args=(self.decoder,), daemon=True)
		x.start()
		#bluetooth.startBluetoothConnection(self.decoder)

	def	sendDataToQueue(self, *args):
		nextData = self.decoder.getNextPoint()
		if nextData:
			print(nextData)
			if self.center_layout.top_menu.input_type_button.text != nextData["type"]:
				self.center_layout.top_menu.input_type_button.text = nextData["type"]
				self.updateGraphTitles(nextData["type"])
				self.multimeter_graph.graph.reset()
			if self.multimeter_graph.graphProfile.ymax < nextData["max_y"]:
				self.multimeter_graph.graphProfile.ymax = nextData["max_y"]
			if self.multimeter_graph.graphProfile.ymin > nextData["min_y"]:
				self.multimeter_graph.graphProfile.ymin = nextData["min_y"]
			self.multimeter_button.selected_display.addpoint(nextData["value"])


	def updateGraphTitles(self, nextDataType):
		if nextDataType == 'Voltmeter':
			self.multimeter_graph.graphProfile.yLabel = "Volts (Vrms)"
			self.multimeter_graph.graphProfile.ymin = 0
			self.multimeter_graph.graphProfile.ymax = 0.4
		if nextDataType == 'Ammeter':
			self.multimeter_graph.graphProfile.yLabel = "Amps (A)"
			self.multimeter_graph.graphProfile.ymin = 0
			self.multimeter_graph.graphProfile.ymax = 0.4
		if nextDataType == 'Ohmmeter':
			self.multimeter_graph.graphProfile.yLabel = "Ohms (Ω)"
			self.multimeter_graph.graphProfile.ymin = 0
			self.multimeter_graph.graphProfile.ymax = 0.4
		if nextDataType == 'Light Sensor':
			self.multimeter_graph.graphProfile.yLabel = "Light Units"
			self.multimeter_graph.graphProfile.ymin = 0
			self.multimeter_graph.graphProfile.ymax = 0.4
		if nextDataType == 'Temperature Sensor':
			self.multimeter_graph.graphProfile.yLabel = "Temperature Units"
			self.multimeter_graph.graphProfile.ymin = 0
			self.multimeter_graph.graphProfile.ymax = 0.4
		
		
	def add_to_graph(self, *args):
		self.multimeter_graph.graph.update_points()



class MultiMeterApp(App):
	def build(self):
		self.title = "UCDAVIS Bluetooth Multimeter"
		Window.minimum_height = 600
		Window.minimum_width = 800
		Window.clearcolor = rgb("#000000")
		app = MutliMeterApp()
		return app

	def build_settings(self, settings):
		# settings.add_json_panel('Test application', self.config, 'app_settings.json')
		return


if __name__ == '__main__':
	btMenu.BtMenuApp().run()
	MultiMeterApp().run()
