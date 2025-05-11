import pygame
from pathlib import Path
from typing import Optional
from Screen_and_Backrounds import  bild_laden
class Player:
    def __init__(self, name, health, damage, money, start_deck,Grafiken_path,block):
        self.name = name
        self.health = health
        self.damage = damage
        self.money = money
        self.start_deck = start_deck
        self.grafiken_path = Path(Grafiken_path)
        self._sprite: Optional[pygame.Surface] = None
        self.block = block
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

    def __str__(self):
        return (f"Player(name={self.name}, health={self.health}, damage={self.damage}, "
                f"money={self.money}, start_deck=[…], Grafiken_path={self.Grafiken_path!r}),block={self.block}")