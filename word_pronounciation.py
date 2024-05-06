from gtts import gTTS
import os

def pronounce_word(word, lang='en'):
    tts = gTTS(text=word, lang=lang)
    tts.save("pronunciation.mp3")
    #os.system("mpg321 pronunciation.mp3")  # For Linux
    os.system("afplay pronunciation.mp3")  # For MacOS

def pronounce_alphabet(lang='nl'):
    dutch_alphabet = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZzÀàÁáÈèÉéËëÍíÏïÓóÖöÙùÚúÜüÛûÝýAaCcEeGgIjOeUu"
    #alphabet = 'abcdefghijklmnopqrstuvwxyz'
    for letter in dutch_alphabet:
        pronounce_word(letter, lang)

pronounce_alphabet()
