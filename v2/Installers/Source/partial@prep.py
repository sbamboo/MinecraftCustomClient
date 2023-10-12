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
    oexit() #repl-exit


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
if args.skipPreRelWait:
    pass
else:
    time.sleep(2)