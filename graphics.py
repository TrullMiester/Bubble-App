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

# The interface will be a subclass of kivy's FloatLayout 
# after starting the app the interface will simply display 
# the current time and date. 

# To perform the health features, we will have a global function 
# that acts as a controller for our entire system. It will 
# check if conditions are met and if they are then it'll 
# perform the checks required. 

# All checks will be implemented seperately in different files. 
# All features will also be implemented seperately, but the kivy 
# elements will all be in this file. 

class QuestionButtons(Button):

    def other(self, button):
        if button == self.yes_button:
            return self.no_button
        else:
            return self.yes_button

    def confirms(self, which, button ,form):
        if button.text == self.confirmation:
            if which:
                self.test.add_score(1)

            current = self.test.next_question()

            if current == self.test.length():
                self.add_widget(self.ending_label)
                time.sleep(5)
            else:
                self.question_button.text = self.test.current_question()
        else:
            button.text = self.confirmation 
        self.other(button).text = ('No' if which else 'Yes') 
    def __init__(self, **kwargs):
        super(QuestionButtons, self).__init__(**kwargs)

class Tester(FloatLayout):

    def __init__(self, **kwargs): 
        super(Tester,self).__init__(**kwargs)

        Window.borderless = True
        Window.fullscreen = 'auto'

        self.in_progress = False
        self.test = TestTTS() 
        health_test_load(self.test)

        self.yes_button = Button(text="Yes", size_hint=(.5, .25), background_color = (0, 1, 0, 1))
        self.yes_button.bind(on_press=lambda func: self.confirms(True, self.yes_button, self.test))

        self.no_button = Button(text="No", size_hint=(.5, .25), pos_hint={'x':.5}, background_color = (1, 0, 0, 1))
        self.no_button.bind(on_press=lambda func: self.confirms(False, self.no_button, self.test))
        
        self.confirmation = "Are you sure?"

        self.question_button = Button(text=self.test.current_question(), size_hint=(1,.75), pos_hint={'y':.25}, background_color=(1,1,1,1))
        self.question_button.bind(on_press=lambda func: self.test.ask_question())

        self.ending_label = Button(text='You are all done!', size_hint=(1,1), background_color=(1,1,1,1))


class QuestionApp(App):
    def build(self):
        return Tester()

class InterfaceHome(FloatLayout):
    def __init__(self, **kwargs):
        super(InterfaceHome,self).__init__(**kwargs)

        Window.borderless = True 
        Window.fullscreen = 'auto' 
        Window.clearcolor = (1,1,1,1)

class Interface(App):
    def build(self): 
        return InterfaceHome()

class events():
    def __init__(self):
        self.checks = []
        self.done = True

    def make_clock_label(self, str):
        return Label(text=str, size_hint = (1, 1))

    def event_handler(self):
        while True:
            if self.done:
                current_time = datetime.datetime.now().strftime('%H:%M:%S')
                print(current_time)

                clock = self.make_clock_label(current_time)
                App().get_running_app().root.add_widget(clock)
                self.has_clock = True

                time.sleep(1)
                App().get_running_app().root.remove_widget(clock)



if __name__ == '__main__':
    Interface().run()

    get_events = events()
    get_events.event_handler()

    
