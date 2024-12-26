import speech_recognition as sr
import json
import random


r = sr.Recognizer()
with open('sentences.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
    sentences = data["sentences"]
    random.shuffle(sentences)

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)

        for sentence in sentences:
            print(sentence["norwegian"])
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

            print("You said: " + heard)
            if heard.lower() == sentence["norwegian"].lower().replace(".", "").replace("?", "").replace("!", "").replace(",", ""):
                print("Correct!")
            else:
                print("Incorrect!")

