from screen import *
from actions import Actions
from pynput.keyboard import Listener
from pynput import keyboard
from time import sleep
import threading
import json

class Hunt:
    def __init__(self):
        self.isStarted = True
        with open("scripts/CaveBot/HUNT-Teste.json", "r") as file:
            infos = file.read()
        self.infos = json.loads(infos)
        self.actions = Actions()
        
    def go_to_flag(self, item):
        window_name = "Projetor em tela cheia (prévia)"
        for i in range(10):
            flag_position = LocateImageCenter(item["flag"], window_name, Region=None, Precision=0.8)
            if flag_position is None:
                return
            self.actions.move_and_click(flag_position)
            sleep(item["wait"])

    def start_route(self):
        while self.isStarted:
            for item in self.infos:
                self.go_to_flag(item)

    def target_key(self, key):
        if key == keyboard.Key.esc:
            return False
        if key == keyboard.Key.delete:
            threading.Thread(target= self.start_route).start()

    def start_keyboard(self):
        with Listener(on_press=self.target_key) as listener:
            listener.join()



hunt = Hunt()
hunt.start_keyboard()


