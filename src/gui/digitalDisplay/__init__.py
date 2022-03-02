import math
import os

from kivy.graphics import Rectangle
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.graphics import Color

Builder.load_file(os.path.join(os.path.dirname(__file__), 'digitalLayout.kv'))

class DigitalLayout(GridLayout):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.rows = 2
		self.topRow = TopDetailDisplay()
		self.largeNumberDisplay = LargeNumberDisplay()
		self.add_widget(self.topRow)
		self.add_widget(self.largeNumberDisplay)

		self.isPaused = False

	def addpoint(self, newValue):
		if not self.isPaused:
			self.largeNumberDisplay.updateDisplay(newValue)
			self.topRow.updateValues(newValue)

class ValueLabel(Label):

	def __init__(self, title, **kwargs):
		super().__init__(**kwargs)
		self.base = title + ': '
		self.text = self.base + '0'

	def on_text(self, *_):
		l = Label(text=self.text)
		l.font_size = '1000dp'
		l.texture_update()
		self.texture = l.texture

	def updateLabel(self, newValue):
		self.text = self.base + f'{newValue:.3f}'

class TopDetailDisplay(GridLayout):

	topOptions = ['MAX', 'MIN', 'AVE']
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.cols = 10
		self.size_hint_y = 0.15
		self.resetPress()
		self.topLabels = {}
		for val in self.topOptions:
			thisLabel = ValueLabel(val)
			self.topLabels[val] = thisLabel
			self.add_widget(thisLabel)
		self.pause = Button(text='PAUSE', on_press=self.pausePress)
		reset = Button(text='RESET', on_press=self.resetPress)
		self.add_widget(self.pause)
		self.add_widget(reset)

	def updateValues(self, newValue):
			self.count += 1
			self.sum += newValue
			if newValue > self.max:
				self.max = newValue
				self.topLabels['MAX'].updateLabel(newValue)
			if newValue < self.min:
				self.min = newValue
				self.topLabels['MIN'].updateLabel(newValue)
			self.topLabels['AVE'].updateLabel(self.sum/self.count)

	def pausePress(self, *_):
		if self.parent.isPaused:
			self.pause.text = 'PAUSE'
			self.parent.isPaused = False
		else:
			self.pause.text = 'RESUME'
			self.parent.isPaused = True

	def resetPress(self, *_):
		self.min = math.inf
		self.max = -math.inf
		self.count = 0
		self.sum = 0


class LargeNumberDisplay(Label):

	def updateDisplay(self, newValue):
		self.text = f'{float(newValue):.3f}'


	def on_text(self, *_):
		l = Label(text=self.text)
		l.font_size = '5000sp'
		l.texture_update()
		self.texture = l.texture