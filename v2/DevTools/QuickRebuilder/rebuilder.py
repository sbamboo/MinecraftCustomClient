import os, argparse, json

parent = os.path.dirname(__file__)
repoFolder = os.path.abspath(os.path.join(parent,"..","..","Repo"))
repoFile = os.path.join(repoFolder,"repo.json")
packagesFolder = os.path.join(repoFolder,"Packages")

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description='Rebuilding Tool')
parser.add_argument('-packs', type=str, help='Packnames split by comma.')
parser.add_argument('-epacks', type=str, help='Packnames to exclude split by comma.')
parser.add_argument('-enc', type=str, help='The file encoding to use')
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

# Make new soure.QuickInstaller.py file
# Iterate over the toIncl packs, backup their build (for win,lnx,mac if found) and their old-build-source,
# Unpack the old build-source into the enviroment, swap the source.QuickInstaller.py files and remember to change the <replacable:> tags
# Remove the old build-source and archive this one
# Build with the new enviroment
# ^ If succeeds remove old build-file and copy over new one, also update repo-entry.
# ^ If fails remove enviroment, new-build-source and replace with the backups, then remove the backups.

# DURING ABOVE BE VERBOSE WITH COLORS