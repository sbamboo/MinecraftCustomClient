#exclude ST
import platform, shutil
def typeval(val,typeV,nm=None,allowNone=False):
    """Raises if type of 'val' does not match 'typeV'!"""
    if type(val) != typeV and (val is not None or not allowNone):
        try: typeN = typeV.__name__
        except: typeN = str(typeV)
        if nm == None: raise Exception(f"Invalid type for parameter, must be '{typeN}'!")
        else: raise Exception(f"Invalid type for parameter '{nm}', must be '{typeN}'!")
def instval(val,instV,nm=None,allowNone=False,instN=None,checkEq=False):
    """Raises if type of 'val' is not instance of 'instV'!"""
    if not isinstance(val, instV) and (val is not None and (checkEq and val != instV) or (not checkEq) or (val is None and not allowNone)) and (val is not None or not allowNone):
        try: typeN = instN if instN != None else instV.__name__
        except: typeN = str(instV)
        if nm == None: raise Exception(f"Invalid type for parameter, must be '{typeN}'!")
        else: raise Exception(f"Invalid type for parameter '{nm}', must be '{typeN}'!")
#exclude END

class Services():

    class local_JVM_Manager():
        def __init__(self,parentPath=str):
            self.platform = platform.system().lower()
            self.parentPath = parentPath

    class JVM_Manager():
        def __init__(self,customJVMBin:str=None):
            typeval(customJVMBin,str,"customJVMBin",True)
            self.platform = platform.system().lower()
            self.localJvmCliCmd = "java"
            self.customJVMBin = customJVMBin
        
        def checkJavaExistence(self) -> bool:
            if self.customJVMBin != None:
                return os.path.exists(self.customJVMBin)
            else:
                # Check if avaliable in cli
                if shutil.which(self.localJvmCliCmd):
                    return True
                else:
                    return False

        def getJavaPath(self) -> str|None:
            if self.customJVMBin != None:
                if os.path.exists(self.customJVMBin) == True:
                    return self.customJVMBin
                else:
                    return None
            else:
                toret = shutil.which(self.localJvmCliCmd)
                if toret:
                    return toret
                else:
                    return None

        def ensureJavaExistance(self,local_JVM_Manager) -> str:
            pass