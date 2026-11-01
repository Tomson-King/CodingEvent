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

def pygame_editor(screen,key,file):
    with open("code_files/codes.json","r")as f:
        code_files=json.load(f)
    code=code_files["codes"][file]["code"]
    font_type=None
    font_size=32
    font_colour=(255,255,255)
    text=pygame.font.Font(font_type,font_size)
    current=code_files["codes"][file]["current"]
    start=code_files["codes"][file]["start"]
    no_lines=30

    
   
    if key==pygame.K_BACKSPACE:
        if(current==0 and len(code[current])==1):
            code[current]=""
            
        elif(len(code[current])==1):
            code.pop()
            current-=1
        else:
            code[current]=code[current][:-1]

    elif key==pygame.K_RETURN:
        code.append("")
        current+=1
        if(current<no_lines):
            start=0
        else:
            start=current-no_lines+1
    else:
        if(key!=None):
            code[current] += key
    for i in range(len(code)):
        space=i*font_size
        text_surface=text.render(code[i],True,font_colour)
        screen.blit(text_surface,(100,space))
    code_files["codes"][file]["code"]=code
    code_files["codes"][file]["current"]=current
    code_files["codes"][file]["start"]=start
    with open("code_files/codes.json","w")as f:
        json.dump(code_files,f,indent=4)

    return code
