import speech_recognition as sr
import json
import random


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
        else:
            for sentence in sentences:
                print(sentence["english"])
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
                if heard.lower() == sentence["norwegian"].lower().replace(".", "").replace("?", "").replace("!",
                                                                                                            "").replace(
                        ",", ""):
                    print("Correct!")
                else:
                    print(f"Incorrect! The correct answer is: {sentence['norwegian']}")

