import speech_recognition as sr
import pyttsx3

class AI:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()

    def listen(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            self.recognizer.energy_threshold = 500
            try:
                audio = self.recognizer.listen(source)
                command = self.recognizer.recognize_google(audio)
                return command
            except sr.UnknownValueError:
                return "Could not understand audio"

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()


