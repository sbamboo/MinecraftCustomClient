import os, json, sys, subprocess, platform

# Ensure importlib.util
try:
    import importlib
    _ = getattr(importlib,"util")
except AttributeError:
    from importlib import util as ua
    setattr(importlib,"util",ua)
    del ua


# Python
def getExecutingPython() -> str:
    '''Returns the path to the python-executable used to start crosshell'''
    return sys.executable

def _check_pip(pipOvw=None) -> bool:
    '''Checks if PIP is present'''
    if pipOvw != None and os.path.exists(pipOvw): pipPath = pipOvw
    else: pipPath = getExecutingPython()
    try:
        with open(os.devnull, 'w') as devnull:
            subprocess.check_call([pipPath, "-m", "pip", "--version"], stdout=devnull, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        return False
    return True

def intpip(pip_args=str,pipOvw=None,pipMuteCommand=False,pipMuteEnsure=False):
    """Function to use pip from inside python, this function should also install pip if needed (Experimental)
    Returns: bool representing success or not
    
    NOTE! Might need --yes in args when using mute!"""

    if pipMuteCommand == True:
        subprocessParamsCommand = { "stdout":subprocess.DEVNULL, "stderr":subprocess.DEVNULL }
    else:
        subprocessParamsCommand = {}

    if pipMuteEnsure == True:
        subprocessParamsEnsure = { "stdout":subprocess.DEVNULL, "stderr":subprocess.DEVNULL }
    else:
        subprocessParamsEnsure = {}

    if pipOvw != None and os.path.exists(pipOvw): pipPath = pipOvw
    else: pipPath = getExecutingPython()
    if not _check_pip(pipOvw):
        print("PIP not found. Installing pip...")
        get_pip_script = "https://bootstrap.pypa.io/get-pip.py"
        try:
            subprocess.check_call([pipPath, "-m", "ensurepip"],**subprocessParamsEnsure)
        except subprocess.CalledProcessError:
            print("Failed to install pip using ensurepip. Aborting.")
            return False
        try:
            subprocess.check_call([pipPath, "-m", "pip", "install", "--upgrade", "pip"],**subprocessParamsEnsure)
        except subprocess.CalledProcessError:
            print("Failed to upgrade pip. Aborting.")
            return False
        try:
            subprocess.check_call([pipPath, "-m", "pip", "install", get_pip_script],**subprocessParamsEnsure)
        except subprocess.CalledProcessError:
            print("Failed to install pip using get-pip.py. Aborting.")
            return False
        print("PIP installed successfully.")
    try:
        subprocess.check_call([pipPath, "-m", "pip"] + pip_args.split(),**subprocessParamsCommand)
        return True
    except subprocess.CalledProcessError:
        print(f"Failed to execute pip command: {pip_args}")
        return False

# Safe import function
def autopipImport(moduleName=str,pipName=None,addPipArgsStr=None,cusPip=None,attr=None,relaunch=False,relaunchCmds=None,intpip_muteCommand=False,intpipt_mutePipEnsure=False):
    '''Tries to import the module, if failed installes using intpip and tries again.'''
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
            #os.system(f"{cusPip} {command}")
            intpip(command,pipOvw=cusPip, pipMuteCommand=intpip_muteCommand,pipMuteEnsure=intpipt_mutePipEnsure)
        else:
            intpip(command, pipMuteCommand=intpip_muteCommand,pipMuteEnsure=intpipt_mutePipEnsure)
        if relaunch == True and relaunchCmds != None and "--noPipReload" not in relaunchCmds:
            relaunchCmds.append("--noPipReload")
            if "python" not in relaunchCmds[0] and isPythonRuntime(relaunchCmds[0]) == False:
                relaunchCmds = [getExecutingPython(), *relaunchCmds]
            print("Relaunching to attempt reload of path...")
            print(f"With args:\n    {relaunchCmds}")
            subprocess.run([*relaunchCmds])
        else:
            imported_module = importlib.import_module(moduleName)
    if attr != None:
        return getattr(imported_module, attr)
    else:
        return imported_module

# Function to load a module from path
def fromPath(path, globals_dict=None):
    '''Import a module from a path. (Returns <module>)'''
    path = path.replace("/",os.sep).replace("\\",os.sep)
    spec = importlib.util.spec_from_file_location("module", path)
    module = importlib.util.module_from_spec(spec)
    if globals_dict:
        module.__dict__.update(globals_dict)
    spec.loader.exec_module(module)
    return module

def fromPathAA(path, globals_dict=None):
    '''Import a module from a path, to be used as: globals().update(fromPathAA(<path>)) (Returns <module>.__dict__)'''
    path = path.replace("/",os.sep).replace("\\",os.sep)
    spec = importlib.util.spec_from_file_location("module", path)
    module = importlib.util.module_from_spec(spec)
    if globals_dict:
        module.__dict__.update(globals_dict)
    spec.loader.exec_module(module)
    return module.__dict__

def installPipDeps(depsFile,encoding="utf-8",tagMapping=dict):
    '''Note! This takes a json file with a "deps" key, the fd function takes a deps list!'''
    deps = json.loads(open(depsFile,'r',encoding=encoding).read())["deps"]
    for dep in deps:
        for key,val in dep.items():
            for tag,tagVal in tagMapping.items():
                dep[key] = val.replace("{"+tag+"}",tagVal)
            _ = autopipImport(**dep)
    
def installPipDeps_fl(deps=list,tagMapping=dict):
    '''Note! This takes a deps list, the file function takes a json with a "deps" key!'''
    for dep in deps:
        for key,val in dep.items():
            for tag,tagVal in tagMapping.items():
                dep[key] = val.replace("{"+tag+"}",tagVal)
            _ = autopipImport(**dep)
    
def isPythonRuntime(filepath=str(),cusPip=None):
    exeFileEnds = [".exe"]
    if os.path.exists(filepath):
        try:
            # [Code]
            # Non Windows
            if platform.system() != "Windows":
                try:
                    magic = importlib.import_module("magic")
                except:
                    command = "install magic"
                    if cusPip != None:
                        #os.system(f"{cusPip} {command}")
                        intpip(command,pipOvw=cusPip)
                    else:
                        intpip(command)
                    magic = importlib.import_module("magic")
                detected = magic.detect_from_filename(filepath)
                return "application" in str(detected.mime_type)
            # Windows
            else:
                fending = str("." +''.join(filepath.split('.')[-1]))
                if fending in exeFileEnds:
                    return True
                else:
                    return False
        except Exception as e: print("\033[31mAn error occurred!\033[0m",e)
    else:
        raise Exception(f"File not found: {filepath}")