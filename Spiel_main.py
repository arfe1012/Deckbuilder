import sys
from pathlib import Path
import pygame
from Screen_and_Backrounds import screenscale, bild_laden, scale_bg
from Sounds.Sound import play_bgm, stop_bgm,play_sfx
import cardslot as hand                      # <– Modul komplett importieren
from Game.GameManager import GameManager


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
    
    # Karten vorbereiten ----------------------------------------------------
    blank = pygame.image.load("Grafiken/card.png").convert_alpha()
    card_imgs = [blank] * 5                       # später echte Artworks hier
    hand_slots = hand.create_hand(card_imgs, screen_rect, current_room)

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
        events = pygame.event.get()               # Liste für Drag-Handling
        for ev in events:
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    running = False
            elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            # Klick-IN-Button?
                if attack_btn_rect.collidepoint(ev.pos):
                    current_room.player_turn()
                    play_sfx("Sounds/card_back.wav", volume=0.8)
            elif ev.type == pygame.VIDEORESIZE:
                sw, sh = ev.size
                screen = pygame.display.set_mode(ev.size, pygame.RESIZABLE)
                background = scale_bg((sw, sh), bg_fight_orig)
                # Slots neu layouten:
                hand_slots = hand.create_hand(card_imgs, screen.get_rect(), current_room)

        # Drag & Drop
        hand.handle_hand_events(events, hand_slots, current_room)

        # ---------------------------- Zeichnen -----------------------------
        screen.blit(background, (0, 0))
        hand.draw_hand(screen, hand_slots)
        Spieler.draw_sprite(screen, scale=0.55) #Spieler zeichnen
        game_manager.room.enemy.draw_sprite(screen,scale=0.55)
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
        game_manager.room.draw_room_result(screen)
        pygame.display.flip()
        clock.tick(60)

    stop_bgm()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main("warrior")
