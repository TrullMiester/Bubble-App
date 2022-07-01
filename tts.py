from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play, _play_with_simpleaudio
import time, os, wave
import kivy
from kivy.uix.button import Button 

class TestTTS:
    def __init__(self, language='en', speed=False): 
        self.lang = language
        self.slow = speed
        self.questions = []
        self.number = 0
        self.playback = None 
        self.score = 0

    def length(self):
        return len(self.questions)

    def add_question(self, question: str):
        self.questions.append(question)

        index = self.length()-1
        file_name = str(index) + ".mp3" 
        tts_object = gTTS(self.questions[index], lang=self.lang, slow=self.slow)
        tts_object.save(file_name)
        
    def ask_question(self):
        audio = AudioSegment.from_mp3(str(self.current_question) + ".mp3")
        self.playback = _play_with_simpleaudio(audio)
     
    def stop_question(self):
        self.playback.stop()

    def next_question(self):
        self.number += 1
        return self.number
    
    def current_question(self):
        assert(self.number < self.length()) 
        
        return self.questions[self.number]
    
    def add_score(self, amount):
        self.score += amount


def health_test_load(form):
    form.add_question("Do you want to answer some questions?")
    form.add_question("Have you encountered today or yesterday chest pain that may feel like pressure, tightness, pain, squeezing or aching?")
    form.add_question("Do you recall recently encountering shortness of breath?")
    form.add_question("Did you feel recently pain or discomfort in the jaw, neck, back, arm or a shoulder?")



def main():
    player = TestTTS()
    health_test_load(player)
    player.ask_question()
    time.sleep(3)
    player.stop_question()
    player.next_question()
    player.ask_question()
    time.sleep(3)
    player.stop_question()



if __name__ == '__main__':
    main()


