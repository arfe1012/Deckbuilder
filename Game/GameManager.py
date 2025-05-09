import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Game_Objects.Card import Card
from Game_Objects.Deck import Deck
from Game_Objects.Player import Player
from Game_Objects.Room import Room


class GameManager:
    def __init__(self, character_name, character_file=None):
        if character_file is None:
            # Load from parent directory
            character_file = os.path.join(os.path.dirname(__file__), "..", "characters.json")
        self.character_name = character_name
        self.character_file = character_file
        self.player = self.load_character()
        self.room = Room(self.player)


    def load_character(self):
        with open(self.character_file, "r") as f:
            data = json.load(f)

        if self.character_name not in data:
            raise ValueError(f"Character '{self.character_name}' not found in {self.character_file}")

        char_data = data[self.character_name]
        cards = [Card(**c) for c in char_data["start_deck"]]
        return Player(
            name=self.character_name,
            health=char_data["health"],
            damage=char_data["damage"],
            money=char_data["money"],
            start_deck=cards
        )
    def load_room(self):
        test = "test"

    def get_player(self):
        return self.player
    
def debug():
    print("This is a testrun")
    test_gamemanager = GameManager("viking")
    print(test_gamemanager.get_player().__str__())
    for card in test_gamemanager.get_player().start_deck:
        print(card.__str__())

if __name__ == "__main__":
    debug()