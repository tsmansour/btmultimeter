import kivy
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.widget import Widget

from kivy.uix.recycleview import RecycleView


class BluetoothGUI(AnchorLayout):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.anchor_x = 'left'
		self.anchor_y = 'top'
		self.add_widget(BTMenu())


class BTMenu(Widget):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)