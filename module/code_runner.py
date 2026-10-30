
import subprocess

def compiler(c_file,c_content):
    try:
        with open(file=c_file,mode='w')as file:
            file.write(c_content)
        ccompiler=['gcc',c_file,'-o','main']
        subprocess.run(ccompiler)
        c_runner=["main.exe"]
        subprocess.run(c_runner)
    except:
        pass


def pythonexe(py_file,py_content):
    try:
    
        with open(file=py_file,mode='w')as file:
                file.write(py_content)
        pyrunner=['py',py_file]
        subprocess.run(pyrunner)
    except:
        pass


def code_runner(file,lang,code):
    try:
        c_file=f"c_files/{file}.c"
        py_file=f"python_files/{file}.py"

        

        match(lang):
            case 1:
                pythonexe(py_file,code)
            case 2:
                compiler(c_file,code)
    except:
        pass