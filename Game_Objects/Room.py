from Game_Objects.Enemy import Enemy

class Room:
    def __init__(self, player):
        self.player = player
        self.enemy = Enemy(name = "Silas", health = 100, damage = 10, reward = 1000)
        self.left_deck = player.start_deck
        self.shown_cards = []
        self.right_deck = []

    def show_next_cards(self):
        for index, card in enumerate(self.left_deck[:5]):
            self.shown_cards.append(card)

    def move_card(self, from_index, to_index):
        print("Moving card " + str(from_index) + " to " + str(to_index))
        tmp_to_index = self.shown_cards[to_index]
        self.shown_cards[to_index] = self.shown_cards[from_index]
        self.shown_cards[from_index] = tmp_to_index
        for card in self.shown_cards:
            print(card)

    def __str__(self):
        return (f"Room:\n"
                f"  Player: {self.player}\n"
                f"  Enemy: {self.enemy}\n"
                f"  Deck: {self.deck}")