import sys
from pathlib import Path
import pygame
from Screen_and_Backrounds import screenscale, bild_laden, scale_bg
from Sounds.Sound import play_bgm, stop_bgm,play_sfx
import cardslot as hand                      # <– Modul komplett importieren
from Game.GameManager import GameManager
import time
class SlashEffect:
    def __init__(self, image: pygame.Surface,
                 start_pos: tuple[int,int],
                 end_pos:   tuple[int,int],
                 duration:  int = 300,scale: float=1.0):
        if scale != 1.0:
            w, h = image.get_size()
            image = pygame.transform.smoothscale(image, (int(w*scale), int(h*scale)))
        self.image = image
        self.start    = pygame.Vector2(start_pos)
        self.end      = pygame.Vector2(end_pos)
        self.duration = duration
        self.elapsed  = 0
        self.rect     = self.image.get_rect(center=start_pos)

    def update(self, dt: int):
        self.elapsed += dt
        t = min(self.elapsed / self.duration, 1.0)
        pos = self.start.lerp(self.end, t)
        self.rect.center = (int(pos.x), int(pos.y))

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)

    def is_finished(self) -> bool:
        return self.elapsed >= self.duration


def main(character_name="warrior"):
    pygame.init()
    # HUD_FONT = pygame.font.SysFont(None, 32, bold=True)
    # HUD_COLOR = (250, 240, 200)            # helles Beige, gut lesbar
    play_bgm(Path("Sounds") / "Hölenmusik.wav", volume=1.0)

    screen, sw, sh = screenscale()
    screen_rect = screen.get_rect()

    # Hintergrund
    asset_dir = Path(__file__).parent / "Grafiken"
    bg_fight_orig = bild_laden(asset_dir / "Arena.png")
    background = scale_bg((sw, sh), bg_fight_orig)

    # Spiellogik initialisieren -------------------------------------------
    game_manager = GameManager(character_name.lower())
    game_manager.room.show_next_cards()
    current_room = game_manager.room
    current_cards = game_manager.room.shown_cards
    #Spieler erzeugen---------------------------------
    Spieler = game_manager.get_player()
    #____________________Gegner Stats__________
    game_manager.room.give_enemy_random_stats()
    # Karten vorbereiten ----------------------------------------------------
    blank = pygame.image.load("Grafiken/card.png").convert_alpha()
    card_imgs = [blank] * 5                       # später echte Artworks hier
    hand_slots = hand.create_hand(card_imgs, screen_rect, current_room)
#_____________angriffeeffeck
    slash_img = pygame.transform.smoothscale(pygame.image.load("Grafiken/attack.png").convert_alpha(),(100, 25))
    slash_img_enemy = pygame.transform.smoothscale(pygame.image.load("Grafiken/attack_enemy.png").convert_alpha(),(100, 25))
    slashes   = []      # wird SlashEffect-Objekte aufnehmen
    attack_queued = False
    attack_phase = None 
#------------------LaoalaWElle----------
    wave_active     = False
    return_active   = False
    wave_start      = 0
    return_start    = 0
    wave_duration   = 800    # ms
    return_duration = 300 
#----------------------------------------
    clock = pygame.time.Clock()
    running = True
    font = pygame.font.SysFont(None, 28, bold=True)

    #___________________________Attackkonopf
    attack_btn_font = pygame.font.SysFont("Comic Sans MS", 24, bold=True)
    attack_btn_text = attack_btn_font.render("Attack", True, (255,255,255))
    attack_btn_padding = 10
    btn_w = attack_btn_text.get_width() + 2*attack_btn_padding
    btn_h = attack_btn_text.get_height() + 2*attack_btn_padding
    # Position des Buttons
    btn_x = sw - btn_w - 100
    btn_y = 720
    attack_btn_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)
    #________________________________________________________________________
    while running:
        dt     = clock.tick(60)
        events = pygame.event.get()               # Liste für Drag-Handling
        for ev in events:
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    running = False
            elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            # Klick-IN-Button?
                if attack_btn_rect.collidepoint(ev.pos)and not attack_queued and len(slashes) == 0 and wave_active   == False:
                    play_sfx("Sounds/card_back.wav", volume=0.8)

                    start_v = pygame.Vector2(player_rect.center)
                    try:
                        end_v = pygame.Vector2(enemy_rect.center)
                    except AttributeError:
                        end_v = pygame.Vector2(player_rect.center) + pygame.Vector2(-100, 0)

                    direction = (end_v - start_v).normalize()

                    # Pixel-Abstand vom Mittelpunkt weglassen
                    start_pad = 50  # schiebt den Anfang weiter vor die Spielfigur
                    end_pad   = 400# lässt den Effekt etwas vor dem Gegner enden
                    Start_pad_en =300
                    end_pad_en = 400
                    # Neue Start- und End-Koordinaten
                    start_pos = (start_v + direction * start_pad)
                    end_pos   = (end_v   - direction * end_pad)
                    #----
                    end_pos_en = (start_v + direction * end_pad_en)
                    start_pos_en   = (end_v   - direction * Start_pad_en)
                    # Slash mit den angepassten Koordinaten starten
                    
                    slashes.append(
                        SlashEffect(
                            slash_img,
                            (int(start_pos.x), int(start_pos.y)),
                            (int(end_pos.x),   int(end_pos.y)),
                            duration=300,scale=5
                        )
                    )
                    slashes.append(
                        SlashEffect(
                            slash_img_enemy,
                            (int(start_pos_en.x), int(start_pos_en.y)),
                            (int(end_pos_en.x),   int(end_pos_en.y)),
                            duration=300,scale=5
                        )
                    )
                    wave_active   = True
                    return_active = False
                    wave_start    = pygame.time.get_ticks()
            elif ev.type == pygame.VIDEORESIZE:
                sw, sh = ev.size
                screen = pygame.display.set_mode(ev.size, pygame.RESIZABLE)
                background = scale_bg((sw, sh), bg_fight_orig)
                # Slots neu layouten:
                hand_slots = hand.create_hand(card_imgs, screen.get_rect(), current_room)

        # Drag & Drop
        now = pygame.time.get_ticks()
        if wave_active:
            elapsed = now - wave_start
            hand.wave_hand(hand_slots, elapsed, amplitude=20)  # z.B. größere Amplitude
            if elapsed >= wave_duration:
                wave_active   = False
                return_active = True
                return_start  = now
                # Merke dir die letzte Offsets:
                for slot in hand_slots:
                    slot._wave_offset = slot.target.y - slot.rect.y

        # ─── Rück-Animation ───────────────────────────────────────────
        elif return_active:
            elapsed = now - return_start
            t = min(elapsed/return_duration, 1.0)
            for slot in hand_slots:
                base_y = slot.target.y
                offset = getattr(slot, "_wave_offset", 0)
                # Lerp von offset → 0
                slot.rect.y = int(base_y - offset * (1 - t))
            if t >= 1.0:
                return_active = False
                # Cleanup: sicher auf Ziel-Y setzen
                for slot in hand_slots:
                    slot.rect.y = slot.target.y
                current_room.player_turn()
                game_manager.room.give_enemy_random_stats()
        
        for slash in slashes:
            slash.update(dt)

        # 2) Draw Slash(s) direkt nach Background, vor allem anderen
        screen.blit(background, (0,0))
        for slash in slashes:
            slash.draw(screen)

        # 3) Fertige Effekte abarbeiten
        finished = [s for s in slashes if s.is_finished()]
        for s in finished:
            slashes.remove(s)
            if attack_queued:
                current_room.player_turn()
                game_manager.room.give_enemy_random_stats()
                attack_queued = False

        hand.handle_hand_events(events, hand_slots, current_room)

        # ---------------------------- Zeichnen -----------------------------
        # screen.blit(background, (0, 0))
        hand.draw_hand(screen, hand_slots)
        player_rect=Spieler.draw_sprite(screen, scale=0.55) #Spieler zeichnen
        enemy_rect=game_manager.room.enemy.draw_sprite(screen,scale=0.55)
        #------------------ Agriffsbutton zeichen----------
        pygame.draw.rect(screen, (255, 0, 0, 128), attack_btn_rect, border_radius=8)
        # 2) leicht hellere Umrandung
        pygame.draw.rect(screen, (200,200,200), attack_btn_rect, width=2, border_radius=8)
        # 3) Text zentriert in Button
        text_x = attack_btn_rect.x + attack_btn_padding
        text_y = attack_btn_rect.y + attack_btn_padding
        screen.blit(attack_btn_text, (text_x, text_y))
        #______________________________________________________

        # Platzhalter-Text auf Karten
        font=pygame.font.SysFont("Comic Sans MS", 24, bold=False, italic=False)
        for index, slot in enumerate(hand_slots):
            if current_room.shown_cards[index].health_operation in ("-", "/"):
                lbl_health = font.render("Health: " + str(current_room.shown_cards[index].health_operation)+" "+ str(current_room.shown_cards[index].health), True, (200, 50, 50))
            else:  
                lbl_health = font.render("Health: " + str(current_room.shown_cards[index].health_operation)+" "+ str(current_room.shown_cards[index].health), True, (0, 0, 0))
            if current_room.shown_cards[index].attack_operation in ("-", "/"):
                lbl_attack = font.render("Attack: " + str(current_room.shown_cards[index].attack_operation)+" "+ str(current_room.shown_cards[index].attack), True, (200, 50, 50))
            else:
                lbl_attack = font.render("Attack: " + str(current_room.shown_cards[index].attack_operation)+" "+ str(current_room.shown_cards[index].attack), True, (0, 0, 0))
            if current_room.shown_cards[index].block_operation in ("-", "/"):
                lbl_block = font.render("Block: " + str(current_room.shown_cards[index].block_operation) +" "+ str(current_room.shown_cards[index].block), True, (200, 50, 50))
            else:
                 lbl_block = font.render("Block: " + str(current_room.shown_cards[index].block_operation) +" "+ str(current_room.shown_cards[index].block), True, (0, 0, 0))   
            if current_room.shown_cards[index].poison_operation in ("-", "/"):
                lbl_poison = font.render("Poison: " + str(current_room.shown_cards[index].poison_operation) +" "+ str(current_room.shown_cards[index].poison), True, (200, 50, 50))
            else:
                lbl_poison = font.render("Poison: " + str(current_room.shown_cards[index].poison_operation) +" "+ str(current_room.shown_cards[index].poison), True, (0, 0, 0))
            if current_room.shown_cards[index].blood_operation in ("-", "/"):
                lbl_blood = font.render("Blood: "+ str(current_room.shown_cards[index].blood_operation) + " "+str(current_room.shown_cards[index].blood), True, (200, 50, 50))
            else:
                lbl_blood = font.render("Blood: "+ str(current_room.shown_cards[index].blood_operation) + " "+str(current_room.shown_cards[index].blood), True, (0, 0, 0))
            if current_room.shown_cards[index].crit_operation in ("-", "/"):
                lbl_crit = font.render("Crit: " + str(current_room.shown_cards[index].crit_operation)+" "+ str(current_room.shown_cards[index].crit), True, (200, 50, 50))
            else:
                lbl_crit = font.render("Crit: " + str(current_room.shown_cards[index].crit_operation)+" "+ str(current_room.shown_cards[index].crit), True, (0, 0, 0))
            if current_room.shown_cards[index].health != 0:
                screen.blit(lbl_health, lbl_health.get_rect(center=(slot.rect.centerx,
                                                  slot.rect.y + 100)))
            if current_room.shown_cards[index].attack != 0:
                screen.blit(lbl_attack, lbl_attack.get_rect(center=(slot.rect.centerx,
                                                  slot.rect.y + 130)))
            if current_room.shown_cards[index].block != 0:
                screen.blit(lbl_block, lbl_block.get_rect(center=(slot.rect.centerx,
                                                  slot.rect.y + 160)))
            if current_room.shown_cards[index].poison != 0:
                screen.blit(lbl_poison, lbl_poison.get_rect(center=(slot.rect.centerx,
                                                  slot.rect.y + 190)))
            if current_room.shown_cards[index].blood != 0:
                screen.blit(lbl_blood, lbl_blood.get_rect(center=(slot.rect.centerx,
                                                  slot.rect.y + 220)))
            if current_room.shown_cards[index].crit != 0:
                screen.blit(lbl_crit, lbl_crit.get_rect(center=(slot.rect.centerx,
                                                  slot.rect.y + 250)))
        game_manager.room.calculate_card_effects()
        game_manager.room.draw_room_result(screen)
        pygame.display.flip()
        clock.tick(60)

    stop_bgm()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main("warrior")
