# import speech recognition modules.
import speech_recognition as sr
import difflib
from tkinter import Text, END, NORMAL, DISABLED

wordlist = [("1", 1), ("one", 1), ("want", 1), ("wand", 1), ("2", 2), ("two", 2), ("to", 2), ("too", 2), ("3", 3), ("three", 3), ("tree", 3), ("4", 4), ("four", 4), ("for", 4), ("far", 4), ("5", 5), ("five", 5), ("v", 5), ("6", 6), ("six", 6), ("fix", 6), ("sex", 6), ("7", 7), ("seven", 7), ("8", 8), ("eight", 8), ("a", 8), ("ate", 8), ("alfa", "a"), ("alpha", "a"), ("bravo", "b"), ("charlie", "c"), ("delta", "d"), ("data", "d"), ("echo", "e"), ("eco", "e"), ("egg", "e"), ("go", "e"), ("foxtrot", "f"), ("foxdrop", "f"), ("pork chop", "f"), ("porkchop", "f"), ("fucktrump", "f"), ("golf", "g"), ("wolf", "g"), ("hotel", "h"), ("potala", "h"), ("resign", -1)]

class SpeechRecognizer:
	
	def __init__(self, commandText = None):
		self.__commandText = commandText
	
	def audio2text_google(self):
		# get audio from the microphone
		r = sr.Recognizer()
		r.pause_threshold = 0.5
		r.phrase_threshold = 0.1
		r.non_speaking_duration = 0.5
		r.dynamic_energy_threshold = False
		r.energy_threshold = 500
		with sr.Microphone() as source:
			r.adjust_for_ambient_noise(source)
			print("Please command for a piece to move: ")
			self.__printToCommandText("Please command for a piece to move: ")
			audio = r.listen(source)
		try:
			# Try to recognize sentence from user by using google api.
			sentence = r.recognize_google(audio)
			sentence = sentence.lower()
			sent = sentence.split(" ")
			if (len(sent) == 4 or len(sent) == 3 or len(sent) == 1):
				sent1 = ""
				for i in range(0, len(sent)):
					sent1 = sent1 + str(self.lookForWord(sent[i]))
				return sent1
			else:
				return -2
		except sr.UnknownValueError:
			return -2
		except sr.RequestError as e:
			print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
			self.__printToCommandText("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
			return 0
	
	def lookForWord(self, word):
		for i in range(0 , len(wordlist)):
			if (word == wordlist[i][0]):
				return wordlist[i][1]
	
	
	def audio2text_sphinx(self, keyword_entries=None, grammar=None):
		# get audio from the microphone
		r = sr.Recognizer()
		r.pause_threshold = 0.8
		r.phrase_threshold = 0.3
		r.non_speaking_duration = 0.8
		with sr.Microphone() as source:
			r.dynamic_energy_threshold = False
			r.adjust_for_ambient_noise(source)
			print("Please command for a piece to move: ")
			self.__printToCommandText("Please command for a piece to move: ")
			audio = r.listen(source)
		try:
			# Try to recognize sentence from user by using pocketsphinx.
			sentence = r.recognize_sphinx(audio_data = audio, language = "en-US", keyword_entries = keyword_entries, grammar = grammar, show_all = False)
			return sentence
		except sr.UnknownValueError:
			return -1
		except sr.RequestError as e:
			return 0
	
	def __printToCommandText(self, string):
		if (self.__commandText != None):
			self.__commandText.config(state = NORMAL)
			self.__commandText.insert(END, "\n" + str(string))
			self.__commandText.config(state = DISABLED)
