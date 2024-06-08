def test_wra(val,instV,allowNone,checkEq):
    if not isinstance(val, instV) and (val is not None and (checkEq and val != instV) or (not checkEq) or (val is None and not allowNone)) and (val is not None or not allowNone):
        return False
    else:
        return True
    
def test(val,instV,allowNone,checkEq,exp=None):
    res = test_wra(val,instV,allowNone,checkEq)
    if exp == None:
        if res == True:
            print("True \033[90m?\033[0m")
        else:
            print("False \033[90m?\033[0m")
    else:
        if res == exp:
            if res == True:
                print("True \033[32m✓\033[0m")
            else:
                print("False \033[32m✓\033[0m")
        else:
            if res == True:
                print("True \033[31m✗\033[0m")
            else:
                print("False \033[31m✗\033[0m")

print('\033[94m"str"\033[0m : \033[33mstr            ',end=" \033[90m=>\033[0m "); test("str",str,False,False,True)
print('\033[94m"str"\033[0m : \033[33mint            ',end=" \033[90m=>\033[0m "); test("str",int,False,False,False)

print(' \033[34mNone\033[0m : \033[33mstr            ',end=" \033[90m=>\033[0m "); test(None,str,False,False,False)
print(' \033[34mNone\033[0m : \033[33mstr \033[90m(allowNone)',end=" \033[90m=>\033[0m "); test(None,str,True,False,True)

print('\033[94m"str"\033[0m : \033[33mstr \033[90m(checkEq)  ',end=" \033[90m=>\033[0m "); test("str",str,False,True,True)
print('\033[94m"str"\033[0m : \033[33mint \033[90m(checkEq)  ',end=" \033[90m=>\033[0m "); test("str",int,False,True,False)
print(' \033[34mNone\033[0m : \033[33mstr  \033[90m(checkEq)  ',end=" \033[90m=>\033[0m "); test(None,str,False,True,False)
print('  \033[34mstr\033[0m : \033[33mstr \033[90m(checkEq)  ',end=" \033[90m=>\033[0m "); test(str,str,False,True,True)