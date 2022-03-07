from bluetoothDecoder import BluetoothDecoder
from BLE_Windows_Mac import startBluetoothConnection
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

from kivy.utils import get_color_from_hex as rgb

ModeButtonsOptions = ['V~', 'V=', 'A', 'Ω', 'C/F', 'Light', '+']

testpoint = 80


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

	def on_touch_down(self, touch):
		# do action when pressed down
		# print("pressed button")
		return


def display_voltage(self):
	print("Displaying Voltage")
	self.dropdown.select(self.text)
	self.layout.parent.current_graph.ylabel = 'Volts (Vrms)'
	return


def display_current(self):
	print("Displaying Current")
	self.dropdown.select(self.text)
	self.layout.parent.current_graph.ylabel = 'Current (A)'
	return


def display_resistance(self):
	print("Displaying Resistance")
	self.dropdown.select(self.text)
	return


def display_temp(self):
	print("Displaying Temp")
	self.dropdown.select(self.text)
	return


def display_light(self):
	print("Displaying Light")
	self.dropdown.select(self.text)
	return


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
	#print(main_layout_top_bar.children[1].text)

	total_layout.children[0].remove_widget(main_layout)
	new_layout = self.graph

	
	# new_layout = Button(text='Layout ' + str(self.btn_number), size_hint = (1, 0.9))
	total_layout.children[0].add_widget(new_layout)

	for child in self.parent.children:
		# child.background_color = (0.878, 0.878, 0.878, 1.0)
		child.background_color = rgb("#33B5E5")
		child.color = (1, 1, 1, 1)
		child.selected = False

	main_layout_top_bar.children[2].text = self.graph.graphProfile.input_type
	self.background_color = rgb('079163')
	self.color = (1, 1, 1, 1)
	self.selected = True
	if self.btn_number == 1:
		main_layout_top_bar.children[1].text = "Delete Recording"
	else:
		main_layout_top_bar.children[1].text = "Remove"

	total_layout.current_graph = self.graph

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
	app = self.parent.parent.parent
	app.open_settings()
	return


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
		

		btn1.graph = GraphLayout(GraphProfile)

		btn1.graph.padding = 3
		self.multimeter_graph = btn1.graph
		add_button_menu.add_button = Button(size_hint=(1, 1))
		add_button_menu.add_button.text = '+'
		add_button_menu.add_button.background_normal = ''
		add_button_menu.add_button.background_color = rgb("#33B5E5")
		menu.add_widget(btn1)

		add_button_menu.add_widget(add_button_menu.add_button)
		add_button_menu.add_button.bind(on_press=add_new_button)


class CenterLayout(BoxLayout):
	def __init__(self, **kwargs):
		super(CenterLayout, self).__init__(**kwargs)
		self.padding = 3

		input_type_button = Button(text="Input Type", size_hint=(0.2, 1), background_normal='',
		                       background_color=rgb("#33B5E5"), disabled = True, background_disabled_normal = "")

		remove_button = Button(text="Delete Recording", size_hint=(0.2, 1), background_normal='',
		                       background_color=rgb("#33B5E5"))
		remove_button.bind(on_press=delete_button)

		settings_button = Button(text="Settings", size_hint=(0.2, 1), background_normal='',
		                         background_color=rgb("#33B5E5"))
		settings_button.bind(on_press=display_settings)

		# config = ConfigParser()
		# config.read('myconfig.ini')
		# settings_button.settings = Settings()
		# settings_button.settings.add_json_panel('My custom panel', config, 'app_settings.json')
		# s.add_json_panel('Another panel', config, 'settings_test2.json')

		top_menu = StackLayout(size_hint=(1, 0.105))
		top_menu.spacing = 3
		# top_menu.padding = 3
		top_menu.add_widget(input_type_button)
		top_menu.add_widget(remove_button)
		top_menu.add_widget(settings_button)

		self.add_widget(top_menu)


class MutliMeterApp(BoxLayout):

	def __init__(self, **kwargs):
		super(MutliMeterApp, self).__init__(**kwargs)
		self.orientation = 'horizontal'
		left_menu = LeftMenu(orientation='vertical', size_hint=(0.2, 1))

		self.add_widget(left_menu, 0)

		center_layout = CenterLayout(orientation='vertical', size_hint=(1, 1))

		main_display = Button(text='Layout 0', size_hint=(1, 0.9))
		center_layout.add_widget(main_display)
		self.add_widget(center_layout)
		self.decoder = BluetoothDecoder()
		self.multimeter_graph = self.children[1].multimeter_graph
		self.queue = self.multimeter_graph.graph.queue
		
		#Clock.schedule_interval(self.getFakeBytes, 1 / 10)
		Clock.schedule_interval(self.sendDataToQueue, 7 / 10)
		Clock.schedule_interval(self.add_to_graph, 7 / 10)
		swap_main(left_menu.current_button)
		startBluetoothConnection(self.decoder)

	def fakeData(self, *args):
		global testpoint
		testpoint += random.choice([-1, 1]) * random.random()
		self.queue.addpoint(testpoint, args[0])

	def getFakeBytes(self, *args):
		
		return

	def	sendDataToQueue(self, *args):
		nextData = self.decoder.getNextPoint()
		if nextData:
			self.queue.addToQueue(nextData, args[0])
		return

	def add_to_graph(self, *args):
		self.multimeter_graph.graph.update_points()
		return


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
	MultiMeterApp().run()