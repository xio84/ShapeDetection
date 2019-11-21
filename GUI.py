# from kivy.animation import Animation
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.image import Image
from kivy.config import Config
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')

import os


Builder.load_string('''
#kivy 1.0.9
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
                    source: 'img/open.png'
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
                    source: 'img/choose.png'
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
                        on_release: main.open(fc.path, fc.selection)

                    Button:
                        text: 'Open Rule Editor'
                        background_normal: ''
                        background_color: 1,1,1,1
                        color: 0,0,0,1
                        font_size: 10
                        size_hint: (1, 0.05)

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

                    Image: #Placeholder
                        id: placeholder
                        pos_hint: {'center_x': 0.5}
                        source: 'img/white.png'
                        allow_stretch: True
                        keep_ratio: True
                        size_hint_y: None
                        size_hint_x: None
                        width: self.parent.width - 15
                        height: self.parent.width - 15 /self.image_ratio
            
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
                    source: 'img/white.png'
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

                Image:
                    id: result
                    pos_hint: {'center_x': 0.5}
                    source: 'img/white.png'
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
                    text: 'Hit Rules'
                    text_size: self.size
                    color: 0,0,0,1
                    halign: 'left'
                    valign: 'middle'
                    font_size: 12
                    pos_hint: {'x': 0.38, 'y': 0.4}

                Image:
                    id: result
                    pos_hint: {'center_x': 0.5}
                    source: 'img/white.png'
                    allow_stretch: True
                    keep_ratio: True
                    size_hint_y: None
                    size_hint_x: None
                    width: self.parent.width - 30
                    height: self.parent.width - 30/self.image_ratio
'''
)

class MainScreen(BoxLayout):
    def open(self, path, filename):
        with open(os.path.join(path, filename[0])) as f:
            print(f.read())
        
    def selected(self, filename):
        print("selected: %s" % filename[0])

class MainApp(App):

    def build(self):
        start = MainScreen()
        return start

if __name__ == '__main__':
    MainApp().run()