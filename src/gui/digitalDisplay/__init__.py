from kivy.graphics import Rectangle
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.graphics import Color


# Builder.load_file(os.path.join(os.path.dirname(__file__), 'digitalLayout.kv'))

class DigitalLayout(GridLayout):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.rows = 2
		self.canvas.add(Color(1., 1., 0))
		self.canvas.add(Rectangle(size=(self.width * 0.7, self.height * 0.7)))

		self.largeNumberDisplay = LargeNumberDisplay()
		self.add_widget(TopDetailDisplay())
		self.add_widget(self.largeNumberDisplay)

	def updateDisplay(self, newValue):
		self.largeNumberDisplay.updateDisplay(newValue)


class TopDetailDisplay(GridLayout):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.cols = 10
		self.size_hint_y = 0.15
		for i in range(10):
			self.add_widget(Label(text=f'Thing {i}'))


class LargeNumberDisplay(Label):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.font_size = 200
		self.text = '120.0'

	def updateDisplay(self, newValue):
		self.text = f'{float(newValue):.2f}'
