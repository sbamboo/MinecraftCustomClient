# [Imports]
from _jarRetrival import getJarByFilename,MJRL
import json
import sys
import os
import requests
import base64
try:
    from os import scandir
except ImportError:
    from scandir import scandir
import argparse
from datetime import datetime

# [Settings]
debugPrefix = "\033[90m[\033[35mDevList\033[90m]\033[0m "
debugEnabled = True
listingFormat = 1
archiveExtensions = ["zip","package"]
forceOffline = False # Debug

# [Arguments]
cparser = argparse.ArgumentParser(prog="MinecraftCustomClient_DevTools: createListing.py")
# Options
cparser.add_argument('-modpack','-modpackpath','-mp','-mpp', dest="modpack", help="The path to the modpack to use.")
cparser.add_argument('-modloader','-loader','-ml', dest="modloader", help="The modloader to use.")
cparser.add_argument('-modloaderVersion','-modloaderVer','-loaderVer','-mlv', dest="modloaderVer", help="The modloader version to use.")
cparser.add_argument('-minecraftVersion','-mcVer','-mcv', dest="mcVer", help="The minecraft version this modpack targets.")
cparser.add_argument('-name','-n', dest="name", help="The name of the modpack. (Default is modpack folder name)")
cparser.add_argument('-version','-ver','-v', dest="version", help="The version of the modpack. (Default: '0.0')")
cparser.add_argument('-destination','-dest','-d', dest="destination", help="Which filepath to save the listing to. (Default is root of this file)")
cparser.add_argument('-customDeclare','-cd', dest="customDeclarations", help='Json string with custom entries to add to list. ([ {"type":"<type>","url":"<url>","filename":"<filename>"} / {"<filename>":"<url>"} ])')
cparser.add_argument('-launcherIcon','-icon','-li', dest="launcherIcon", help='Base64 in format: "data:image/png;base64,<base64>" or a direct link to the image')
cparser.add_argument('-missingActionStr', dest="missingActionStr", help='An action string to use for missing links.')
cparser.add_argument('-archiveActionStr', dest="archiveActionStr", help='An action string to use for archives.')
cparser.add_argument('--silent', dest="silent", help='If given the script will only prompt the user and not print anything else.', action='store_true')
# Create main arguments object
argus = cparser.parse_args()

# [Setup]
modpack  = argus.modpack
mods     = os.path.join(modpack,"mods")
manifest = os.path.join(modpack,f"minecraftinstance.json")
urls = []
lookedAtFiles = []
if argus.silent == True: debugEnabled = False

# [Functions]
# Function to yeild a iterable of pathobjects
def scantree(path=str()):
        '''Filesys: Returns a scantree of a path.'''
        for entry in scandir(path):
            if entry.is_dir(follow_symlinks=False):
                yield from scantree(entry.path)
            else:
                yield entry
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

# Retrive URLS
d.pr(f"\033[33mScanning mods directory of: '{modpack.split(os.sep)[-1]}'")
pathObjects = scantree(mods)
possProfile = os.path.join(modpack,"profile.json")
profileData = {}
filename_to_slug = {}
if os.path.exists(possProfile):
    profileData = json.loads(open(possProfile,'r',encoding="utf-8").read())
    projs = profileData.get("projects")
    if projs != None:
        for key,value in projs.items():
            fn = os.path.basename(key)
            if value.get("metadata") != None:
                if value["metadata"].get("project") != None:
                    if value["metadata"]["project"].get("slug") != None:
                        filename_to_slug[fn] = value["metadata"]["project"]["slug"]
for obj in pathObjects:
    if obj.name.endswith(".jar"):
        # From modrinth
        if has_connection() == True and obj.name not in lookedAtFiles:
            modrinth = MJRL("sbamboo/MinecraftCustomClient")
            name = obj.name
            name = name.replace("-", " ")
            name = name.replace("_", " ")
            suggestedProject = name.split(" ")[0]
            nameHits = modrinth.SearchForQuery(suggestedProject, suggestedProject)
            if len(nameHits) > 0:
                retrivedUrls = modrinth.GetLinksPerFilename(suggestedProject,obj.name)
                if len(retrivedUrls) > 0:
                    lookedAtFiles.append(obj.name)
                    for url in retrivedUrls:
                        urls.append({"type":"modrinth","url":url,"filename":obj.name})
                        d.pr(f"\033[32mFound url on modrinth \033[90m: \033[32m{url}")
            else:
                # check slugs
                try:
                    retrivedUrls = modrinth.GetLinksPerFilename(filename_to_slug[obj.name],obj.name)
                except:
                    retrivedUrls = []
                if len(retrivedUrls) > 0:
                    lookedAtFiles.append(obj.name)
                    for url in retrivedUrls:
                        urls.append({"type":"modrinth","url":url,"filename":obj.name})
                        d.pr(f"\033[32mFound url on modrinth \033[90m: \033[32m{url}")
        # From curseforgeManifest
        if os.path.exists(manifest) and obj.name not in lookedAtFiles:
            retrivedUrls = getJarByFilename("curseforge",obj.name,curseforgeManifest=manifest)
            if len(retrivedUrls) > 0:
                lookedAtFiles.append(obj.name)
                for url in retrivedUrls:
                    urls.append({"type":"curseforgeManifest","url":url,"filename":obj.name})
                    d.pr(f"\033[34mFound url in manifest \033[90m: \033[34m{url}")
        elif obj.name not in lookedAtFiles:
            d.pr(f"\033[31mNo network, modrinth?  \033[90m: \033[31m{obj.name}")
    # Non jar files
    else:
        if obj.name.split(".")[-1] in archiveExtensions:
            urls.append({"type":"temp:archive","url":obj.path,"filename":obj.name})
        else:
            d.pr(f"\033[93mFound non-jar file    \033[90m: \033[93m{obj.name}")

# Not looked over files
d.pr(f"\033[33mListing non founds...")
notFounds = []
pathObjects = scantree(mods)
for obj in pathObjects:
    if obj.name not in lookedAtFiles and obj.name.endswith(".jar"):
        urls.append({"type":"notFound","url":obj.path,"filename":obj.name})
        notFounds.append(obj.name)
# Prints out the files not found with a number (this number will work up to 9999)
for _id,entry in enumerate(notFounds):
    prem = f"\033[90m{_id}: \033[91mNo url found for"
    spacing = 4
    spacing = spacing - len(str(_id))
    d.pr(prem+spacing*" "+f"\033[90m: \033[91m{entry}")
if len(notFounds) == 0:
    d.pr(f"\033[33m ^^^ Empty             \033[90m(Al found files were listed above)")
else:
    if argus.missingActionStr:
        actionString = argus.missingActionStr
        print(debugPrefix + f"Running automated action: {actionString}")
    else:
        actionString = input(debugPrefix + f"\033[33mNon founds exists, action? \033[90m[\033[35mi\033[90m: ignore, \033[35mm\033[90m: manual, \033[35mb\033[90m: inlude as base64, \033[35ml\033[90m: just don't install, \033[35mEnter\033[90m: ignore, To not apply to al use '<action>:<indexes_sepparated_by_coma>'] "+"\033[0m")
    actionString = (actionString.lower()).strip()
    ids = None
    workingWith = urls.copy()
    modsToAction = {}
    # Specific Indexes
    if ":" in actionString:
        actions = actionString.split(" ")
        for action in actions:
            # Get elements
            act = action.split(":")[0]
            ids = action.split(":")[-1]
            if ids == "":
                for fname in notFounds:
                    if modsToAction.get(fname) == None:
                        modsToAction[fname] = act
            else:
                ids = ids.split(",")
                # Get names of files that map to the given ids
                for i,_id in enumerate(ids):
                    ids[i] = int(ids[i])
                # Add to list
                for i,name in enumerate(notFounds):
                    if i in ids:
                        modsToAction[name] = act
    # Al elements
    else:
        for fname in notFounds:
            modsToAction[fname] = actionString
    # Auto act on non set and count comments
    toComment = {"m":0,"l":0,"i":0,"b":0}
    for mod in notFounds:
        if modsToAction.get(mod) == None or modsToAction.get(mod) == "":
            modsToAction[mod] = "i"
        toComment[modsToAction[mod]] += 1
    # Comment
    if toComment['b'] > 0: d.pr(f"\033[33mIncluding {toComment['b']}st file(s) as base64...")
    if toComment['m'] > 0: d.pr(f"\033[33mAdding the comment '\033[32m<ManualUrlWaitingToBeFilledIn>\033[33m' for {toComment['m']}st mod(s), and setting type to 'custom'...")
    if toComment['l'] > 0: d.pr(f"\033[33mSetting the type to 'filenameOnly' for {toComment['l']}st mod(s)...")
    if toComment['i'] > 0: d.pr(f"\033[33mIgnoring {toComment['i']}st mod(s)...")
    # Carry out actions
    for fname,action in modsToAction.items():
        if action == "b":
            for i,url in enumerate(workingWith):
                if url["type"] == "notFound" and url["filename"] == fname:
                    try:
                        with open(workingWith[i]["url"], 'rb') as file:
                            file_contents = file.read()
                            base64_encoded = base64.b64encode(file_contents).decode('utf-8')
                    except IOError as e:
                        d.pr("\033[31mFailed to read base64 file!")
                        base64_encoded = None
                    workingWith[i]["base64"] = base64_encoded
                    workingWith[i]["url"] = None
                    workingWith[i]["type"] = "customB64"
        elif action == "m":
            for i,url in enumerate(workingWith):
                if url["type"] == "notFound" and url["filename"] == fname:
                    workingWith[i]["url"] = "<ManualUrlWaitingToBeFilledIn>"
                    workingWith[i]["type"] = "custom"
        elif action == "l":
            for i,url in enumerate(workingWith):
                if url["type"] == "notFound" and url["filename"] == fname:
                    workingWith[i]["type"] = "filenameOnly"
        elif action == "i":
            toRemove = []
            for i,url in enumerate(workingWith):
                if url["type"] == "notFound" and url["filename"] == fname:
                    toRemove.append(i)
            toRemove = toRemove[::-1]
            for i in toRemove:
                workingWith.pop(i)
    urls = workingWith

# Work with archives files
archives = []
for url in urls:
    if url["type"] == "temp:archive":
        archives.append(url)
d.pr(f"\033[33mListing archives...")
# Prints out the found archives with a number (this number will work up to 9999)
for _id,entry in enumerate(archives):
    prem = f"\033[90m{_id}: \033[91mArchive file"
    spacing = 8
    spacing = spacing - len(str(_id))
    d.pr(prem+spacing*" "+f"\033[90m: \033[91m{entry['filename']}")
if len(archives) == 0:
    d.pr(f"\033[33m ^^^ Empty             \033[90m(Al found files were listed above)")
else:
    if argus.archiveActionStr:
        actionString = argus.archiveActionStr
        print(debugPrefix + f"Running automated action: {actionString}")
    else:
        actionString = input(debugPrefix + f"\033[33mSome archives were found? \033[90m[\033[35mi\033[90m: ignore, \033[35mb\033[90m: include as base64, \033[35ml\033[90m: just don't install, \033[35mEnter\033[90m: ignore, To not apply to al use '<action>:<indexes_sepparated_by_coma>'] "+"\033[0m")
    actionString = (actionString.lower()).strip()
    ids = None
    workingWith = urls.copy()
    archivesToAction = {}
    # Specific Indexes
    if ":" in actionString:
        actions = actionString.split(" ")
        for action in actions:
            # Get elements
            act = action.split(":")[0]
            ids = action.split(":")[-1]
            if ids == "":
                for archive in archives:
                    if archivesToAction.get(fname) == None:
                        archivesToAction[archive["filename"]] = act
            else:
                ids = ids.split(",")
                # Get names of files that map to the given ids
                for i,_id in enumerate(ids):
                    ids[i] = int(ids[i])
                # Add to list
                for i,name in enumerate(archives):
                    if i in ids:
                        archivesToAction[name["filename"]] = act
    # Al elements
    else:
        for archive in archives:
            archivesToAction[archive["filename"]] = actionString
    # Auto act on non set and count comments
    toComment = {"b":0,"l":0,"i":0}
    for archive in archives:
        if archivesToAction.get(archive["filename"]) == None or archivesToAction.get(archive["filename"]) == "":
            archivesToAction[archive["filename"]] = "i"
        toComment[archivesToAction[archive["filename"]]] += 1
    # Comment
    if toComment['b'] > 0: d.pr(f"\033[33mIncluding {toComment['b']}st file(s) as base64...")
    if toComment['l'] > 0: d.pr(f"\033[33mSetting the type to 'filenameOnly' for {toComment['l']}st file(s)...")
    if toComment['i'] > 0: d.pr(f"\033[33mIgnoring {toComment['i']}st file(s)...")
    # Carry out actions
    for fname,action in archivesToAction.items():
        if action == "b":
            for i,url in enumerate(workingWith):
                if url["type"] == "temp:archive" and url["filename"] == fname:
                    try:
                        with open(workingWith[i]["url"], 'rb') as file:
                            file_contents = file.read()
                            base64_encoded = base64.b64encode(file_contents).decode('utf-8')
                    except IOError as e:
                        d.pr("\033[31mFailed to read base64 file!")
                        base64_encoded = None
                    workingWith[i]["base64"] = base64_encoded
                    workingWith[i]["url"] = None
                    workingWith[i]["type"] = "customArchiveB64"
        elif action == "l":
            for i,url in enumerate(workingWith):
                if url["type"] == "temp:archive" and url["filename"] == fname:
                    workingWith[i]["url"] = None
                    workingWith[i]["type"] = "filenameOnly"
        elif action == "i":
            toRemove = []
            for i,url in enumerate(workingWith):
                if url["type"] == "temp:archive" and url["filename"] == fname:
                    toRemove.append(i)
            toRemove = toRemove[::-1]
            for i in toRemove:
                workingWith.pop(i)
    urls = workingWith

# Apply presets to arguments
if argus.name == None: argus.name = os.path.basename(modpack)
if argus.version == None: argus.version = "0.0"
if argus.destination == None: argus.destination = os.path.join( os.path.abspath(os.path.dirname(__file__)), "listing.json" )

# Add in custom declarations if provided
if argus.customDeclarations != None:
    customDeclareData = []
    if argus.customDeclarations.startswith("{") and argus.customDeclarations.endswith("}"): argus.customDeclarations = "[" + argus.customDeclarations + "]"
    customDeclareDict = json.loads(argus.customDeclarations)
    d.pr(f"\033[33mAdding {len(customDeclareDict)}st custom declaration(s)...")
    for declare in customDeclareDict:
        if declare.get("type") == None:
            key,value = list(declare.keys())[0], list(declare.values())[0]
            customDeclareData.append( {"type":"custom","url":value,"filename":key} )
        else:
            customDeclareData.append(declare)
    urls.extend(customDeclareData)

# Assemble listing file
listingData = {
    "format": listingFormat,
    "name": argus.name,
    "version": argus.version,
    "modloader": argus.modloader,
    "modloaderVer": argus.modloaderVer,
    "minecraftVer": argus.mcVer,
    "created": datetime.now().strftime("%Y-%m-%d"),
    "launcherIcon": argus.launcherIcon,
    "sources": urls,
    "sourceLength": len(urls)
}

# Put to file
destinationFile = argus.destination
json = json.dumps(listingData)
if os.path.exists(destinationFile): os.remove(destinationFile)
open(destinationFile,'w').write(json)