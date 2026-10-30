from module import *

def main():
    file="test"
    lang=int(input("Enter 1 for python 2 for c"))

    test_code=code_editor()

    code_runner(file,lang,test_code)

main()
