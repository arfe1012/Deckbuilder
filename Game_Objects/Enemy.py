class Enemy:
    def __init__(self, name, health, damage, reward):
        self.name = name
        self.health = health
        self.damage = damage
        self.reward = reward
        self.alive = True 

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.alive = False

    def attack(self, player):
        player.take_damage(self.damage)

    def __str__(self):
        return (f"Player(name={self.name}, health={self.health}, damage={self.damage}, "
                f"reward={self.reward})")