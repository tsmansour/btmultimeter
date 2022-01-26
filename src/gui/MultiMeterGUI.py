from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

class MenuSelection(Widget):
    pass

class MainLayout(Widget):
    layout = GridLayout(cols=3, rows=0)
    lb1 = Label(text="Hello")
    layout.add_widget(lb1)

class MultiMeterApp(App):
    def build(self):
        app = MainLayout()
        return app


if __name__ == '__main__':
    MultiMeterApp().run()