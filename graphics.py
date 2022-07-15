import kivy
kivy.require('2.1.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.button import Button 
from kivy.uix.label import Label 
from kivy.uix.floatlayout import FloatLayout 
from kivy.core.window import Window 

import time
import datetime

from tts import TestTTS, health_test_load
from audio import Calls, Input

# The interface will be a subclass of kivy's FloatLayout 
# after starting the app the interface will simply display 
# the current time and date. 

# To perform the health features, we will have a global function 
# that acts as a controller for our entire system. It will 
# check if conditions are met and if they are then it'll 
# perform the checks required. 

# Currently I still need to use this framework more, I don't have 
# much experience as this is my first time using it. For now I will 
# have a start button, if conditions are right it'll prompt the user 
# to start whatever checks it wants

class InterfaceHome(FloatLayout):
    def perform_check(self):
        self.inp.get_input()
        if self.inp.check_yes():
            self.next_question(True)

    def next_question(self, which):
        if which:
            self.health_test.add_score(1)

        current = self.health_test.next_question()

        if current < self.health_test.length():
            self.question_button.text = self.health_test.current_question()
        else:
            self.remove_widget(self.yes_button)
            self.remove_widget(self.no_button)
            self.remove_widget(self.question_button)

            label_text = ''
            score = self.health_test.current_question()

            if score >= 2:
                label_text = 'You should get checked out, we are scheduling an appointment ASAP!'
                self.caller.call()
            else:
                label_text = 'Everything looks great!'

            end = TestTTS()
            end.add_question(label_text) 
            self.end_button = Button(text=end.current_question())
            self.add_widget(self.end_button)
            end.ask_question() 
            time.sleep(10)
            self.remove_widget(self.end_button) 
            self.health_test_done = True
            
            self.add_widget(self.start_button)

    def start_health_test(self):
        self.remove_widget(self.start_button) 

        self.health_test = TestTTS()
        health_test_load(self.health_test)

        self.question_button = Button(text=self.health_test.current_question(), size_hint = (1,0.75), pos_hint = {'y':0.25})
        self.question_button.bind(on_press=lambda func: self.health_test.ask_question())
        self.add_widget(self.question_button)
        
        self.yes_button = Button(text='yes', size_hint = (0.5, 0.25), background_color = (0,1,0,1))
        self.yes_button.bind(on_press=lambda func: self.next_question(True))
        self.add_widget(self.yes_button)

        self.no_button = Button(text='no', size_hint = (0.5, 0.25), pos_hint = {'x' : 0.5}, background_color = (1,0,0,1))
        self.no_button.bind(on_press=lambda func: self.next_question(False))
        self.add_widget(self.no_button)

        self.mic_button = Button(text = 'M', size_hint = (0.1, 0.1), pos_hint = {'y' : 0.5}, background_color = (1, 1, 0, 1))
        self.mic_button.bind(on_press=lambda func: self.perform_check())
        self.add_widget(self.mic_button)


    def check(self):
        current_time = str(datetime.datetime.now().strftime('%H:%M:%S'))
        hms = list(map(int, current_time.split(':')))

        if hms[0] == 14 and not self.health_test_done:
            self.start_health_test()

    def __init__(self, **kwargs):
        super(InterfaceHome,self).__init__(**kwargs)

        Window.borderless = True 
        Window.fullscreen = 'auto' 

        self.inp = Input()
        self.caller = Calls()

        self.health_test_done = False

        self.start_button = Button(text='Start')
        self.start_button.bind(on_press=lambda func: self.check())
        self.add_widget(self.start_button)

class Interface(App):
    def get_root(self):
        return self.root 

    def build(self): 
        root = self.get_root()
        return root
    
    def __init__(self, **kwargs):
        super(Interface,self).__init__(**kwargs)

        self.root = InterfaceHome()

if __name__ == '__main__':
    app = Interface()
    app.run()


    
