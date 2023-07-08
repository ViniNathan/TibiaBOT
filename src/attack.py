from src.screen import WindowCapture, TemplateMatcher
import pyautogui
import json


class AttackClick:
    def __init__(self):
        pass

    def attack(self):
        window_name = "Projetor em tela cheia (prévia)"
        template_folder = "images/monsters/names/"
        monsters_file = "scripts/monsters.json"

        # Carregar os nomes dos monstros a partir do arquivo JSON
        with open(monsters_file) as file:
            monsters_data = json.load(file)
        
        if "monsters" in monsters_data:
            monster_names = monsters_data["monsters"]
            
            for monster_name in monster_names:
                # Compor o caminho do template para o nome atual
                template_path = template_folder + monster_name + ".png"

                window_capture = WindowCapture(window_name)
                template_matcher = TemplateMatcher(template_path)

                screenshot = window_capture.capture()
                template_location = template_matcher.find_template(screenshot)

                if template_location is not None:
                    print("O template foi encontrado na posição:", template_location)
                    pyautogui.moveTo(template_location)
                    pyautogui.leftClick()
                    pyautogui.moveTo(1056, 58)
                    break  # Parar a iteração caso o template seja encontrado
                    
            else:
                print("Nenhum template encontrado na tela para os monstros especificados.")
        else:
            print("Nenhum monstro encontrado no arquivo:", monsters_file)

while True:
    atacar = AttackClick()
    atacar.attack()