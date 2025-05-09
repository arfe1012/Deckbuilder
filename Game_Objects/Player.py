class Player:
    def __init__(self, name, health, damage, money, start_deck):
        self.name = name
        self.health = health
        self.damage = damage
        self.money = money
        self.start_deck = start_deck

    def __str__(self):
        return (f"Player(name={self.name}, health={self.health}, damage={self.damage}, "
                f"money={self.money}, start_deck={self.start_deck})")