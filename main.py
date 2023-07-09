from src.getters import *
from src.attack import *
from src.start import *

class Main:
    def __init__(self):
        pass

    def start_route(self):
        replay = ReplayKeyStrokes()
        replay.run()
    
    def start_attack(self):
        atacar = AttackClick()
        atacar.attack()

    def start_key(self):
        keyboard.on_press_key("page down", self.start_route())
        keyboard.on_press_key("page down", self.start_attack())

while True:
    GoHunt = Main()
    GoHunt.start_key() 