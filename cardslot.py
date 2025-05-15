# hand.py  ──  minimaler Helfer für dein Deck-Builder-HUD
import pygame
from typing import List
from Sounds.Sound import play_sfx
from pathlib import Path
import math
import numpy as np

CARD_SCALE = 0.35          # größenabhängig von Original-PNG
CARD_GAP   = 30            # horizontaler Abstand zwischen Karten

class CardSlot:
    """Hält die Surface (Bild) und das Ziel-Rect einer Handkarte."""
    def __init__(self, surf: pygame.Surface, target_rect: pygame.Rect, card) -> None:
        self.surf = surf
        self.target = target_rect      # Slot-Position
        self.rect   = surf.get_rect(center=target_rect.center)  # aktuelle (für Drag)
        self.drag   = False
        self.card = card

def create_hand(card_imgs: List[pygame.Surface], screen_rect: pygame.Rect, room) -> List[CardSlot]:
    """Erzeugt fünf Slots und skaliert die Karten herunter."""
    hand_slots: List[CardSlot] = []
    
    # ── Einheitliche Kartengröße bestimmen ────────────────────────────────
    w0, h0 = card_imgs[0].get_size()
    w, h   = int(w0 * CARD_SCALE), int(h0 * CARD_SCALE)

    total_w = 5 * w + 4 * CARD_GAP
    start_x = screen_rect.centerx - total_w // 2
    y       = screen_rect.bottom - h // 2 - 20   # 20 px Abstand zum Rand

    for i, img in enumerate(card_imgs[:5]):      # nur 5 Karten
        surf  = pygame.transform.smoothscale(img, (w, h))
        slot_rect = pygame.Rect(start_x + i * (w + CARD_GAP), y, w, h)
        hand_slots.append(CardSlot(surf, slot_rect, room.shown_cards[i]))
    return hand_slots

def draw_hand(screen: pygame.Surface, hand: List[CardSlot]) -> None:
    """Zeichnet alle Karten; draggende Karte zuletzt für korrekte Z-Order."""
    for slot in hand:
        if not slot.drag:                       # feste Karten zuerst
            screen.blit(slot.surf, slot.rect)
    # Karten unter Maus zuletzt zeichnen (oberste Ebene)
    for slot in hand:
        if slot.drag:
            screen.blit(slot.surf, slot.rect)

def handle_hand_events(events, hand: List[CardSlot], room) -> None:
    """Drag-&-Drop-Logik: Karte verschieben & bei Loslassen Reihenfolge tauschen."""
    mouse_pos = pygame.mouse.get_pos()
    dragged_slot = next((s for s in hand if s.drag), None)

    for ev in events:
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            # mit oberster (zuletzt gezeichneter) beginnend suchen:
            for slot in reversed(hand):
                if slot.rect.collidepoint(ev.pos):
                    slot.drag = True
                    # kleine Verschiebung, damit Karte zentriert unter Maus klebt
                    dx = slot.rect.width  // 2
                    dy = slot.rect.height // 2
                    slot.offset = (ev.pos[0] - slot.rect.x,
                                    ev.pos[1] - slot.rect.y)
                    break

        elif ev.type == pygame.MOUSEBUTTONUP and ev.button == 1 and dragged_slot:
            # Ziel-Slot erkennen: das erste, dessen target-Rect Maus berührt
            target_idx = None
            for i, slot in enumerate(hand):
                if slot.target.collidepoint(ev.pos):
                    target_idx = i
                    break
            origin_idx = hand.index(dragged_slot)

            # Reihenfolge tauschen, falls sinnvoll
            if target_idx is not None and target_idx != origin_idx:
                room.move_card(origin_idx, target_idx)
                play_sfx(Path("Sounds") / "card_slide.wav", volume=0.8)

            # Slot auf Ziel-Rect zurückschnappen lassen
            for i, slot in enumerate(hand):
                slot.rect.topleft = slot.target.topleft
                slot.drag = False
                play_sfx(Path("Sounds") / "card_back.wav", volume=0.8)

        elif ev.type == pygame.MOUSEMOTION and dragged_slot:
            # Karte folgt Maus (unter Beibehaltung des Klick-Offsets)
            ox, oy = getattr(dragged_slot, "offset", (0, 0))
            dragged_slot.rect.topleft = (ev.pos[0] - ox, ev.pos[1] - oy)

def wave_hand(hand_slots: List[CardSlot], time_ms: int,
              amplitude: int = 1000, wavelength: float = 0.5*math.pi) -> None:
    """
    Verschiebt die Karten wie eine La-Ola-Welle: jede Karte wandert
    sinusförmig ein Stück nach oben.

    Args:
        hand_slots: Liste der CardSlot-Objekte
        time_ms:    aktuelle Zeit in Millisekunden (z.B. pygame.time.get_ticks())
        amplitude:  maximale Höhe der Welle in Pixeln
        wavelength: Abstand im Sinus zwischen Karten
    """
    for idx, slot in enumerate(hand_slots):
        # Grundposition am target halten
        base_y = slot.target.y
        # Wellenoffset berechnen
        phase = time_ms / 200.0 + idx * (wavelength / len(hand_slots))
        offset = int(np.abs(math.sin(phase) * amplitude))
        slot.rect.y = base_y - offset
        play_sfx(Path("Sounds") / "card_Wave_1.wav", volume=0.4)