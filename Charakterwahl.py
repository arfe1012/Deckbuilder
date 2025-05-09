"""Character-Select-Screen

Zeigt vier Charakter-Portraits. Sobald der Mauszeiger über einem Portrait liegt,
werden Name und Basis‑Stats eingeblendet. Ein Mausklick auf einen Charakter
liefert dessen Objekt zurück (kann später an die Game‑Loop übergeben werden).

Benötigt:
- Verzeichnis "Grafiken" mit vier Bildern (PNG, 1:1‑Seitenverhältnis empfohlen)
  Namensschema: char_<index>.png  (char_0.png … char_3.png)
- Das Hilfs‑Modul Screen_and_Backrounds (screenscale, bild_laden, scale_bg)
"""

from __future__ import annotations

import sys
from pathlib import Path
from dataclasses import dataclass

import pygame
from Screen_and_Backrounds import screenscale, bild_laden, scale_bg

# ──────────────────────────────────────────────────────────────────────────────
# Datenmodell
# ──────────────────────────────────────────────────────────────────────────────

@dataclass(slots=True)
class Character:
    name: str
    image: pygame.Surface
    stats: dict[str, int]
    rect: pygame.Rect  # Position auf dem Screen (wird nachträglich gesetzt)


# ──────────────────────────────────────────────────────────────────────────────
# Hilfsfunktionen
# ──────────────────────────────────────────────────────────────────────────────

def load_characters(asset_dir: Path) -> list[Character]:
    """Erstellt vier Beispiel‑Charaktere (Name, Stats, Bild)."""
    raw_data = [
        ("Rogue",  {"HP": 70, "Attack": 12, "Speed": 18}, asset_dir / "char_0.png"),
        ("Knight", {"HP": 90, "Attack": 15, "Speed": 10}, asset_dir / "char_1.png"),
        ("Mage",   {"HP": 60, "Attack": 20, "Speed": 12}, asset_dir / "char_2.png"),
        ("Cleric", {"HP": 80, "Attack": 10, "Speed": 14}, asset_dir / "char_3.png"),
    ]

    characters: list[Character] = []
    for name, stats, path in raw_data:
        img = bild_laden(path)
        if img is None:
            # Fallback: farbige Fläche mit Namens‑Text
            img = pygame.Surface((256, 256))
            img.fill((80, 80, 80))
            font = pygame.font.SysFont(None, 32, bold=True)
            text_surf = font.render(name[0], True, (220, 220, 220))
            text_rect = text_surf.get_rect(center=img.get_rect().center)
            img.blit(text_surf, text_rect)
        characters.append(Character(name=name, image=img, stats=stats, rect=pygame.Rect(0, 0, 0, 0)))

    return characters


def layout_characters(characters: list[Character], screen_rect: pygame.Rect) -> None:
    """Setzt die rect‑Attribute gleichmäßig nebeneinander zentriert."""
    cols = len(characters)
    gap = 40
    available_width = screen_rect.width - gap * (cols + 1)
    img_w = img_h = min(available_width // cols, screen_rect.height // 2)

    x = gap
    y = screen_rect.centery - img_h // 2
    for char in characters:
        char.rect = pygame.Rect(x, y, img_w, img_h)
        # Bild ggf. skalieren auf das Ziel‑Rect (quadratisch)
        char.image = scale_bg((img_w, img_h), char.image)
        x += img_w + gap


# ──────────────────────────────────────────────────────────────────────────────
# Haupt‑Loop
# ──────────────────────────────────────────────────────────────────────────────

def run_character_select() -> Character | None:
    pygame.init()

    screen, sw, sh = screenscale()
    screen_rect = screen.get_rect()

    asset_dir = Path(__file__).parent / "Grafiken"
    characters = load_characters(asset_dir)
    layout_characters(characters, screen_rect)

    font_title = pygame.font.SysFont(None, 48, bold=True)
    font_stats = pygame.font.SysFont(None, 32)

    clock = pygame.time.Clock()
    running = True
    hovered: Character | None = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                hovered = None
                for char in characters:
                    if char.rect.collidepoint(event.pos):
                        hovered = char
                        break
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and hovered:
                # Charakter gewählt → zurückgeben
                return hovered

        # ── Zeichnen ────────────────────────────────────────────────────────
        screen.fill((25, 25, 35))

        # Charakterportraits
        for char in characters:
            screen.blit(char.image, char.rect)
            # Rahmen
            pygame.draw.rect(screen, (200, 200, 200), char.rect, width=3 if char is hovered else 1)

        # Stats‑Panel, wenn etwas gehovered ist
        if hovered:
            panel_w, panel_h = 300, 160
            panel_rect = pygame.Rect(0, 0, panel_w, panel_h)
            panel_rect.midbottom = (screen_rect.centerx, screen_rect.bottom - 30)
            pygame.draw.rect(screen, (50, 50, 70), panel_rect, border_radius=12)
            pygame.draw.rect(screen, (220, 220, 220), panel_rect, width=2, border_radius=12)

            name_surf = font_title.render(hovered.name, True, (240, 240, 240))
            screen.blit(name_surf, (panel_rect.x + 16, panel_rect.y + 12))

            y_cursor = panel_rect.y + 60
            for key, value in hovered.stats.items():
                stat_text = f"{key}: {value}"
                stat_surf = font_stats.render(stat_text, True, (220, 220, 220))
                screen.blit(stat_surf, (panel_rect.x + 16, y_cursor))
                y_cursor += 32

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    return None


# ──────────────────────────────────────────────────────────────────────────────
# Direktstart (zum Testen)
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    chosen = run_character_select()
    if chosen:
        print("Gewählt:", chosen.name)
    sys.exit()
