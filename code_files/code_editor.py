import pygame
import json


def terminal_editor():
    print("Enter the code \n")
    line=""
    code=[]
    while(line!="run"):
        line=input()
        if(line=="run"):
            break
        code.append(line)
    test_code="\n".join(code)
    return test_code


def pygame_editor(screen, key, file,lang="py"):
    with open("code_files/codes.json", "r") as f:
        code_files = json.load(f)

    file_data = code_files["codes"].setdefault(file, {
        "code": [""],
        "lang":"py",
        "start": 0,
        "current": 0,
        "cursor_pos": 0
    })

    code = file_data.get("code", [""])
    if not code:
        code = [""]
    lang=file_data["lang"]
    current = file_data.get("current", 0)
    cursor_pos = file_data.get("cursor_pos", 0)
    start = file_data.get("start", 0)

    # Clean any legacy trailing cursor underscores
    if current < len(code) and code[current].endswith('_') and cursor_pos == len(code[current]) - 1:
        code[current] = code[current][:-1]

    current = max(0, min(current, len(code) - 1))
    cursor_pos = max(0, min(cursor_pos, len(code[current])))

    font_type = None
    font_size = 20
    font_colour = (255, 255, 255)
    text = pygame.font.Font(font_type, font_size)

    # Layout constants
    top_offset = 56
    bottom_offset=120
    text_x_offset = 200
    line_num_x = 160
    code_start_y = top_offset + 12
    no_lines = max(1, (screen.get_height() - code_start_y - bottom_offset) // font_size)

    # Run button dimensions & hit-box
    btn_w, btn_h = 115, 36
    btn_rect = pygame.Rect(screen.get_width() - btn_w - 25, 10, btn_w, btn_h)
    btn1_rect = pygame.Rect(1000, 600, 140, 40)#py button
    btn2_rect = pygame.Rect(1000, 660, 140, 40)#c button

    action = None
    modified = False

    # Check Run button triggered via direct action key (e.g. F5 or Ctrl+Enter)
    if key == "RUN":
        action = "RUN"
        modified = True

    elif key is not None:
        modified = True

        # --- Mouse Click to Reposition Cursor or Click Run Button ---
        if isinstance(key, tuple) and len(key) == 2 and key[0] == "CLICK":
            mouse_x, mouse_y = key[1]
            if btn_rect.collidepoint(mouse_x, mouse_y):
                action = "RUN"
            if btn1_rect.collidepoint(mouse_x, mouse_y):
                lang="py"
            if btn2_rect.collidepoint(mouse_x, mouse_y):
                lang="c"    
            elif mouse_y >= code_start_y:
                clicked_line = start + ((mouse_y - code_start_y) // font_size)
                if 0 <= clicked_line < len(code):
                    current = clicked_line
                    target_x = max(0, mouse_x - text_x_offset)
                    line_str = code[current]
                    best_pos = len(line_str)
                    for idx in range(len(line_str) + 1):
                        w = text.size(line_str[:idx])[0]
                        if w >= target_x:
                            if idx > 0:
                                prev_w = text.size(line_str[:idx - 1])[0]
                                if abs(target_x - prev_w) < abs(target_x - w):
                                    best_pos = idx - 1
                                else:
                                    best_pos = idx
                            else:
                                best_pos = 0
                            break
                    cursor_pos = best_pos

        # --- Cursor Movement ---
        elif key == pygame.K_LEFT:
            if cursor_pos > 0:
                cursor_pos -= 1
            elif current > 0:
                current -= 1
                cursor_pos = len(code[current])

        elif key == pygame.K_RIGHT:
            if cursor_pos < len(code[current]):
                cursor_pos += 1
            elif current < len(code) - 1:
                current += 1
                cursor_pos = 0

        elif key == pygame.K_UP:
            if current > 0:
                current -= 1
                cursor_pos = min(cursor_pos, len(code[current]))

        elif key == pygame.K_DOWN:
            if current < len(code) - 1:
                current += 1
                cursor_pos = min(cursor_pos, len(code[current]))

        elif key == pygame.K_HOME:
            cursor_pos = 0

        elif key == pygame.K_END:
            cursor_pos = len(code[current])

        # --- Editing / Deleting ---
        elif key == pygame.K_BACKSPACE:
            if cursor_pos > 0:
                line = code[current]
                code[current] = line[:cursor_pos - 1] + line[cursor_pos:]
                cursor_pos -= 1
            elif current > 0:
                prev_len = len(code[current - 1])
                curr_line = code.pop(current)
                current -= 1
                code[current] += curr_line
                cursor_pos = prev_len

        elif key == pygame.K_DELETE:
            line = code[current]
            if cursor_pos < len(line):
                code[current] = line[:cursor_pos] + line[cursor_pos + 1:]
            elif current < len(code) - 1:
                next_line = code.pop(current + 1)
                code[current] += next_line

        elif key == pygame.K_RETURN:
            line = code[current]
            code[current] = line[:cursor_pos]
            code.insert(current + 1, line[cursor_pos:])
            current += 1
            cursor_pos = 0

        elif key == pygame.K_TAB:
            spaces = "    "
            line = code[current]
            code[current] = line[:cursor_pos] + spaces + line[cursor_pos:]
            cursor_pos += len(spaces)

        # --- Character Input ---
        elif isinstance(key, str) and key.isprintable():
            line = code[current]
            code[current] = line[:cursor_pos] + key + line[cursor_pos:]
            cursor_pos += len(key)

    # Scroll adjustment to keep cursor in view
    if current < start:
        start = current
    elif current >= start + no_lines:
        start = current - no_lines + 1

    # Mouse hover state & cursor update
    mouse_pos = pygame.mouse.get_pos()
    is_btn_hover = btn_rect.collidepoint(mouse_pos)
    mouse_pressed = pygame.mouse.get_pressed()[0]

    try:
        if is_btn_hover:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif mouse_pos[0] >= text_x_offset and mouse_pos[1] >= code_start_y and mouse_pos[1] <(screen.get_height-bottom_offset):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    except Exception:
        pass

    # --- Render Code Lines ---
    for display_idx, line_idx in enumerate(range(start, min(len(code), start + no_lines))):
        y_pos = code_start_y + display_idx * font_size
        line_str = code[line_idx]

        # Line numbers
        line_num = text.render(str(line_idx + 1), True, (90, 90, 95))
        screen.blit(line_num, (line_num_x, y_pos))

        # Text content
        text_surface = text.render(line_str, True, font_colour)
        screen.blit(text_surface, (text_x_offset, y_pos))

    # --- Render Cursor ---
    if start <= current < start + no_lines:
        cursor_y = code_start_y + (current - start) * font_size
        prefix = code[current][:cursor_pos]
        cursor_x = text_x_offset + text.size(prefix)[0]
        # Blinking vertical cursor line
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            pygame.draw.line(screen, (255, 255, 255), (cursor_x, cursor_y + 2), (cursor_x, cursor_y + font_size - 4), 2)

        # --- Render Two Additional Buttons ---
    

    

    # Button 1
    btn1_hover = btn1_rect.collidepoint(mouse_pos)
    btn1_color = (46, 215, 110) if btn1_hover else (34, 197, 94)

    pygame.draw.rect(screen, btn1_color, btn1_rect, border_radius=8)
    pygame.draw.rect(screen, (74, 222, 128), btn1_rect, 1, border_radius=8)

    btn_font = pygame.font.Font(None, 24)
    btn1_text = btn_font.render("Python File", True, (255, 255, 255))
    screen.blit(btn1_text, btn1_text.get_rect(center=btn1_rect.center))

    # Button 2
    btn2_hover = btn2_rect.collidepoint(mouse_pos)
    btn2_color = (46, 215, 110) if btn2_hover else (34, 197, 94)

    pygame.draw.rect(screen, btn2_color, btn2_rect, border_radius=8)
    pygame.draw.rect(screen, (74, 222, 128), btn2_rect, 1, border_radius=8)

    btn2_text = btn_font.render("C File", True, (255, 255, 255))
    screen.blit(btn2_text, btn2_text.get_rect(center=btn2_rect.center))

    # --- Render Top Toolbar Header ---
    pygame.draw.rect(screen, (24, 24, 28), (0, 0, screen.get_width(), top_offset))
    pygame.draw.line(screen, (45, 45, 52), (0, top_offset), (screen.get_width(), top_offset), 1)

    # File badge / title on top left
    tab_rect = pygame.Rect(30, 11, 140, 34)
    pygame.draw.rect(screen, (36, 36, 42), tab_rect, border_radius=6)
    pygame.draw.rect(screen, (55, 55, 65), tab_rect, width=1, border_radius=6)
    pygame.draw.circle(screen, (34, 197, 94), (46, 28), 4)  # Active dot
    badge_font = pygame.font.Font(None, 20)
    badge_txt = badge_font.render(f"{file}.{lang}", True, (215, 215, 220))
    screen.blit(badge_txt, (58, 21))

    # --- Render Run Button ---
    if is_btn_hover:
        if mouse_pressed:
            btn_color = (21, 128, 61)       # Pressed dark green
            border_color = (34, 197, 94)
            offset_y = 1
        else:
            btn_color = (46, 215, 110)      # Bright hover green
            border_color = (134, 239, 172)
            offset_y = 0
    else:
        btn_color = (34, 197, 94)           # Default Emerald green
        border_color = (74, 222, 128)
        offset_y = 0

    # Button Drop Shadow
    pygame.draw.rect(screen, (10, 24, 14), (btn_rect.x, btn_rect.y + 2, btn_rect.width, btn_rect.height), border_radius=8)
    # Button Surface
    draw_btn_rect = pygame.Rect(btn_rect.x, btn_rect.y + offset_y, btn_rect.width, btn_rect.height)
    pygame.draw.rect(screen, btn_color, draw_btn_rect, border_radius=8)
    pygame.draw.rect(screen, border_color, draw_btn_rect, width=1, border_radius=8)

    # Play Icon (Triangle) + "Run" Text
    btn_font = pygame.font.Font(None, 22)
    btn_text_surf = btn_font.render("Run", True, (255, 255, 255))
    total_content_w = 10 + 8 + btn_text_surf.get_width()
    icon_x = draw_btn_rect.x + (draw_btn_rect.width - total_content_w) // 2
    icon_y = draw_btn_rect.centery
    triangle_points = [(icon_x, icon_y - 6), (icon_x, icon_y + 6), (icon_x + 10, icon_y)]
    pygame.draw.polygon(screen, (255, 255, 255), triangle_points)
    screen.blit(btn_text_surf, (icon_x + 10 + 8, draw_btn_rect.centery - btn_text_surf.get_height() // 2))

    # Save state if modified
    if modified:
        file_data["lang"]= lang
        file_data["code"] = code
        file_data["current"] = current
        file_data["cursor_pos"] = cursor_pos
        file_data["start"] = start
        with open("code_files/codes.json", "w") as f:
            json.dump(code_files, f, indent=4)
    result=(code, action)
    return  result , lang
