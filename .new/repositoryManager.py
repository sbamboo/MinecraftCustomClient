# File to update/create/remove repositories
# [Imports]
import os
import sys
import argparse
import json
import uuid
import requests
from datetime import datetime

# [Settings]
debugPrefix = "\033[90m[\033[35mRepoMan\033[90m]\033[0m "
debugEnabled = True
listingFormat = 1
forceOffline = False # Debug
def_repoAuthor = "Someone"
def_repoVersion = "0.0"

# [Arguments]
cparser = argparse.ArgumentParser(prog="MinecraftCustomClient_DevTools: repositoryManager.py")
# Options
cparser.add_argument('-repositoryFile','-repoFile','-rf', dest="repoFile", help="The path to the repoFile.")
cparser.add_argument('-repoAuthor', dest="repoAuthor", help='The author to the repository.')
cparser.add_argument('-repoVersion', dest="repoVersion", help='The version to the repository.')
cparser.add_argument('-flavorName', dest="flavorName", help='The name of the flavor to add.')
cparser.add_argument('-flavorDesc', dest="flavorDesc", help='The description of the flavor to add.')
cparser.add_argument('-flavorSourceType','-sourceType', dest="flavorSourceType", help='The source type to use.')
cparser.add_argument('-flavorSource', dest="flavorSource", help='The source to use.')
cparser.add_argument('-flavorArchiveType','-archiveType', dest="flavorArchiveType", help='LE: Archive type, reffer docs')
cparser.add_argument('-flavorDataFile','-dataFile', dest="flavorDataFile", help='LE: The data file to use, reffer docs')
cparser.add_argument('-flavorLauncherIcon','-launcherIcon', dest="flavorLauncherIcon", help='LE: Launcher icon, reffer docs')
cparser.add_argument('-flavorModLoader','-modLoader', dest="flavorModLoader", help='LE: Modloader, reffer docs')
cparser.add_argument('-flavorModLoaderVer','-modLoaderVer', dest="flavorModLoaderVer", help='LE: Modloader Version, reffer docs')
cparser.add_argument('-flavorMinecraftVer','-minecraftVer','-mcVer', dest="flavorMinecraftVer", help='LE: Minecraft Version, reffer docs')
cparser.add_argument('-bwcinstallLocation', dest="bwc_installLocation", help='BackwardsCompat: Install Location')
cparser.add_argument('--flavorHidden','--hidden', dest="flavorHidden", help='Is it tagged hidden?', action='store_true')
cparser.add_argument('--flavorSupported','--supported', dest="flavorSupported", help='Is it tagged supported?', action='store_true')
cparser.add_argument('--create', dest="createRepo", help='Creates a repository.', action='store_true')
cparser.add_argument('--update', dest="updateRepo", help='Updates a repository.', action='store_true')
cparser.add_argument('--template', dest="createTemplate", help='Creates a template for a flavor.', action='store_true')
cparser.add_argument('--add', dest="addFlavor", help='Adds a flavor.', action='store_true')
cparser.add_argument('--silent', dest="silent", help='If given the script will only prompt the user and not print anything else.', action='store_true')
cparser.add_argument('--backwardsCompat',dest="backwardsCompat",help="When using legacy sourceType: Includes extra fields for backwards compatability.", action='store_true')
cparser.add_argument('--bwcNoAllowcopy',dest="bwc_noAllowCopy",help="BackwardsCompat: AllowCopy Tag=False", action='store_true')
# Create main arguments object
argus = cparser.parse_args()

# [Setup]
repoFile = os.path.abspath(argus.repoFile)
repoAuthor = def_repoAuthor
repoVersion = def_repoVersion
if argus.repoAuthor != None: repoAuthor = argus.repoAuthor
if argus.repoVersion != None: repoVersion = argus.repoVersion

# [Functions]
# Function to check for an internet connection
def has_connection(override_url=None) -> bool:
    if forceOffline == True: return False # This is here to simulate no internet :P 
    if override_url == None: override_url = "https://google.com" # If no url is given, default to google.com
    # Check/Validate the connection, catch exceptions and return boolean
    try:
        req = requests.get(override_url)
        return True
    except:
        return False

# [Classes]
class debugOut():
    def __init__(self,enabled,prefix):
        self.enabled = enabled
        self.prefix = prefix
    def pr(self,msg):
        if self.enabled == True:
            print(self.prefix+msg+"\033[0m")
d = debugOut(debugEnabled, debugPrefix)

# [Create]
if argus.createRepo == True:
    # Create file
    d.pr("\033[33mStarting creation of repo file...")
    d.pr(f"\033[90m({repoFile})")
    d.pr("\033[33mGenerating data...")
    # Prep data
    repoData = {
        "format":  listingFormat,
        "author":  repoAuthor,
        "version": repoVersion,
        "created": datetime.now().strftime("%Y-%m-%d"),
        "lastUpdated": datetime.now().strftime("%Y-%m-%d"),
        "flavors": []
    }
    repoData_json = json.dumps(repoData)
    open(repoFile,"w").write(repoData_json)
    d.pr("\033[32mDone!")

# [UpdateInfo]
if argus.updateRepo == True:
    # Get file
    d.pr("\033[33mGetting content of file...")
    d.pr(f"\033[90m({repoFile})")
    _json = json.loads( open(repoFile,"r").read() )
    # Apply changes
    repoData = {
        "format":  listingFormat,
        "author":  repoAuthor,
        "version": repoVersion,
        "created": datetime.now().strftime("%Y-%m-%d"),
        "lastUpdated": datetime.now().strftime("%Y-%m-%d"),
        "flavors": []
    }
    d.pr("\033[33mApplying changes...")
    _json |= repoData
    repoData_json = json.dumps(_json)
    open(repoFile,"w").write(repoData_json)
    d.pr("\033[32mDone!")
    
# [Create Flavor Template] Taking: sourceType and --backwardsCompat
if argus.createTemplate == True:
    sourceType = argus.flavorSourceType
    backwardsCompat = argus.backwardsCompat
    _id = str(uuid.uuid4())
    # Get file
    d.pr("\033[33mGetting content of file...")
    d.pr(f"\033[90m({repoFile})")
    _json = json.loads( open(repoFile,"r").read() )
    # Generate Template
    d.pr(f"\033[33mGenerating template for sourceType: {sourceType}...")
    flavorData = {
        "name": "<Name Here>",
        "desc": "<Desc Here>",
        "id": _id,
        "hidden": False,
        "supported": True,
        "sourceType": sourceType
    }
    if sourceType == "urlListing":
        flavorData["source"] = "<Url>"
    elif sourceType == "included": 
        flavorData["source"] = "<FullListingJson>"
    elif sourceType == "legacy":
        flavorData["source"] = {
            "url": "<Url>",
            "archiveType": "<ArchiveType>",
            "flavorDataFile": "<fileName>",
            "launcherIcon": "",
            "modLoader": "<ModLoader>",
            "modLoaderVer": "<ModLoaderVer>",
            "minecraftVer": "<minecraftVer>"
        }
    elif sourceType == "legacyB64":
        flavorData["source"] = {
            "base64": "<base64>",
            "archiveType": "<ArchiveType>",
            "flavorDataFile": "<fileName>",
            "launcherIcon": "",
            "modLoader": "<ModLoader>",
            "modLoaderVer": "<ModLoaderVer>",
            "minecraftVer": "<minecraftVer>"
        }
    if sourceType == "legacy" or sourceType == "legacyB64":
        if backwardsCompat == True:
            d.pr(f"\033[33mApplied backwardsCompatability.")
            flavorData["source"]["backwardsCompat"] = {
                "installLocation": "<InstallPathRelativeToRoot>",
                "allowCopy": True
            }
    # Save to file
    d.pr("\033[33mApplying changes...")
    _json["flavors"].append(flavorData)
    repoData_json = json.dumps(_json)
    open(repoFile,"w").write(repoData_json)
    d.pr("\033[32mDone!")

# [Add modpack] generate id and return
name = argus.flavorName
desc = argus.flavorDesc

_id = str(uuid.uuid4())
hidden = argus.flavorHidden
supported = argus.flavorSupported
sourceType = argus.flavorSourceType
sourceInluded = argus.flavorSource
sourceUrl = argus.flavorSource
LE_url = argus.flavorSource
LE_base64 = argus.flavorSource
LE_dataFile = argus.flavorDataFile
LE_modLoader = argus.flavorModLoader
LE_modLoaderVer = argus.flavorModLoaderVer
LE_minecraftVer = argus.flavorMinecraftVer
bwc_installLocation = argus.bwc_installLocation
bwc_allowCopy = True
if argus.bwc_noAllowCopy == True: bwc_allowCopy == False

# [Remove modpack] by id or by name
name = argus.flavorName
_id = argus.flavorName # When searching by id use --flavorName param

# [Add listing] add a listing either included or url and cli for name/desc and generate id
sourceType = argus.flavorSourceType
sourceInluded = argus.flavorSource
sourceUrl = argus.flavorSource
_id = str(uuid.uuid4())