import os
from twilio.rest import Client
import speech_recognition as sr

class Calls:
    def __init__(self):
        self.account_sid = os.environ['TWILIO_ACCOUNT_SID']
        self.auth_token = os.environ['TWILIO_AUTH_TOKEN']
        self.client = Client(self.account_sid, self.auth_token)

    def call(self):
        self.client.calls.create(
            url='http://demo.twilio.com/docs/voice.xml',
            to='+13127527493',
            from_='+18455169336')

class Input:
    def __init__(self):
        self.recog = sr.Recognizer()
        self.mic = sr.Microphone()
        self.text = ''
    
    def get_input(self):
        with self.mic as source:
            audio = self.recog.listen(source)
        
        self.text = self.recog.recognize_google(audio)

    def check_yes(self):
        words = self.text.split()

        contains = False
        for word in words:
            if word == 'yes':
                contains = True 

        return contains
    

if __name__ == '__main__':
    inp = Input()
    inp.get_input()
    print(inp.check_yes())

