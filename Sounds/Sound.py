# music_utils.py
import pygame
from pathlib import Path

def play_bgm(path: str | Path, *, volume: float = 0.6,
             loops: int = -1, fade_ms: int = 1000) -> None:
    """
    Spielt eine Audiodatei als Hintergrundmusik.
    
    Parameters
    ----------
    path : str | pathlib.Path
        Pfad zur Musikdatei (MP3, OGG, WAV …).
    volume : float, optional
        Lautstärke 0.0‒1.0 (Standard: 0.6).
    loops : int, optional
        Wie oft wiederholen: -1 = unendlich (Default), 0 = einmal usw.
    fade_ms : int, optional
        Millisekunden für weiches Einblenden (0 = sofort).
    """
    # Mixer nur 1× initialisieren (sicher gegen Mehrfachaufrufe)
    if not pygame.mixer.get_init():
        pygame.mixer.init()

    # Laden
    try:
        pygame.mixer.music.load(str(path))
    except pygame.error as e:
        raise RuntimeError(f"Musik konnte nicht geladen werden: {e}") from e

    # Einstellungen
    pygame.mixer.music.set_volume(max(0.0, min(1.0, volume)))
    
    # Abspielen
    pygame.mixer.music.play(loops=loops, fade_ms=fade_ms)


def stop_bgm(fade_ms: int = 500) -> None:
    """Stoppt die Hintergrundmusik (sanftes Ausfaden in fade_ms ms)."""
    if pygame.mixer.get_init():
        pygame.mixer.music.fadeout(fade_ms)
# music_utils.py  (Ergänzung unter play_bgm / stop_bgm)
# -------------------------------------------------------
from functools import lru_cache
import pygame
from pathlib import Path

@lru_cache(maxsize=64)          # bis zu 64 verschiedene Sounds im RAM behalten
def _load_sfx(path: str | Path) -> pygame.mixer.Sound:
    """Lädt eine Sound-Datei und gibt ein Sound-Objekt zurück (mit Cache)."""
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    return pygame.mixer.Sound(str(path))


def play_sfx(path: str | Path, *, volume: float = 1.0) -> None:
    """
    Spielt einen kurzen Sound-Effekt ab.

    Parameters
    ----------
    path : str | pathlib.Path
        Pfad zur WAV/OGG/MP3-Datei.
    volume : float, optional
        0.0‒1.0 Lautstärke (Default 1.0).
    """
    sound = _load_sfx(path)
    sound.set_volume(max(0.0, min(1.0, volume)))
    sound.play()                   # automatisch auf erstem freien Channel
