from Game_Objects.Enemy import Enemy
import pygame

class Room:
    def __init__(self, player):
        self.player = player
        self.enemy = Enemy(name = "Silas", health = 100, damage = 10, reward = 1000)
        self.left_deck = player.start_deck
        self.shown_cards = []
        self.right_deck = []
        self.Hud_font = HUD_FONT = pygame.font.SysFont(None, 32, bold=True)
        self.Hud_color = HUD_COLOR = (250, 240, 200)  

    def show_next_cards(self):
        for index, card in enumerate(self.left_deck[:5]):
            self.shown_cards.append(card)

    def move_card(self, from_index, to_index):
        
        tmp_to_index = self.shown_cards[to_index]
        self.shown_cards[to_index] = self.shown_cards[from_index]
        self.shown_cards[from_index] = tmp_to_index

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

        final_block = 0
        tmp_block =[]
        tmp_block_operation = []

        final_poison = 0
        tmp_poison = []
        tmp_poison_operation =[]

        final_blood = 0
        tmp_blood = []
        tmp_blood_operation =[]

        for card in self.shown_cards:
            tmp_health.append(card.health)
            tmp_health_operation.append(card.health_operation)
            tmp_damage.append(card.attack)
            tmp_damage_operation.append(card.attack_operation)
            tmp_crit.append(card.crit)
            tmp_crit_operation.append(card.crit_operation)
            tmp_block.append(card.block)
            tmp_block_operation.append(card.block_operation)
            tmp_poison.append(card.poison)
            tmp_poison_operation.append(card.poison_operation)
            tmp_blood.append(card.blood)
            tmp_blood_operation.append(card.blood_operation)
        for index, value in enumerate(tmp_health):
            final_health = self.make_operation(final_health, tmp_health[index], tmp_health_operation[index])
            final_damage = self.make_operation(final_damage, tmp_damage[index], tmp_damage_operation[index])
            final_crit = self.make_operation(final_crit, tmp_crit[index], tmp_crit_operation[index])
            final_block = self.make_operation(final_block, tmp_block[index], tmp_block_operation[index])
            final_poison = self.make_operation(final_poison, tmp_poison[index], tmp_poison_operation[index])
            final_blood = self.make_operation(final_blood, tmp_blood[index], tmp_blood_operation[index])
        return final_health,final_crit,final_damage,final_block,final_blood,final_poison
        
    def make_operation(self, a, b, operation):
        if operation == "+":
            return a+b
        if operation == "-":
            return a-b
        if operation == "*":
            return a*b
        if operation == "/":
            return a/b


    def draw_room_result(self,screen: pygame.Surface,
                        final_health: int,
                        final_damage: int,
                        final_crit: int,
                        final_block: int,
                        final_poison:int,
                        final_blood:int,
                        player_health:int,
                        player_damage: int,
                        player_block: int,
                        player_money:int,
                        x: int = 20,
                        y: int = 20,
                        line_gap: int = 6) -> None:
        
        lines = [
            f"Health : {round(player_health,2)} + this fight  {round(final_health,2)}",
            f"Damage : {round(player_damage,2)} + this fight  {round(final_damage,2)}",
            f"Block  : {round(player_block,2)}  + this fight  {round(final_block,2)}",
            f"Poison : {round(final_poison,2)}",
            f"Blood  : {round(final_blood,2)}",
            f"Crit   : {round(final_crit,2)}%",
            f" ",
            f"Money : {player_money}"
        ]
        
        y_cursor = y
        self.Hud_font = pygame.font.SysFont("Comic Sans MS", 24, bold=False, italic=False)
        for line in lines:
            surf = self.Hud_font.render(line, True, self.Hud_color)
            screen.blit(surf, (x, y_cursor))
            y_cursor += surf.get_height() + line_gap



    def __str__(self):
        return (f"Room:\n"
                f"  Player: {self.player}\n"
                f"  Enemy: {self.enemy}\n"
                f"  Deck: {self.deck}")