import sys
import pygame
from pathlib import Path


def main() -> None:
    """Startet ein Pygame‑Fenster, das sich automatisch an die Bildschirmgröße
    anpasst und ein Slay‑the‑Spire‑ähnliches Hintergrundbild skaliert anzeigt."""

    pygame.init()

    # Aktuelle Display‑Auflösung
    info = pygame.display.Info()
    screen_width, screen_height = info.current_w, info.current_h

    # Resizables Fenster öffnen
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    pygame.display.set_caption("Mein Pygame‑Spiel")

    # Hintergrundbild laden (muss als "background_sts.png" im selben Ordner liegen)
    background_orig = None
    # Pfad zum Bild relativ zur Skriptdatei (..../Grafiken/background_sts.png)
    img_path = Path(__file__).parent / "Grafiken" / "background_sts.png"
    if img_path.exists():
        try:
            background_orig = pygame.image.load(str(img_path)).convert()
        except pygame.error as e:
            print("[Warnung] Hintergrund konnte nicht geladen werden:", e)

    def scale_bg(size: tuple[int, int]):
        """Skaliert das Originalbild weich auf die gewünschte Größe."""
        return (
            pygame.transform.smoothscale(background_orig, size)
            if background_orig is not None
            else None
        )

    background = scale_bg((screen_width, screen_height))

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                # Neues Fenster‑Surface sowie neue BG‑Skalierung
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                screen_width, screen_height = event.size
                background = scale_bg(event.size)

        # === Zeichnen ===
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill((30, 30, 30))  # Fallback‑Farbe, falls Bild fehlt

        # Debug‑Rahmen (kann entfernt werden)
        pygame.draw.rect(screen, (200, 200, 200), screen.get_rect(), width=5)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
