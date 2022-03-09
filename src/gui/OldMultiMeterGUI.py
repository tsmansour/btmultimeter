from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.animation import Animation

# Starting Environment 
# kivy_venv\Scripts\activate
# cd ECS193Project\btmultimeter\src\gui
# python MultiMeterGUI.py

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



def resizeLeftSideBar(self):

    if self.parent.collapsed:
        # Grows Sidebar
        anim = Animation(size_hint = (0.2,1), duration = 0.4, t = 'in_out_cubic')
        anim.start(self.parent)
        self.parent.collapsed = False
        self.parent.add_widget(self.parent.btn2)
        self.parent.add_widget(self.parent.btn3)
        self.parent.add_widget(self.parent.btn4)
        self.parent.add_widget(self.parent.btn5)
        self.parent.add_widget(self.parent.btn6)
        #self.size_hint = (1,0.2)
    else:
        # Shrinks Sidebar
        anim = Animation(size_hint = (0.1,1), duration = 0.4, t = 'in_out_cubic')
        anim.start(self.parent)
        self.parent.collapsed = True
        self.parent.remove_widget(self.parent.btn2)
        self.parent.remove_widget(self.parent.btn3)
        self.parent.remove_widget(self.parent.btn4)
        self.parent.remove_widget(self.parent.btn5)
        self.parent.remove_widget(self.parent.btn6)
    
    return

def display_voltage(self):
    print("Displaying Voltage")
    return

def display_current(self):
    print("Displaying Current")
    return

def display_resistance(self):
    print("Displaying Resistance")
    return

def display_temp(self):
    print("Displaying Temp")
    return

def display_light(self):
    print("Displaying Light")
    return

class MainLayout(BoxLayout):

    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        #menu = BoxLayout(orientation='vertical')
        menu = GridLayout(cols = 1, rows = 6)
        #menu.width = 100
        menu.row_default_size = 20
        menu.size_hint = (0.2,1)
        menu.collapsed = False
        menu.btn1 = Button(text='Resize', size_hint_y = 0.15)
        menu.btn1.bind(on_press=resizeLeftSideBar)
        menu.btn2 = Button(text='Voltage', size_hint = (1,0.15))
        menu.btn2.bind(on_press=display_voltage)
        menu.btn3 = Button(text='Current', size_hint = (1,0.15))
        menu.btn3.bind(on_press=display_current)
        menu.btn4 = Button(text='Resistance', size_hint = (1,0.15))
        menu.btn4.bind(on_press=display_resistance)
        menu.btn5 = Button(text='Temp', size_hint = (1,0.15))
        menu.btn5.bind(on_press=display_temp)
        menu.btn6 = Button(text='Light', size_hint = (1,0.15))
        menu.btn6.bind(on_press=display_light)
        menu.add_widget(menu.btn1)
        menu.add_widget(menu.btn2)
        menu.add_widget(menu.btn3)
        menu.add_widget(menu.btn4)
        menu.add_widget(menu.btn5)
        menu.add_widget(menu.btn6)
        menu.spacing = 10
        menu.padding = 10
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


#if __name__ == '__main__':
#    MultiMeterApp().run()