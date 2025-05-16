import pygame
from pathlib import Path
from typing import Optional
from Screen_and_Backrounds import  bild_laden
class Player:
    def __init__(self, name, health, damage, money, start_deck, Grafiken_path, block):
        self.name = name
        self.health = health
        self.damage = damage
        self.block = block
        self.crit = 0
        self.poison = 0
        self.blood = 0
        self.card_stats = {}
        self.money = money
        self.start_deck = start_deck
        self.grafiken_path = Path(Grafiken_path)
        self._sprite: Optional[pygame.Surface] = None

    def update_stats(self, heal_amount: int, block_amount: int, 
                     crit_amount: int, damage_amount: int, 
                     blood_amount: int, poison_amount: int) -> None:
        """Updatet die Spieler Stats wenn Karten bestätigt werden."""
        self.health += heal_amount
        self.card_stats["damage"] = damage_amount
        self.card_stats["block"] = block_amount
        self.card_stats["crit"] = crit_amount
        self.card_stats["blood"] = blood_amount
        self.card_stats["poison"] = poison_amount

    def attack(self, enemy):
        enemy.take_damage(self.damage + self.card_stats["damage"])
        # TODO Hier noch crit, blood, poison und block einfügen

    def take_damage(self, amount: int) -> None:
        """Verringert die Lebenspunkte des Spielers."""
        self.health -= amount
        if self.health <= 0:
            self.die()
    
    def die(self) -> None:
        """Behandelt den Tod des Spielers."""
        print(f"{self.name} ist gestorben!")
        # Hier noch weitere Logik hinzufügen, z.B. Spiel beenden oder Neustart anbieten

    def draw_sprite(self,
                screen: pygame.Surface,
                *,
                scale: float | None = 0.3,
                anchor: str = "bottomleft",
                offset: tuple[int, int] = (120, 300)) -> None:
        
        # ————————————————————————————————————————————————————————————————
        # 1) Lazy-Load & Cache
        # ————————————————————————————————————————————————————————————————
        if self._sprite is None:
            surf = bild_laden(self.grafiken_path)
            if surf is None:
                return  # Ladefehler → nichts zu tun

            # Skalieren (z. B. 30 % Originalgröße)
            if scale is not None:
                w, h = surf.get_size()
                surf = pygame.transform.smoothscale(
                    surf, (int(w * scale), int(h * scale))
                )
            self._sprite = surf

        # ————————————————————————————————————————————————————————————————
        # 2) Positionieren & Zeichnen
        # ————————————————————————————————————————————————————————————————
        rect = self._sprite.get_rect()
        screen_rect = screen.get_rect()

        # z. B. rect.bottomleft = (screen_rect.left+offset[0], screen_rect.bottom-offset[1])
        setattr(rect, anchor,
                (getattr(screen_rect, anchor)[0] + offset[0],
                    getattr(screen_rect, anchor)[1] - offset[1]))
        screen.blit(self._sprite, rect)
        self.last_rect = rect
        return rect

    def __str__(self):
        return (f"Player(name={self.name}, health={self.health}, damage={self.damage}, "
                f"money={self.money}, start_deck=[…], Grafiken_path={self.Grafiken_path!r}),block={self.block}")