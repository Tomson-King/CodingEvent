import pygame

def display_questions(screen,key,selected):

    btn_w, btn_h = 50, 36
    button_placement=[10,60]
    Q_btn =[]
    for i in range(7):
        Q_btn.append( pygame.Rect(button_placement[0],button_placement[1]+(i*(2*btn_h)), btn_w, btn_h))

    modified = False
    mouse_pos = pygame.mouse.get_pos()
    is_btn_hover=[False,False,False,False,False,False,False]
    if key is not None:
        modified = True
        
        # --- Mouse Click to Reposition Cursor or Click Run Button ---
        if isinstance(key, tuple) and len(key) == 2 and key[0] == "CLICK":
            mouse_x, mouse_y = key[1]
            for i in range(7):
                if Q_btn[i].collidepoint(mouse_x, mouse_y):
                    selected=i

        
    
    for i in range(7):
            if Q_btn[i].collidepoint(mouse_pos):
                is_btn_hover[i] = Q_btn[i].collidepoint(mouse_pos)
                mouse_pressed = pygame.mouse.get_pressed()[0]
            
    for i in range(7):
        try:
            if is_btn_hover[i]:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        except Exception:
             pass


    btn_color =[]    # Bright hover green
    border_color = []
    offset_y = []
    for i in range(7):
        if is_btn_hover[i]:

            btn_color.append((46, 215, 110))    # Bright hover green
            border_color.append((134, 239, 172))
            offset_y.append(0)
        else:
            btn_color.append((34, 197, 94))         # Default Emerald green
            border_color.append((74, 222, 128))
            offset_y.append(0)
    

    btn_font = pygame.font.Font(None, 22)
    btn_text_surf=[]
    for i in range(7):
        if(i==6):
            btn_text_surf.append(btn_font.render(f"Test", True, (255, 255, 255)))
        else:
            btn_text_surf.append(btn_font.render(f"Q{i+1}", True, (255, 255, 255)))


    draw_btn_rect=[]        
    for i in range(7):
        draw_btn_rect.append(pygame.Rect(Q_btn[i].x, Q_btn[i].y + offset_y[i], Q_btn[i].width, Q_btn[i].height))
        pygame.draw.rect(screen, btn_color[i], draw_btn_rect[i], border_radius=8)
        pygame.draw.rect(screen, border_color[i], draw_btn_rect[i], width=1, border_radius=8)
    
    for i in range(7):
        screen.blit(btn_text_surf[i], (10 + 8, draw_btn_rect[i].centery - btn_text_surf[i].get_height() // 2))
    

    return selected