import __main__
import subprocess
test_file="test.c"
test_content="#include <stdio.h>\nint main(){\nprintf(\"hi\");\n}"
def compiler(c_file,c_content):
    try:
        with open(file=c_file,mode='w')as file:
            file.write(c_content)
        ccompiler=['gcc',c_file,'-o','main']
        subprocess.run(ccompiler)
        crunner=[".\\main.exe"]
        subprocess.run(crunner)
    except:
        pass
if(__name__==__main__):
    compiler(test_file,test_content)