import pyautogui
from screen import WindowCapture, TemplateMatcher

class Actions:
    def __init__(self):
        pass

    def move_and_click(self, image_location):
        pyautogui.moveTo(image_location)
        pyautogui.leftClick()

            