# This file is for creating an installer for only one modpack

# [Settings]
installer_version = "1.0"
installer_release = "2023-09-22"
modpack = "<replaceble:modpack>"
repository_url = "https://raw.githubusercontent.com/sbamboo/MinecraftCustomClient/main/v2/Repo/repo.json"

# [Setup]
import requests,platform,sys,os
title = f"Minecraft Custom Client - QuickInstaller {installer_version}: {modpack}"

# [Functions]

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

# [Code]
setConTitle(title)

print("Downloading repository...")
repo = requests.get(repository_url).text

flavorData = None
for flavor in repo.get("flavors"):
    if flavor["name"] == modpack:
        flavorData = flavor["name"]
        break

# IncludeInline: ./assets/flavorFunctions.py

if flavorData != None:
    installFlavor(flavorData)