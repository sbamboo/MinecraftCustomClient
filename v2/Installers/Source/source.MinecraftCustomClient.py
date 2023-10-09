# This is the big installer who shows and installes from repositories

# [Settings]
installer_version = "1.1"
installer_release = "2023-10-07(0)"
prefix    = "\033[90m[\033[35mInstaller\033[90m]\033[0m "
prefix_dl = "\033[90m[\033[34mDown-List\033[90m]\033[0m "
prefix_jv = "\033[90m[\033[33mJava-Inst\033[90m]\033[0m "
prefix_la = "\033[90m[\033[94mLnch-Agnt\033[90m]\033[0m "
title = f"MinecraftCustomClient - Installer {installer_version}: <modpack>"
temp_foldername = "MCC_Installer_Temp"

win_java_url = "https://aka.ms/download-jdk/microsoft-jdk-17.0.8.1-windows-x64.zip"
lnx_java_url = "https://aka.ms/download-jdk/microsoft-jdk-17.0.8.1-linux-x64.tar.gz"
mac_java_url = "https://aka.ms/download-jdk/microsoft-jdk-17.0.8.1-macOS-x64.tar.gz"

fabric_url = "https://maven.fabricmc.net/net/fabricmc/fabric-installer/0.11.2/fabric-installer-0.11.2.jar"
forge_url  = "https://files.minecraftforge.net/net/minecraftforge/forge"
forForgeList = "https://raw.githubusercontent.com/sbamboo/MinecraftCustomClient/main/v2/Installers/Assets/forge-links.json"

legacy_repo_url = "https://raw.githubusercontent.com/sbamboo/MinecraftCustomClient/main/v1_legacy/Repo/MinecraftCustomClient_flavors.json"

icon_base64_icon128 = "data:image/png;base64,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"
icon_base64_legacy  = "data:image/png;base64,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"
icon_base64_modded  = "data:image/png;base64,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"
icon_base64_default = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAYAAADDPmHLAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADr8AAA6/ATgFUyQAAAt8SURBVHhe7Z3JsyRVFcbrGdFMAs6uDGdUBgW6QUYR2lkxwsCN84iACqiITH8A8yiooIjjFsOFG0UbkLmhG5DJ2ZU7FW1owN6053e6sjyVL6syX+a952ZV3l/E56sT0q8y8/vuqay8+fKu7By95Vej0ehdojZsFZ0mup9iZfQ7fmQiI56NX43WiS4Una3V2rmFAOwcF23ZIvqiKIfAAWP+biLM/7pWLXne+GcXNoi+LTqMwmxgJjChzYcQAQDM/874Zw5BBErmXyTqbD6ECgBgPp2AjpBDEBBzLHcXXSw6S6sAhAwAHC6iE+QQBKJkPiP/a1oFInQAgBDQCdZT5BC0p2LkBzUfYgQA3iqiE+QQtMQcsz1EmP9VrQITKwBACOgEh1LkEDTHy3yIGQA4QkQnOIQih6CekvmXiL6iVSRiBwByCBpijs2eIsw/U6uIeAQAjhQRgoMpcghWk8J88AoA5BDMoML8M7RywDMAcJSIE0Pd4xyCqWOwl+hSkZv54B0AOFpEJxh8CCrMP10rR1IEAAgBneDNFEMMQYX5X9bKGQKweddLd44R0QkGFwKzr88XXSZKYr6wgwB8SaRz+QkgBHSCgyiGEIIK8zn+KdghuoAATN3QkYBjRXSCpQ9Bhfkc9xRg/vmiK4pzAEJAEh/Qyh9CQCc4kGIZQ2D2aW/R5aLU5l9JscL/mI2burEjAXeIODCPUSzL7WUl8xn53EeZgv+KMP8qCo6vBgDMRk7N6SfgtyJC8DjFooegYuSfqpU/mH+e6GqK4rhOvgaaA825AAbwsZCC40R8HBxAYQ7gwmG2fR/RFaJemQ+TDlBgNnpqTj8Bt4sI4hMUi9YJSuYz8k/Ryp/nRJh/DUX5OK4KAJRCcL1I5/RjcNtG3mI2x2/aTCdYqBCY47ev7N9/xq8rkf0bv4oC5p8r+iZF1fGbfARYzH/I1jEKH9QqDXwcvIkX5sD2Fmu+iJGfilrzoTIAYP7BfSJC8JBW/hwvWogQlMznM/8LWvnzrOgc0VzzYWYAoEchOEFECN5I0ccQmG16gYjv2Cdr5Q/mM/KvpZhnPswNAJhfcK+Ii0UPa+VPb0NQMp+R/3mt/ClGfiPzoTYAYH7RPSI6QaoQbBQRgjdQ9CEEFSM/lfnPiL4huo6iifnQKABQCgGdoNk7hKc3ITDv/UIR5n9OK38wn5H/LYqm5kPjAID5xXeL6ASpQvAOETu7H0WKEPTI/O0iRv6azYfK6wCWWzeePPfPx+V77CPyQ+f021B3HaAOeX86wZ94vdadb4s1X7b/yfHrVnS8DrBd3p+ZxZmcsOnGuR6vqQPMgE5ACFJB8l/PC49OUBr5OqmSiGLkdyJEAO4ScU7wqFb+8HQTzgmih6BkPtfVP6OVP0+LeCoIl+o7ESIAcKeITpAyBHSC11HECIH5nS8SYf6ntfIH8xn5XKLvTOcAmM9dQkAn0Ln8BLxbRCcIHoKemc/IV/NDnPME6QBmQ6Zu6EgAIaATvJYiRAjM73ixiBm1T2nlz1MizL+BItQJb6iPgHII6AR6Q0cC3iMKEoKS+Yz8T2rlTxTzIVgAwGwYd/WkDMF7RYTgNRRtQmD+zUtEjPyU5vM8oO9ShDQfOl8HqEO+5zKXv/+uau0EuE5AJ/gbr5sePGu+vP8/xq9b0fF7/jZ5f2YWW+NxHaAOOoHe0JEIOsGredGkE1SM/FRsEwV5Etg8PAJwm4gQ/F4rf94nahQC8/+9VMRc+se18oe7iHgS2I1aRcQjAJA6BO8XEYJXUVSFoGQ+I/9jWvmD+Yz872sVmegBMJ+7t4oIwR+08mdmCMzrl4kY+SnNZ+Sr+aFP+Kpw6QA9CsEHRMyXv5IC40vmM/I/qpU//xZh/k0UHuaD10eA3aFNIv4a9o9a+XOiiE6gIRhTjPxBmQ9uAQCzY78R0QlShoBOwFcsHrmO+R8RpYDpZB4A+QMKT/Oh9jpAHQGuEzCXrzd2tKHuOkHN93DWSuCvZj6oVQUdf38dT8rvZ36hNXXf8+tw7QAzoBPoDR0JYO5gpvmRKUZ+UvoQgF+LOCf4s1b+dF0wow3/EmH+j7RKSB8CALeI6AQpQtD5Y3CN9MZ8SB4Ac9JDCOgEf9FqOfmniOf+/pjC+4Svil50AHMgOClb1hBgPiP/JxR9MB/68hFgD8gvRYTgr1otB8XI75X50JsAwJKGgOlkzP8pRZ/Mh+gnQHXXCfY9/UPjV8Nk23U/H7+qpuv3/Dp61QEy/uQADJwcgIGTAzBwcgAGTg7AwMkBGDjeEyGr2PKzX6SYjesNG046MakHuQMMnByAgZMDMHByAAZODsDAyQEYODkAAyf5dYD9RxvnXge46eZui2mu+zt/dNOelVe8fPyqHZ84SddmmskTo035OkAmHTkAAycHYODkAAycHICBkzQA9ikdQyX1MUgWgGz+/0l5LJJ8BzU7vN/Wm89K9ZCIZqzwzKgO7Jz/mMH1H76S5wPoxYoUfzTi3gGM+Sz0wMOdhw5Xinj8fJJO4BqACvPfqdWw+ayIlcZYdMo9BG4BMDvGsm8sdMC6P5ldsN4QncA9BC4BKJnPyGflr8w0hMC9E0QPgNkRln5l5GfzZ8Oag4RAHxDtEYKoASiZz8hn9c/MfFxDEC0AZsN5VDwjP5vfHNYdZuXx6CGIEoCS+Yx8VgBfTPge30XtYeVxQrAPRawQBA+A2dADRIz8xTU/PdFDEDQAJfMZ+W/XKtOFU0SEYG+K0CEIFgCzYQeKGPnZ/HBEC0GQAFSYf5xWmZCcKrpMFDQEnQNgNuQgEea/TatMDE4TEQJdMDpECDoFIJufhKAhaB0A88YsHY/5x2qV8YDVWYOEoNX9ABXmH6OVP9xLwAMleeK423y62X9WD2cSp9Mz/zvANy0Wkn6Gos3+rzkAZud5wQakNJ8njLP6iPvNFKUQXCXSOf0EsPzNOaJWIVjTR0DJ/JQjn0WnkpkP5j1/KGK9n25/gtQeOuClor0ojEeNaNwBzC8+WMTIP1orfwrzWXwqifkWc1ym5vQTwBpIdIJnKZoel0YBKJnPyD9KK39YeBLzWX4uufkFPQrBtaJzRY1DUPsRYHbuENH1omx+CbMtLPvGqp8sAJmCM0SXiPakMN7NZG4HKJnPyD9SK39YfBrzWYK2V+ZbzPFiTp9O0Gnl7w6wDB6d4DmKecdrZgcwO3OoiJGfza/BbBtLv9IJWAE8BWeK6AR7UMzrBJUBMP9gvYiRf4RW/jwu4qJH780vMNvIyt9ni57Syh9CcLFobghWfQRUmD9/5cR4YD4j/3aKRTDfYo4jc/rc4qVz+gm4WnSeiAUyVx3HqQ5gNnqDKKX5j4kY+QtpPpht/p4oZSdguRo6we4U5U4w6QAV5h+ulT+F+XdQLKL5FnNcmc6dzOkngKuV54umOoF2ALORh4lSmv+oaGnMB7MPN4joBE9r5Q9L1l0k2o2i8Hylwnx+pqAw/06KZTDfYo5zMZ2bqhPw9ZROsIOiOAdgxKc0/xHR0poPZp/4Ss0M3nat/GHe4kKRdgICkM13okch4BoFIVjHR8AWecFXvhRwRPiqdxfFMptvMR8H7DszeXpjRwIuJwCpFmzAbUb+3RRDMb+gFALOCXQ615vKK4EOPCwarPlg9pmp9ckNHd6kCMDgzS8w+z51V48n3gF4SIT591AM2fyCUggmc/leeAYgmz8Dcyy4q8c1BF4BeFDEBZB7KbL5qzHHpLirR+fyY+MRAMxn5N9Hkc2fTYoQxA7AVhEjP5vfEHOMpu7qiUXMAHCBiZG/mSKb35xSCCZz+TGIFYBsfkfMMbtGFC0EMQLwgAjz76fI5rfHHLupu3pCEjoA2fzAlEIwmcYNRcgAYDrmE4JsfkDMsSzu6gkWglAByOZHxhzTqRs6uhIiAJzoYT4nftn8iJRCcIGoYwhGo/8B8jQywGfvp+kAAAAASUVORK5CYII="

repo_url = "https://raw.githubusercontent.com/sbamboo/MinecraftCustomClient/main/v2/Repo/repo.json"

#region [IncludeInline: ./assets/lib_crshpiptools.py]
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
def autopipImport(moduleName=str,pipName=None,addPipArgsStr=None,cusPip=None):
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
        imported_module = importlib.import_module(moduleName)
    return imported_module
#endregion [IncludeInline: ./assets/lib_crshpiptools.py]

# Handle cusPip
import sys,os
cusPip = None
for i,a in enumerate(sys.argv):
    if a == "-cusPip":
        try:
            cusPip = sys.argv[i+1]
        except: pass
if cusPip != None:
    if os.path.exists(cusPip):
        int_autopipImport = autopipImport
        def autopipImport(*args,**kwargs):
            int_autopipImport(*args,**kwargs,cusPip=cusPip)


# [Setup]
import requests,platform,os,sys,shutil,argparse,zipfile
import json,time
parent = os.path.abspath(os.path.dirname(__file__))

# Enable ansi on windows
os.system("")

# [Args]
encoding = "utf-8"
parser = argparse.ArgumentParser(description='MinecraftCustomClient QuickInstaller')
parser.add_argument('-enc', type=str, help='The file encoding to use')
parser.add_argument('--install', type=str, help='Action: Install')
parser.add_argument('-mcf','-cMinecraftLoc', dest="mcf", type=str, help='MinecraftFolder (.minecraft)')
parser.add_argument('-destination','-dest', dest="dest", type=str, help='Where should the client be installed?')
parser.add_argument('--fabprofile', help='Should fabric create a profile?', action="store_true")
parser.add_argument('--dontkill', help='Should the install not kill minecraft process?', action="store_true")
parser.add_argument('--autostart', help='Should the installer attempt to start the launcher?', action="store_true")
parser.add_argument('-cLnProfFileN', type=str, help='The filename to overwrite the profile-listing file with.')
parser.add_argument('-cLnBinPath', type=str, help='If autostart and no msstore launcher if found, overwrite launcher with this.')
#parser.add_argument('--curse', help='Should the installer attempt to install into curseforge instead?', action="store_true")
#parser.add_argument('-curseInstanceP', type=str, help='A custom path to curseforge/minecraft/Instances')
parser.add_argument('--rinth', help='Should the installer attempt to install into modrinth instead?', action="store_true")
parser.add_argument('-rinthInstanceP', type=str, help='A custom path to com.modrinth.theseus/profiles')
parser.add_argument('-excurse', type=str, help='Should the installer export to a curseforge pack instead of installing? (Takes a filepath to the zip to export to [non-existing])')
parser.add_argument('--excurse', dest="excurse_parent", help='Same as -excurse but takes no arguments and places in <parent>/<modpack>.zip', action="store_true")
parser.add_argument('--y', help='always answer with Yes', action="store_true")
parser.add_argument('--n', help='always answer with No', action="store_true")
parser.add_argument('-exprt', help='Exports a copy of the unpacked tempdata, takes the zip to export to. (its created so give path to non-existent file)', type=str)
parser.add_argument('-imprt', help='Imports a copy of the unpacked tempdata, takes the zip to import from.', type=str)
parser.add_argument('--nopause', help="Won't pause on exit/finish", action="store_true")
parser.add_argument('-modpack', type=str, help="Preselect modpack (str)")
parser.add_argument('-modpackFile', type=str, help="Forced custom modpack file (path)")
parser.add_argument('-cuspip', type=str, help="Custom pip binary path. (Advanced)")
args = parser.parse_args()
if args.enc:
    encoding = args.enc

#region [IncludeInline: ./partial@prep.py]
# [Functions]
def dummy():
    pass
try:
    oexit = exit
except:
    oexit = dummy

# Pause
def cli_pause(text=None):
    if text == None:
        text = ""
    # Get platform
    platformv = platform.system()
    # Linux using resize
    if platformv == "Linux":
        os.system(f"read -p '{text}'")
    # Mac using resize
    elif platformv == "Darwin":
        os.system(f"read -n 1 -s -r -p '{text}'")
    # Windows using PAUSE
    elif platformv == "Windows":
        print(text)
        os.system(f"PAUSE > nul")
    # Fix
    else:
        _ = input(text)

def exit(): 
    global args
    if args.nopause != True:
        cli_pause("Received exit, press any key to continue...")
    raise Exception('EXIT') #repl-exit


def cleanUp(tempFolder,modpack_path=None):
    try:
        if os.path.exists(tempFolder): shutil.rmtree(tempFolder)
    except:
        if os.path.exists(tempFolder):
            if platform.system() == "Windows":
                os.system(f'rmdir /s /q "{tempFolder}"')
            else:
                os.system(f'rm -rf "{tempFolder}"')
    if modpack_path != None:
        if os.path.exists(modpack_path): os.remove(modpack_path)

# ConUtils functions, note the lib is made by Simon Kalmi Claesson.
def setConTitle(title):
    '''ConUtils: Sets the console title on supported terminals (Input as string)
    ConUtils is dependent on platform commands so this might not work everywere :/'''
    # Get platform
    platformv = platform.system()
    # Linux using ANSI codes
    if platformv == "Linux":
        sys.stdout.write(f"\x1b]2;{title}\x07")
    # Mac not supported
    elif platformv == "Darwin":
        sys.stdout.write(f"\x1b]2;{title}\x07")
    # Windows using the title command
    elif platformv == "Windows":
        os.system(f'title {title}')
    # Error message if platform isn't supported
    else:
        raise Exception(f"Error: Platform {platformv} not supported yet!")

# [Pre Release softwere notice]
print(prefix+"\033[33mNote! This is pre-release software, the installer is provided AS-IS and i take no responsibility for issues that may arrise when using it.\nIf you wish to stop this script, close it now.\033[0m")
time.sleep(2)
#endregion [IncludeInline: ./partial@prep.py]

# [Set title]
setConTitle(title)

#region [IncludeInline: ./assets/ui_dict_selector.py]
import os
import sys
import readchar

# Function to clear the terminal screen
def clear_screen():
    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')

# Function to display the list of items
def display_items(selected_index, items, selkey, selTitle="Select an option:", selSuffix=None, dispWidth="vw", stripAnsi=False):
    # get dispWidth
    width,height = os.get_terminal_size()
    if dispWidth == "vw": dispWidth = width
    if dispWidth == "vh": dispWidth = height
    # clear screen (use function for os-indep)
    clear_screen()
    # get the length of the longest key
    max_key_length = max(len(key) for key in items.keys())
    # print
    if stripAnsi == True:
        print(selTitle)
    else:
        print("\x1b[0m"+selTitle) # include reset to fix wrong-coloring
    for i, key in enumerate(list(items.keys())):
        # get the org-value based on selkey
        if selkey == "" or selkey == None:
            ovalue = items[key]
        else:
            ovalue = items[key][selkey]
        if "ncb:" not in ovalue:
            value = "{" + ovalue + "}"
        else:
            value = ovalue.replace("ncb:","")
        # concat a string using left-adjusted keys
        string = f"  {key.ljust(max_key_length)}   {value}"
        # if over dispwidth cut with ... to correct size (indep of key-length)
        if len(string) > dispWidth-2:
            if "ncb:" not in ovalue:
                off = 10+max_key_length                                               # numerical amnt to cut (10 is what worked and the next is so it reacts on key-len)
                string = string.replace(value,ovalue[:dispWidth-off] + "...") # chn string based on cutoff
            else:
                off = 12+max_key_length                                               # numerical amnt to cut (12 is what worked and the next is so it reacts on key-len)
                string = string.replace(value,"{"+ovalue[:dispWidth-off] + "..."+"}") # chn string based on cutoff
        # print the string with formatting if enabeld
        if i == int(selected_index):
            string = ">" + string[1:] # add the >
            if stripAnsi == True:
                print(f"{string}")
            else:
                print(f"\x1b[32m{string}\x1b[0m")
        else:
            print(f"{string}")
    # print suffix msg
    if selSuffix != None:
        print(selSuffix)

# Function to get a single keypress
def get_keypress():
    return readchar.readchar()

# Function to get the up-key
def getup(keylow):
    if os.name == 'nt':
        return keylow == "h"
    else:
        return keylow == "a"

# Function to get the down-key
def getdown(keylow):
    if os.name == 'nt':
        return keylow == "p"
    else:
        return keylow == "b"

# Function to get the enter-key
def getent(keylow):
    if os.name == 'nt':
        return keylow == "\r"
    else:
        return keylow == "\n"

# Main function to show a dictionary based on the dict.value.<key> / or dict.value (if selkey = ""/None)
def showDictSel(nameDescDict=dict, selKey="desc", sti=0, selTitle="Select an option:", selSuffix=None, dispWidth="vw", stripAnsi=False):
    '''
    Add "ncb:" to your value to ommit the curly brackets.
    '''
    selected_index = sti # start index
    disp = True
    while True:
        # display the items if disp = True
        if disp == True:
            display_items(selected_index, nameDescDict, selKey, selTitle, selSuffix, dispWidth, stripAnsi)
        else:
            disp = True
        # check keys and change selected index depends on keys
        key = get_keypress()
        if getup(key.lower()):
            selected_index = selected_index - 1
            # roll-over
            if selected_index < 0: selected_index = len(nameDescDict)-1
        elif getdown(key.lower()):
            selected_index = selected_index + 1
            # roll-over
            if selected_index > len(nameDescDict)-1: selected_index = 0
        elif getent(key.lower()):
            return list(nameDescDict.keys())[selected_index]
        elif key.lower() == "q" or key.lower() == "\x1b":
            return None
        # if no key pressed set disp to false, so it wont redisp on an-uncaught key
        else:
            disp = False
#endregion [IncludeInline: ./assets/ui_dict_selector.py]

# [Show action select]
action_install = False
# show selector
selTitle  = "Welcome to MinecraftCustomClient!\nSelect the action you would like to do:"
selSuffix = "\033[90m\nUse your keyboard to select:\n↑ : Up\n↓ : Down\n↲ : Select (ENTER)\nq : Quit\n␛ : Quit (ESC)\033[0m"
if platform.system() == "Darwin":
    selSuffix = "\033[90m\nUse your keyboard to select:\na : Up\nb : Down\n↲ : Select (ENTER)\nq : Quit (ESC)"
actionsDict = {"[Install]":{"desc":"ncb:Runs the installer action."}}
actionsDict["[Exit]"] = {"desc": "ncb:"}
action = showDictSel(actionsDict,selTitle=selTitle,selSuffix=selSuffix)
if action == None or action not in list(actionsDict.keys()) or action == "[Exit]":
    args.nopause = True
    exit()
if args.install or action == "[Install]":
    action_install = True

# [Show repo]
if action_install == True:
    modpack_path = None
    if args.modpackFile:
        if os.path.exists(args.modpackFile):
            modpack_path = args.modpackFile
    if args.imprt:
        modpack_path = args.imprt
    elif modpack_path == None:
        # get repo
        try:
            repoContent = requests.get(repo_url).text
            repoData = json.loads(repoContent)
        except:
            print("Failed to get repository")
            exit()
        # show select
        flavors = repoData.get("flavors")
        flavorsDict = {}
        for fl in flavors:
            n = fl["name"]
            fl.pop("name")
            flavorsDict[n] = fl
        flavorsDict["[Exit]"] = {"desc": "ncb:"}
        # show os-dep keybinds:
        selTitle  = "Welcome to MinecraftCustomClient installer!\nSelect a flavor to install:"
        if args.modpack:
            key = args.modpack
        else:
            key = showDictSel(flavorsDict,selTitle=selTitle,selSuffix=selSuffix)
        if key == None or key not in list(flavorsDict.keys()) or key == "[Exit]":
            args.nopause = True
            exit()
        # get modpack url
        modpack_url = flavorsDict[key]["source"]
        # download url
        modpack_path = os.path.join(parent,os.path.basename(modpack_url))
        response = requests.get(modpack_url)
        if response.status_code == 200:
            # Content of the file
            cont = response.content
        else:
            cont = None
        if cont != None and cont != "":
            if os.path.exists(modpack_path) == False:
                open(modpack_path,'wb').write(cont)
        else:
            print(prefix+"Failed to get modpack!")
            exit()

    # [Prep selected package]
    modpack = os.path.basename(modpack_path)
    title = title.replace("<modpack>", modpack)
    system = platform.system().lower()

#region [IncludeInline: ./partial@installermain.py]
# [Code]

#region [IncludeInline: ./assets/lib_filesys.py]
# FileSys: Library to work with filesystems.
# Made by: Simon Kalmi Claesson

# Imports
import os
import shutil
import platform
try:
    from os import scandir
except ImportError:
    from scandir import scandir

# Simple alternative to conUtils
class altConUtils():
    def IsWindows():
        # Get platform and return boolean value depending of platform
        platformv = platform.system()
        if platformv == "Linux":
            return False
        elif platformv == "Darwin":
            return False
        elif platformv == "Windows":
            return True
        else:
            return False
    def IsLinux():
        # Get platform and return boolean value depending of platform
        platformv = platform.system()
        if platformv == "Linux":
            return True
        elif platformv == "Darwin":
            return False
        elif platformv == "Windows":
            return False
        else:
            return False
    def IsMacOS():
        # Get platform and return boolean value depending of platform
        platformv = platform.system()
        if platformv == "Linux":
            return False
        elif platformv == "Darwin":
            return True
        elif platformv == "Windows":
            return False
        else:
            return False

# Class containing functions
class filesys():

    defaultencoding = "utf-8"

    sep = os.sep

    # Help function
    def help(ret=False):
        helpText = '''
        This class contains functions to perform filessytem actions like creating and removing files/directories.
        Functions included are:
          - help: Shows this help message.
          - errorhandler: Internal function to handle errors. (Taking "action=<str_action>", "path=<str_path>" and "noexist=<bool>"
          - renameFile: Renames a file. (Taking "filepath=<str>", "newFilepath=<str>")
          - renameDir: Renames a directory. (Taking "folderpath=<str>", "newFolderpath=<str>")
          - doesExist: Checks if a file/directory exists. (Taking "path=<str>")
          - notExist: Checks if a file/directory does not exist. (Taking "path=<str>")
          - isFile: Checks if a object is a file. (Taking "path=<str>")
          - isDir: Checks if a object is a directory. (Taking "path=<str>")
          - getFileName: Returns the filename of the given file, excluding file extension. (Taking "path=<str>")
          - createFile: Creates a file. (Taking "filepath=<str>", "overwrite=<bool>" and "encoding=<encoding>")
          - createDir: Creates a directory. (Taking "folderpath=<str>")
          - deleteFile: Deletes a file. (Taking "filepath=<str>")
          - deleteDir: Deletes an empty directory. (Taking "folderpath=<str>")
          - deleteDirNE: Deletes a non empty directory, wrapping shutil.rmtree. (Taking "folderpath=<str>")
          - writeToFile: Writes to a file. (Taking "inputs=<str>", "filepath=<str>", "append=<bool>" and "encoding=<encoding>")
          - readFromFile: Gets the content of a file. (Taking "filepath=<str>" and "encoding=<encoding>")
          - getWorkingDir: Gets the current working directory.
          - setWorkingDir: Sets or changes the working directory. (Taking "dir=<str>")
          - copyFile: Wrapper around shutil.copy2. (Taking "sourcefile=<str>" and "destination=<str>")
          - copyFolder: Wrapper around shutil.copytree. (Taking "sourceDirectory=<str>" and "destinationDirectory=<str>")
          - copyFolder2: Custom recursive folder copy, destination may exists. (Taking "sourceDirectory=<str>", "destinationDirectory=<str>" and "debug=<bool>")
          - archive: Creates an archive of a folder. (Taking "sourceDirectory=<str>","<destination=<str>" and "format=<archive.format>") Note! Paths on on windows must be double slashed.
          - unArchive: Unpacks a archive into a folder. (Taking "archiveFile=<str>","<destination=<str>") Note! Paths on on windows must be double slashed.
          - scantree: Returns a generator, wrapps scantree. (Taking "path=<str>")
          - isExecutable: Checks if a file is an executable. (Taking "filepath=<str>" and optionally "fileEndings=<list>")
          - getMagicMime: Gets the magic-mime info of a file. (Taking "filepath=<str>")
          - openFolder: Opens a folder in the host's filemanager. (Taking "path=<str>") Might not work on al systems!
        For al functions taking encoding, the argument is an overwrite for the default encoding "filesys.defaultencoding" that is set to {filesys.defaultencoding}.
        '''
        if ret != True: print(helpText)
        else: return helpText

    def replaceSeps(path=str()):
        '''Replaces the path separators with os.sep'''
        spath = path
        if "/" in path:
            spath = path.replace("/", os.sep)
        if "\\" in path:
            spath = path.replace("\\", os.sep)
        return spath

    # Function to check if a file/directory exists
    def doesExist(path=str()):
        return bool(os.path.exists(path))
        
    # Function to check if a file/directory does not exist
    def notExist(path=str()):
        if os.path.exists(path): return False
        else: return True

    # Function to create a path, folder per folder
    def ensureDirPath(path=str()):
        '''Creates a path, folder per folder. DON'T INCLUDE FILES IN THE PATH'''
        path = filesys.replaceSeps(path)
        sections = path.split(os.sep)
        firstSection = sections[0]
        sections.pop(0)
        # Save cd then goto root
        curdir = filesys.getWorkingDir()
        filesys.setWorkingDir(f"{firstSection}{os.sep}")
        try:
            for section in sections:
                sectionpath = os.path.join(filesys.getWorkingDir(), section)
                if filesys.notExist(sectionpath):
                    filesys.createDir(sectionpath)
                filesys.setWorkingDir(sectionpath)
        except: pass
        filesys.setWorkingDir(curdir)

    # Function to check if object is file
    def isFile(path=str()):
        return bool(os.path.isfile(path))

    # Function to check if object is directory
    def isDir(path=str()):
        return bool(os.path.isdir(path))

    # Function to get the filename of file (Excluding file extension)
    def getFileName(path=str()):
        if "." in path:
            return ('.'.join(os.path.basename(path).split(".")[:-1])).strip(".")
        else:
            return os.path.basename(path)

    def getFileExtension(path=str()):
        if "." in path:
            return os.path.basename(path).split(".")[-1]
        else:
            return None

    # Error handler function where noexists flips functionality, checks for filetype and existance
    def errorHandler(action,path,noexist=False):
        output = True
        # Noexists checks
        if noexist:
            if filesys.doesExist(path):
                if action == "dir": output = f"\033[31mError: Directory already exists! ({path})\033[0m"
                if action == "file": output = f"\033[31mError: File already exists! ({path})\033[0m"
        else:
            if filesys.doesExist(path):
                # Directory
                if action == "dir":
                    if not filesys.isDir(path):
                        output = f"\033[31mError: Object is not directory. ({path})\033[0m"
                # Files
                elif action == "file":
                    if not filesys.isFile(path):
                        output = f"\033[31mError: Object is not file. ({path})\033[0m"
            # Not found
            else:
                if action == "folder": output = f"\033[31mError: Folder not found! ({path})\033[0m"
                if action == "file": output = f"\033[31mError: File not found! ({path})\033[0m"
        return output

    # Function to rename a file
    def renameFile(filepath=str(),newFilepath=str()):
        # Validate
        valid1 = filesys.errorHandler("file",filepath)
        valid2 = filesys.errorHandler("file",newFilepath,noexist=True)
        if valid1 != True:
            print("[filepath]"+valid1)
        elif valid2 != True:
            print("[newFilepath]"+valid2)
        else:
            try:
                os.rename(filepath,newFilepath)
            except Exception as e: print("\033[31mAn error occurred!\033[0m",e)

    # Function to rename a folder
    def renameDir(folderpath=str(),newFolderpath=str()):
        # Validate
        valid1 = filesys.errorHandler("dir",folderpath)
        valid2 = filesys.errorHandler("dir",newFolderpath,noexist=True)
        if valid1 != True:
            print("[folderpath]"+valid1)
        elif valid2 != True:
            print("[newFolderpath]"+valid2)
        else:
            try:
                shutil.move(folderpath,newFolderpath)
            except Exception as e: print("\033[31mAn error occurred!\033[0m",e)

    # Function to create file
    def createFile(filepath=str(), overwrite=False, encoding=None):
        # Validate
        valid = filesys.errorHandler("file",filepath,noexist=True)
        # Overwrite to file
        if "already exists" in str(valid):
            if overwrite == False:
                print("File already exists, set overwrite to true to overwrite it.")
            else:
                try:
                    f = open(filepath, "x", encoding=encoding)
                    f.close()
                except Exception as e: print("\033[31mAn error occurred!\033[0m",e)
        # Create new file
        else:
            try:
                f = open(filepath, "w", encoding=encoding)
                f.close()
            except Exception as e: print("\033[31mAn error occurred!\033[0m",e)
    
    # Function to create directory
    def createDir(folderpath=str()):
        # Validate
        valid = filesys.errorHandler("dir",folderpath,noexist=True)
        # Make directory
        if valid == True:
            try: os.mkdir(folderpath)
            except Exception as e: print("\033[31mAn error occurred!\033[0m",e)
        else:
            print(valid); exit()
    
    # Function to delete a file
    def deleteFile(filepath=str()):
        # Validate
        valid = filesys.errorHandler("file",filepath)
        # Delete file
        if valid == True:
            try: os.remove(filepath)
            except Exception as e: print("\033[31mAn error occurred!\033[0m",e)
        else:
            print(valid); exit()

    # Function to delete directory
    def deleteDir(folderpath=str()):
        # Validate
        valid = filesys.errorHandler("dir",folderpath)
        # Delete directory
        if valid == True:
            try: os.rmdir(folderpath)
            except Exception as e: print("\033[31mAn error occurred!\033[0m",e)
        else:
            print(valid); exit()

    # Function to delete directory NON EMPTY
    def deleteDirNE(folderpath=str()):
        # Validate
        valid = filesys.errorHandler("dir",folderpath)
        # Delete directory
        if valid == True:
            try: shutil.rmtree(folderpath)
            except Exception as e: print("\033[31mAn error occurred!\033[0m",e)
        else:
            print(valid); exit()

    # Function to write to a file
    def writeToFile(inputs=str(),filepath=str(), append=False, encoding=None, autocreate=False):
        if encoding != None: encoding = filesys.defaultencoding
        # AutoCreate
        if autocreate == True:
            if not os.path.exists(filepath): filesys.createFile(filepath=filepath,encoding=encoding)
        # Validate
        valid = filesys.errorHandler("file",filepath)
        if valid == True:
            # Check if function should append
            if append == True:
                try:
                    f = open(filepath, "a", encoding=encoding)
                    f.write(inputs)
                    f.close()
                except Exception as e: print("\033[31mAn error occurred!\033[0m",e)
            # Overwrite existing file
            else:
                try:
                    f = open(filepath, "w", encoding=encoding)
                    f.write(inputs)
                    f.close()
                except Exception as e: print("\033[31mAn error occurred!\033[0m",e)
        else:
            print(valid); exit()

    # Function to get file contents from file
    def readFromFile(filepath=str(),encoding=None):
        if encoding != None: encoding = filesys.defaultencoding
        # Validate
        valid = filesys.errorHandler("file",filepath)
        # Read from file
        if valid == True:
            try: 
                f = open(filepath, 'r', encoding=encoding)
                content = f.read()
                f.close()
                return content
            except Exception as e: print("\033[31mAn error occurred!\033[0m",e)
        else:
            print(valid); exit()

    # Function to get current working directory
    def getWorkingDir():
        return os.getcwd()
    
    # Function to change working directory
    def setWorkingDir(dir=str()):
        os.chdir(dir)

    # Function to copy a file
    def copyFile(sourcefile=str(),destination=str()):
        valid = filesys.errorHandler("file",sourcefile)
        if valid == True:
            try:
                shutil.copy2(sourcefile, destination)
            except Exception as e: print("\033[31mAn error occurred!\033[0m",e)
        else:
            print(valid); exit()

    # Function to copy a folder
    def copyFolder(sourceDirectory=str(),destinationDirectory=str()):
        valid = filesys.errorHandler("dir",sourceDirectory)
        if valid == True:
            try:
                shutil.copytree(sourceDirectory, destinationDirectory)
            except Exception as e: print("\033[31mAn error occurred!\033[0m",e)
        else:
            print(valid); exit()

    # Another function to copy a folder, custom made to allow the destination to exists
    def copyFolder2(sourceDirectory=str(),destinationDirectory=str(),debug=False):
        # Validate
        valid = filesys.errorHandler("dir", sourceDirectory)
        if valid == True:
            # Get files and folders in source that should be copied.
            entries = filesys.scantree(sourceDirectory)
            # Make sure that the destination directory only contains os.sep characters.
            destinationDirectory = destinationDirectory.replace("\\",os.sep)
            destinationDirectory = destinationDirectory.replace("/",os.sep)
            # Save the old working directory
            olddir = os.getcwd()
            # DEBUG
            if debug: print(f"Copying from '{sourceDirectory}' to '{destinationDirectory}' and was working in '{olddir}'\n\n")
            # Loop through al the files/folders that should be copied
            for entrie in entries:
                # Create the path to the file/folder in the source.
                newpath = (entrie.path).replace(sourceDirectory,f"{destinationDirectory}{os.sep}")
                newpath = newpath.replace(f"{os.sep}{os.sep}",os.sep)
                folderpath = newpath
                # If the source is a file then remove it from the path to make sure that al folders can be created before copying the file.
                if os.path.isfile(entrie.path):
                    folderpath = os.path.dirname(folderpath)
                # Make sure al the folders in the path exists
                splitdir = folderpath.split(os.sep)
                # goto root and remove root from splitdir
                if altConUtils.IsWindows():
                    if splitdir[0][-1] != "\\": splitdir[0] = splitdir[0] + '\\'
                    os.chdir(splitdir[0])
                    splitdir.pop(0)
                else: os.chdir("/")
                # DEBUG
                if debug: print(f"Working on '{entrie.path}' with new directory of '{folderpath}' and type-data 'IsFile:{os.path.isfile(entrie.path)}' and splitdir '{splitdir}'\n")
                # Iterate over the files
                for part in splitdir:
                    partPath = os.path.realpath(str(f"{os.getcwd()}{os.sep}{part}"))
                    try:
                        os.chdir(partPath)
                        # DEBUG
                        if debug: print(f"{entrie.name}: 'Working on path partial '{part}'")
                    except:
                        os.mkdir(partPath)
                        os.chdir(partPath)
                        # DEBUG
                        if debug: print(f"{entrie.name}: 'Needed to create path partial '{part}'")
                # If the source was a file copy it
                if os.path.isfile(entrie.path):
                    shutil.copy2(entrie.path,newpath)
                    # DEBUG
                    if debug: print(f"Copied file '{entrie.path}'")
                # DEBUG
                if debug: print("\n\n")
            os.chdir(olddir)
        else:
            print(valid); exit()

    # Function to zip a file
    def archive(sourceDirectory=str(),destination=str(),format=str()):
        valid = filesys.errorHandler("dir", destination)
        if valid == True:
            try:
                shutil.make_archive(('.'.join(destination.split(".")[:-1]).strip("'")), format=format, root_dir=sourceDirectory)
            except:  print("\033[31mAn error occurred!\033[0m")
        else:
            print(valid); exit()

    # Function to unzip a file
    def unArchive(archiveFile=str(),destination=str()):
        valid = filesys.errorHandler("file", archiveFile)
        if valid == True:
            try:
                shutil.unpack_archive(archiveFile, destination)
            except Exception as e: print("\033[31mAn error occurred!\033[0m",e)
        else:
            print(valid); exit()
        
    # Function to scantree using scantree()
    def scantree(path=str()):
        valid = filesys.errorHandler("dir", path)
        if valid == True:
            try:
                # Code
                for entry in scandir(path):
                    if entry.is_dir(follow_symlinks=False):
                        yield from filesys.scantree(entry.path)
                    else:
                        yield entry
            except Exception as e: print("\033[31mAn error occurred!\033[0m",e)
        else:
            print(valid); exit()

    # Function to check if a file is an executable
    def isExecutable(filepath=str(),fileEndings=None):
        exeFileEnds = [".exe",".cmd",".com",".py"]
        if fileEndings != None: exeFileEnds = fileEndings
        valid = filesys.errorHandler("file", filepath)
        if valid == True:
            try:
                # [Code]
                # Non Windows
                if altConUtils.IsLinux() or altConUtils.IsMacOS():
                    try: import magic
                    except:
                        os.system("pip3 install file-magic")
                    detected = magic.detect_from_filename(filepath)
                    return "application" in str(detected.mime_type)
                # Windows
                if altConUtils.IsWindows():
                    fending = str("." +''.join(filepath.split('.')[-1]))
                    if fending in exeFileEnds:
                        return True
                    else:
                        return False
            except Exception as e: print("\033[31mAn error occurred!\033[0m",e)
        else:
            print(valid); exit()

    # Function to get magic-mime info:
    def getMagicMime(filepath=str()):
        import magic # Internal import since module should only be loaded if function is called.
        detected = magic.detect_from_filename(filepath)
        return detected.mime_type

    # Function to open a folder in the host's filemanager
    def openFolder(path=str()):
        # Local imports:
        try: import distro
        except:
            os.system("python3 -m pip install distro")
            import distro
        # Launch manager
        if altConUtils.IsWindows(): os.system(f"explorer {path}")
        elif altConUtils.IsMacOS(): os.system(f"open {path}")
        elif altConUtils.IsLinux():
            #Rassberry pi
            if distro.id() == "raspbian": os.system(f"pcmanfm {path}")


# Class with "powershell-styled" functions
class pwshStyled():

    # Alias to doesExist
    def testPath(path=str()):
        return filesys.doesExist(path)

    # Alias to readFromFile
    def getContent(filepath=str(),encoding=None):
        return filesys.readFromFile(filepath=filepath,encoding="utf-8")
    
    # Alias to writeToFile
    def outFile(inputs=str(),filepath=str(),append=False,encoding=None):
        filesys.writeToFile(inputs=str(),filepath=str(),append=False,encoding=None)

    # Alias to createFile
    def touchFile(filepath=str(),encoding=None):
        filesys.createFile(filepath=filepath, overwrite=False, encoding=encoding)
#endregion [IncludeInline: ./assets/lib_filesys.py]

#region [IncludeInline: ./assets/flavorFunctions.py]
# Imports
import base64,os,shutil,requests,json,platform
import subprocess
import zipfile
import tarfile
import getpass
import uuid
from datetime import datetime
import hashlib

# FlavorFunctions fix missing filesys instance
try:
    filesys.defaultencoding
except:
    from lib_filesys import filesys as fs

# [Base64 helpers]
def encodeB64U8(str) -> str:
    return base64.b64encode(str).decode('utf-8')

def decodeB64U8(b64) -> str:
    return base64.b64decode(b64.encode('utf-8'))

# [Url helpers]
def getUrlContent(url) -> str:
    response = requests.get(url)
    if response.status_code == 200:
        # Content of the file
        return response.content
    else:
        return None

def downUrlFile(url,filepath):
    cont = getUrlContent(url)
    if cont != None and cont != "":
        if fs.notExist(filepath):
            open(filepath,'wb').write(cont)

# [Functionos]
def installListing(listingData=str,destinationDirPath=str,encoding="utf-8",prefix=""):
    sources = listingData.get("sources")
    webinclude = listingData.get("webInclude")

    # handle webinclude
    if webinclude != None:
        for incl in webinclude:
            url = list(incl.keys())[0]
            relpathToDest = list(incl.values())[0]
            if relpathToDest.startswith(".\\"):
                relpathToDest = relpathToDest.replace(".\\","",1)
            elif relpathToDest.startswith("./"):
                relpathToDest = relpathToDest.replace("./","",1)
            fpath = os.path.join(destinationDirPath,relpathToDest)
            fpath = fpath.replace("\\",os.sep)
            fpath = fpath.replace("/",os.sep)
            fs.ensureDirPath(os.path.dirname(fpath))
            downUrlFile(url,fpath)
    
    # ensure mods directory
    modsF = os.path.join(destinationDirPath,"mods")
    if fs.notExist(modsF): fs.createDir(modsF)

    # iterate over sources to extract them to the dest
    resources_zip_found = False
    listedNameOnlys = []
    downloadable = ["custom","curseforgeManifest","modrinth"]
    for source in sources:
        _type     = source.get("type")
        _url      = source.get("url")
        _filename = source.get("filename")
        _base64   = source.get("base64")
        # debug
        print(prefix+f"Installing '{_filename}' of type '{_type}'...")
        # base64 archive
        if _type == "customArchiveB64":
            # handle resources.zip (a listingIncluded base64 archive to be extracted to root)
            if _filename == "resources.zip" and resources_zip_found == False:
                zipC = decodeB64U8(_base64)
                nf = os.path.join(destinationDirPath,_filename)
                with open(destinationDirPath,'wb') as file:
                    file.write(zipC)
                if fs.getFileExtension(nf) != "zip":
                    znf = os.path.join(os.path.dirname(nf),fs.getFileName(nf)+".zip")
                    fs.renameFile(nf,znf)
                    nf = znf
                shutil.unpack_archive(nf,destinationDirPath)
            # Regular zip file
            else:
                zipC = decodeB64U8(_base64)
                nf = os.path.join(modsF,_filename)
                with open(destinationDirPath,'wb') as file:
                    file.write(zipC)
                shutil.unpack_archive(nf,modsF)
        # customB64 (non-archive)
        if _type == "customB64":
            jarC = decodeB64U8(_base64)
            nf = os.path.join(modsF,_filename)
            with open(nf,'wb') as file:
                file.write(jarC)
        # downloadable
        if _type in downloadable:
            if "<ManualUrlWaitingToBeFilledIn>" not in _url:
                downUrlFile(_url,os.path.join(modsF,_filename))
        # nameOnly
        if _type == "filenameOnly":
            listedNameOnlys.append(_filename)
    # write filenameOnly
    if listedNameOnlys != []:
        tx = ""
        for fn in listedNameOnlys:
            tx += f"{fn}\n"
        nolf = os.path.join(modsF,"listedFilenames.txt")
        if fs.doesExist(nolf): fs.deleteFile(nolf)
        open(nolf,'w',encoding=encoding).write(tx)

def extractModpackFile(modpack_path,parent,encoding="utf-8") -> str:
    # get type
    listingType = fs.getFileExtension(modpack_path)
    # ensure extractFolder
    dest = os.path.join(parent,fs.getFileName(os.path.basename(modpack_path)))
    if fs.notExist(dest): fs.createDir(dest)
    # handle archives (.zip/.package/.mListing) they are diffrent but handled the same at this stage
    if listingType != "listing":
        if listingType != "zip":
            newfile = os.path.join(os.path.dirname(modpack_path),fs.getFileName(modpack_path)+".zip")
            fs.copyFile(modpack_path,newfile)
            shutil.unpack_archive(newfile,dest)
            fs.deleteFile(newfile)
        else:
            shutil.unpack_archive(modpack_,dest)
    else:
        oldname = os.path.join(dest,os.path.basename(modpack_path))
        newname = os.path.join(dest,"listing.json")
        fs.copyFile(modpack_path,dest)
        fs.renameFile(oldname,newname)
    return dest

def downListingCont(extractedPackFolderPath=str,parentPath=str,encoding="utf-8",prefix=""):
    dest = extractedPackFolderPath
    # get data
    poss = os.path.join(dest,"listing.json")
    # If there is a listing file we must install the listing content
    if fs.doesExist(poss):
        content = open(poss,'r',encoding=encoding).read()
        listing = json.loads(content)
        installListing(listing,extractedPackFolderPath,encoding,prefix)

def _getJvb(path):
    java_binary = os.path.join(path, "java")
    if platform.system().lower() == "windows":
        java_binary += ".exe"
    if os.path.exists(java_binary):
        return java_binary
    else:
        return None

def find_java_binary(folder):
    # Check in folder
    jvb = _getJvb(folder)
    if jvb != None: return jvb
    # Check subsequent folders
    for elem in os.listdir(folder):
        elem = os.path.join(folder,elem)
        if os.path.isdir(elem):
            jvb = _getJvb(elem)
            if jvb != None: return jvb
    # Traverse
    for root, _, _ in os.walk(folder):
        if "bin" in root:
            java_binary = os.path.join(root, "java")
            if platform.system().lower() == "windows":
                java_binary += ".exe"
            if os.path.exists(java_binary):
                return java_binary

def getjava(prefix="",temp_folder=str,lnx_url=str,mac_url=str,win_url=str,forceDownload=False):
    # Check if Java is available in the CLI
    try:
        subprocess.check_output(["java", "-version"], stderr=subprocess.STDOUT, universal_newlines=True)
        if forceDownload != True:
            print(prefix+"Found java in path, continuing...")
            return "java"  # Java is already available
    except FileNotFoundError:
        print(prefix+"Java not found in path, downloading...")

    # Determine the appropriate download URL based on the operating system
    system = platform.system().lower()
    if system == "linux":
        url = lnx_url
    elif system == "darwin":
        url = mac_url
    elif system == "windows":
        url = win_url
    else:
        raise NotImplementedError("Unsupported operating system")

    # Create a "java" folder in the temp_folder
    java_folder = os.path.join(temp_folder, "java")
    os.makedirs(java_folder)

    # Download and unpack Java
    response = requests.get(url, stream=True)
    print(prefix+"Java downloaded, extracting archive...")
    if response.status_code == 200:
        if url.endswith(".zip"):
            with open(os.path.join(java_folder, "java.zip"), "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            with zipfile.ZipFile(os.path.join(java_folder, "java.zip"), 'r') as zip_ref:
                zip_ref.extractall(java_folder)
        elif url.endswith(".tar.gz"):
            with open(os.path.join(java_folder, "java.tar.gz"), "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            with tarfile.open(os.path.join(java_folder, "java.tar.gz"), 'r:gz') as tar_ref:
                tar_ref.extractall(java_folder)
        else:
            raise NotImplementedError("Unsupported archive format")

    print(prefix+"Java extracted, locating binary...")

    # Find the Java binary
    java_binary = find_java_binary(java_folder)
    if not java_binary:
        raise RuntimeError("Java binary not found in the extracted folder")

    # Mark the Java binary as executable on macOS and Linux
    if system in ["linux", "darwin"]:
        print(prefix+"Found, marking as executable...")
        os.chmod(java_binary, 0o755)
    else:
        print(prefix+"Found.")

    # Return the path to the Java binary
    print(prefix+"Continuing with downloaded java instance...")
    return java_binary

# Function to scape minor version urls from curseforge website
def scrapeMinorVerLinks(webcontent=str,baseurl=str):
    vers = webcontent.split('</li></div></div></ul>')
    vers = '</li></div></div></ul>'.join(vers)
    vers = vers.split('<li class="li-version-list">')
    vers.pop(0)
    versions = {}
    for ver in vers:
        # get minor
        ver = ver.split('<ul class="nav-collapsible " style="display: none;">')[-1]
        ver = ver.split('</ul>')[0]
        ver = ver.replace("<li>","")
        ver = ver.replace("</li>","")
        ver = ver.split('<ul class="nav-collapsible ">')[-1]
        for line in ver.split("\n"):
            if "<a href=" in line:
                line = line.split('<a href="')[-1]
                line = line.split('</a>')[0]
                parts = line.split('">')
                if parts[-1] != "":
                    if baseurl.endswith("/") != True: baseurl = baseurl+"/"
                    versions[parts[-1]] = baseurl + parts[0]
    return versions

# Function to using the previously scraped link scrape the accuallt installer links
def scrapeUniversals(prefix,scrapedPages=dict):
    universals = {}
    for ver,page in scrapedPages.items():
        # scape page
        wtext = requests.get(page).text
        if '<i class="fa classifier-universal' in wtext:
            wtext = wtext.split('<i class="fa classifier-universal')
            #wtext.pop(0)
            #wtext.pop(-1)
            for segment in wtext:
                seg = segment.split('<div class="link">')[-1]
                seg = seg.split('" title="Universal"')[0]
                seg = seg.split('<a href="')[-1]
                if "privacy.html" not in seg:
                    print(prefix+"Found universal jar: "+seg)
                    if universals.get(ver) == None:
                        universals[ver] = {"latest":"","recommended":""}
                    if universals[ver]["latest"] == "" and ".zip" not in seg:
                        universals[ver]["latest"] = seg
                    else:
                        if ".zip" not in seg:
                            universals[ver]["recommended"] = seg
        elif '<i class="fa classifier-installer' in wtext:
            wtext = wtext.split('<i class="fa classifier-installer')
            #wtext.pop(0)
            #wtext.pop(-1)
            for segment in wtext:
                seg = segment.split('<div class="link-boosted">')[-1]
                seg = seg.split('" title="Installer"')[0]
                seg = seg.split('<a href="')[-1]
                if "privacy.html" not in seg:
                    print(prefix+"Found installer jar: "+seg)
                    if universals.get(ver) == None:
                        universals[ver] = {"latest":"","recommended":""}
                    if universals[ver]["latest"] == "" and ".zip" not in seg:
                        universals[ver]["latest"] = seg
                    else:
                        if ".zip" not in seg:
                            universals[ver]["recommended"] = seg
    # remove empty
    new_universals = {}
    for key,value in universals.items():
        if value != {"latest":"","recommended":""}:
            new_universals[key] = value
    return new_universals

# Function to join together two forge-client listings
def _joinForgeListings(stdlist,newlist):
    joinedList = stdlist
    for key,value in newlist.items():
        if key not in stdlist.keys():
            joinedList[key] = value
        else:
            if joinedList[key] == None:
                joinedList[key] = value
            else:
                # prioritate std
                if newlist[key].get("latest") != "":
                    joinedList[key]["latest"] = newlist[key]["latest"]
                if newlist[key].get("recommended") != "":
                    joinedList[key]["recommended"] = newlist[key]["recommended"]
    return joinedList

# Function to get the download url for a loader
def getLoaderUrl(prefix,loaderType="fabric",tempFolder=str,fabricUrl=str,forgeUrl=str,forgeMakeUrl=True,forgeMakeUrlType="installer",forForgeMcVer=str,forForgeLdVer=str,forForgeInstType="latest",forForgeList=str,regetForge=False) -> str:
    '''Downloads a loader and return the path to it'''
    # Fabric (just return fabricURL)
    if loaderType.lower() == "fabric":
        return fabricUrl
    # Forge
    if loaderType.lower() == "forge":
        url = None
        # Compile fstring url
        if forgeMakeUrl == True:
            print(prefix+"Attempting to build list...")
            url = f"https://maven.minecraftforge.net/net/minecraftforge/forge/{forForgeMcVer}-{forForgeLdVer}/forge-{forForgeMcVer}-{forForgeLdVer}-{forgeMakeUrlType}.jar"
        # Otherwise use listing
        else:
            print(prefix+"Getting stdlist from github...")
            # get stdlist
            stdlist = {}
            cont = getUrlContent(forForgeList)
            if cont != None and cont != "":
                stdlist = json.loads(cont)
            # scrape current
            if regetForge == True:
                print(prefix+"Re-scraping list...")
                # scrape webcontent
                webcontent = requests.get(forgeUrl).text
                scrapedPages = scrapeMinorVerLinks(webcontent,forgeUrl)
                # scrape universals
                universals = scrapeUniversals(prefix,scrapedPages)
                # join
                if stdlist != {} and universals != None and universals != {}:
                    print(prefix+"Joining lists...")
                    stdlist = _joinForgeListings(stdlist,universals)
            # return without empty listings
            if forForgeMcVer in stdlist.keys():
                urlL = stdlist[forForgeMcVer]
                late = urlL.get("latest")
                reco = urlL.get("recommended")
                if forForgeInstType.lower() == "latest":
                    if late != "":
                        url = late
                    elif reco != "":
                        url = reco
                else:
                    if reco != "":
                        url = reco
                    elif late != "":
                        url = late
        return url

# Function to get the loader given an url 
def getLoader(basedir,loaderType="fabric",loaderLink=str) -> str:
    loader_folder = os.path.join(basedir,loaderType.lower())
    if fs.notExist(loader_folder): fs.createDir(loader_folder)
    loader_filen = os.path.basename(loaderLink)
    loader_filep = os.path.join(loader_folder,loader_filen)
    downUrlFile(loaderLink, loader_filep)
    return loader_filep

# Function to get the os-standard .minecraft path
def getLauncherDir(preset=None):
    if preset is not None:
        return preset
    else:
        user = getpass.getuser()
        system = platform.system().lower()
        if system == "windows":
            return f"C:\\Users\\{user}\\AppData\\Roaming\\.minecraft"
        elif system == "darwin":  # macOS
            return f"{getTilde()}/Library/Application Support/minecraft"
        elif system == "linux":
            return f"{getTilde()}/.minecraft"
        else:
            raise ValueError("Unsupported operating system")

# Function to run installer for a loader
def installLoader(prefix=str,java_path=str,loaderType="fabric",loaderFile=None,f_snapshot=False,f_dir=None,f_mcversion=None,f_loaderver=None,f_noprofile=False):
    if loaderType.lower() == "fabric":
        print(prefix+"Starting fabric install...")
        command = java_path + " -jar " + f'"{loaderFile}"' + " client"
        if f_snapshot == True:
            command += " -snapshot"
        if f_dir != None:
            command += f' -dir "{f_dir}"'
        if f_mcversion != None:
            command += f' -mcversion "{f_mcversion}"'
        if f_loaderver != None:
            command += f' -loader "{f_loaderver}"'
        if f_noprofile == True:
            command += " -noprofile"
        os.system(command)
        print(prefix+"Continuing...")
    elif loaderType.lower() == "forge":
        print(prefix+"Starting forge install...")
        print(prefix+"Follow the forge installers instructions.")
        # set dir to forge install to make sure log is placed in right folder
        olddir = os.getcwd()
        os.chdir(os.path.dirname(loaderFile))
        # run
        os.system(f'{java_path} -jar "{loaderFile}"')
        # move back to the prv dir
        os.chdir(olddir)
        #_ = input(prefix+"Once the installer is done, press any key to continue...")
        print(prefix+"Continuing...")

# Get client versionID
def getVerId(loaderType,loaderVer,mcVer):
    if loaderType.lower() == "fabric":
        return f"fabric-loader-{loaderVer}-{mcVer}"
    elif loaderType.lower() == "forge":
        return f"{mcVer}-forge-{loaderVer}"
    else:
        return mcVer

# Legacy > newFormat converter
def convFromLegacy(flavorMTAfile,legacyRepoUrl,encoding="utf-8") -> dict:
    # get flavorMTAcontent
    raw = open(flavorMTAfile,'r',encoding=encoding).read()
    mta = json.loads(raw)
    nameFound = os.path.basename(os.path.dirname(flavorMTAfile))
    # get props from name
    for segment in mta["Data"]:
        if segment.get("Name") != None:
            nameFound = segment.get("Name")
    # retrive repo for file
    lrepo = {}
    try:
        lrepo_raw = getUrlContent(legacyRepoUrl)
        lrepo = json.loads(lrepo_raw)
    except: pass
    lrepo_flavors = lrepo["Flavors"]
    listFlavorData = {}
    for flavor in lrepo_flavors:
        if list(flavor.keys())[0] == nameFound:
            listFlavorData = flavor[nameFound]
    flavorData = {}
    for item in listFlavorData:
        key = list(item.keys())[0]
        flavorData[key] = item[key]
    # create template
    listing = {
        "format": 1,
        "name": nameFound,
        "version": "0.0",
        "modloader": "fabric",
        "modloaderVer": flavorData["fabric_loader"],
        "minecraftVer": flavorData["minecraft_version"],
        "created": datetime.now().strftime('%Y-%m-%d_%H-%M-%S'),
        "launcherIcon": flavorData["launcher_icon"],
        "_legacy_fld": flavorData
    }
    return listing

# Function for Mac to get eqv to ~
def getTilde():
    user = getpass.getuser()
    system = platform.system().lower()
    if system == "darwin":
        return f"/Users/{user}"
    else:
        return f"/home/{user}"
        

# Apply user directory to a path
def applyDestPref(shortDest) -> str:
    user = getpass.getuser()
    system = platform.system().lower()
    if system == "windows":
        p = os.path.join(f"C:\\users\\{user}\\",shortDest)
    elif system == "darwin":
        p = os.path.join(getTilde(),shortDest)
    else:
        p = os.path.join(f"/home/{user}/",shortDest)
    return fs.replaceSeps(p)

# Get std final destination
def getStdInstallDest(system):
    p = applyDestPref(f"installs\\minecraft-custom-client\\v2")
    return p

# Function to handle icon
def _getIcon(icon,icon128,legacy,modded):
    if icon == "mcc:icon128":
        return icon128
    elif icon == "mcc:legacy":
        return legacy
    elif icon == "mcc:modded":
        return modded
    else:
        return icon
def getIcon(icon,icon128,legacy,modded,default):
    _icon = _getIcon(icon,icon128,legacy,modded)
    if _icon == None:
        return default
    else:
        return _icon

def getIconFromListing(listingData):
    ico = listingData.get("icon")
    if ico == None:
        return listingData.get("launcherIcon")
    else:
        return ico

# [Curseforge]
def getCFdir(ovv=None):
    if ovv != None:
        return ovv
    else:
        return applyDestPref("curseforge\\minecraft\\Instances")

def getCFinstanceDict(modld,ldver,mcver):
    if modld.lower() == "fabric":
        return {
            "baseModLoader": {
                "forgeVersion": ldver,
                "name": f"fabric-{ldver}-{mcver}",
                "minecraftVersion": mcver
            }
        }
    else:
        return {
            "baseModLoader": {
                "forgeVersion": ldver,
                "name": f"{modld.lower()}-{ldver}",
                "minecraftVersion": mcver
            }
        }

def createCFmanifest(manifestFile,mcver,modld,ldver,name,ver,encoding="utf-8"):
    manifest = {
        "minecraft": {
            "version": mcver,
            "modLoaders": [
            {
                "id": f"{modld.lower()}-{ldver}",
                "primary": True
            }
            ]
        },
        "manifestType": "minecraftModpack",
        "manifestVersion": 1,
        "name": name,
        "version": ver,
        "author": "",
        "files": [],
        "overrides": "overrides"
    }
    open(manifestFile,'w',encoding=encoding).write(json.dumps(manifest))

def zipCFexport(modpackFolder, manifest, exportZip):
    # Create a new zip file
    with zipfile.ZipFile(exportZip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add the contents of the folder to the zip file
        for folder_root, _, files in os.walk(modpackFolder):
            for file in files:
                file_to_zip = os.path.join(folder_root, file)
                arcname = os.path.relpath(file_to_zip, modpackFolder)
                arcname = os.path.join('overrides', arcname)  # Place files under "overrides" folder
                zipf.write(file_to_zip, arcname=arcname)
        # Add the specified file to the zip file
        zipf.write(manifest, arcname=os.path.basename(manifest))

# [Modrinth]
def getMRdir(system,ovv=None):
    if ovv != None:
        return ovv
    else:
        if system == "windows":
            return applyDestPref("Appdata\\Roaming\\com.modrinth.theseus\\profiles")
        elif system == "darwin":
            p = os.path.abspath(f"{getTilde()}/Library/Application Support/com.modrinth.theseus/profiles")
            fs.ensureDirPath(p)
            return p
        else:
            return applyDestPref(f"com.modrinth.theseus/profiles")

def getMRloaderURL(modld,ldver,mcver):
    if modld.lower() == "fabric":
        return f"https://meta.modrinth.com/fabric/v0/versions/{ldver}.json"
    elif modld.lower() == "forge":
        return f"https://meta.modrinth.com/forge/v0/versions/{mcver}-forge-{ldver}.json"

def getMRinstanceDict(modld,ldver,mcver,modDestF,name,icon):
    return {
        "uuid": str(uuid.uuid4()),
        "install_stage": "installed",
        "path": os.path.basename(modDestF),
        "metadata": {
        "name": name,
        "icon": str(icon),
        "groups": [],
        "game_version": mcver,
        "loader": modld,
        "loader_version": {
            "id": ldver,
            "url": getMRloaderURL(modld,ldver,mcver),
            "stable": True
        }
        },
        "fullscreen": None,
        "projects": {},
        "modrinth_update_version": None
    }

def sha1_hash_file(filepath):
    sha1 = hashlib.sha1()
    with open(filepath, "rb") as file:
        while True:
            data = file.read(65536)  # Read the file in 64k chunks
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()

def prepMRicon(modpackDestF,icon):
    iconPath = ""
    if icon == None:
        return icon
    finalPng = os.path.join(modpackDestF,"mcc_generated_icon.png")
    if os.path.exists(finalPng): os.remove(finalPng)
    # handle b64
    if "data:image/png;base64," in icon:
        icon = icon.replace("data:image/png;base64,","",1)
        icon_binary = base64.b64decode(icon)
        with open(finalPng, "wb") as f:
            f.write(icon_binary)
    else:
        if os.path.exists(icon):
            fs.copyFile(icon,finalPng)
        else:
            iconPath = icon.replace("\\","/")
    iconPath = finalPng.replace("\\","/")
    # get hash
    sha1 = sha1_hash_file(iconPath)
    cacheF = '/'.join([os.path.dirname(iconPath),"..","..","caches","icons",sha1+".png"])
    cacheF = os.path.abspath(cacheF)
    fs.copyFile(iconPath,cacheF)
    return cacheF
#endregion [IncludeInline: ./assets/flavorFunctions.py]

#region [IncludeInline: ./assets/minecraftLauncherAgent.py]
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
#endregion [IncludeInline: ./assets/minecraftLauncherAgent.py]

if action_install == True:

    print(prefix+f"Starting install for '{modpack}'...")

    # Create tempfolder
    fs = filesys
    print(prefix+"Creating temp folder...")
    tempFolder = os.path.join(parent,temp_foldername)
    try:
        if os.path.exists(tempFolder): shutil.rmtree(tempFolder)
    except:
        if os.path.exists(tempFolder):
            if platform.system() == "Windows":
                os.system(f'rmdir /s /q "{tempFolder}"')
            else:
                os.system(f'rm -rf "{tempFolder}"')
    fs.createDir(tempFolder)

    # IMPORT
    if args.imprt:
        pass
    else:
        # get type
        listingType = fs.getFileExtension(modpack_path)

        # extract archive to temp
        print(prefix+f"Extracting listing... (type: {listingType})")
        dest = extractModpackFile(modpack_path,tempFolder,encoding)

        if listingType != "package":
            # get listing data
            listingFile = os.path.join(dest,"listing.json")
            if fs.doesExist(listingFile) == True:
                listingData = json.loads(open(listingFile,'r',encoding=encoding).read())
            else:
                print("Failed to retrive listing content!")
                cleanUp(tempFolder,modpack_path)
                exit()
        else:
            try:
                mtaFile = os.path.join(dest,"flavor.mta")
                listingData = convFromLegacy(mtaFile,legacy_repo_url,encoding=encoding)
            except Exception as e:
                print("Failed to retrive listing content!",e)
                cleanUp(tempFolder,modpack_path)
                exit()

        # get data
        print(prefix+f"Downloading listing content... (type: {listingType})")
        try:
            downListingCont(dest,tempFolder,encoding,prefix_dl)
        except Exception as e:
            print(prefix+"Failed to download listing content!",e)
            cleanUp(tempFolder,modpack_path)
            exit()

        # get java
        print(prefix+f"Checking java...")
        try:
            javapath = getjava(prefix_jv,tempFolder,lnx_java_url,mac_java_url,win_java_url)
        except Exception as e:
            print(prefix+"Failed to get java!",e)
            cleanUp(tempFolder,modpack_path)
            exit()

        # handle install dest
        install_dest = getStdInstallDest(system)
        if listingData.get("_legacy_fld") != None:
            _legacy_fld_isntLoc = listingData["_legacy_fld"].get("install_location")
            if _legacy_fld_isntLoc != None and listingData["_legacy_fld"].get("install_location") != "":
                install_dest = applyDestPref(_legacy_fld_isntLoc)
        if args.dest:
            install_dest = args.dest
        fs.ensureDirPath(install_dest)
        ## handle curse
        #if args.curse == True:
        #    install_dest = getCFdir(
        #        args.curseInstanceP
        #    )
        #    fs.ensureDirPath(install_dest)
        ## create subfolder
        ## handle modrinth
        if args.rinth == True:
            install_dest = getMRdir(
                system,
                args.rinthInstanceP
            )
            ## handle modrinth profile already existing
            if args.rinth == True:
                _p = os.path.join(install_dest,fs.getFileName(modpack))
                if os.path.exists(_p):
                    if args.y:
                        c = args.y
                    elif args.n:
                        c = args.n
                    else:
                        c = input("Modrith profile already exists, overwrite it? [y/n]")
                    if c.lower() == "n":
                        cleanUp(tempFolder,modpack_path)
                        exit()
            fs.ensureDirPath(install_dest)
        ## get modpack destination folder
        modpack_destF = os.path.join(install_dest,fs.getFileName(modpack))
        if os.path.exists(modpack_destF) != True: os.mkdir(modpack_destF)

        # get mod info
        try:
            modld = listingData["modloader"]
            ldver = listingData["modloaderVer"]
            mcver = listingData["minecraftVer"]
            f_snapshot = False
            if "snapshot:" in mcver:
                mcver = mcver.replace("snapshot:","")
                f_snapshot = True
            print(prefix+f"Retriving loader-install url... ({modld}: {ldver} for {mcver})")
            tryMakeFrgUrl = True
            reScrapeFrgLst = False
            loaderURL = getLoaderUrl(prefix,modld,tempFolder,fabric_url,forge_url,tryMakeFrgUrl,mcver,ldver,"latest",forForgeList,reScrapeFrgLst)
            print(prefix+f"Using: {loaderURL}")

            print(prefix+f"Downloading loader...")
            loaderFp = getLoader(tempFolder,modld,loaderURL)
            # fail fix with forge makeurl
            if fs.notExist(loaderFp) and modld == "forge" and tryMakeFrgUrl == True:
                print(prefix+f"Failed, retrying to get forge url...")
                loaderURL = getLoaderUrl(prefix,modld,tempFolder,fabric_url,forge_url,False,mcver,ldver,"latest",forForgeList,reScrapeFrgLst)
                print(prefix+f"Downloading loader...")
                loaderFp = getLoader(tempFolder,modld,loaderURL)
            # fail
            if fs.notExist(loaderFp):
                print("Failed to downloader loader!")
                cleanUp(tempFolder,modpack_path)
                exit()
        except Exception as e:
            print(prefix+"Failed to get loader!",e)
            cleanUp(tempFolder,modpack_path)
            exit()

    # EXPORT
    infoFile = os.path.join(tempFolder,"modpack_info.json")
    if args.exprt:
        if args.exprt.endswith(".zip"):
            args.exprt = args.exprt[::-1].replace("piz.","",1)[::-1]
        modpackInfo = {
            "modpack": modpack,
            "modpack_path": modpack_path,
            "dest": dest,
            "listingData": listingData,
            "listingType": listingType,
            "listingFile": listingFile,
            "loaderFp": loaderFp,
            "javapath": javapath,
            "install_dest": install_dest,
            "modpack_destF": modpack_destF,
            "f_snapshot": f_snapshot,
            "loaderURL": loaderURL
        }
        open(infoFile,'w',encoding=encoding).write(json.dumps(modpackInfo))
        print(f"Exporting to '{args.exprt}'")
        shutil.make_archive(args.exprt, "zip", tempFolder)
        cleanUp(tempFolder,modpack_path)
        exit()
    elif args.imprt:
        print(f"Importing from '{args.imprt}'")
        try:
            if not os.path.exists(tempFolder):
                os.makedirs(tempFolder)
            # Extract the contents of the zip file to the tempFolder
            with zipfile.ZipFile(args.imprt, 'r') as zip_ref:
                zip_ref.extractall(tempFolder)
            impData = json.loads( open(infoFile,'r',encoding=encoding).read() )
        except:
            print("Failed to import tempfolder!")
            cleanUp(tempFolder)
            exit()
        modpack = impData["modpack"]
        modpack_path = impData["modpack_path"]
        dest = impData["dest"]
        listingData = impData["listingData"]
        listingType = impData["listingType"]
        listingFile = impData["listingFile"]
        loaderFp = impData["loaderFp"]
        javapath = impData["javapath"]
        install_dest = impData["install_dest"]
        modpack_destF = impData["modpack_destF"]
        f_snapshot = impData["f_snapshot"]
        loaderURL = impData["loaderURL"]
        modld = listingData["modloader"]
        ldver = listingData["modloaderVer"]
        mcver = listingData["minecraftVer"]

    # Install loader
    print(prefix+f"Starting install of loader... ({loaderFp})")
    f_dir = getLauncherDir(args.mcf)
    f_mcversion = mcver
    f_loaderver = ldver
    f_noprofile = args.fabprofile
    try:
        installLoader(prefix,javapath,modld,loaderFp,f_snapshot,f_dir,f_mcversion,f_loaderver,True)
    except Exception as e:
        print(prefix+"Failed to install loader!",e)
        cleanUp(tempFolder,modpack_path)
        exit()

    # Copy content to final dest
    fs.copyFolder2(dest,modpack_destF)

    # Create profile
    print(prefix+f"Creating profile for: {modpack}")
    # Export to curse file
    if (args.excurse != None and args.excurse != False and args.excurse != "") or args.excurse_parent == True:
        # Handle --excurse
        if args.excurse_parent == True:
            if "MinecraftCustomClient" in str(sys.executable):
                _parent = os.path.dirname(str(sys.executable))
            else:
                _parent = os.path.dirname(__file__)
            args.excurse = os.path.join(_parent,listingData["name"]+"_excurse.zip")
            if os.path.exists(args.excurse): os.remove(args.excurse)
        # Msg
        print(prefix+f"Exporting to curseforge file: '{args.excurse}'")
        # fix .zip double
        if args.excurse.endswith(".zip") != True:
            args.excurse = args.excurse + ".zip"
        # create manifest file
        print(prefix+f"Creating manifest...")
        manifest = os.path.join(tempFolder,"manifest.json")
        createCFmanifest(manifest,mcver,modld,ldver,listingData["name"],listingData["version"],encoding)
        # export
        print(prefix+f"Exporting...")
        zipCFexport(dest,manifest,args.excurse)
        print(prefix+f"Done!")
        # cleanup
        cleanUp(tempFolder,modpack_path)
        exit()
    elif args.rinth == True:
        try:
            gicon = getIcon(
                getIconFromListing(listingData),
                icon_base64_icon128,
                icon_base64_legacy,
                icon_base64_modded,
                icon_base64_default
            )
            gicon = prepMRicon(modpack_destF,gicon)
            mrInstanceFile = os.path.join(modpack_destF,"profile.json")
            mrInstanceDict = getMRinstanceDict(modld,ldver,mcver,modpack_destF,listingData["name"],gicon)
            if os.path.exists(mrInstanceFile): os.remove(mrInstanceFile)
            open(mrInstanceFile,'w',encoding=encoding).write(
                json.dumps(mrInstanceDict)
            )
        except Exception as e:
            print(prefix+"Failed to create profile in modrinth app!",e)
    else:
        try:
            gicon = getIcon(
                getIconFromListing(listingData),
                icon_base64_icon128,
                icon_base64_legacy,
                icon_base64_modded,
                icon_base64_default
            )
            MinecraftLauncherAgent(
                prefix=prefix_la,
                add=True,

                name=listingData["name"],
                gameDir=modpack_destF,
                icon=gicon,
                versionId=getVerId(modld,ldver,mcver),

                dontkill=args.dontkill,
                startLauncher=args.autostart,
                overWriteLoc=args.mcf,
                overWriteFile=args.cLnProfFileN,
                overWriteBinExe=args.cLnBinPath,

                excProcNameList=["minecraftcustomclient.exe"]
            )
        except Exception as e:
            print(prefix+"Failed to create profile in minecraft launcher",e)
            cleanUp(tempFolder,modpack_path)
            exit()
        #elif args.curse:
        #    cfInstanceFile = os.path.join(modpack_destF,"minecraftinstance.json")
        #    cfInstanceDict = getCFinstanceDict(modld,ldver,mcver)
        #    if os.path.exists(cfInstanceFile): os.remove(cfInstanceFile)
        #    open(cfInstanceFile,'w',encoding=encoding).write(
        #        json.dumps(cfInstanceDict)
        #    )

    # Add to installed-list
    mcc_installed_file = os.path.join(getStdInstallDest(system),"modpacks.json")
    mcc_installed = {
        "DefaultInstallDirectory": getStdInstallDest(system),
        "Installs":[]
    }
    ## handle existing
    if fs.doesExist(mcc_installed_file):
        raw = open(mcc_installed_file,'r',encoding=encoding).read()
        mcc_installed = json.loads(raw)
    ## get id
    mcc_installed_id = "<uuid>"
    if listingData.get("_legacy_fld") != None:
        mcc_installed_id = listingData["_legacy_fld"].get("ID")
    ## add client
    mcc_installed_current = {
        "id": mcc_installed_id,
        "name": os.path.basename(modpack),
        "path": modpack_destF
    }
    mcc_installed["Installs"].append(mcc_installed_current)
    ## write
    raw = json.dumps(mcc_installed)
    open(mcc_installed_file,'w',encoding=encoding).write(raw)


    # Clean up
    print(prefix+"Cleaning up...")
    try:
        if os.path.exists(tempFolder): shutil.rmtree(tempFolder)
    except:
        if os.path.exists(tempFolder):
            if platform.system() == "Windows":
                os.system(f'rmdir /s /q "{tempFolder}"')
            else:
                os.system(f'rm -rf "{tempFolder}"')
    if args.autostart:
        print(prefix+"Done, Enjoy!")
    else:
        print(prefix+"Done, now start your launcher and enjoy!")

    cli_pause("Received exit, press any key to continue...")
#endregion [IncludeInline: ./partial@installermain.py]