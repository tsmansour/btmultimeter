from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.button import Button



class ModeButton(Widget):

    def __init__(self, text,  **kwargs):
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
        print("pressed button")





class MainLayout(BoxLayout):

    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        menu = BoxLayout(orientation='vertical')
        menu.width = 100
        btn1 = Button(text='Hello', width=100)
        btn2 = Button(text='World', width=100)
        menu.add_widget(btn1)
        menu.add_widget(btn2)
        menu.spacing = 20
        menu.padding = 20
        self.add_widget(menu, 0)
        btn3 = Button(text='All alone')
        self.add_widget(btn3)


        




class MultiMeterApp(App):
    def build(self):
        self.title = "UCDAVIS Bluetooth Multimeter"
        Window.minimum_height = 600
        Window.minimum_width = 800
        app = MainLayout()
        return app


if __name__ == '__main__':
    MultiMeterApp().run()