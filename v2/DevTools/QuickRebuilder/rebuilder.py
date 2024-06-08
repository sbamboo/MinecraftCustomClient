import os, argparse, json, shutil, subprocess

from libs.stringTags import formatStringTags

def fprint(inp,prefix=True):
    if prefix == True:
        inp = "[{f.magenta}ReBuilder{r}] "+inp
    print(formatStringTags(inp))

parent = os.path.dirname(__file__)
repoFolder = os.path.abspath(os.path.join(parent,"..","..","Repo"))
repoFile = os.path.join(repoFolder,"repo.json")
packagesFolder = os.path.join(repoFolder,"Packages")

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description='Rebuilding Tool')
parser.add_argument('-packs', type=str, help='Packnames split by comma.')
parser.add_argument('-epacks', type=str, help='Packnames to exclude split by comma.')
parser.add_argument('-enc', type=str, help='The file encoding to use.')
parser.add_argument('--skipGitSync', help='Skip git-pulling.', action='store_true')
args = parser.parse_args()

# Handle enc
if args.enc:
    encoding = args.enc
else:
    encoding = "utf-8"

foundFolders = []
foundFiles = []
found = {}
repoData = {}

if args.skipGitSync != True:
    fprint("{f.darkyellow}Retriving git repository root path...{r}")
    try:
        root_path_bytes = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'])
        root_path = root_path_bytes.decode('utf-8').strip()
        fprint("{f.darkblue}Found: '{f.darkgray}"+str(root_path)+"'{r}")
    except:
        root_path = None
    if root_path != None and os.path.exists(root_path):
        fprint("{f.darkyellow}Pulling repository:{r}")
        olddir = os.getcwd()
        os.chdir(root_path)
        os.system('git pull')
        fprint("{f.darkgreen}Done!{r}")
        os.chdir(olddir)

fprint("{f.darkyellow}Discovering modpacks in local repos...{r}")

if os.path.exists(repoFile):
    repoData = json.loads(open(repoFile,'r',encoding=encoding).read())

[foundFolders.append(entry) if os.path.isdir(os.path.join(packagesFolder,entry)) else foundFiles.append(entry) for entry in os.listdir(packagesFolder)]

for folder in foundFolders:
    found[folder] = {
        "folderPath": os.path.join(packagesFolder,folder),
        "filePath": "",
        "repoEntry": {}
    }

mapping = {}
for name in list(found.keys()):
    mapping[name.split("-quickcompile")[0].replace(" ","-") if "-quickcompile" in name else name.replace(" ","-")] = name

for file in foundFiles:
    shortName = os.path.splitext(file)[0]
    if "-quickcompile" in shortName:
        parts = shortName.split("_")
        shortName = shortName.replace("_"+parts[-1],"").replace("_"+parts[-2],"")
    
    if shortName in list(mapping.keys()):
        found[mapping[shortName]]["filePath"] = os.path.join(packagesFolder,file)

for name in found.keys():
    format_ = repoData.get("format")
    if format_ == 1:
        flavors_ = repoData.get("flavors")
        flavorNames = {}
        [flavorNames.__setitem__(x["name"],i) for i,x in enumerate(flavors_)]
        if name in flavorNames.keys():
            found[name]["repoEntry"] = flavors_[flavorNames[name]]

toIncl = list(found.keys())

if args.packs:
    toIncl = []
    for p in args.packs.split(","):
        if p in found.keys():
            toIncl.append(p)

if args.epacks:
    for p in args.epacks.split(","):
        if p in found.keys():
            toIncl.remove(p)

fprint("{f.darkblue}Found "+str(len(toIncl))+" items. (Filtered amount){r}")
fprint("{f.darkyellow}Ensuring temp/backup folders...{r}")

# Make temp folder
tempFolder = os.path.join(parent,".temp")
if os.path.exists(tempFolder): shutil.rmtree(tempFolder)
os.mkdir(tempFolder)

# Make backup folder
backupFolder = os.path.join(parent,".backup")
if os.path.exists(backupFolder): shutil.rmtree(backupFolder)
os.mkdir(backupFolder)

fprint("{f.darkgreen}Done!{r}")
fprint("{f.darkblue}Backing up current builds:{r}")

# Iterate over the toIncl packs
for i,incl in enumerate(toIncl):
    procStr = "  ({f.darkmagenta}≈"+str(round(i/(len(toIncl)-1)*100))+"%{f.darkgray})"
    fprint("{f.darkgreen} - {f.darkgray}"+incl+procStr+"{r}")
    # Make a folder for them in both temp and backup
    folName = os.path.basename(found[incl]["folderPath"])
    temName = os.path.join(tempFolder,folName)
    bacName = os.path.join(backupFolder,folName)
    if os.path.exists(temName): shutil.rmtree(temName)
    os.mkdir(temName)
    
    # Backup old version
    if os.path.exists(bacName): shutil.rmtree(bacName)
    shutil.copytree(found[incl]["folderPath"], bacName)

# Make new soure.QuickInstaller.py file
# Unpack the old build-source into the enviroment, swap the source.QuickInstaller.py files and remember to change the <replacable:> tags
# Remove the old build-source and archive this one
# Build with the new enviroment
# ^ If succeeds remove old build-file and copy over new one, also update repo-entry.
# ^ If fails remove enviroment, new-build-source and replace with the backups, then remove the backups.
# Remove temp folder

# DURING ABOVE BE VERBOSE WITH COLORS
