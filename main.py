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
 
    running=True
 

    while(running):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False 
                
    pygame.quit()

if __name__ == "__main__":
    test()
