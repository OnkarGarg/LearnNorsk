import json
import random
from io import BytesIO

import pygame
import speech_recognition as sr
from gtts import gTTS
from pygame import mixer

print("Welcome, human.")
print("dir() is a function, returning a list.")
print("This has no output")
a_list = dir(sr)
print("but this does", dir(sr))
print("The help() command uses pydoc to print to stdout")
help(sr)
print("This program is gratified to be of use.")

def speak(text):
    mp3_fp = BytesIO()
    tts = gTTS(text, lang='no')
    tts.write_to_fp(mp3_fp)
    mixer.init()
    mp3_fp.seek(0)
    mixer.music.load(mp3_fp, "mp3")
    mixer.music.play()
    while mixer.music.get_busy():
        pygame.time.Clock().tick(10)


def hear(recognizer: sr.Recognizer, audio_source):
    audio = recognizer.listen(audio_source)
    heard = ""
    while not heard:
        try:
            heard = recognizer.recognize_google(audio, language="no-NO")
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            recognizer.adjust_for_ambient_noise(audio_source)
            audio = recognizer.listen(audio_source)
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return heard


def hear_norwegian(recognizer: sr.Recognizer, audio_source, text):
    heard = hear(recognizer, audio_source)

    print("You said: " + heard)
    if heard.lower() == text["norwegian"].lower().replace(".", "").replace("?", "").replace("!", "").replace(",",
                                                                                                             ""):
        print("Correct!")
        speak(text["norwegian"])
    else:
        print(f"Incorrect! The correct answer is: {text['norwegian']}")
        speak(text["norwegian"])


if __name__ == "__main__":
    # obtain audio from the microphone
    r = sr.Recognizer()
    with open('sentences.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        sentences = data["sentences"]
        random.shuffle(sentences)
        mode = input("Choose mode: 1 for Norwegian prompts requiring spoken norwegian,"
                     " 2 for English prompts requiring spoken norwegian: ")
        mode = int(mode) % 2
        print("Mode: " + str(mode + 2))

        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)

            if mode == 1:
                for sentence in sentences:
                    print(sentence["norwegian"])
                    hear_norwegian(r, source, sentence)
            else:
                for sentence in sentences:
                    print(sentence["english"])
                    hear_norwegian(r, source, sentence)
