from SpeechRecognizer import SpeechRecognizer

grammarPath = "./whynot.gram"
grammarPath2 = "./digits.gram"
grammarPath3 = "./commands.gram"

a = SpeechRecognizer()

while (True):
	print(a.audio2text_google())
	# inp = int(input("quit? "))
	# if (inp == 1):
		# break
	# inp = int(input("tuple?"))
	# inp2 = int(input("grammar?"))
	# if (inp == 0 & inp2 == 0):
		# print(a.audio2text_sphinx())
	# elif (inp == 0 & inp2 == 1):
		# print(a.audio2text_sphinx(grammar = grammarPath))
	# elif (inp == 0 & inp2 == 2):
		# print(a.audio2text_sphinx(grammar = grammarPath2))
	# elif (inp == 0 & inp2 == 3):
		# print(a.audio2text_sphinx(grammar = grammarPath3))
	# elif (inp == 1):
		# print(a.audio2text_sphinx(keyword_entries = tup))
	# else:
		# print(a.audio2text_sphinx())