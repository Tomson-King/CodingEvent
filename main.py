from code_files import *
import pygame
import os
import json

def code_init():
    with open("code_files/codes.json", "w") as code_file:
        code={"code_1":"","code_2":"","code_3":"","code_4":"","code_5":"","code_6":"","test":""}
        json.dump(code,code_file)





def test():
    file="test"
    lang=int(getch("Enter 1 for python 2 for c"))

    test_code=terminal_editor()
    clear_screen()
    code_runner(file,lang,test_code)
    clear_screen()


def pygame_display():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    key=None
    
    file="test"
 
    running=True
 

    while(running):
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_BACKSPACE:
                    key=(pygame.K_BACKSPACE)
                elif event.key==pygame.K_RETURN:
                    key=(pygame.K_RETURN)
                else:
                    key = event.unicode
        code=pygame_editor(screen,key,file)
        key=None
        pygame.display.flip()
        
        if (code[-1]=="run"):
            running==True
    clock.tick(60)
    code.pop()
    test_code="\n".join(code)         
    pygame.quit()
    return test_code

if __name__ == "__main__":
    test_code=pygame_display()
    file="test"
    lang=int(getch("Enter 1 for python 2 for c"))
    clear_screen()
    code_runner(file,lang,test_code)
    clear_screen()