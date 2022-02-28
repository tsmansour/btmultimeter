from kivy.core.window import Window
from kivy.input.providers.mouse import MouseMotionEvent
from kivy.uix.popup import Popup
from graph import Graph, MeshLinePlot, VBar, PointPlot
from kivy.utils import get_color_from_hex as rgb
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


class GraphProfile:
        title = 'Volts in AC'
        xmax = 10.0
        xmin = 0
        ymin = 0
        ymax = 140
        xlabel = 'Time (s)'
        ylabel = 'Volts (Vrms)'
        backgroundColor = rgb('ffffffff')
        plotline_Color = rgb('ff0000')
        vbar_color = rgb('5e34eb')
        tick_color = rgb('b8c6db')
        border_color = rgb('8a94a6')
        points_color = rgb('000000')
        point_label_color = rgb('000000')
        save_to_directory = './save/'
        save_to_image_name = './save/graphImage'
        save_to_file_name = './save/graphData'
        plot_points_color = rgb('000000')


class GraphWidget(Graph):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._selfConfig()
        self.queue = myQueue(1000)
        self.point_label = Label(font_size='9sp', color=rgb('000000'))
        self.add_widget(self.point_label)
        self.plot = MeshLinePlot(color=rgb('ff0000'))
        self.add_plot(self.plot)
        self.vbar = VBar()
        self.add_plot(self.vbar)
        self.plot_points = PointPlot(color=rgb('000000'))
        self.plot_points.point_size = 5
        self.add_plot(self.plot_points)

    def _selfConfig(self):
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
        self.label_options = {'color': rgb('444444'), 'bold': True}
        self.currentTime = 0
        self.evenTrigger = self._getNewEventTrigger()
        self.bind(on_touch_up=self._touch_up)

    def _touch_up(self, graphwidget, mouseMotion: MouseMotionEvent):
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
        self.plot_points.points = []
        self.point_label.disabled = True
        self.vbar.points = []


    def add_point(self, value, timeDif):
        time = self.currentTime + timeDif
        if time > self.xmax:
            self.xmax += 5
            self.xmin += 5
        if len(self.plot_points.points):
            self.point_label.disabled = False
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
        self.background_normal = 'assets/floppy-drive.png'
        self.dropdown = DropDown()
        self.size_hint_max_x = 50
        self.size_hint_max_y = 50
        btnSaveImage = Button(text='PNG', size_hint_y=None)
        btnSaveImage.size_hint_max_x = 50
        btnSaveData = Button(text='Data', size_hint_y=None)
        btnSaveData.size_hint_max_x = 50
        btnSaveImage.bind(on_release=self.selectSaveImage)
        btnSaveData.bind(on_release=self.selectSaveData)
        self.imagePath = 'image.png'
        self.filePath = 'image.png'
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
        self.assignedGraph.export_to_png(self.imagePath+'.png')
        print(f'saved {self.imagePath}')
        pass

    def selectSaveData(self, path, *args):
        data_to_save = {
            'xmin': self.assignedGraph.xmin,
            'xmax': self.assignedGraph.xmax,
            'ymin': self.assignedGraph.ymin,
            'ymax': self.assignedGraph.ymax,
            'points': self.assignedGraph.plot.points,
        }
        with open(self.filePath, 'w') as file:
            file.write(data_to_save.__str__()+'.graph')
            popup = Popup(title=f'File Saved to {self.filePath}',
                          content=Label(text='Hello world'),
                          size_hint=(None, None), size=(200, 200))

            btnOk = Button(text="OK", on_touch_up=popup.close)
            popup.content = btnOk
            popup.open()
        print('savedata')
        pass


class GraphLayout(GridLayout):

    def __init__(self, graphProfile: GraphProfile, **kwargs):
        super().__init__(**kwargs)
        self.rows = 2
        # Graph setup
        self.graphProfile = graphProfile
        self.graph = GraphWidget()
        # Button Setup
        buttonRow = BoxLayout()
        buttonRow.orientation = "horizontal"
        buttonRow.spacing = 100
        buttonRow.size_hint_max_y = 75
        buttonRow.padding = [100, 0]
        recordButton = Button(text='START')
        recordButton.bind(on_press=self.recordPress)
        recordButton.background_color = rgb('079163')
        recordButton.background_normal = ''
        self.saveDropdown = SaveButtonWithDropdown(assigned_graph=self.graph)
        buttonRow.add_widget(recordButton)
        buttonRow.add_widget(self.saveDropdown)
        self.add_widget(buttonRow)
        self.add_widget(self.graph)
        self.state_record = 0
        self.graphProfile.assignedGraph = self
        self.updatetoLatestGraphProfile()

    def updatetoLatestGraphProfile(self):
        self.graph.ymax = self.graphProfile.ymax
        self.graph.ymin = self.graphProfile.ymin
        self.graph.xmin = self.graphProfile.xmin
        self.graph.xmax = self.graphProfile.xmax
        self.graph.xlabel = self.graphProfile.xlabel
        self.graph.ylabel = self.graphProfile.ylabel
        self.graph.background_color = self.graphProfile.backgroundColor
        self.graph.plot.color = self.graphProfile.plotline_Color
        self.graph.vbar.color = self.graphProfile.vbar_color
        self.graph.tick_color = self.graphProfile.tick_color
        self.graph.border_color = self.graphProfile.border_color
        self.graph.plot_points.color = self.graphProfile.plot_points_color
        self.saveDropdown.imagePath = self.graphProfile.save_to_image_name
        self.saveDropdown.filePath = self.graphProfile.save_to_file_name

    iconsIterator = iter(['assets/start.png', 'assets/stop.png', 'assets/skip-back.png'])

    def recordPress(self, *args):

        if self.state_record == 0:
            self.state_record = 1
            self.graph.startClock()
            #args[0].text = 'STOP'
            args[0].background_normal = next(self.iconsIterator)

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