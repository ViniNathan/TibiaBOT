import keyboard
import json

class KeystrokeRecorder:
    def __init__(self):
        self.keystrokes = []

    def on_keypress(self, event):
        allowed_keys = ["w", "a", "s", "d", "up", "down", "left", "right"]
        if event.name in allowed_keys and event.name != "page up":
            self.keystrokes.append(event.name)


    def start_recording(self):
        keyboard.on_press(self.on_keypress)
        print("Gravação iniciada. Pressione Esc para parar.")

    def stop_recording(self):
        keyboard.unhook_all()
        with open("scripts/keystrokes.json", "w") as file:
            json.dump(self.keystrokes, file)
        print("As teclas pressionadas foram armazenadas em keystrokes.json.")

    def page_up_press(self, event):
        self.start_recording()

    def esc_press(self, event):
        self.stop_recording()
    
    def run(self):
        keyboard.on_press_key("page up", self.page_up_press)
        keyboard.on_press_key("esc", self.esc_press)
        input("Gravação de teclas iniciada\nPressione Esc para encerrar o programa...\n")


