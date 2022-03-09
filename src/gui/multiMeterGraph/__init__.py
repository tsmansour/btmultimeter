
import os
import json
from pathlib import Path
from time import time as nowTime

from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.input.providers.mouse import MouseMotionEvent
from kivy.uix.label import Label
from kivy.utils import get_color_from_hex as rgb
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from src.gui.graph import Graph, MeshLinePlot, PointPlot, VBar


class SaveButtonWithDropdown(Button):

    def __init__(self, assigned_graph, **kwargs):
        super().__init__(**kwargs)
        self.text = "Save As"
        self.dropdown = DropDown()
        self.size_hint_x = 0.30
        btnSaveImage = Button(text='PNG', size_hint_y=None)
        btnSaveImage.size_hint_max_x = 50
        btnSaveData = Button(text='Data', size_hint_y=None)
        btnSaveData.size_hint_max_x = 50
        btnSaveImage.bind(on_press=self.selectSaveImage)
        btnSaveData.bind(on_press=self.selectSaveData)
        self.assignedGraph: GraphWidget = assigned_graph
        self.dropdown.add_widget(btnSaveImage)
        self.dropdown.add_widget(btnSaveData)
        self.dropdown.opacity = 0
        self.dropdown.auto_dismiss = True
        self.add_widget(self.dropdown)
        self.bind(on_press=self.buttonRelease)

    def buttonRelease(self, *args):
        self.dropdown.open(self)
        self.dropdown.opacity = 100

    def selectSaveImage(self, *args):
        self.dropdown.dismiss()
        self.fileSaveFormat = self.assignedGraph.export_to_png
        self.fileType = '.png'
        self.export_data = self
        self.popUpSave()

    def selectSaveData(self, *args):
        data = {
            'title': str(self.parent.getTitle()),
            'type': str('missingType'),
            'xmin': str(self.assignedGraph.xmin),
            'xmax': str(self.assignedGraph.xmax),
            'ymin': str(self.assignedGraph.ymin),
            'ymax': str(self.assignedGraph.ymax),
            'mesh_points': list(self.assignedGraph.plot.points),
        }

        def writeto(c):
            with open(c, 'w') as f:
                json.dump(data, f)

        self.dropdown.dismiss()
        self.fileType = '.graph'
        self.fileSaveFormat = writeto
        self.popUpSave()

    def popUpSave(self):
        self.popup = Popup(title=f'Choose file Location:', auto_dismiss=True,
                           size_hint=(None, None), size=(Window.width * 0.7, Window.height * 0.7))
        layout = GridLayout()
        layout.rows = 2
        self.fc = FileChooserListView(path=str(Path.home()), filters=[self.fileType])
        layout.add_widget(self.fc, 1)
        bottom = GridLayout(cols=3, size_hint_y=0.1)

        btnOk = Button(text="OK", size_hint_x=0.15, size_hint_max_y=50, disabled=True)
        btnOk.bind(on_press=self._pathFormatter)
        self.input_save_text = PathInput(btnOk)
        btnCancel = Button(text="Cancel", size_hint_x=0.15, size_hint_max_y=None, on_press=self.popup.dismiss)
        bottom.add_widget(self.input_save_text)
        bottom.add_widget(btnOk)
        bottom.add_widget(btnCancel)
        layout.add_widget(bottom)
        self.popup.content = layout
        self.popup.open()

    def _pathFormatter(self, item: Button):
        dir = Path(self.fc.path)
        file = str(self.input_save_text.text)
        if '/' in file:
            split = str(self.input_save_text.text).split('/')
            file = split.pop()
            for s in split:
                dir = dir.joinpath(s)
                if not os.path.exists(dir):
                    os.mkdir(dir)
        file += '' if file.endswith(self.fileType) else self.fileType
        path = dir.joinpath(file)
        self.fileSaveFormat(str(path))
        self.popup.dismiss()


class PathInput(TextInput):
    def __init__(self, okButton: Button, **kwargs):
        super().__init__(**kwargs)
        self.button = okButton
        self.multiline = False

    def _refresh_text(self, text, *largs):
        self.button.disabled = len(str(self.text)) < 1
        super(PathInput, self)._refresh_text(text, *largs)

    def insert_text(self, substring, from_undo=False):
        self.button.disabled = len(substring) < 1
        substring = str(substring).replace('\n', '')
        return super().insert_text(substring, from_undo=from_undo)


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
        self.lastClockTime = None
        self.evenTrigger = self._getNewEventTrigger()
        self.bind(on_touch_up=self._touch_up)

    def _touch_up(self, graphwidget, mouseMotion: MouseMotionEvent):
        self._set_selectable_graph_window()
        v = self.plot.get_px_bounds()
        if self.x_start < mouseMotion.x < self.x_end and self.y_start < mouseMotion.y < self.y_end:
            x, y = self._window_position_to_graph_value(*mouseMotion.pos)
            if 0 != len(self.plot.points):
                # https://www.geeksforgeeks.org/python-find-closest-number-to-k-in-given-list/
                point_ref = self.plot.points[min(range(len(self.plot.points)),
                                                 key=lambda i: abs(self.plot.points[i][0] - x))]
                self.vbar.points = [point_ref[0]]
                self.point_label.text = '({0:.3f},{1:.3f})'.format(x, y)
                edge = Window.width - self.graph_pos_to_window_pos(*point_ref)[0] - self.point_label.width
                if edge < 0:
                    self.point_label.pos = Window.width - self.point_label.width - 10, \
                                           self.graph_pos_to_window_pos(*point_ref)[1]
                else:
                    self.point_label.pos = self.graph_pos_to_window_pos(*point_ref)
                if 'right' == mouseMotion.button:
                    if len(self.plot_points.points):
                        self.plot_points.points.pop()
                else:
                    self.plot_points.points.append(point_ref)
                print(f'X:{x} Y:{y}')

    def _getNewEventTrigger(self):
        return Clock.create_trigger(self.update_points, interval=True, timeout=1 / 10)

    def _graph_transform(self, x, y):
        x_start = self.pos[0] + self.view_pos[0]
        x_end = self.x_start + self.view_size[0]
        y_start = self.pos[1] + self.view_pos[1]
        y_end = self.y_start + self.view_size[1]
        if not (x_start < x < x_end and y_start < y < y_end):
            return None
        x_out = self.xmin + (x - x_start) * (self.xmax - self.xmin) / self.view_size[0]
        y_out = self.ymin + (y - y_start) * (self.ymax - self.ymin) / self.view_size[1]
        return x_out, y_out

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
        self.lastClockTime = nowTime()
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

    def add_point(self, value):
        now = nowTime()
        time = now - self.lastClockTime + self.currentTime
        if time > self.xmax:
            self.xmax += 5
            self.xmin += 5
        if len(self.plot_points.points):
            self.point_label.disabled = False
            self.point_label.pos = self.graph_pos_to_window_pos(*self.plot_points.points[0])
        self.queue.addToeQueue(value, self.currentTime)
        self.currentTime = time
        self.lastClockTime = now

    def update_points(self, *args):
        self.plot.points = self.queue.get()


class GraphTopRow(BoxLayout):
    def __init__(self, assignedGraph, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = .05
        self.recordButton = Button(text='START')
        self.recordButton.background_normal = 'assets/start.png'
        self.saveDropdown = SaveButtonWithDropdown(assigned_graph=assignedGraph)
        self.graphTitle = GraphTitleInput()
        self.add_widget(self.graphTitle)
        self.add_widget(self.recordButton)
        self.add_widget(self.saveDropdown)

    def bindPress(self, function):
        self.recordButton.bind(on_press=function)

    def getTitle(self):
        return self.graphTitle.getTitle()


class GraphTitleInput(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2
        self.title_input = TextInput(text='Graph', multiline=False, halign='left')
        self.label = Label(text='Title:', size_hint_x=.20)
        self.add_widget(self.label)
        self.add_widget(self.title_input)
        self.size_hint_max_y = 40

    def getTitle(self):
        return str(self.title_input.text)


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


class GraphLayout(GridLayout):

    def __init__(self, graphProfile: GraphProfile, **kwargs):
        super().__init__(**kwargs)

        self.state_record = 0
        self.rows = 2
        # Graph setup
        self.graphProfile = graphProfile
        self.graph = GraphWidget()
        # Button Setup
        self.topRow = GraphTopRow(self.graph)
        self.topRow.bindPress(self.recordPress)
        self.add_widget(self.topRow)
        self.add_widget(self.graph)
        self.graphProfile.assignedGraph = self
        self.updatetoLatestGraphProfile()

    def getGraphTitle(self):
        return str(self.topRow.graphTitle.getTitle())

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

    iconsIterator = iter(['assets/start.png', 'assets/stop.png', 'assets/skip-back.png'])

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

    def addpoint(self, value):
        if self.state_record == 1:
            self.graph.add_point(value)

    @staticmethod
    def getTableFormFile(path):
        data = {}
        if os.path.exists(path):
            with open(path, 'r') as inFile:
                data = dict(json.load(inFile))
        thisGraph = GraphLayout()
        return data


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
