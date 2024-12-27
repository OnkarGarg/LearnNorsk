import pygame
import speech_recognition as sr
import json
import random
from gtts import gTTS
from io import BytesIO
from pygame import mixer, event
import time


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


def hear(r, source):
    audio = r.listen(source)
    heard = ""
    while not heard:
        try:
            heard = r.recognize_google(audio, language="no-NO")
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return heard


def hear_norwegian(r, source, sentence):
    heard = hear(r, source)

    print("You said: " + heard)
    if heard.lower() == sentence["norwegian"].lower().replace(".", "").replace("?", "").replace("!", "").replace(",",
                                                                                                                 ""):
        print("Correct!")
        speak(sentence["norwegian"])
    else:
        print(f"Incorrect! The correct answer is: {sentence['norwegian']}")
        speak(sentence["norwegian"])


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

