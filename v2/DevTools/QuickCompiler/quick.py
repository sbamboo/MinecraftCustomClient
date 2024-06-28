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
import json
import shutil
from libs.configTui_wrapper.wrapper_with_crshModuloTools import configTui_WrapperMain
import platform
import uuid

def generate_uuid():
    return str(uuid.uuid4())

def autoBool(val):
    if type(val) == bool:
        return val
    else:
        if val.lower() == "true":
            return True
        elif val.lower() == "false":
            return False

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
iconTmp = f"{tempFolder}{os.sep}icon.tmp"

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description='Quick compiler')
parser.add_argument('-path', type=str, help='The path to the modpacks folder')
parser.add_argument('-cmpl', type=str, help='The compile.yml file')
parser.add_argument('-enc', type=str, help='The file encoding to use')
parser.add_argument('--prioCF', dest="prio_curseforge", help='If given the script will prioritize looking at curseforge.', action='store_true')
parser.add_argument('--skipProjId', dest="curseforge_skip_project_id", help="If given the script will not include curseforge projectId's.", action='store_true')
args = parser.parse_args()

usable_UUID = generate_uuid()

# Handle enc
if args.enc:
    encoding = args.enc

# Check path
if fs.notExist(args.path):
    print(f"Invalid modpack path: {args.path}")
    exit()

# Get sent compile
built_in_compile = os.path.join(args.path,"compile.yml")
if os.path.exists(built_in_compile) and args.cmpl == None:
    args.cmpl = built_in_compile

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

compyml["name"] = fs.makeWinPathSafe(compyml["name"])

# pull
if compyml.get('gitsync') == True:
    import subprocess
    print("Retriving git repository root path...")
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

# To long icon
iconTx = compyml["icon"]
if "data:image/png;base64" in iconTx:
    open(iconTmp,'x',encoding="utf-8").write(iconTx)
    iconTx = "iconTmp:" + iconTmp

# Run jar retriver
nonAllowed = ["",None]
command = f' -modpack "{args.path}" -dest "{listing}"'
command += f' -mcVer "{compyml["minecraftVer"]}"'
command += f' -loader "{compyml["modloader"]}"'
command += f' -loaderVer "{compyml["modloaderVer"]}"'
command += f' -name "{compyml["name"]}"'
if compyml.get("ver") not in nonAllowed:
    command += f' -ver "{compyml["version"]}"'
if compyml.get("icon") not in nonAllowed:
    command += f' -icon "{iconTx}"'
if compyml.get("lister") not in nonAllowed:
    if compyml["lister"].get("silent") == True:
        command += " --silent"
    if compyml["lister"].get("missingLinkAction") not in nonAllowed:
        command += f' -missingActionStr "{compyml["lister"]["missingLinkAction"]}"'
    if compyml["lister"].get("archiveFoundAction") not in nonAllowed:
        command += f' -archiveActionStr "{compyml["lister"]["archiveFoundAction"]}"'
if args.prio_curseforge == True:
    command += " --prioCF"
if args.curseforge_skip_project_id != True:
    command += " --addProjId"

os.system(f"python3 {lister} {command}")
print("")

# Check for manual includes and prompt user regarding it:
content = open(listing,'r',encoding=encoding).read()
if "<ManualUrlWaitingToBeFilledIn>" in content and compyml["lister"].get("promptOnManual") == True:
    print("Found files selected for manual include, do you want to open the modpack here to be able to include the files?")
    print(f"File: {listing}")
    c = input("(Obs! You can make changes to the file yourself, if you wait with answering this prompt) [Y/N] ")
    if c.lower() == "y":
        print("Lovely, opening in configTUI... (Creds: https://github.com/Prudhvi-pln/ConfigTUI)")
        configTui_WrapperMain(listing)
    else:
        print("Okay, remember to change on install :P")

# Include webinclude
wincl = compyml.get("webInclude")
if wincl != None:
    print(f"Including '{wincl}' as webInclude...")
    _content = json.loads(content)
    _content["webInclude"] = wincl
    content = json.dumps(_content)
    open(listing,'w',encoding=encoding).write(content)

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
    newfile = f"{compyml['name'].replace(' ','-')}_{fs.getFileName(zipfile)}.mListing"
    reptype = "mlisting"
    fs.renameFile(zipfile,newfile)
    newfile = f"{parent}{os.sep}{newfile}"
    os.chdir(olddir)

else:
    listingfile = f"{os.path.basename(tempFolder)}.listing"
    print(f"Writing modpack... ({listingfile})")
    newfile = f"{parent}{os.sep}{compyml['name'].replace(' ','-')}_{listingfile}"
    reptype = "urlListing"
    fs.copyFile(listing,newfile)
    print("Cleaning up...")
    fs.deleteDirNE(tempFolder)

# add to repo file
gitsp = compyml.get("gitsyncPath")
if gitsp != None:
    gitsp = gitsp.replace("{compiler}",parent)
    if gitsp.startswith(".\\"):
        gitsp = gitsp.replace(".\\",os.path.dirname(args.cmpl),1)
    elif gitsp.startswith("./"):
        gitsp = gitsp.replace("./",os.path.dirname(args.cmpl),1)

    if newfile != None:
        # file
        print("Copying to repo...")
        pkgs = f"{gitsp}{os.sep}Packages"
        if fs.notExist(pkgs):
            fs.createDir(pkgs)
        destfile = f"{pkgs}{os.sep}{os.path.basename(newfile)}"
        fs.copyFile(newfile,destfile)
        fs.deleteFile(newfile)
        # repofile
        poss = f"{gitsp}{os.sep}repo.json"
        if fs.doesExist(poss):
            print(f"Attempting to create repostitory instance in: ({os.path.abspath(gitsp)})")
            # get content
            raw = open(poss,'r',encoding=encoding).read()
            dRepo = json.loads(raw)
            # get url
            try:
                listurl = compyml["gitsyncBURL"] + "/Packages/" + os.path.basename(newfile)
            except:
                listurl = ""
            # get id
            listuuid = usable_UUID
            # make entry
            entryWa = {
                "name": compyml['name'],
                "desc": compyml['desc'],
                "author": compyml['author'],
                "id": listuuid,
                "hidden": autoBool(compyml['hidden']),
                "supported": True,
                "sourceType": reptype,
                "source": listurl
            }
            # add entry if not exist with same id
            exists = False
            for entry in dRepo.get("flavors"):
                if entry["id"] == listuuid:
                    exists = True
                    break
            if exists == False:
                dRepo["flavors"].append(entryWa)
            # save repo
            if dRepo.get("lastUpdated") != None:
                dRepo["lastUpdated"] = datetime.now().strftime('%Y-%m-%d')
            jRepo = json.dumps(dRepo)
            open(poss,'w',encoding=encoding).write(jRepo)
        # bundle
        if compyml.get("bundle") == True:
            print("Bundling quickinstaller...")
            destfolder = os.path.join(gitsp,"Packages",compyml['name'])
            fs.ensureDirPath(destfolder)
            bundleFile = os.path.join(destfolder,"bundle.zip")
            bundleScript = os.path.join(parent,"_bundleQuick.py")
            # create bundle
            os.system(f'{sys.executable} {bundleScript} -modpack "{destfile}" -destzip "{bundleFile}" --inclScripts --skipExcludes -uuid "{str(usable_UUID)}"')
            print("Done!")
        # build
        if compyml.get("build") != None and compyml.get("build") != False:
            print("Prepping build enviroment for quickinstaller...")
            destfolder = os.path.join(gitsp,"Packages",compyml['name'])
            fs.ensureDirPath(destfolder)
            bundleFile = os.path.join(destfolder,"build_source.zip")
            bundleScript = os.path.join(parent,"_bundleQuick.py")
            # create bundle for build-env
            os.system(f'{sys.executable} {bundleScript} -modpack "{destfile}" -destzip "{bundleFile}" --prepbuild -uuid "{str(usable_UUID)}"')
            print("Done!")
            # build
            if compyml["build"].get("autobuildwin") == True:
                print("Attempting to build quickinstaller (win_x86)...")
                # extract build env
                buildenv = os.path.join(os.path.dirname(bundleFile),"build-env")
                shutil.unpack_archive(bundleFile,buildenv)
                # run build-script
                buildScript = os.path.join(buildenv,"build.py")
                if os.path.exists(buildScript) != True:
                    raise Exception("No build script found, invalid build-env!")
                olddir = os.getcwd()
                os.chdir(buildenv)
                os.system(f'{sys.executable} "{buildScript}" --debug')
                os.chdir(buildenv)
                # get exe for quickInstaller
                quickInstExe = os.path.join(buildenv,"QuickInstaller.exe")
                exeDest = os.path.join(destfolder,"build-win_x86")
                fs.ensureDirPath(exeDest)
                fs.copyFile(quickInstExe,os.path.join(exeDest,os.path.basename(quickInstExe)))
                # clean up
                import time
                print("Waiting 2s for process to finish...")
                time.sleep(2)
                print("Continuing...")
                try:
                    shutil.rmtree(buildenv)
                except:
                    print(f"Failed to remove build enviroment, please manually remove: '{os.path.abspath(buildenv)}'")
                print("Done!")