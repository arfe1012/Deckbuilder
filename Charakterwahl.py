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
from Spiel_main import main
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
    """Erstellt vier Beispiel-Charaktere (Name, Stats, Bild)."""
    raw_data = [
        ("Assasin",  {"HP": 70, "Damage": 30, "Money": 80, "Deck": "Blutungsschaden"}, asset_dir / "char_0.png"),
        ("Mushroom", {"HP": 90, "Damage": 15, "Money": 40, "Deck": "Giftschaden"},    asset_dir / "char_1.png"),
        ("Viking",   {"HP": 130, "Damage": 20, "Money": 60, "Deck": "Block"},          asset_dir / "char_2.png"),
        ("Warrior",  {"HP": 120, "Damage": 18, "Money": 50, "Deck": "Angriffsschaden"}, asset_dir / "char_3.png"),
    ]

    characters: list[Character] = []
    for name, stats, path in raw_data:
        img = bild_laden(path)
        if img is None:
            # Fallback: farbige Fläche mit Namens-Text
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

    screen,screen_width,screen_height = screenscale()

    # ── Hintergrundbilder laden ────────────────────────────────────────────
    asset_dir = Path(__file__).parent / "Grafiken"
    ladescreen_orig = bild_laden(asset_dir / "background_sts.png")
    kampfscreen_orig = bild_laden(asset_dir / "Arena.png")

    # Aktuell angezeigtes Originalbild & skalierte Variante
    current_orig = ladescreen_orig
    background = scale_bg((screen_width, screen_height), current_orig)
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
            elif event.type == pygame.VIDEORESIZE:
                screen_width, screen_height = event.size
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                background = scale_bg(event.size, current_orig)

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
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill((30, 30, 30))

        # Charakterportraits
        for char in characters:
            screen.blit(char.image, char.rect)
            # Rahmen
            pygame.draw.rect(screen, (200, 200, 200), char.rect, width=3 if char is hovered else 1)

        # Stats‑Panel, wenn etwas gehovered ist
        if hovered:
            # Dynamische Höhe je nach Anzahl der Stat-Zeilen
            line_h = font_stats.get_height() + 4
            stats_lines = [f"{k}: {v}" for k, v in hovered.stats.items()]
            panel_w = 360
            panel_h = 28 + line_h * (len(stats_lines) + 1)

            panel_rect = pygame.Rect(0, 0, panel_w, panel_h)
            panel_rect.midbottom = (screen_rect.centerx, screen_rect.bottom - 30)

            # Halbtransparente Fläche, KEIN sichtbarer Rahmen
            panel_surf = pygame.Surface(panel_rect.size, pygame.SRCALPHA)
            panel_surf.fill((40, 40, 60, 220))
            screen.blit(panel_surf, panel_rect)

            # Titel
            name_surf = font_title.render(hovered.name, True, (240, 240, 240))
            screen.blit(name_surf, (panel_rect.x + 16, panel_rect.y + 10))

            # Stat-Zeilen
            y_cursor = panel_rect.y + 10 + font_title.get_height() + 8
            for line in stats_lines:
                stat_surf = font_stats.render(line, True, (220, 220, 220))
                screen.blit(stat_surf, (panel_rect.x + 16, y_cursor))
                y_cursor += line_h

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
        main(chosen.name)
    sys.exit()
