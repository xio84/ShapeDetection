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
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.treeview import *
# from kivy.uix.image import Image
from kivy.config import Config
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')

import shapeDetector as sd

import os

# from shapeDetector import *

file_path = 'img/open.png'
CHOSEN_SHAPE = -1

Builder.load_string('''
#:kivy 1.0.9
#:import TreeViewLabel kivy.uix.treeview.TreeViewLabel
#:import Clock kivy.clock.Clock
<MainScreen>:
    id: main
    canvas.before:
        Color:
            rgba: 0.84, 0.84, 0.84, 1
        Rectangle:
            pos: self.pos
            size: self.size
    on_enter: root.createTree(), Clock.schedule_once(root.update, 0.3)
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
                        on_release: 
                            root.manager.current= 'Filechooser'

                    Button:
                        text: 'Open Rule Editor'
                        background_normal: ''
                        background_color: 1,1,1,1
                        color: 0,0,0,1
                        font_size: 10
                        size_hint: (1, 0.05)
                        on_release: 
                            root.openRuleEditor()

                    Button:
                        text: 'Show Rules'
                        background_normal: ''
                        background_color: 1,1,1,1
                        color: 0,0,0,1
                        font_size: 10
                        size_hint: (1, 0.05)
                        on_release: root.changeRulesText(root.arrayRules)

                    Button:
                        text: 'Show Facts'
                        background_normal: ''
                        background_color: 1,1,1,1
                        color: 0,0,0,1
                        font_size: 10
                        size_hint: (1, 0.05)
                        on_release: root.changeFactsText(root.arrayFacts)
                    
                    Button:
                        text: 'Search'
                        background_normal: ''
                        background_color: 1,1,1,1
                        color: 0,0,0,1
                        font_size: 10
                        size_hint: (1, 0.05)
                        on_release: root.search()

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
                            text: root.factsText
                    
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
                            text: root.rulesText

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

    Button:
        text: 'Back to Main Screen'
        background_normal: ''
        background_color: 0,0,0,0
        color: 1,1,1,1
        font_size: 20
        size_hint: (0.5, 0.05)
        pos_hint: {'center_x': 0.5, 'center_y': 0.08}
        on_release: 
            root.manager.current= 'MainScreen'
            
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

class MainScreen(Screen):
    sourceimg = StringProperty('img/open.png')
    detectionimg = StringProperty('img/choose.png')
    resultimg = StringProperty('img/white.png')

    factsText = StringProperty('')
    rulesText = StringProperty('')

    arrayFacts = ''
    arrayRules = ''

    def changeArrayFacts(self, text):
        self.arrayFacts = text
    
    def changeArrayRules(self, text):
        self.arrayRules = text

    def changeStatus(self, success):
        if (success):
            self.resultimg = 'img/success.png'
        else:
            self.resultimg = 'img/fail.png'
            text = ['']
            self.changeFactsText(text)
            self.changeRulesText(text)
            self.changeDetection('img/white.png')

    def changeSource(self):
        self.sourceimg = file_path
    
    def changeDetection(self, path):
        self.detectionimg = path
    
    def changeFactsText(self, arrayText):
        text = ''
        for i in arrayText:
            text += i + '\n'
        self.factsText = text
    
    def changeRulesText(self, arrayText):
        text = ''
        for i in arrayText:
            text += i + '\n'
        self.rulesText = text

    def openRuleEditor(self):
        osCommandString = "notepad.exe shapeClassification.clp"
        os.system(osCommandString)

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
        beraturan = self.ids.tv.add_node(CustomLabel(text='Beraturan', font_size='10', internal_id=12), parralelogram)
        self.ids.tv.add_node(CustomLabel(text='Persegi', font_size='10', internal_id=13), beraturan)
        self.ids.tv.add_node(CustomLabel(text='Paralelogram', font_size='10', internal_id=14), beraturan)
        self.ids.tv.add_node(CustomLabel(text='Layang-layang', font_size='10', internal_id=15), parralelogram)

        trapezoid = self.ids.tv.add_node(CustomLabel(text='Trapesium', font_size='10', internal_id=16), quad)
        self.ids.tv.add_node(CustomLabel(text='Sama kaki', font_size='10', internal_id=17), trapezoid)
        self.ids.tv.add_node(CustomLabel(text='Rata kanan', font_size='10', internal_id=18), trapezoid)
        self.ids.tv.add_node(CustomLabel(text='Rata kiri', font_size='10', internal_id=19), trapezoid)

        penta = self.ids.tv.add_node(CustomLabel(text='Pentagon', font_size='10', internal_id=20))

        hexa = self.ids.tv.add_node(CustomLabel(text='Hexagon', font_size='10', internal_id=21))
    
    def search(self):
        text = ['']
        self.changeFactsText(text)
        self.changeRulesText(text)
        shapes = sd.shapeDetection("img/shapes.jpg", threshold=240)['shapesArray']
        status = False
        if (CHOSEN_SHAPE == 2):
            # shapeName = 'Segitiga Lancip'
            for shape in shapes:
                for i in shape['facts']:
                    if (' sharp' in i):
                        status = True
                        self.changeDetection(shape['imgPath'])
                        self.changeArrayFacts(shape['facts'])
                        self.changeArrayRules(shape['rules'])
                        break
            self.changeStatus(status)
        elif (CHOSEN_SHAPE == 3):
            # shapeName = 'Segitiga Tumpul'
            for shape in shapes:
                for i in shape['facts']:
                    if ('obstuse' in i):
                        status = True
                        self.changeDetection(shape['imgPath'])
                        self.changeArrayFacts(shape['facts'])
                        self.changeArrayRules(shape['rules'])
                        break
            self.changeStatus(status)
        elif (CHOSEN_SHAPE == 4):
            # shapeName = 'Segitiga Siku'
            for shape in shapes:
                for i in shape['facts']:
                    if (' right' in i):
                        status = True
                        self.changeDetection(shape['imgPath'])
                        self.changeArrayFacts(shape['facts'])
                        self.changeArrayRules(shape['rules'])
                        break
            self.changeStatus(status)
        elif (CHOSEN_SHAPE == 6):
            # shapeName = 'Segitiga Sama Kaki dan Siku'
            for shape in shapes:
                for i in shape['facts']:
                    if (' isosceles' in i and ' right' in i):
                        status = True
                        self.changeDetection(shape['imgPath'])
                        self.changeArrayFacts(shape['facts'])
                        self.changeArrayRules(shape['rules'])
                        break
            self.changeStatus(status)
        elif (CHOSEN_SHAPE == 7):
            # shapeName = 'Segitiga Sama Kaki dan Tumpul'
            for shape in shapes:
                for i in shape['facts']:
                    if (' isosceles' in i and ' obstuse' in i):
                        status = True
                        self.changeDetection(shape['imgPath'])
                        self.changeArrayFacts(shape['facts'])
                        self.changeArrayRules(shape['rules'])
                        break
            self.changeStatus(status)
        elif (CHOSEN_SHAPE == 8):
            # shapeName = 'Segitiga Sama Kaki dan Lancip'
            for shape in shapes:
                for i in shape['facts']:
                    if (' isoscelse' in i and ' sharp' in i):
                        status = True
                        self.changeDetection(shape['imgPath'])
                        self.changeArrayFacts(shape['facts'])
                        self.changeArrayRules(shape['rules'])
                        break
            self.changeStatus(status)
        elif (CHOSEN_SHAPE == 9):
            # shapeName = 'Segitiga Sama Sisi'
            for shape in shapes:
                for i in shape['facts']:
                    if (' equilateral' in i):
                        status = True
                        self.changeDetection(shape['imgPath'])
                        self.changeArrayFacts(shape['facts'])
                        self.changeArrayRules(shape['rules'])
                        break
            self.changeStatus(status)
        elif (CHOSEN_SHAPE == 13):
            # shapeName = 'Persegi'
            for shape in shapes:
                for i in shape['facts']:
                    if (' rectangle' in i):
                        status = True
                        self.changeDetection(shape['imgPath'])
                        self.changeArrayFacts(shape['facts'])
                        self.changeArrayRules(shape['rules'])
                        break
            self.changeStatus(status)
        elif (CHOSEN_SHAPE == 14):
            # shapeName = 'Paralelogram'
            for shape in shapes:
                for i in shape['facts']:
                    if (' parallelogram' in i):
                        status = True
                        self.changeDetection(shape['imgPath'])
                        self.changeArrayFacts(shape['facts'])
                        self.changeArrayRules(shape['rules'])
                        break
            self.changeStatus(status)      
        elif (CHOSEN_SHAPE == 15):
            # shapeName = 'Layang-Layang'
            for shape in shapes:
                for i in shape['facts']:
                    if (' kite' in i):
                        status = True
                        self.changeDetection(shape['imgPath'])
                        self.changeArrayFacts(shape['facts'])
                        self.changeArrayRules(shape['rules'])
                        break
            self.changeStatus(status)
        elif (CHOSEN_SHAPE == 17):
            # shapeName = 'Trapesium Sama Kaki'
            for shape in shapes:
                for i in shape['facts']:
                    if (' regular' in i):
                        status = True
                        self.changeDetection(shape['imgPath'])
                        self.changeArrayFacts(shape['facts'])
                        self.changeArrayRules(shape['rules'])
                        break
            self.changeStatus(status)
        elif (CHOSEN_SHAPE == 18):
            # shapeName = 'Trapesium Rata Kanan'
            for shape in shapes:
                for i in shape['facts']:
                    if (' rigth-side' in i):
                        status = True
                        self.changeDetection(shape['imgPath'])
                        self.changeArrayFacts(shape['facts'])
                        self.changeArrayRules(shape['rules'])
                        break
            self.changeStatus(status)
        elif (CHOSEN_SHAPE == 19):
            # shapeName = 'Trapesium Rata Kiri'
            for shape in shapes:
                for i in shape['facts']:
                    if (' left-side' in i):
                        status = True
                        self.changeDetection(shape['imgPath'])
                        self.changeArrayFacts(shape['facts'])
                        self.changeArrayRules(shape['rules'])
                        break
            self.changeStatus(status)
        elif (CHOSEN_SHAPE == 20):
            # shapeName = 'Pentagon'
            for shape in shapes:
                for i in shape['facts']:
                    if (' pentagon' in i):
                        status = True
                        self.changeDetection(shape['imgPath'])
                        self.changeArrayFacts(shape['facts'])
                        self.changeArrayRules(shape['rules'])
                        break
            self.changeStatus(status)
        elif (CHOSEN_SHAPE == 21):
            # shapeName = 'Hexagon'
            for shape in shapes:
                for i in shape['facts']:
                    if (' hexagon' in i):
                        status = True
                        self.changeDetection(shape['imgPath'])
                        self.changeArrayFacts(shape['facts'])
                        self.changeArrayRules(shape['rules'])
                        break
            self.changeStatus(status)

        # print(sd.shapeDetection("img/shapes.jpg", threshold=240))
        # print(shapeName)
    
    def open(self, path, filename):
        with open(os.path.join(path, filename[0])) as f:
            print(f.read())
    

    def update(self, instance):
        self.changeSource()

# create the layout class 
class Filechooser(Screen): 
    def select(self, *args): 
        try: 
            global file_path
            self.label.text = args[1][0] 
            file_path = args[1][0]
        except: pass
    def changeSource(self, instance):
        self.ids.source.source = StringProperty(file_path)

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
