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


def pygame_editor(screen, key, file):
    with open("code_files/codes.json", "r") as f:
        code_files = json.load(f)

    file_data = code_files["codes"].setdefault(file, {
        "code": [""],
        "start": 0,
        "current": 0,
        "cursor_pos": 0
    })

    code = file_data.get("code", [""])
    if not code:
        code = [""]

    current = file_data.get("current", 0)
    cursor_pos = file_data.get("cursor_pos", 0)
    start = file_data.get("start", 0)

    # Clean any legacy trailing cursor underscores from previously stored lines
    if current < len(code) and code[current].endswith('_') and cursor_pos == len(code[current]) - 1:
        code[current] = code[current][:-1]

    current = max(0, min(current, len(code) - 1))
    cursor_pos = max(0, min(cursor_pos, len(code[current])))

    font_type = None
    font_size = 32
    font_colour = (255, 255, 255)
    text = pygame.font.Font(font_type, font_size)
    no_lines = max(1, screen.get_height() // font_size)

    modified = False

    if key is not None:
        modified = True

        # --- Cursor Movement ---
        if key == pygame.K_LEFT:
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

        # --- Mouse Click to Reposition Cursor ---
        elif isinstance(key, tuple) and len(key) == 2 and key[0] == "CLICK":
            mouse_x, mouse_y = key[1]
            clicked_line = start + (mouse_y // font_size)
            if 0 <= clicked_line < len(code):
                current = clicked_line
                target_x = max(0, mouse_x - 100)
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

    # Render lines
    for display_idx, line_idx in enumerate(range(start, min(len(code), start + no_lines))):
        y_pos = display_idx * font_size
        line_str = code[line_idx]

        # Line numbers
        line_num = text.render(str(line_idx + 1), True, (90, 90, 90))
        screen.blit(line_num, (30, y_pos))

        # Text content
        text_surface = text.render(line_str, True, font_colour)
        screen.blit(text_surface, (100, y_pos))

    # Render cursor
    if start <= current < start + no_lines:
        cursor_y = (current - start) * font_size
        prefix = code[current][:cursor_pos]
        cursor_x = 100 + text.size(prefix)[0]
        # Blinking vertical cursor line
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            pygame.draw.line(screen, (255, 255, 255), (cursor_x, cursor_y + 2), (cursor_x, cursor_y + font_size - 4), 2)

    # Save state if modified
    if modified:
        file_data["code"] = code
        file_data["current"] = current
        file_data["cursor_pos"] = cursor_pos
        file_data["start"] = start
        with open("code_files/codes.json", "w") as f:
            json.dump(code_files, f, indent=4)

    return code
