import subprocess,sys,importlib,os

def getExecutingPython() -> str:
    '''CSlib: Returns the path to the python-executable used to start crosshell'''
    return sys.executable

def _check_pip() -> bool:
    '''CSlib_INTERNAL: Checks if PIP is present'''
    try:
        with open(os.devnull, 'w') as devnull:
            subprocess.check_call([sys.executable, "-m", "pip", "--version"], stdout=devnull, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        return False
    return True
def intpip(pip_args=str):
    '''CSlib: Function to use pip from inside python, this function should also install pip if needed (Experimental)
    Returns: bool representing success or not'''
    if not _check_pip():
        print("PIP not found. Installing pip...")
        get_pip_script = "https://bootstrap.pypa.io/get-pip.py"
        try:
            subprocess.check_call([sys.executable, "-m", "ensurepip"])
        except subprocess.CalledProcessError:
            print("Failed to install pip using ensurepip. Aborting.")
            return False
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        except subprocess.CalledProcessError:
            print("Failed to upgrade pip. Aborting.")
            return False
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", get_pip_script])
        except subprocess.CalledProcessError:
            print("Failed to install pip using get-pip.py. Aborting.")
            return False
        print("PIP installed successfully.")
    try:
        subprocess.check_call([sys.executable, "-m", "pip"] + pip_args.split())
        return True
    except subprocess.CalledProcessError:
        print(f"Failed to execute pip command: {pip_args}")
        return False

# Safe import function
def autopipImport(moduleName=str,pipName=None,addPipArgsStr=None,cusPip=None,relaunch=False,relaunchCmds=None):
    '''CSlib: Tries to import the module, if failed installes using intpip and tries again.'''
    try:
        imported_module = importlib.import_module(moduleName)
    except:
        if pipName != None:
            command = f"install {pipName}"
        else:
            command = f"install {moduleName}"
        if addPipArgsStr != None:
            if not addPipArgsStr.startswith(" "):
                addPipArgsStr = " " + addPipArgsStr
            command += addPipArgsStr
        if cusPip != None:
            os.system(f"{cusPip} {command}")
        else:
            intpip(command)
        if relaunch == True and relaunchCmds != None:
            print("Relaunching to attempt reload of path...")
            subprocess.run(*relaunchCmds)
        else:
            imported_module = importlib.import_module(moduleName)
    return imported_module
