# import
import os,platform,subprocess,json,getpass
from datetime import datetime

# launcherDirGet
def getLauncherDir(preset=None):
    if preset is not None:
        return preset
    else:
        user = getpass.getuser()
        system = platform.system().lower()
        if system == "windows":
            return f"C:\\Users\\{user}\\AppData\\Roaming\\.minecraft"
        elif system == "darwin":  # macOS
            return f"~/Library/Application Support/minecraft"
        elif system == "linux":
            return f"~/.minecraft"
        else:
            raise ValueError("Unsupported operating system")

# terminateMc
def terminateMC(excProcNameList=None):
    import psutil
    # Get a list of all running processes
    for process in psutil.process_iter(['pid', 'name']):
        try:
            process_name = process.info['name']
            valid = True
            if excProcNameList != None:
                if process_name.lower() in excProcNameList:
                    valid = False
            # Check if the process name contains "Minecraft"
            if 'minecraft' in process_name.lower() and valid == True:
                # Terminate the process
                pid = process.info['pid']
                psutil.Process(pid).terminate()
                print(f"Terminated process '{process_name}' with PID {pid}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass  # Handle exceptions if necessary

# Check if a command exists
def check_command_exists(command):
    try:
        subprocess.check_output([command, '--version'], stderr=subprocess.STDOUT, shell=True, text=True)
        return True
    except subprocess.CalledProcessError:
        return False

# Launch appxLauncher if avaliable
def check_and_launch_appxMinecraftLauncher():
    # Check if the OS is Windows
    if platform.system().lower() != 'windows':
        return False
    # Check if "pwsh" or "powershell" command is available
    if check_command_exists("pwsh"):
        powershell_command = "pwsh"
    elif check_command_exists("powershell"):
        powershell_command = "powershell"
    else:
        return False
    # Check if "get-appxpackage" command is available inside PowerShell
    ps_script = """
    $result = Get-Command -Name "get-appxpackage" -ErrorAction SilentlyContinue
    if ($result -ne $null) {
        $familyName = (Get-AppxPackage -Name "Microsoft.4297127D64EC6").PackageFamilyName
        try {
            iex('Start-Process shell:AppsFolder\\' + $familyName + '!Minecraft')
        }
        catch {
            Write-Host "Error: $_"
            exit 1
        }
    }
    """
    # Execute the PowerShell script and capture the return code
    try:
        subprocess.check_call([powershell_command, "-Command", ps_script])
        return True  # Return True if the script executes successfully
    except subprocess.CalledProcessError as e:
        print(f"PowerShell script execution failed with exit code {e.returncode}.")
        return False  # Return False if the script fails

def pause():
    '''Pauses the terminal (Waits for input)
    ConUtils is dependent on platform commands so this might not work everywere :/'''
    # Get platform
    platformv = platform.system()
    # Linux using resize
    if platformv == "Linux":
        os.system(f"read -p ''")
    # Mac using resize
    elif platformv == "Darwin":
        os.system(f"read -n 1 -s -r -p ''")
    # Windows using PAUSE
    elif platformv == "Windows":
        os.system("PAUSE > nul")
    # Error message if platform isn't supported
    else:
        raise Exception(f"Error: Platform {platformv} not supported yet!")

def get_current_datetime_mcpformat():
    current_datetime = datetime.utcnow()
    formatted_datetime = current_datetime.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    return formatted_datetime

def get_current_datetime_logformat():
    current_datetime = datetime.utcnow()
    formatted_datetime = current_datetime.strftime('%d_%m_%Y %H-%M-%S')
    return formatted_datetime

# Main function
def MinecraftLauncherAgent(
    #Minecraft Launcher Agent
    #This function helps to add/remove/list or replace minecraft launcher installs.
    #
    #Made by Simon Kalmi Claesson
    #Version:  2023-09-25(1) 2.1 PY
    #

    # [Arguments]
    ## extra
    prefix="",
    encoding="utf-8",
    ## Options
    startLauncher=False,
    suppressMsgs=False,
    dontkill=False,

    ## Prio inputs
    add=False,
    remove=False,
    list=False,
    get=False,
    replace=False,

    ## Later inputs
    oldInstall=str,
    gameDir=str,
    icon=str,
    versionId=str,
    name=str,
    overWriteLoc=str,
    overWriteFile=str,
    overWriteBinExe=str,

    ## extraAdditions
    dontbreak=False,
    excProcNameList=None
):
    # [Setup]
    ## Variables
    doExitOnMsg = False
    doPause = False
    toReturn = None
    system = platform.system().lower()
    ## DontBreak
    if dontbreak == True:
        doExitOnMsg = False

    ## Presets
    defa_MCFolderLoc = getLauncherDir()
    defa_MCProfFileN = "launcher_profiles.json"
    backupFolderName = ".installAgentBackups"
    familyName = "Microsoft.4297127D64EC6_8wekyb3d8bbwe"
    binlaunchdir = "C:\\Program Files (x86)\\Minecraft Launcher\\MinecraftLauncher.exe"
    if overWriteBinExe != None and overWriteBinExe != str:
        binlaunchdir = overWriteBinExe
    opHasRun = False
    returnPath = os.getcwd()

    ## Text
    #Text
    text_MissingParam = "You have not supplied one or more of the required parameters for this action!"
    text_NoLauncher = "No launcher found! (Wont auto start)"
    text_OPhasRun = "Operation has been run."

    # Kill launcher
    if dontkill != True:
        # Non windows dont kill
        if system != "windows":
            print(prefix+"Non-windows platform identified, won't kill launcher.")
            _ = input(prefix+"Kill the minecraft/launcher processes manually and then press ENTER to continue...")
        # kill
        terminateMC(excProcNameList)

    # [Add]
    if add == True:
        # missing params
        if gameDir == None or versionId == None or name == None:
            if suppressMsgs != True:
                print(prefix+text_MissingParam)
            if doPause == True:
                pause()
            if dontbreak != True:
                if doExitOnMsg == True: exit()
                else: return
        # overwrite
        loc = defa_MCFolderLoc
        file = defa_MCProfFileN
        if overWriteLoc != None and overWriteLoc != str:
            loc = overWriteLoc
        if overWriteFile != None and overWriteFile != str:
            file = overWriteFile

        # get file content and change to dict
        os.chdir(loc)
        jsonFile = open(file,'r',encoding=encoding).read()
        _dict = json.loads(jsonFile)
        profiles = _dict.get("profiles")
        if profiles == None: profiles = {}

        # create template profile
        template = {
            "created": get_current_datetime_mcpformat(),
            "gameDir": gameDir,
            "icon": icon,
            "lastVersionId": versionId,
            "name": name,
            "type": "custom"
        }

        # create temporary vars and fix add profile to data
        newProfiles = profiles.copy()
        newProfiles[template['name']] = template
        newDict = _dict.copy()
        newDict["profiles"] = newProfiles
        # convert to JSON
        endJson = json.dumps(newDict)
        
        #Prep Backup
        newFileName = "(" + get_current_datetime_logformat() + ")" + file
        newFileName = newFileName.replace("/","_")
        newFileName = newFileName.replace(":","-")
        #Backup
        if os.path.exists(backupFolderName) != True:
            os.mkdir(backupFolderName)
        cl = os.getcwd()
        if system == "windows":
            newFilePath = os.path.join(".\\",backupFolderName,newFileName)
        else:
            newFilePath = os.path.join("./",backupFolderName,newFileName)
        open(newFilePath,'w',encoding=encoding).write(jsonFile)

        # Replace content in org file
        open(file,'w',encoding=encoding).write(endJson)

        #Done
        if suppressMsgs != True:
            print(prefix+text_OPhasRun)
            os.chdir(returnPath)
            if startLauncher == True:
                succed = check_and_launch_appxMinecraftLauncher()
                if succed == False:
                    if os.path.exists(binlaunchdir):
                        os.system(binlaunchdir)
                    else:
                        print(prefix+text_NoLauncher)
        opHasRun = True

    # Remove install
    elif remove == True:
        # missing params
        if name == None:
            if suppressMsgs != True:
                print(prefix+text_MissingParam)
            if doPause == True:
                pause()
            if dontbreak != True:
                if doExitOnMsg == True: exit()
                else: return
        # overwrite
        loc = defa_MCFolderLoc
        file = defa_MCProfFileN
        if overWriteLoc != None and overWriteLoc != str:
            loc = overWriteLoc
        if overWriteFile != None and overWriteFile != str:
            file = overWriteFile

        # get file content and change to dict
        os.chdir(loc)
        jsonFile = open(file,'r',encoding=encoding).read()
        _dict = json.loads(jsonFile)
        profiles = _dict.get("profiles")
        if profiles == None: profiles = {}

        # create temporary vars and fix add profile to data
        newProfiles = profiles.copy()
        if newProfiles.get(name) != None:
            newProfiles.pop(name)
        newDict = _dict.copy()
        newDict["profiles"] = newProfiles

        # convert to JSON
        endJson = json.dumps(newDict)
        
        #Prep Backup
        newFileName = "(" + get_current_datetime_logformat() + ")" + file
        newFileName = newFileName.replace("/","_")
        newFileName = newFileName.replace(":","-")
        #Backup
        if os.path.exists(backupFolderName) != True:
            os.mkdir(backupFolderName)
        cl = os.getcwd()
        system
        if system == "windows":
            newFilePath = os.path.join(".\\",backupFolderName,newFileName)
        else:
            newFilePath = os.path.join("./",backupFolderName,newFileName)
        open(newFilePath,'w',encoding=encoding).write(jsonFile)

        # Replace content in org file
        open(file,'w',encoding=encoding).write(endJson)

        #Done
        if suppressMsgs != True:
            print(prefix+text_OPhasRun)
            os.chdir(returnPath)
            if startLauncher == True:
                succed = check_and_launch_appxMinecraftLauncher()
                if succed == False:
                    if os.path.exists(binlaunchdir):
                        os.system(binlaunchdir)
                    else:
                        print(prefix+text_NoLauncher)
        opHasRun = True

    # List profiles
    elif list == True:
        # overwrite
        loc = defa_MCFolderLoc
        file = defa_MCProfFileN
        if overWriteLoc != None and overWriteLoc != str:
            loc = overWriteLoc
        if overWriteFile != None and overWriteFile != str:
            file = overWriteFile
            
        # get file content and change to dict
        os.chdir(loc)
        jsonFile = open(file,'r',encoding=encoding).read()
        _dict = json.loads(jsonFile)
        profiles = _dict.get("profiles")
        if profiles == None: profiles = {}

        print('\n'.join([key for key in profiles.keys()]))

        #Done
        if suppressMsgs != True:
            print(prefix+text_OPhasRun)
            os.chdir(returnPath)
            if startLauncher == True:
                succed = check_and_launch_appxMinecraftLauncher()
                if succed == False:
                    if os.path.exists(binlaunchdir):
                        os.system(binlaunchdir)
                    else:
                        print(prefix+text_NoLauncher)
        opHasRun = True

    # Get profiles
    elif get == True:
        # overwrite
        loc = defa_MCFolderLoc
        file = defa_MCProfFileN
        if overWriteLoc != None and overWriteLoc != str:
            loc = overWriteLoc
        if overWriteFile != None and overWriteFile != str:
            file = overWriteFile
            
        # get file content and change to dict
        os.chdir(loc)
        jsonFile = open(file,'r',encoding=encoding).read()
        _dict = json.loads(jsonFile)
        profiles = _dict.get("profiles")
        if profiles == None: profiles = {}

        toReturn = profiles

        #Done
        if suppressMsgs != True:
            print(prefix+text_OPhasRun)
            os.chdir(returnPath)
            if startLauncher == True:
                succed = check_and_launch_appxMinecraftLauncher()
                if succed == False:
                    if os.path.exists(binlaunchdir):
                        os.system(binlaunchdir)
                    else:
                        print(prefix+text_NoLauncher)
        opHasRun = True
    
    # Replace profiles
    elif replace == True:
        # missing params
        if oldInstall == None or gameDir == None or versionId == None or name == None:
            if suppressMsgs != True:
                print(prefix+text_MissingParam)
            if doPause == True:
                pause()
            if dontbreak != True:
                if doExitOnMsg == True: exit()
                else: return
        # overwrite
        loc = defa_MCFolderLoc
        file = defa_MCProfFileN
        if overWriteLoc != None and overWriteLoc != str:
            loc = overWriteLoc
        if overWriteFile != None and overWriteFile != str:
            file = overWriteFile

        # get file content and change to dict
        os.chdir(loc)
        jsonFile = open(file,'r',encoding=encoding).read()
        _dict = json.loads(jsonFile)
        profiles = _dict.get("profiles")
        if profiles == None: profiles = {}

        # create template profile
        template = {
            "created": get_current_datetime_mcpformat(),
            "gameDir": gameDir,
            "icon": icon,
            "lastVersionId": versionId,
            "name": name,
            "type": "custom"
        }

        # create temporary vars and fix add profile to data
        newProfiles = profiles.copy()
        newProfiles[oldInstall] = template
        newDict = _dict.copy()
        newDict["profiles"] = newProfiles
        # convert to JSON
        endJson = json.dumps(newDict)
        
        #Prep Backup
        newFileName = "(" + get_current_datetime_logformat() + ")" + file
        newFileName = newFileName.replace("/","_")
        newFileName = newFileName.replace(":","-")
        #Backup
        if os.path.exists(backupFolderName) != True:
            os.mkdir(backupFolderName)
        cl = os.getcwd()
        if system == "windows":
            newFilePath = os.path.join(".\\",backupFolderName,newFileName)
        else:
            newFilePath = os.path.join("./",backupFolderName,newFileName)
        open(newFilePath,'w',encoding=encoding).write(jsonFile)

        # Replace content in org file
        open(file,'w',encoding=encoding).write(endJson)

        #Done
        if suppressMsgs != True:
            print(prefix+text_OPhasRun)
            os.chdir(returnPath)
            if startLauncher == True:
                succed = check_and_launch_appxMinecraftLauncher()
                if succed == False:
                    if os.path.exists(binlaunchdir):
                        os.system(binlaunchdir)
                    else:
                        print(prefix+text_NoLauncher)
        opHasRun = True

    # If no param is given show help
    if opHasRun != True: 
        print(prefix+"MinecraftLauncher InstallAgent (GameInstalls)")
    
    # Go return path
    os.chdir(returnPath)

    # return content
    if toReturn != None: return toReturn