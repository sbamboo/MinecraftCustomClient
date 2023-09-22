import os
import argparse
from libs.filesys import filesys as fs
from datetime import datetime
import sys
try:
    import yaml
except:
    os.system(f"{sys.executable} -m pip install pyyaml")
    import yaml
import shutil

# enable ansi
os.system("")

# Get parent
parent = os.path.abspath(os.path.dirname(__file__))

# Setup
encoding = "utf-8"
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
tempFolder = f"{parent}{os.sep}{timestamp}-quickcompile"
lister = f"{parent}{os.sep}_createListing.py"
listing = f"{tempFolder}{os.sep}listing.json"

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description='Quick compiler')
parser.add_argument('-path', type=str, help='The path to the modsfolder')
parser.add_argument('-cmpl', type=str, help='The compile.yml file')
parser.add_argument('-enc', type=str, help='The file encoding to use')
args = parser.parse_args()

# Handle enc
if args.enc:
    encoding = args.enc

# Create temporary folder
fs.createDir(tempFolder)

# Get compile.yml
## get path
if fs.notExist(args.cmpl):
    args.cmpl == None
    while args.cmpl == None:
        t = input("Invalid compile.yml path: ")
        if fs.doesExist(t):
            args.cmpl = t
## get content
content = open(args.cmpl,'r',encoding=encoding).read()
compyml = yaml.safe_load(content)

# pull
if compyml.get('gitsync') == True:
    import subprocess
    print("Retriving hit repostiroy root path...")
    try:
        root_path_bytes = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'])
        root_path = root_path_bytes.decode('utf-8').strip()
        print(f"Found: '{root_path}'")
    except:
        root_path = None
    if root_path != None and fs.doesExist(root_path):
        print("Pulling repository...")
        olddir = os.getcwd()
        os.chdir(root_path)
        os.system('git pull')
        print("")
        os.chdir(olddir)

# Run jar retriver
if fs.notExist(args.path):
    print(f"Invalid modpack path: {args.path}")
else:
    nonAllowed = ["",None]
    command = f' -modpack "{args.path}" -dest "{listing}"'
    command += f' -mcVer "{compyml["minecraftVer"]}"'
    command += f' -loader "{compyml["modloader"]}"'
    command += f' -loaderVer "{compyml["modloaderVer"]}"'
    command += f' -name "{compyml["name"]}"'
    if compyml.get("ver") not in nonAllowed:
        command += f' -ver "{compyml["version"]}"'
    if compyml.get("icon") not in nonAllowed:
        command += f' -icon "{compyml["icon"]}"'
    if compyml.get("lister") not in nonAllowed:
        if compyml["lister"]["silent"] == True:
            command += " --silent"
    if compyml.get("missingLinkAction") not in nonAllowed:
        command += f' -missingActionStr "{compyml["missingLinkAction"]}"'
    if compyml.get("archiveFoundAction") not in nonAllowed:
        command += f' -archiveActionStr "{compyml["archiveFoundAction"]}"'
    os.system(f"python3 {lister} {command}")

# Find other things to include
incl = compyml.get("include")
if incl != None:
    # specified
    if type(incl) == list:
        for pa in incl:
            if pa.startswith(".\\"):
                pa = pa.replace(".\\","",1)
            elif pa.startswith("./"):
                pa = pa.replace("./","",1)
            pa2 = f"{args.path}{os.sep}{pa}"
            dest = f"{tempFolder}{os.sep}{pa}{os.sep}"
            if fs.doesExist(pa2):
                if fs.isFile(pa2):
                    print(f"Including file...   '.{pa2.replace(args.path,'')}'")
                    fs.copyFile(pa2,tempFolder)
                elif fs.isDir(pa2):
                    print(f"Including folder... '.{pa2.replace(args.path,'')}'")
                    fs.copyFolder2(pa2,dest)
    # everything
    elif type(incl) == str:
        entries = os.scandir(args.path)
        for entry in entries:
            if entry.name != "mods":
                dest = f"{tempFolder}{os.sep}{entry.name}{os.sep}"
                entry = str(entry.path)
                if fs.doesExist(entry):
                    if entry != args.cmpl:
                        if fs.isFile(entry):
                            print(f"Including file...   '.{entry.replace(args.path,'')}'")
                            fs.copyFile(entry,tempFolder)
                        elif fs.isDir(entry):
                            print(f"Including folder... '.{entry.replace(args.path,'')}'")
                            fs.copyFolder2(entry,dest)

    # zip
    olddir = os.getcwd()
    os.chdir(parent)
    zipfile = f"{os.path.basename(tempFolder)}.zip"
    print(f"Zipping modpack... ({zipfile})")
    shutil.make_archive(tempFolder, 'zip', tempFolder)
    print("Cleaning up...")
    fs.deleteDirNE(tempFolder)
    fs.renameFile(zipfile,f"{compyml['name'].replace(' ','-')}_{fs.getFileName(zipfile)}.mListing")
    os.chdir(olddir)

else:
    listingfile = f"{os.path.basename(tempFolder)}.listing"
    print(f"Writing modpack... ({listingfile})")
    fs.copyFile(listing,os.path.join(tempFolder,f"{parent}{os.sep}{compyml['name'].replace(' ','-')}_{listingfile}"))
    print("Cleaning up...")
    fs.deleteDirNE(tempFolder)