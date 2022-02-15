import random

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.recycleview import RecycleView
from kivy.clock import Clock
from mygraph import GraphLayout

ModeButtonsOptions = ['V~', 'V=', 'A', 'Ω', 'C/F', 'Light', '+']


class ModeButton(Widget):
    counter = 0

    def __init__(self, text, **kwargs):
        super(ModeButton, self).__init__(**kwargs)
        button = Button()
        button.width = 300
        button.height = 100
        button.pos = self.pos
        button.color = "red"
        button.text = text
        self.add_widget(button)

    def on_touch_down(self, touch):
        # do action when pressed down
        print("pressed button {}".format(self.counter))
        self.counter += 1


class ModeSelectList(RecycleView):

    def __init__(self, **kwargs):
        super(ModeSelectList, self).__init__(**kwargs)
        self.size_hint_max_x = 85
        self.data = [
            {'text': str(x), 'width': 75, 'height': 75}
            for x in ModeButtonsOptions
        ]


class MainLayout(BoxLayout):

    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        menu = ModeSelectList()
        self.add_widget(menu)
        self.graph = GraphLayout()
        self.add_widget(self.graph)


class MainGrid(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2
        menu = ModeSelectList()
        self.add_widget(menu, index=1)
        self.graph = GraphLayout()
        self.add_widget(self.graph, index=0)
        Clock.schedule_interval(self.fakeData, 1 / 10)

    testpoint = 120

    def fakeData(self, *args):
        self.testpoint += random.choice([-1, 1]) * random.random()
        self.graph.addpoint(self.testpoint, args[0])


class MultiMeterApp(App):
    def build(self):
        self.title = "UCDAVIS Bluetooth Multimeter"
        Window.minimum_height = 400
        Window.minimum_width = 600
        app = MainGrid()
        return app


if __name__ == '__main__':
    MultiMeterApp().run()
