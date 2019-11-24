# from kivy.animation import Animation
from kivy.uix.scrollview import ScrollView
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.treeview import *
# from kivy.uix.image import Image
from kivy.config import Config
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')

import os

# from shapeDetector import *

CHOSEN_SHAPE = -1

Builder.load_string('''
#kivy 1.0.9
#import TreeViewLabel kivy.uix.treeview.TreeViewLabel
<MainScreen>:
    id: main
    canvas.before:
        Color:
            rgba: 0.84, 0.84, 0.84, 1
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        orientation: 'vertical'
        space: 20
        #UPPER LAYOUT
        BoxLayout:
            orientation: 'horizontal'

            BoxLayout:
                orientation: 'vertical'
                Label: 
                    text: 'Source Image'
                    text_size: self.size
                    color: 0,0,0,1
                    halign: 'left'
                    valign: 'middle'
                    font_size: 12
                    pos_hint: {'x': 0.37, 'y': 1}

                Image:
                    id: source
                    pos_hint: {'center_x': 0.5}
                    source: root.sourceimg
                    allow_stretch: True
                    keep_ratio: True
                    size_hint_y: None
                    size_hint_x: None
                    width: self.parent.width - 5
                    height: self.parent.width - 5/self.image_ratio

            BoxLayout:
                orientation: 'vertical'
                Label: 
                    text: 'Detection Image'
                    text_size: self.size
                    color: 0,0,0,1
                    halign: 'left'
                    valign: 'middle'
                    font_size: 12
                    pos_hint: {'x': 0.32, 'y': 1}

                Image:
                    id: detection
                    pos_hint: {'center_x': 0.5}
                    source: root.detectionimg
                    allow_stretch: True
                    keep_ratio: True
                    size_hint_y: None
                    size_hint_x: None
                    width: self.parent.width - 5
                    height: self.parent.width - 5 /self.image_ratio
                    
            BoxLayout:
                orientation: 'vertical'
                size_hint_x: 0.5

                BoxLayout:
                    orientation: 'vertical'
                    spacing: 10
                    padding: 10, 20, 10, 0

                    Button:
                        text: 'Open Image'
                        background_normal: ''
                        background_color: 1,1,1,1
                        color: 0,0,0,1
                        font_size: 10
                        size_hint: (1, 0.05)
                        on_release: root.createTree()

                    Button:
                        text: 'Open Rule Editor'
                        background_normal: ''
                        background_color: 1,1,1,1
                        color: 0,0,0,1
                        font_size: 10
                        size_hint: (1, 0.05)
                        on_release: root.changeImg()

                    Button:
                        text: 'Show Rules'
                        background_normal: ''
                        background_color: 1,1,1,1
                        color: 0,0,0,1
                        font_size: 10
                        size_hint: (1, 0.05)

                    Button:
                        text: 'Show Facts'
                        background_normal: ''
                        background_color: 1,1,1,1
                        color: 0,0,0,1
                        font_size: 10
                        size_hint: (1, 0.05)
                    
                    Button:
                        text: 'Search'
                        background_normal: ''
                        background_color: 1,1,1,1
                        color: 0,0,0,1
                        font_size: 10
                        size_hint: (1, 0.05)
                        on_release: root.search()
                    
                    Button:
                        text: 'Init Tree'
                        background_normal: ''
                        background_color: 1,1,1,1
                        color: 0,0,0,1
                        font_size: 10
                        size_hint: (1, 0.05)
                        on_release: root.createTree()

                BoxLayout:
                    orientation: 'vertical'
                    padding: 10, 10, 10, 0

                    Label:
                        text: 'What shape do you want'
                        text_size: self.size
                        color: 0,0,0,1
                        halign: 'left'
                        valign: 'middle'
                        font_size: 10
                        size_hint_y: 0.11

                    BoxLayout:
                        canvas.before:
                            Color:
                                rgba: 0,0,0,1
                            Rectangle:
                                size: self.size
                                pos: self.pos
                        
                        ScrollView:
                            CustomTreeView:
                                id: tv
                                root_options: {'text': 'Shapes','font_size': 10}
                                hide_root: False
                                indent_level: 4
                                size_hint_y: None
                                
                    # Image: #Placeholder
                    #     id: placeholder
                    #     pos_hint: {'center_x': 0.5}
                    #     source: 'img/white.png'
                    #     allow_stretch: True
                    #     keep_ratio: True
                    #     size_hint_y: None
                    #     size_hint_x: None
                    #     width: self.parent.width - 15
                    #     height: self.parent.width - 15 /self.image_ratio
            
            # FileChooser:
            #     id: fc
            #     on_selection: main.selected(fc.selection)
            
        #BOTTOM LAYOUT
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: 0.8
          
            BoxLayout:
                orientation: 'vertical'
                padding: 25,0,25,5
                Label: 
                    text: 'Detection Result'
                    text_size: self.size
                    color: 0,0,0,1
                    halign: 'left'
                    valign: 'middle'
                    font_size: 12
                    pos_hint: {'x': 0.31, 'y': 0.4}

                Image:
                    id: result
                    pos_hint: {'center_x': 0.5}
                    source: root.resultimg
                    allow_stretch: True
                    keep_ratio: True
                    size_hint_y: None
                    size_hint_x: None
                    width: self.parent.width - 30
                    height: self.parent.width - 30/self.image_ratio

            BoxLayout:
                orientation: 'vertical'
                padding: 0,0,25,5
                Label: 
                    text: 'Matched facts'
                    text_size: self.size
                    color: 0,0,0,1
                    halign: 'left'
                    valign: 'middle'
                    font_size: 12
                    pos_hint: {'x': 0.35, 'y': 0.4}
                    size_hint_y: 0.11
                
                BoxLayout:
                    # size_hint: 1.08, 1.08
                    canvas.before:
                        Color:
                            rgba: 1,1,1,1
                        Rectangle:
                            size: self.size
                            pos: self.pos
                    
                    ScrollView:
                        Label:
                            pos_hint: {'y': 5}
                            size_hint_y: None
                            text_size: self.width, None
                            height: self.texture_size[1]
                            size: self.texture_size
                            color: 0,0,0,10
                            padding: 10, 10
                            halign: 'left'
                            valign: 'top'
                            text: ('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.' * 30)
                    
            BoxLayout:
                orientation: 'vertical'
                padding: 0,0,25,5
                Label: 
                    text: 'Hit Rules'
                    text_size: self.size
                    color: 0,0,0,1
                    halign: 'left'
                    valign: 'middle'
                    font_size: 12
                    pos_hint: {'x': 0.38, 'y': 0.4}
                    size_hint_y: 0.11

                BoxLayout:
                    # size_hint: 1.08, 1.08
                    canvas.before:
                        Color:
                            rgba: 1,1,1,1
                        Rectangle:
                            size: self.size
                            pos: self.pos
                    
                    ScrollView:
                        Label:
                            pos_hint: {'y': 5}
                            size_hint_y: None
                            text_size: self.width, None
                            height: self.texture_size[1]
                            size: self.texture_size
                            color: 0,0,0,10
                            padding: 10, 10
                            halign: 'left'
                            valign: 'top'
                            text: ('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.' * 30)
'''
)
class CustomLabel(TreeViewLabel):
    internal_id = NumericProperty()

    def selected_node(self):
        global CHOSEN_SHAPE
        CHOSEN_SHAPE = self.internal_id

class CustomTreeView(TreeView):
    internal_id = NumericProperty()
    
    def select_node(self, node):
        if (node.parent_node != None):
            node.selected_node()

class MainScreen(BoxLayout):
    sourceimg = 'img/open.png'
    detectionimg = 'img/choose.png'
    resultimg = 'img/white.png'

    def changeImg(self):
        print(self.sourceimg)
        self.sourceimg = 'img/success.png'

    def createTree(self):
        tv = CustomTreeView(internal_id=0)
        self.ids.tv.bind(minimum_height=self.ids.tv.setter('height'))

        triangle = self.ids.tv.add_node(CustomLabel(text='Triangle', font_size='10', internal_id=1))
        self.ids.tv.add_node(CustomLabel(text='Lancip', font_size='10', internal_id=2), triangle)
        self.ids.tv.add_node(CustomLabel(text='Tumpul', font_size='10', internal_id=3), triangle)
        self.ids.tv.add_node(CustomLabel(text='Siku-siku', font_size='10', internal_id=4), triangle)

        isosTriangle = self.ids.tv.add_node(CustomLabel(text='Sama kaki', font_size='10', internal_id=5), triangle)
        self.ids.tv.add_node(CustomLabel(text='Sama kaki dan siku-siku', font_size='10', internal_id=6), isosTriangle)
        self.ids.tv.add_node(CustomLabel(text='Sama kaki dan tumpul', font_size='10', internal_id=7), isosTriangle)
        self.ids.tv.add_node(CustomLabel(text='Sama kaki dan lancip', font_size='10', internal_id=8), isosTriangle)
        self.ids.tv.add_node(CustomLabel(text='Sama sisi', font_size='10', internal_id=9), triangle)
        
        quad = self.ids.tv.add_node(CustomLabel(text='Quadrilateral', font_size='10', internal_id=10))

        parralelogram = self.ids.tv.add_node(CustomLabel(text='Jajar genjang', font_size='10', internal_id=11), quad)
        self.ids.tv.add_node(CustomLabel(text='Beraturan', font_size='10', internal_id=12), parralelogram)
        self.ids.tv.add_node(CustomLabel(text='Layang-layang', font_size='10', internal_id=13), parralelogram)

        trapezoid = self.ids.tv.add_node(CustomLabel(text='Trapesium', font_size='10', internal_id=14), quad)
        self.ids.tv.add_node(CustomLabel(text='Sama kaki', font_size='10', internal_id=15), trapezoid)
        self.ids.tv.add_node(CustomLabel(text='Rata kanan', font_size='10', internal_id=16), trapezoid)
        self.ids.tv.add_node(CustomLabel(text='Rata kiri', font_size='10', internal_id=17), trapezoid)

        penta = self.ids.tv.add_node(CustomLabel(text='Pentagon', font_size='10', internal_id=18))

        hexa = self.ids.tv.add_node(CustomLabel(text='Hexagon', font_size='10', internal_id=19))
    
    def search(self):
        shapeName = ''
        if (CHOSEN_SHAPE == 2):
            shapeName = 'Segitiga Lancip'
        elif (CHOSEN_SHAPE == 3):
            shapeName = 'Segitiga Tumpul'
        elif (CHOSEN_SHAPE == 4):
            shapeName = 'Segitiga Siku'
        elif (CHOSEN_SHAPE == 6):
            shapeName = 'Segitiga Sama Kaki dan Siku'
        elif (CHOSEN_SHAPE == 7):
            shapeName = 'Segitiga Sama Kaki dan Tumpul'
        elif (CHOSEN_SHAPE == 8):
            shapeName = 'Segitiga Sama Kaki dan Lancip'
        elif (CHOSEN_SHAPE == 9):
            shapeName = 'Segitiga Sama Sisi'
        elif (CHOSEN_SHAPE == 12):
            shapeName = 'Jajar Genjang Beraturan'
        elif (CHOSEN_SHAPE == 13):
            shapeName = 'Jajar Genjang Layang'
        elif (CHOSEN_SHAPE == 15):
            shapeName = 'Trapesium Sama Kaki'
        elif (CHOSEN_SHAPE == 16):
            shapeName = 'Trapesium Rata Kanan'
        elif (CHOSEN_SHAPE == 17):
            shapeName = 'Trapesium Rata Kiri'
        elif (CHOSEN_SHAPE == 18):
            shapeName = 'Pentagon'
        elif (CHOSEN_SHAPE == 19):
            shapeName = 'Hexagon'
        
        print(shapeName)

class MainApp(App):

    def build(self):
        start = MainScreen()
        return start

if __name__ == '__main__':
    MainApp().run()