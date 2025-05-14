from Game_Objects.Enemy import Enemy
import pygame

class Room:
    def __init__(self, player):
        self.player = player
        self.enemy = Enemy(name = "Silas", health = 100, damage = 10, reward = 1000,Grafiken_path="Grafiken\enemy_1.png")
        self.left_deck = player.start_deck
        self.shown_cards = []
        self.right_deck = []
        self.round = 1
        self.Hud_font = HUD_FONT = pygame.font.SysFont(None, 32, bold=True)
        self.Hud_color = HUD_COLOR = (250, 240, 200)  

    def show_next_cards(self):
        for index, card in enumerate(self.left_deck[:5]):
            self.shown_cards.append(card)

    def move_card(self, from_index, to_index):
        
        tmp_to_index = self.shown_cards[to_index]
        self.shown_cards[to_index] = self.shown_cards[from_index]
        self.shown_cards[from_index] = tmp_to_index

    def player_turn(self) -> None:
        print("Player turn")
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
        
        self.player.update_stats(heal_amount = final_health, block_amount = final_block, 
                                 crit_amount = final_crit, damage_amount = final_damage, 
                                 blood_amount = final_blood, poison_amount = final_poison)
        self.player.attack(self.enemy)

        if self.check_if_enemy_alive():
            print("Enemy died in round", self.round)
        else:
            print("Enemy is alive")
            # Enemy attacks player
            self.enemy.attack(self.player)
            if self.check_if_player_alive():
                print("Player died in round", self.round)
            else:
                print("Player is alive")
        self.round += 1
        # TODO Reset the shown cards for the next round
        
    def make_operation(self, a, b, operation):
        if operation == "+":
            return a+b
        if operation == "-":
            return a-b
        if operation == "*":
            return a*b
        if operation == "/":
            return a/b

    def check_if_enemy_alive(self):
        if self.enemy.alive == False:
            return False
        else:
            self.player.money += self.enemy.reward
            return True
    
    def check_if_player_alive(self):
        if self.player.health <= 0:
            return False
        else:
            return True

    def draw_room_result(self,screen: pygame.Surface,
                        x: int = 20,
                        y: int = 20,
                        line_gap: int = 6) -> None:
        
        # Show player stats
        lines_player = [
            f"Health : {round(self.player.health,2)} + this fight  {round(self.player.last_health_increase,2)}",
            f"Damage : {round(self.player.damage,2)} + this fight  {round(self.player.last_damage_increase,2)}",
            f"Block  : {round(self.player.block,2)}",
            f"Poison : {round(self.player.poison,2)}",
            f"Blood  : {round(self.player.blood,2)}",
            f"Crit   : {round(self.player.crit,2)}%",
            f" ",
            f"Money : {self.player.money}"
        ]
        
        # Show current round
        self.Hud_font = pygame.font.SysFont("Comic Sans MS", 36, bold=True, italic=True)
        round_text = f"Round: {self.round}"
        surf = self.Hud_font.render(round_text, True, self.Hud_color)
        screen.blit(surf, (screen.get_width() // 2, y))

        # Show player stats
        y_cursor = y
        self.Hud_font = pygame.font.SysFont("Comic Sans MS", 24, bold=False, italic=False)
        for line in lines_player:
            surf = self.Hud_font.render(line, True, self.Hud_color)
            screen.blit(surf, (x, y_cursor))
            y_cursor += surf.get_height() + line_gap

        # Show enemy stats
        lines_enemy = [
            f"Enemy: {self.enemy.name}",
            f"Health : {round(self.enemy.health,2)}",
            f"Damage : {round(self.enemy.damage,2)}",
            f"Reward : {self.enemy.reward}"
        ]

        x = screen.get_width() - 250
        y_cursor = y
        for line in lines_enemy:
            surf = self.Hud_font.render(line, True, self.Hud_color)
            screen.blit(surf, (x, y_cursor))
            y_cursor += surf.get_height() + line_gap



    def __str__(self):
        return (f"Room:\n"
                f"  Player: {self.player}\n"
                f"  Enemy: {self.enemy}\n"
                f"  Deck: {self.deck}")