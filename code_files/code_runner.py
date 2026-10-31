
import subprocess
import os

def getch(msg):
    import msvcrt
    print(msg)
    return msvcrt.getch().decode("utf-8", errors="ignore")

def clear_screen():
    os.system("cls")

def compiler(c_file,c_content):
    with open(file=c_file,mode='w')as file:
        file.write(c_content)
    ccompiler=['gcc',c_file,'-o','main']
    subprocess.run(ccompiler)
    print (result.stderr)
    c_runner=["main.exe"]
    result=subprocess.run(c_runner)
   



def pythonexe(py_file,py_content):    
    with open(file=py_file,mode='w')as file:
            file.write(py_content)
    py_runner=['py',py_file]
    result=subprocess.run(py_runner,text=True)
    
        



def code_runner(file,lang,code):
    try:
        c_file=f"c_files/{file}.c"
        py_file=f"python_files/{file}.py"
        
        clear_screen()
        match(lang):
            case 1:
                pythonexe(py_file,code)
            case 2:
                compiler(c_file,code)
        out=getch("--------------------------------------------\npress any key to continue. . .")
        clear_screen()
    except:
        pass