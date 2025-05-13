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
from moviepy.video.io.VideoFileClip import VideoFileClip
import pygame
from Screen_and_Backrounds import screenscale, bild_laden, scale_bg
from Spiel_main import main
from Sounds.Sound import play_bgm, stop_bgm,play_sfx
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

#---------------------------------------------intro Video, das man mit Leertaste skippen kann.
def play_intro(path: str | Path, screen: pygame.Surface, clock: pygame.time.Clock) -> None:
    """
    Spielt Video + Audio per MoviePy ab.
    Leertaste überspringt sofort beides.
    """
    clip = VideoFileClip(str(path))  # kein logger-Argument mehr

    # Audio extrahieren (WAV), einmalig
    audio_path = Path(path).with_suffix('.wav')
    if not audio_path.exists():
        clip.audio.write_audiofile(
            str(audio_path),
            logger=None     # stillt weitere Logs
        )

    # Pygame-Mixer starten und Audio abspielen
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    pygame.mixer.music.load(str(audio_path))
    pygame.mixer.music.play()

    fps = clip.fps or 24
    try:
        for frame in clip.iter_frames(fps=fps, dtype="uint8"):
            surf = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "RGB")
            surf = pygame.transform.scale(surf, screen.get_size())
            screen.blit(surf, (0, 0))
            pygame.display.flip()

            for ev in pygame.event.get():
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_SPACE:
                    pygame.mixer.music.stop()
                    return
                if ev.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()

            clock.tick(fps)
    finally:
        pygame.mixer.music.stop()
        clip.close()

# ──────────────────────────────────────────────────────────────────────────────
# Haupt‑Loop
# ──────────────────────────────────────────────────────────────────────────────

def run_character_select() -> Character | None:
    pygame.init()

    screen,screen_width,screen_height = screenscale()
    clock = pygame.time.Clock()
    # Intro-Video vor dem Menü
    intro_path = Path(__file__).parent / "Videos" / "introo.mp4"
    if intro_path.exists():
        play_intro(intro_path, screen, clock)
    play_bgm("Sounds\game soundtrack 2.wav", volume=1)
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

    font_title = pygame.font.SysFont("Comic Sans MS", 45, bold=True, italic=False)
    font_stats = pygame.font.SysFont("Comic Sans MS", 24, bold=False, italic=False)

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
                play_sfx("Sounds\card_back.wav", volume=1)
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
            # Dynamische Höhe je nach Anzahl der Stat-Zeileng
            line_h = font_stats.get_height() + 4
            stats_lines = [f"{k}: {v}" for k, v in hovered.stats.items()]
            panel_w = 360
            panel_h = 28 + line_h * (len(stats_lines) + 1)

            panel_rect = pygame.Rect(0, 0, panel_w, panel_h)
            padding = 10  # frei wählbarer Abstand in Pixeln
            panel_rect.midtop = (hovered.rect.centerx, hovered.rect.bottom + padding)

            # Halbtransparente Fläche, KEIN sichtbarer Rahmen
            panel_surf = pygame.Surface(panel_rect.size, pygame.SRCALPHA)
            panel_surf.fill((0, 0, 0, 0))
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
        stop_bgm()
        print("Gewählt:", chosen.name)
        main(chosen.name)
    sys.exit()
