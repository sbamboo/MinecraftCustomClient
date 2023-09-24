# This file is for creating an installer for only one modpack

# [Settings]
installer_version = "1.0"
installer_release = "2023-09-22"
prefix    = "\033[90m[\033[35mQuickInst\033[90m]\033[0m "
prefix_dl = "\033[90m[\033[34mDown-List\033[90m]\033[0m "
prefix_jv = "\033[90m[\033[33mJava-Inst\033[90m]\033[0m "
title = f"MinecraftCustomClient - QuickInstaller {installer_version}: <modpack>"
temp_foldername = "MCC_QuickInstaller_Temp"

win_java_url = "https://aka.ms/download-jdk/microsoft-jdk-17.0.8.1-windows-x64.zip"
lnx_java_url = "https://aka.ms/download-jdk/microsoft-jdk-17.0.8.1-linux-x64.tar.gz"
mac_java_url = "https://aka.ms/download-jdk/microsoft-jdk-17.0.8.1-macOS-x64.tar.gz"

fabric_url = "https://maven.fabricmc.net/net/fabricmc/fabric-installer/0.11.2/fabric-installer-0.11.2.jar"
forge_url  = "https://files.minecraftforge.net/net/minecraftforge/forge"
forForgeList = "https://raw.githubusercontent.com/sbamboo/MinecraftCustomClient/main/v2/Installers/Assets/forge-links.json"

modpack = "<replaceble:modpack_relative_path_to_parent>"

# IncludeInline: ./assets/lib_crshpiptools.py

# [Imports]
_ = autopipImport("argparse")
_ = autopipImport("scandir")
_ = autopipImport("requests")

# [Setup]

import requests,platform,sys,os,shutil,argparse
import json
parent = os.path.abspath(os.path.dirname(__file__))
modpack_path = os.path.join(parent,modpack)
modpack = os.path.basename(modpack)
title = title.replace("<modpack>", modpack)

# [Args]
encoding = "utf-8"
parser = argparse.ArgumentParser(description='MinecraftCustomClient QuickInstaller')
parser.add_argument('-enc', type=str, help='The file encoding to use')
args = parser.parse_args()
if args.enc:
    encoding = args.enc

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

print(prefix+f"Starting install for '{modpack}'...")

# IncludeInline: ./assets/lib_filesys.py

# IncludeInline: ./assets/flavorFunctions.py

# Create tempfolder
fs = filesys
print(prefix+"Creating temp folder...")
tempFolder = os.path.join(parent,temp_foldername)
try:
    if os.path.exists(tempFolder): shutil.rmtree(tempFolder)
except:
    if platform.system() == "Windows":
        os.system(f'rmdir /s /q "{tempFolder}"')
    else:
        os.system(f'rm -rf "{tempFolder}"')
fs.createDir(tempFolder)

# get type
listingType = fs.getFileExtension(modpack_path)

# extract archive to temp
print(prefix+f"Extracting listing... (type: {listingType})")
dest = extractModpackFile(modpack_path,tempFolder,encoding)
listingFile = os.path.join(dest,"listing.json")

# get listing data
if fs.doesExist(listingFile) == True:
    listingData = json.loads(open(listingFile,'r',encoding=encoding).read())
else:
    print("Failed to retrive listing content!")
    exit()

# get data
print(prefix+f"Downloading listing content... (type: {listingType})")
#downListingCont(dest,tempFolder,encoding,prefix_dl)

# get java
print(prefix+f"Checking java...")
javapath = getjava(prefix_jv,tempFolder,lnx_java_url,mac_java_url,win_java_url)

modld = listingData["modloader"]
ldver = listingData["modloaderVer"]
mcver = listingData["minecraftVer"]
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
    exit()

print(prefix+f"Starting install of loader... ({loaderFp})")
f_snapshot = False
f_dir = getLauncherDir()
f_mcversion = mcver
f_loaderver = ldver
f_noprofile = False
installLoader(prefix,javapath,modld,loaderFp,f_snapshot,f_dir,f_mcversion,f_loaderver,f_noprofile)