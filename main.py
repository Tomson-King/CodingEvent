from code_files import *
import pygame
import os
import json


def code_init():
    with open("code_files/codes.json", "w") as code_file:
        files = ["code_1", "code_2", "code_3", "code_4", "code_5", "code_6", "test"]
        code = {"codes": {f: {"Question": [""],"lang":"py","code": [""], "start": 0, "current": 0, "cursor_pos": 0} for f in files}}
        json.dump(code, code_file, indent=4)


def test():
    file = "test"
    lang = int(getch("Enter 1 for python 2 for c"))

    test_code = terminal_editor()
    clear_screen()
    code_runner(file, lang, test_code)
    clear_screen()


def pygame_display():
    lang="py"
    pygame.init()
    pygame.key.set_repeat(400, 40)
    screen = pygame.display.set_mode((1280, 720))

    pygame.display.set_caption(f"Code Editor")
    clock = pygame.time.Clock()

    key = None

    running = True
    selected=6
    files = ["code_1", "code_2", "code_3", "code_4", "code_5", "code_6", "test"]
    while running:
        screen.fill((18, 18, 20))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                key = ("CLICK", event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F5:
                    key = "RUN"
                elif event.key == pygame.K_RETURN and (event.mod & pygame.KMOD_CTRL):
                    key = "RUN"
                elif event.key == pygame.K_BACKSPACE:
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
        selected=display_questions(screen,key,selected)
        file=files[selected]
        result ,lang= pygame_editor(screen, key, file,lang)
        if isinstance(result, tuple):
            code, action = result
        else:
            code, action = result, None

        if action == "RUN":
            running = False

        key = None
        pygame.display.flip()
        clock.tick(60)

    with open("code_files/codes.json", "r") as f:
        code_files = json.load(f)
    code = code_files["codes"][file]["code"]

    test_code = "\n".join(code)
    pygame.quit()
    if(action!="RUN"):
        action="quit"
    return test_code,file,action,lang


if __name__ == "__main__":
    code_init()
    action=""

    while(action!="quit"):
        test_code,file,action,lang = pygame_display()
        if(action=="quit"):
            break
        if(action=="RUN"):
            clear_screen()
            code_runner(file, lang, test_code)
            clear_screen()
            print(lang)
