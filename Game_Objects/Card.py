class Card:
    def __init__(self, attack=0, health=0, block=0, poison=0, blood=0, crit=0,attack_operation="",health_operation="",block_operation="",poison_operation="",blood_operation="",crit_operation=""):
        self.attack = attack
        self.attack_operation = attack_operation
        self.health = health
        self.health_operation = health_operation
        self.block = block
        self.block_operation = block_operation
        self.poison = poison
        self.poison_operation = poison_operation
        self.blood = blood
        self.blood_operation = blood_operation
        self.crit = crit
        self.crit_operation = crit_operation

    def __str__(self) -> str:
        # sorgt dafür, dass auch zukünftige Attribute automatisch angezeigt werden
        parts = []
        for name, value in vars(self).items():
            parts.append(f"{name}={value}")
        return "Card(" + ", ".join(parts) + ")"