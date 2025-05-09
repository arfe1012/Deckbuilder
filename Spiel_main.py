import sys
from pathlib import Path
import pygame
from Screen_and_Backrounds import screenscale,bild_laden,scale_bg
from Game.GameManager import GameManager


from Sounds.Sound import play_bgm,stop_bgm
from cardslot import create_hand
# ──────────────────────────────────────────────────────────────────────────────
# Hauptprogramm
# ──────────────────────────────────────────────────────────────────────────────

def main(character_name):
    pygame.init()
    play_bgm("Sounds\Hölenmusik.wav", volume=1.2)
    screen,screen_width,screen_height = screenscale()

    # ── Hintergrundbilder laden ────────────────────────────────────────────
    asset_dir = Path(__file__).parent / "Grafiken"
    ladescreen_orig = bild_laden(asset_dir / "background_sts.png")
    kampfscreen_orig = bild_laden(asset_dir / "Arena.png")

    # Aktuell angezeigtes Originalbild & skalierte Variante
    current_orig = kampfscreen_orig
    background = scale_bg((screen_width, screen_height), current_orig)

    clock = pygame.time.Clock()
    running = True

    game_manager = GameManager(character_name.lower())

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

            elif event.type == pygame.VIDEORESIZE:
                screen_width, screen_height = event.size
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                background = scale_bg(event.size, current_orig)

        # ── Zeichnen ────────────────────────────────────────────────────────
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill((30, 30, 30))


        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
