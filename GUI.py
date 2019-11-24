# Program to explain how to use File chooser in kivy 
		
# import kivy module	 
import kivy 
from kivy.lang import Builder
# base Class of your App inherits from the App class.	 
# app:always refers to the instance of your application	 
from kivy.app import App 
		
# this restrict the kivy version i.e 
# below this kivy version you cannot 
# use the app or software 
kivy.require('1.9.0') 

# BoxLayout arranges widgets in either in 
# a vertical fashion that is one on top of 
# another or in a horizontal fashion 
# that is one after another. 

from kivy.uix.boxlayout import BoxLayout 
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen

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
                        on_release: 
                            root.manager.current= 'Filechooser'

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
                
                BoxLayout:
                    # size_hint: 1.08, 1.08
                    # pos_hint: {'top': 2}
                    canvas.before:
                        Color:
                            rgba: 1,1,1,1
                        Rectangle:
                            size: self.size
                            pos: self.pos
                    
                    ScrollView:
                        # do_scroll_x: False
                        # do_scroll_y: True
                        Label:
                            size_hint_y: None
                            height: self.texture_size[1]
                            size: self.texture_size
                            color: 0,0,0,1
                            padding: 10, 10
                            halign: 'left'
                            valign: 'top'
                            text: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
                    
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
                    id: rules
                    pos_hint: {'center_x': 0.5}
                    source: 'img/white.png'
                    allow_stretch: True
                    keep_ratio: True
                    size_hint_y: None
                    size_hint_x: None
                    width: self.parent.width - 30
                    height: self.parent.width - 30/self.image_ratio
<Filechooser>: 
      
    label: label 
  
    # Providing the orentation 
    orientation: 'vertical'
  
    # Creating the File list / icon view 
      
    BoxLayout: 
        # Creating Icon view other side 
        FileChooserIconView: 
            canvas.before: 
                Color: 
                    rgb: .5, .4, .5
                Rectangle: 
                    pos: self.pos 
                    size: self.size 
            on_selection: root.select(*args) 
        
    Button:
        text: 'Back to Main Screen'
        background_normal: ''
        background_color: 1,1,1,1
        color: 0,0,0,1
        font_size: 10
        size_hint: (0.5, 0.05)
        on_release: 
            root.manager.current= 'MainScreen'
                

    # Adding label 
    Label: 
        id: label 
        size_hint_y: .1
        canvas.before: 
            Color: 
                rgb: .5, .5, .4
            Rectangle: 
                pos: self.pos 
                size: self.size 
         
''')

file_path = ''

class MainScreen(Screen):
    def open(self, path, filename):
        with open(os.path.join(path, filename[0])) as f:
            print(f.read())
        
    def selected(self, filename):
        print("selected: %s" % filename[0])

# create the layout class 
class Filechooser(Screen): 
    def select(self, *args): 
        try: 
            self.label.text = args[1][0] 
            file_path = args[1][0]
            print(file_path)
        except: pass

sm = ScreenManager()
sm.add_widget(MainScreen(name='MainScreen'))
sm.add_widget(Filechooser(name='Filechooser'))
# Create the App class 
class MainApp(App): 
    def build(self): 
        return sm 
  
# run the App 
if __name__ == '__main__': 
    MainApp().run() 
