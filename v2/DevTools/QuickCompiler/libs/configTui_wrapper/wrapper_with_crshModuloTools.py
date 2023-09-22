import os

import sys
import subprocess
import importlib

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
def autopipImport(moduleName=str,pipName=None,addPipArgsStr=None):
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
        intpip(command)
        imported_module = importlib.import_module(moduleName)
    return imported_module

# Function to load a module from path
def fromPath(path):
    '''CSlib: Import a module from a path.'''
    path = path.replace("\\",os.sep)
    spec = importlib.util.spec_from_file_location("module", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

_ = autopipImport("ruamel.yaml")
_ = autopipImport("textual")
_ = autopipImport("argparse")
_ = autopipImport("rich")

def configTui_WrapperMain(file):
    parent = os.path.abspath(os.path.dirname(__file__))
    configUi_app = os.path.join(parent,f"..{os.sep}Prudhvi-pln_configTUI{os.sep}config-tui.py")
    os.system(f"{sys.executable} {configUi_app} -i {file}")