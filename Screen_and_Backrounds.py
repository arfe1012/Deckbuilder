#HIlfsfunktionen zum erstellen eines Screen, Hintergrundbilder laden und  dessen Scalierung

import sys
from pathlib import Path
import pygame

#erzeugt einen Screen auf den Mapen des Bildschirm und gibt die Screnngröße zurück
def screenscale():
    # Aktuelle Display‑Auflösung
    info = pygame.display.Info()
    screen_width, screen_height = info.current_w, info.current_h

    # Fenster öffnen (resizable)
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    pygame.display.set_caption("Deckbuilder")
    return screen,screen_width,screen_height 

# Funktion zum bilder laden
def bild_laden(path: Path) -> pygame.Surface | None:
    """Versucht, eine Bilddatei zu laden und gibt ein Surface zurück.
    Liefert **None**, falls die Datei nicht existiert oder das Laden scheitert."""
    if not path.exists():
        print(f"[Warnung] Datei nicht gefunden: {path}")
        return None

    try:
        return pygame.image.load(path.as_posix()).convert_alpha()
    except pygame.error as e:
        print(f"[Warnung] Bild konnte nicht geladen werden: {e}")
        return None

#skaliert das HIntergurnd bild auf die richtige göße
def scale_bg(size: tuple[int, int], original: pygame.Surface | None) -> pygame.Surface | None:
    """Skaliert ein Surface weich auf *size* oder gibt **None** zurück."""
    return pygame.transform.smoothscale(original, size) if original else None