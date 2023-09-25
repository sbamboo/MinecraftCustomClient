# This file is for creating an installer for only one modpack

# [Settings]
installer_version = "1.0"
installer_release = "2023-09-22"
prefix    = "\033[90m[\033[35mQuickInst\033[90m]\033[0m "
prefix_dl = "\033[90m[\033[34mDown-List\033[90m]\033[0m "
prefix_jv = "\033[90m[\033[33mJava-Inst\033[90m]\033[0m "
prefix_la = "\033[90m[\033[94mLnch-Agnt\033[90m]\033[0m "
title = f"MinecraftCustomClient - QuickInstaller {installer_version}: <modpack>"
temp_foldername = "MCC_QuickInstaller_Temp"

win_java_url = "https://aka.ms/download-jdk/microsoft-jdk-17.0.8.1-windows-x64.zip"
lnx_java_url = "https://aka.ms/download-jdk/microsoft-jdk-17.0.8.1-linux-x64.tar.gz"
mac_java_url = "https://aka.ms/download-jdk/microsoft-jdk-17.0.8.1-macOS-x64.tar.gz"

fabric_url = "https://maven.fabricmc.net/net/fabricmc/fabric-installer/0.11.2/fabric-installer-0.11.2.jar"
forge_url  = "https://files.minecraftforge.net/net/minecraftforge/forge"
forForgeList = "https://raw.githubusercontent.com/sbamboo/MinecraftCustomClient/main/v2/Installers/Assets/forge-links.json"

modpack = f"Example-modpack_2023-09-22_22-56-15-quickcompile.listing"

#region [IncludeInline: ./assets/lib_crshpiptools.py]: START
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
#endregion [IncludeInline: ./assets/lib_crshpiptools.py]: END

# [Imports]
_ = autopipImport("argparse")
_ = autopipImport("scandir")
_ = autopipImport("requests")
_ = autopipImport("getpass")
_ = autopipImport("subprocess")
_ = autopipImport("datetime")
_ = autopipImport("json")
_ = autopipImport("psutil")

# [Setup]

import requests,platform,sys,os,shutil,argparse
import json
parent = os.path.abspath(os.path.dirname(__file__))
modpack_path = os.path.join(parent,modpack)
modpack = os.path.basename(modpack)
title = title.replace("<modpack>", modpack)
system = platform.system().lower()

# [Args]
encoding = "utf-8"
parser = argparse.ArgumentParser(description='MinecraftCustomClient QuickInstaller')
parser.add_argument('-enc', type=str, help='The file encoding to use')
parser.add_argument('-mcf','-cMinecraftLoc', dest="mcf", type=str, help='MinecraftFolder (.minecraft)')
parser.add_argument('--fabprofile', help='Should fabric create a profile?', action="store_true")
parser.add_argument('--dontkill', help='Should the install not kill minecraft process?', action="store_true")
parser.add_argument('--autostart', help='Should the installer attempt to start the launcher?', action="store_true")
parser.add_argument('-cLnProfFileN', type=str, help='The filename to overwrite the profile-listing file with.')
parser.add_argument('-cLnBinPath', type=str, help='If autostart and no msstore launcher if found, overwrite launcher with this.')
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

#region [IncludeInline: ./assets/lib_filesys.py]: START
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

    # Function to check if a file/directory exists
    def doesExist(path=str()):
        return bool(os.path.exists(path))
        
    # Function to check if a file/directory does not exist
    def notExist(path=str()):
        if os.path.exists(path): return False
        else: return True

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
            except: print("\033[31mAn error occurred!\033[0m")

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
            except: print("\033[31mAn error occurred!\033[0m")

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
                except: print("\033[31mAn error occurred!\033[0m")
        # Create new file
        else:
            try:
                f = open(filepath, "w", encoding=encoding)
                f.close()
            except: print("\033[31mAn error occurred!\033[0m")
    
    # Function to create directory
    def createDir(folderpath=str()):
        # Validate
        valid = filesys.errorHandler("dir",folderpath,noexist=True)
        # Make directory
        if valid == True:
            try: os.mkdir(folderpath)
            except: print("\033[31mAn error occurred!\033[0m")
        else:
            print(valid); exit()
    
    # Function to delete a file
    def deleteFile(filepath=str()):
        # Validate
        valid = filesys.errorHandler("file",filepath)
        # Delete file
        if valid == True:
            try: os.remove(filepath)
            except: print("\033[31mAn error occurred!\033[0m")
        else:
            print(valid); exit()

    # Function to delete directory
    def deleteDir(folderpath=str()):
        # Validate
        valid = filesys.errorHandler("dir",folderpath)
        # Delete directory
        if valid == True:
            try: os.rmdir(folderpath)
            except: print("\033[31mAn error occurred!\033[0m")
        else:
            print(valid); exit()

    # Function to delete directory NON EMPTY
    def deleteDirNE(folderpath=str()):
        # Validate
        valid = filesys.errorHandler("dir",folderpath)
        # Delete directory
        if valid == True:
            try: shutil.rmtree(folderpath)
            except: print("\033[31mAn error occurred!\033[0m")
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
                except: print("\033[31mAn error occurred!\033[0m")
            # Overwrite existing file
            else:
                try:
                    f = open(filepath, "w", encoding=encoding)
                    f.write(inputs)
                    f.close()
                except: print("\033[31mAn error occurred!\033[0m")
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
            except: print("\033[31mAn error occurred!\033[0m")
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
            except: print("\033[31mAn error occurred!\033[0m")
        else:
            print(valid); exit()

    # Function to copy a folder
    def copyFolder(sourceDirectory=str(),destinationDirectory=str()):
        valid = filesys.errorHandler("dir",sourceDirectory)
        if valid == True:
            try:
                shutil.copytree(sourceDirectory, destinationDirectory)
            except: print("\033[31mAn error occurred!\033[0m")
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
            except: print("\033[31mAn error occurred!\033[0m")
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
            except: print("\033[31mAn error occurred!\033[0m")
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
            except: print("\033[31mAn error occurred!\033[0m")
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
#endregion [IncludeInline: ./assets/lib_filesys.py]: END

#region [IncludeInline: ./assets/flavorFunctions.py]: START
import base64,os,shutil,requests,json,platform
import subprocess
import zipfile
import tarfile
import getpass

# flavorFunctions fix missing fs
try:
    filesys.defaultencoding
except:
    from lib_filesys import filesys as fs

def encodeB64U8(str) -> str:
    return base64.b64encode(str).decode('utf-8')

def decodeB64U8(b64) -> str:
    return base64.b64decode(b64.encode('utf-8'))

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

def installListing(listingData=str,destinationDirPath=str,encoding="utf-8",prefix=""):
    sources = listingData.get("sources")
    
    # ensure mods directory
    modsF = os.path.join(destinationDirPath,"mods")
    if fs.notExist(modsF): fs.createDir(modsF)

    # iterate over sources to extract them to the dest
    resources_zip_found = False
    listedNameOnlys = []
    downloadable = ["custom","curseforgeManifest","modrith"]
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
                with open(destinationDirPath,'wb', encoding=encoding) as file:
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
                with open(destinationDirPath,'wb', encoding=encoding) as file:
                    file.write(zipC)
                shutil.unpack_archive(nf,modsF)
        # customB64 (non-archive)
        if _type == "customB64":
            jarC = decodeB64U8(_base64)
            nf = os.path.join(modsF,_filename)
            with open(nf,'wb', encoding=encoding) as file:
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

def _joinForgeListings(stdlist,newlist):
    joinedList = stdlist
    for key,value in newlist.items():
        if key not in stdlist.keys():
            joinedList[key] = value
        else:
            if joinedList[key] == None:
                joinedList[key] = value
            else:
                if newlist[key].get("latest") != "":
                    joinedList[key]["latest"] = newlist[key]["latest"]
                if newlist[key].get("recommended") != "":
                    joinedList[key]["recommended"] = newlist[key]["recommended"]
    return joinedList

def getLoaderUrl(prefix,loaderType="fabric",tempFolder=str,fabricUrl=str,forgeUrl=str,forgeMakeUrl=True,forgeMakeUrlType="installer",forForgeMcVer=str,forForgeLdVer=str,forForgeInstType="latest",forForgeList=str,regetForge=False) -> str:
    '''Downloads a loader and return the path to it'''
    # Fabric
    if loaderType.lower() == "fabric":
        return fabricUrl
    # Forge
    if loaderType.lower() == "forge":
        url = None
        if forgeMakeUrl == True:
            print(prefix+"Attempting to build list...")
            url = f"https://maven.minecraftforge.net/net/minecraftforge/forge/{forForgeMcVer}-{forForgeLdVer}/forge-{forForgeMcVer}-{forForgeLdVer}-{forgeMakeUrlType}.jar"
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
            # return
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
            
def getLoader(basedir,loaderType="fabric",loaderLink=str) -> str:
    loader_folder = os.path.join(basedir,loaderType.lower())
    if fs.notExist(loader_folder): fs.createDir(loader_folder)
    loader_filen = os.path.basename(loaderLink)
    loader_filep = os.path.join(loader_folder,loader_filen)
    downUrlFile(loaderLink, loader_filep)
    return loader_filep

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

def getVerId(loaderType,loaderVer,mcVer):
    if loaderType.lower() == "fabric":
        return f"fabric-loader-{loaderVer}-{mcVer}"
    elif loaderType.lower() == "forge":
        return f"{mcVer}-forge-{loaderVer}"
    else:
        return mcVer#endregion [IncludeInline: ./assets/flavorFunctions.py]: END

#region [IncludeInline: ./assets/minecraftLauncherAgent.py]: START
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
def terminateMC():
    import psutil
    # Get a list of all running processes
    for process in psutil.process_iter(['pid', 'name']):
        try:
            process_name = process.info['name']
            # Check if the process name contains "Minecraft"
            if 'minecraft' in process_name.lower():
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
    dontbreak=False
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
    binlaunchdir = "C:\Program Files (x86)\Minecraft Launcher\MinecraftLauncher.exe"
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
        terminateMC()

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
    if toReturn != None: return toReturn#endregion [IncludeInline: ./assets/minecraftLauncherAgent.py]: END

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
    exit()

print(prefix+f"Starting install of loader... ({loaderFp})")
f_dir = getLauncherDir(args.mcf)
f_mcversion = mcver
f_loaderver = ldver
f_noprofile = args.fabprofile
installLoader(prefix,javapath,modld,loaderFp,f_snapshot,f_dir,f_mcversion,f_loaderver,True)

print(prefix+f"Creating profile for: {modpack}")
MinecraftLauncherAgent(
    add=True,

    name=fs.getFileName(modpack),
    gameDir=dest,
    icon=listingData.get("icon"),
    versionId=getVerId(modld,ldver,mcver),

    dontkill=args.dontkill,
    startLauncher=args.autostart,
    overWriteLoc=args.mcf,
    overWriteFile=args.cLnProfFileN,
    overWriteBinExe=args.cLnBinPath
)