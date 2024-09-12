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
import urllib.parse

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
cparser.add_argument('--prioCF', dest="prio_curseforge", help='If given the script will prioritize looking at curseforge.', action='store_true')
cparser.add_argument('--addProjId', dest="curseforge_ask_project_id", help="If given the script will include curseforge projectId's.", action='store_true')
cparser.add_argument('--skipModrinthIcon', dest="skip_modrinth_icon", help="If given the script will not include icons from modrinth profiles.", action='store_true')
cparser.add_argument('--skipModrinthIndexIcon', dest="skip_modrinth_index_icon", help="If given the script will not use the information in modrinth-export-index files to fetch for icons.", action='store_true')
cparser.add_argument('--matchModrinthIndexDownloads', dest="match_modrinth_index_downloads", help="If given the script will only use a modrinth-export-index file download if it has a matching filename.", action='store_true')
# Create main arguments object
argus = cparser.parse_args()

# [Setup]
modpack  = argus.modpack
mods     = os.path.join(modpack,"mods")
manifest = os.path.join(modpack,f"minecraftinstance.json") #Curseforge Manifest
profile  = os.path.join(modpack,"profile.json") #Modrinth profile
mdrindex = os.path.join(modpack,"modrinth.index.json") #Modrinth Export Index

urls = []
lookedAtFiles = []
if argus.silent == True: debugEnabled = False

if "iconTmp:" in argus.launcherIcon:
    iconTmp = argus.launcherIcon.replace("iconTmp:","",1)
    if os.path.exists(iconTmp):
        argus.launcherIcon = open(iconTmp,'r',encoding="utf-8").read()

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

# Function to get progress str
def getProgStr(_amntFiles=int,_scannedFiles=int):
    proc = str((_scannedFiles/_amntFiles)*100)[:3]
    padding = (len(str(_amntFiles))-len(str(_scannedFiles)))*" "
    if proc.endswith("."):
        proc = proc.rstrip(".")
        padding += " "
    proc += "%"
    build = f"{padding}\033[90m({_scannedFiles}/{_amntFiles}, {proc})\033[0m "
    _scannedFiles += 1
    return build,_scannedFiles

# Function to check curseforge manifest
def checkmanifest(manifest,name,_lookedAtFiles,_urls,_amntFiles,_scannedFiles,curseforgeAskProjId=False):
    if os.path.exists(manifest) and name not in _lookedAtFiles:
        retrivedUrls = getJarByFilename("curseforge",name,curseforgeManifest=manifest,curseforgeAskProjId=curseforgeAskProjId)
        if len(retrivedUrls) > 0:
            _lookedAtFiles.append(name)
            if curseforgeAskProjId == True:
                for url in retrivedUrls:
                    _urls.append({"type":"curseforgeManifest","url":url[0],"filename":name,"curseforgeProjId":url[1]})
                    prog,_scannedFiles = getProgStr(_amntFiles,_scannedFiles)
                    d.pr(f"{prog}\033[34mFound url in manifest \033[90m: \033[34m{url[0]}")
            else:
                for url in retrivedUrls:
                    _urls.append({"type":"curseforgeManifest","url":url,"filename":name})
                    prog,_scannedFiles = getProgStr(_amntFiles,_scannedFiles)
                    d.pr(f"{prog}\033[34mFound url in manifest \033[90m: \033[34m{url}")
    return _lookedAtFiles,_urls,_scannedFiles

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
profileData = None
mdrindexData = None
filename_to_slug = {}
if os.path.exists(profile):
    profileData = json.loads(open(profile,'r',encoding="utf-8").read())
    projs = profileData.get("projects")
    if projs != None:
        for key,value in projs.items():
            fn = os.path.basename(key)
            if value.get("metadata") != None:
                if value["metadata"].get("project") != None:
                    if value["metadata"]["project"].get("slug") != None:
                        filename_to_slug[fn] = value["metadata"]["project"]["slug"]
if os.path.exists(mdrindex):
    mdrindexData = json.loads(open(mdrindex,'r',encoding="utf-8").read())
    
# get list of al jarfiles
entries = []
for obj in pathObjects:
    if os.path.isfile(obj.path):
        entries.append(obj.path)
amntFiles = len(entries)
d.pr(f"\033[34mFound {amntFiles} files.")
scannedFiles = 0

# retrive links
if has_connection():
    modrinth = MJRL("sbamboo/MinecraftCustomClient")
else:
    modrinth = None
for _path in entries:
    _name = os.path.basename(_path)
    if _name.endswith(".jar"):
        # Prio curseforge?
        if argus.prio_curseforge == True:
            lookedAtFiles,urls,scannedFiles = checkmanifest(manifest,_name,lookedAtFiles,urls,amntFiles,scannedFiles,curseforgeAskProjId=argus.curseforge_ask_project_id)
        # From modrinth profile.json
        if profileData != None and type(profileData) == dict and _name not in lookedAtFiles:
            projs = profileData.get("projects")
            if projs != None:
                for projSubPath,projData in projs.items():
                    # match
                    if projData.get("file_name") == _name:
                        # check for url
                        if type(projData["metadata"]["version"]) == dict: # can be str if non-modrinth hosted
                            projFiles = projData["metadata"]["version"].get("files")
                            if projFiles != None and len(projFiles) > 0:
                                _selectedProjFile = None
                                if len(projFiles) > 1:
                                    # iterate for primary
                                    for projFile in projFiles:
                                        if projFile.get("primary") == True:
                                            _selectedProjFile = projFile
                                            break
                                    # fall back to first
                                    if _selectedProjFile == None:
                                        _selectedProjFile = projFiles[0]
                                # if only one select it
                                else:
                                    _selectedProjFile = projFiles[0]
                                
                                # check for url
                                if _selectedProjFile.get("url") != None:
                                    lookedAtFiles.append(_name)
                                    urlData = {"type":"modrinth","url":_selectedProjFile.get("url"),"filename":_name,"modrinthType":"profile"}
                                    # icon?
                                    if argus.skip_modrinth_icon != True:
                                        if projData["metadata"].get("project") != None:
                                            if projData["metadata"]["project"].get("icon_url") != None:
                                                if len(projData["metadata"]["project"]["icon_url"]) > 90:
                                                    if projData["metadata"]["project"].get("id") != None:
                                                        urlData["modrinthIcon"] = "proj:" + str(projData["metadata"]["project"]["id"])
                                                else:
                                                    urlData["modrinthIcon"] = projData["metadata"]["project"]["icon_url"]
                                    # Append
                                    urls.append(urlData)
                                    prog,scannedFiles = getProgStr(amntFiles,scannedFiles)
                                    d.pr(f"{prog}\033[32mFound url in profile \033[90m: \033[32m{_selectedProjFile.get('url')}")

        # From modrinth export index
        if mdrindexData != None and type(mdrindexData) == dict and _name not in lookedAtFiles:
            indexFiles = mdrindexData.get("files")
            if indexFiles != None:
                if len(indexFiles) > 0:
                    for indexFile in indexFiles:
                        if indexFile.get("path") != None:
                            # match
                            if indexFile["path"].endswith(_name):
                                indexDownloadUrl = None
                                # Get download link
                                if argus.match_modrinth_index_downloads:
                                    for x in indexFile.get("downloads"):
                                        # Try exact
                                        if x.endswith(_name):
                                            indexDownloadUrl = x
                                        # Try HTML encoded
                                        elif x.endswith(urllib.parse.quote(_name)):
                                            indexDownloadUrl = x
                                else:
                                    if len(indexFile.get("downloads")) > 0:
                                        indexDownloadUrl = indexFile.get("downloads")[0]
                                # Set
                                if indexDownloadUrl != None:
                                    lookedAtFiles.append(_name)
                                    urlData = {"type":"modrinth","url":indexDownloadUrl,"filename":_name,"modrinthType":"export-index"}
                                    # Icon?
                                    if indexDownloadUrl.startswith("https://cdn.modrinth.com/data/"):
                                        possibleId = indexDownloadUrl.replace("https://cdn.modrinth.com/data/","",1).split("/")[0]
                                        if argus.skip_modrinth_index_icon != True and modrinth != None:
                                            meta = modrinth.GetProject(possibleId)
                                            if type(meta) == dict:
                                                if meta.get("icon_url") != None and meta.get("icon_url") != "":
                                                    if len(meta.get("icon_url")) > 90:
                                                        urlData["modrinthIcon"] = f"proj:{possibleId}"
                                                    else:
                                                        urlData["modrinthIcon"] = meta.get("icon_url")
                                        else:
                                            urlData["modrinthIcon"] = f"proj:{possibleId}"

                                    # Append
                                    urls.append(urlData)
                                    prog,scannedFiles = getProgStr(amntFiles,scannedFiles)
                                    d.pr(f"{prog}\033[32mFound url in exindex \033[90m: \033[32m{indexDownloadUrl}")

        # From modrinth web
        if modrinth != None and _name not in lookedAtFiles:
            name = _name
            name = name.replace("-", " ")
            name = name.replace("_", " ")
            suggestedProject = name.split(" ")[0]
            try:
                nameHits = modrinth.SearchForQuery(suggestedProject, suggestedProject)
            except json.decoder.JSONDecodeError:
                nameHits = []
            if len(nameHits) > 0:
                try:
                    retrivedUrls = modrinth.GetLinksPerFilename(suggestedProject,_name)
                except json.decoder.JSONDecodeError:
                    retrivedUrls = []
                if len(retrivedUrls) > 0:
                    lookedAtFiles.append(_name)
                    for url in retrivedUrls:
                        urls.append({"type":"modrinth","url":url,"filename":_name,"modrinthType":"api"})
                        prog,scannedFiles = getProgStr(amntFiles,scannedFiles)
                        d.pr(f"{prog}\033[32mFound url on modrinth api \033[90m: \033[32m{url}")
            else:
                # check slugs
                try:
                    retrivedUrls = modrinth.GetLinksPerFilename(filename_to_slug[_name],_name)
                except:
                    retrivedUrls = []
                if len(retrivedUrls) > 0:
                    lookedAtFiles.append(_name)
                    for url in retrivedUrls:
                        urls.append({"type":"modrinth","url":url,"filename":_name,"modrinthType":"api/slug"})
                        prog,scannedFiles = getProgStr(amntFiles,scannedFiles)
                        d.pr(f"{prog}\033[32mFound url on modrinth api with slug \033[90m: \033[32m{url}")
                        
        # From curseforgeManifest (no prio)
        if argus.prio_curseforge != True:
            lookedAtFiles,urls,scannedFiles = checkmanifest(manifest,_name,lookedAtFiles,urls,amntFiles,scannedFiles,curseforgeAskProjId=argus.curseforge_ask_project_id)
        elif _name not in lookedAtFiles:
            prog,scannedFiles = getProgStr(amntFiles,scannedFiles)
            d.pr(f"{prog}\033[31mNo network, modrinth? \033[90m: \033[31m{_name}")
    # Non jar files
    else:
        if _name.split(".")[-1] in archiveExtensions:
            urls.append({"type":"temp:archive","url":_path,"filename":_name})
        else:
            prog,scannedFiles = getProgStr(amntFiles,scannedFiles)
            d.pr(f"{prog}\033[93mFound non-jar file    \033[90m: \033[93m{_name}")

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