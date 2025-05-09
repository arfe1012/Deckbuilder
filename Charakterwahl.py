import sys
from pathlib import Path
import pygame
from Screen_and_Backrounds import screenscale,bild_laden,scale_bg

def main() -> None:
    pygame.init()

    screen,screen_width,screen_height = screenscale()

    # ── Hintergrundbilder laden ────────────────────────────────────────────
    asset_dir = Path(__file__).parent / "Grafiken"
    ladescreen = bild_laden(asset_dir / "background_sts.png")

    # Aktuell angezeigtes Originalbild & skalierte Variante
    
    background = scale_bg((screen_width, screen_height), ladescreen)

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
        

            elif event.type == pygame.VIDEORESIZE:
                screen_width, screen_height = event.size
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                background = scale_bg(event.size, ladescreen)

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