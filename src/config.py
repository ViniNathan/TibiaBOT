import json
from src.getters import *

def update_health_position(health_position):
    with open("scripts/positions.json", "r") as file:
        data = json.load(file)

    data["Positions"]["LifePosition"][0]["x"] = health_position[0]
    data["Positions"]["LifePosition"][0]["y"] = health_position[1]
    data["Positions"]["LifePosition"][0]["Stats"] = True

    with open("scripts/positions.json", "w") as file:
        json.dump(data, file, indent=4)

def update_mana_position(mana_position):
    with open("scripts/positions.json", "r") as file:
        data = json.load(file)

    data["Positions"]["ManaPosition"][0]["x"] = mana_position[0]
    data["Positions"]["ManaPosition"][0]["y"] = mana_position[1]
    data["Positions"]["ManaPosition"][0]["Stats"] = True

    with open("scripts/positions.json", "w") as file:
        json.dump(data, file, indent=4)

def update_battle_position(battle_position):
    with open("scripts/positions.json", "r") as file:
        data = json.load(file)

    data["Positions"]["BattlePosition"][0]["x"] = battle_position[0]
    data["Positions"]["BattlePosition"][0]["y"] = battle_position[1]
    data["Positions"]["BattlePosition"][0]["Stats"] = True

    with open("scripts/positions.json", "w") as file:
        json.dump(data, file, indent=4)

def update_map_position(map_position):
    with open("scripts/positions.json", "r") as file:
        data = json.load(file)

    data["Boxes"]["MapBox"][0]["x"] = map_position[0]
    data["Boxes"]["MapBox"][0]["y"] = map_position[1]
    data["Boxes"]["MapBox"][0]["w"] = map_position[2]
    data["Boxes"]["MapBox"][0]["h"] = map_position[3]
    data["Boxes"]["MapBox"][0]["Stats"] = True

    with open("scripts/positions.json", "w") as file:
        json.dump(data, file, indent=4)

def update_player_position(player_position):
    with open("scripts/positions.json", "r") as file:
        data = json.load(file)

    data["Positions"]["PlayerPosition"][0]["x"] = player_position[0]
    data["Positions"]["PlayerPosition"][0]["y"] = player_position[1]
    data["Positions"]["PlayerPosition"][0]["Stats"] = True

    with open("scripts/positions.json", "w") as file:
        json.dump(data, file, indent=4)