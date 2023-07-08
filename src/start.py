import keyboard
import json
import time

class ReplayKeyStrokes:
    def __init__ (self):
        pass
    
    def run(self):
        with open("scripts/keystrokes.json", "r") as file:
            keystrokes = json.load(file)

        print("Reproduzindo as teclas pressionadas...")
        time.sleep(4)  # Aguarda 4 segundos antes de começar a reprodução

        for key in keystrokes:
            keyboard.press_and_release(key)
            time.sleep(0.40)  # Aguarda 0.4 segundo entre cada tecla
        quit()

    