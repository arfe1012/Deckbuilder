from Game_Objects.Enemy import Enemy

class Room:
    def __init__(self, player):
        self.player = player
        self.enemy = Enemy(name = "Silas", health = 100, damage = 10, reward = 1000)
        self.left_deck = player.start_deck
        self.shown_cards = []
        self.right_deck = []

    def show_next_cards(self):
        tmp_cards = []
        for card in self.left_deck[:3]:
            tmp_cards.append(card)
        self.shown_cards = tmp_cards

    def move_card(self, from_index, to_index):
        tmp_cards = [0,0,0] #bad, because hardcoded and fixed length
        tmp_cards[to_index] = self.shown_cards[from_index]
        tmp_cards[from_index] = self.shown_cards[to_index]
        self.shown_cards = tmp_cards

    def __str__(self):
        return (f"Room:\n"
                f"  Player: {self.player}\n"
                f"  Enemy: {self.enemy}\n"
                f"  Deck: {self.deck}")