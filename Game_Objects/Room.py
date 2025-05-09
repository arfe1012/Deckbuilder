from Game_Objects.Enemy import Enemy

class Room:
    def __init__(self, player):
        self.player = player
        self.enemy = Enemy(name = "Silas", health = 100, damage = 10, reward = 1000)
        self.left_deck = player.start_deck
        self.right_deck = []

    def show_next_cards(self):
        tmp_cards = []
        for card in self.left_deck[:3]:
            tmp_cards.append(card)
        return tmp_cards

    def __str__(self):
        return (f"Room:\n"
                f"  Player: {self.player}\n"
                f"  Enemy: {self.enemy}\n"
                f"  Deck: {self.deck}")