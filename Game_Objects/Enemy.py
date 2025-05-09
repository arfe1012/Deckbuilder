class Enemy:
    def __init__(self, name, health, damage, reward):
        self.name = name
        self.health = health
        self.damage = damage
        self.reward = reward

    def __str__(self):
        return (f"Player(name={self.name}, health={self.health}, damage={self.damage}, "
                f"reward={self.reward})")