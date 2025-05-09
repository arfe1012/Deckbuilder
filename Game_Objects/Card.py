class Card:
    def __init__(self, attack=0, health=0, block=0, poison=0, blood=0, crit=0):
        self.attack = attack
        self.health = health
        self.block = block
        self.poison = poison
        self.blood = blood
        self.crit = crit

    def __str__(self):
        return (f"Card(Attack={self.attack}, Health={self.health}, Block={self.block}, "
                f"Poison={self.poison}, Blood={self.blood}, Crit={self.crit})")