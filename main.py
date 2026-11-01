from code_files import *
import pygame
import os
import json


def code_init():
    with open("code_files/codes.json", "w") as code_file:
        files = ["code_1", "code_2", "code_3", "code_4", "code_5", "code_6", "test"]
        code = {"codes": {f: {"code": [""], "start": 0, "current": 0, "cursor_pos": 0} for f in files}}
        json.dump(code, code_file, indent=4)


def test():
    file = "test"
    lang = int(getch("Enter 1 for python 2 for c"))

    test_code = terminal_editor()
    clear_screen()
    code_runner(file, lang, test_code)
    clear_screen()


def pygame_display():
    pygame.init()
    pygame.key.set_repeat(400, 40)
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    key = None

    file = "test"
    running = True

    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                key = ("CLICK", event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    key = pygame.K_BACKSPACE
                elif event.key == pygame.K_DELETE:
                    key = pygame.K_DELETE
                elif event.key == pygame.K_RETURN:
                    key = pygame.K_RETURN
                elif event.key == pygame.K_UP:
                    key = pygame.K_UP
                elif event.key == pygame.K_DOWN:
                    key = pygame.K_DOWN
                elif event.key == pygame.K_RIGHT:
                    key = pygame.K_RIGHT
                elif event.key == pygame.K_LEFT:
                    key = pygame.K_LEFT
                elif event.key == pygame.K_TAB:
                    key = pygame.K_TAB
                elif event.key == pygame.K_HOME:
                    key = pygame.K_HOME
                elif event.key == pygame.K_END:
                    key = pygame.K_END
                else:
                    if event.unicode and event.unicode.isprintable():
                        key = event.unicode

        code = pygame_editor(screen, key, file)
        key = None
        pygame.display.flip()
        clock.tick(60)

    with open("code_files/codes.json", "r") as f:
        code_files = json.load(f)
    code = code_files["codes"][file]["code"]

    test_code = "\n".join(code)
    pygame.quit()
    return test_code


if __name__ == "__main__":
    test_code = pygame_display()
    file = "test"
    lang = int(getch("Enter 1 for python 2 for c"))
    clear_screen()
    code_runner(file, lang, test_code)
    clear_screen()
