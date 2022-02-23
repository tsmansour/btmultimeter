from kivy.core.window import Window
from kivy.input.providers.mouse import MouseMotionEvent
from kivy.uix.popup import Popup
from kivymd.uix.button import MDIconButton

from graph import Graph, MeshLinePlot, VBar, Point, PointPlot
from kivy.utils import get_color_from_hex as rgb
from kivy.clock import Clock
import itertools
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivymd.icon_definitions import md_icons as Icons
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


class GraphProfile:
        title = 'Volts in AC'
        xmax = 10.0
        xmin = 0
        ymin = 0
        ymax = 160
        xlabel = 'Time (s)'
        ylabel = 'Volts (Vrms)'


class GraphWidget(Graph):
    def __init__(self, graphProfile: GraphProfile ,**kwargs):
        super().__init__(**kwargs)
        colors = itertools.cycle([
            rgb('7dac9f'), rgb('dc7062'), rgb('66a8d4'), rgb('e5b060')])
        self.profile = graphProfile
        self.xlabel = graphProfile.xlabel
        self.ylabel = graphProfile.ylabel
        self.x_ticks_minor = 1
        self.x_ticks_major = 1
        self.y_ticks_major = 20
        self.y_grid_label = True
        self.x_grid_label = True
        self.padding = 0
        self.xlog = False
        self.ylog = False
        self.x_grid = True
        self.y_grid = True
        self.xmin = graphProfile.xmin
        self.xmax = graphProfile.xmax
        self.ymin = graphProfile.ymin
        self.ymax = graphProfile.ymax
        self.background_color = rgb('ffffffff')
        self.label_options = {'color': rgb('444444'), 'bold': True}
        self.border_color = rgb('f8f8f2')
        self.tick_color = rgb('808080')
        self.border_color = rgb('808080')
        self.queue = myQueue(1000)
        self.point_label = Label(font_size='9sp')
        self.point_label.color = rgb('000000')
        self.add_widget(self.point_label)
        self.plot = MeshLinePlot(color=rgb('ff0000'))
        #self.view_size = 10
        self.add_plot(self.plot)
        self.vbar = VBar()
        self.vbar.color = rgb('5e34eb')
        self.add_plot(self.vbar)
        self.plot_points = PointPlot(color=rgb('000000'))
        self.plot_points.point_size = 10
        self.add_plot(self.plot_points)
        self.currentTime = 0
        self.evenTrigger = self._getNewEventTrigger()
        self.bind(on_touch_up=self._touch_up)


    def _touch_up(self, graphwidget, mouseMotion: MouseMotionEvent ):
        self._set_selectable_graph_window()
        if self.x_start < mouseMotion.x < self.x_end and self.y_start < mouseMotion.y < self.y_end:
            x, y = self._window_position_to_graph_value(*mouseMotion.pos)
            if 0 != len(self.plot.points):
                # https://www.geeksforgeeks.org/python-find-closest-number-to-k-in-given-list/
                point_ref = self.plot.points[min(range(len(self.plot.points)),
                                                 key=lambda i: abs(self.plot.points[i][0]-x))]
                self.vbar.points = [point_ref[0]]
                self.point_label.text = '({0:.3f},{1:.3f})'.format(x, y)
                edge = Window.width - self.graph_pos_to_window_pos(*point_ref)[0] - self.point_label.width
                if edge < 0:
                    self.point_label.pos = Window.width - self.point_label.width - 10, self.graph_pos_to_window_pos(*point_ref)[1]
                else:
                    self.point_label.pos = self.graph_pos_to_window_pos(*point_ref)
                if 'right' == mouseMotion.button:
                    if len( self.plot_points.points):
                        self.plot_points.points.pop()
                else:
                    self.plot_points.points.append(point_ref)
                print(f'X:{x} Y:{y}')

    def _getNewEventTrigger(self):
        return Clock.create_trigger(self.update_points, interval=True, timeout=1/10)

    def _set_selectable_graph_window(self):
        self.x_start = self.pos[0] + self.view_pos[0]
        self.x_end = self.x_start + self.view_size[0]
        self.y_start = self.pos[1] + self.view_pos[1]
        self.y_end = self.y_start + self.view_size[1]

    def _window_position_to_graph_value(self, x, y):
        x_out = self.xmin + (x - self.x_start) * (self.xmax - self.xmin) / self.view_size[0]
        y_out = self.ymin + (y - self.y_start) * (self.ymax - self.ymin) / self.view_size[1]
        return x_out, y_out

    def graph_pos_to_window_pos(self, x, y):
        x_out = self.pos[0] + self.view_pos[0] + (x - self.xmin) * (self.view_size[0]) / (self.xmax - self.xmin)
        y_out = self.pos[1] + self.view_pos[1] + (y - self.ymin) * (self.view_size[1]) / (self.ymax - self.ymin)
        return x_out, y_out

    def startClock(self):
        self.evenTrigger()

    def stopClock(self):
        self.evenTrigger()

    def reset(self):
        self.currentTime = 0
        self.xmax = 10
        self.xmin = 0
        self.queue.clear()
        self.plot.points = []

    def add_point(self, value, timeDif):
        time = self.currentTime + timeDif
        #print(f'V: {value} , Time:{time}')
        if time > self.xmax:
            self.xmax += 5
            self.xmin += 5
        if len(self.plot_points.points):
            self.point_label.pos = self.graph_pos_to_window_pos(*self.plot_points.points[0])
        self.queue.addToeQueue(value, self.currentTime)
        self.currentTime = time

    def update_points(self, *args):
        self.plot.points = self.queue.get()


class myQueue:
    def __init__(self, size):
        self.queue = []
        self.size = size

    def addToeQueue(self, newValue, time):
        if len(self.queue) > self.size:
            self.queue.pop()
        self.queue.insert(0, (time, newValue))

    def get(self):
        return self.queue

    def clear(self):
        self.queue.clear()

    def __len__(self):
        return len(self.queue)

    def __index__(self):
        return self.queue


class SaveButtonWithDropdown(Button):

    def __init__(self, assigned_graph, **kwargs):
        super().__init__(**kwargs)
        #self.size_hint=(None, None)
        self.dropdown = DropDown()
        btnSaveImage = Button(text='PNG', size_hint_y=None, height=50)
        btnSaveData = Button(text='Data', size_hint_y=None, height=50)
        btnSaveImage.bind(on_release=self.selectSaveImage)
        btnSaveData.bind(on_release=self.selectSaveData)
        self.assignedGraph: GraphWidget = assigned_graph
        self.dropdown.add_widget(btnSaveImage)
        self.dropdown.add_widget(btnSaveData)
        self.dropdown.opacity = 0
        self.dropdown.auto_dismiss = True
        self.add_widget(self.dropdown)
        self.bind(on_release=self.buttonRelease)

    def buttonRelease(self, *args):
        self.dropdown.open(self)
        self.dropdown.opacity = 100

    def selectSaveImage(self, *args):
        self.assignedGraph.export_to_png("image.png")
        print('saveimage')
        pass

    def selectSaveData(self, *args):
        data_to_save = {
            'xmin': self.assignedGraph.xmin,
            'xmax': self.assignedGraph.xmax,
            'ymin': self.assignedGraph.ymin,
            'ymax': self.assignedGraph.ymax,
            'points': self.assignedGraph.plot.points,
        }
        with open('test.txt', 'w') as file:
            file.write(data_to_save.__str__())
            popup = Popup(title='File Saved',
                          content=Label(text='Hello world'),
                          size_hint=(None, None), size=(200, 200))

            btnOk = Button(text="OK")
            popup.content = btnOk
            popup.open()
        print('savedata')
        pass


class GraphLayout(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rows = 2
        # Graph setup
        self.graph = GraphWidget(GraphProfile())
        # Button Setup
        buttonRow = BoxLayout()
        buttonRow.orientation = "horizontal"
        buttonRow.spacing = 100
        buttonRow.size_hint_max_y = 50
        buttonRow.padding = [100, 0]
        config = Button(text='Config')
        config.bind(on_press=self.configPress)
        recordButton = Button(text='START')
        recordButton.background_color = kwargs.get('background_color', rgb('ffffffff'))
        recordButton.bind(on_press=self.recordPress)
        saveDropdown = SaveButtonWithDropdown(text='Save', assigned_graph=self.graph)
        buttonRow.add_widget(recordButton)
        buttonRow.add_widget(saveDropdown)


        self.add_widget(buttonRow)
        self.add_widget(self.graph)
        self.state_record = 0


    def recordPress(self, *args):
        if self.state_record == 0:
            self.state_record = 1
            self.graph.startClock()
            args[0].text = 'STOP'

        elif self.state_record == 1:
            self.state_record = 2
            self.graph.stopClock()
            args[0].text = 'RESET'
        else:
            self.state_record = 0
            self.graph.reset()
            args[0].text = 'START'

    def configPress(self, *args):
        print('config done')


    def addpoint(self, value, time):
        if self.state_record == 1:
            self.graph.add_point(value, time)