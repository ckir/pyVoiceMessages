import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')

for voice in voices:
   print(voice.name)
   engine.setProperty('voice', voice.id)
   engine.setProperty("rate", 178) 
   engine. say("Warning! " + "I am the text spoken after changing the speech rate.")
   # a = 'The quick brown fox jumped over the lazy dog. Hello'
   a = 'Warning! The server edition.cnn.com is not responding'
   # engine.say('The quick brown fox jumped over the lazy dog.')
   # engine.say(a)
   # b = 'Hello'
   # engine.say(b)
engine.runAndWait()

