def code_editor():
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
