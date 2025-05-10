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

    def attack(self):
        final_health = 0
        tmp_health = []
        tmp_health_operation = []
        
        final_damage = 0
        tmp_damage = []
        tmp_damage_operation = []
        
        final_crit = 0
        tmp_crit = []
        tmp_crit_operation = []
        for card in self.shown_cards:
            tmp_health.append(card.health)
            tmp_health_operation.append(card.health_operation)
            tmp_damage.append(card.attack)
            tmp_damage_operation.append(card.attack_operation)
            tmp_crit.append(card.crit)
            tmp_crit_operation.append(card.crit_operation)
        for index, value in enumerate(tmp_health):
            final_health = self.make_operation(final_health, tmp_health[index], tmp_health_operation[index])
            final_damage = self.make_operation(final_damage, tmp_damage[index], tmp_damage_operation[index])
            final_crit = self.make_operation(final_crit, tmp_crit[index], tmp_crit_operation[index])
        print("Final Health: " + str(final_health) + " Final Damage: " + str(final_damage) + " Final Crit: " + str(final_crit))
        return final_health,final_crit,final_damage
        
    def make_operation(self, a, b, operation):
        if operation == "+":
            return a+b
        if operation == "-":
            return a-b
        if operation == "*":
            return a*b
        if operation == "/":
            return a/b

    def __str__(self):
        return (f"Room:\n"
                f"  Player: {self.player}\n"
                f"  Enemy: {self.enemy}\n"
                f"  Deck: {self.deck}")