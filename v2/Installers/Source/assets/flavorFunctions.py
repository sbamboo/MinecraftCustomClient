# Imports
import base64,os,shutil,requests,json,platform,re
import subprocess
import zipfile
import tarfile
import getpass
import uuid
from datetime import datetime
import hashlib

# IncludeInline: ./assets/lib_fancyPants.py

# IncludeInline: ./assets/lib_chibit.py

# FlavorFunctions fix missing filesys instance
try:
    filesys.defaultencoding
except:
    from lib_filesys import filesys as fs

# [Base64 helpers]
def encodeB64U8(str) -> str:
    return base64.b64encode(str).decode('utf-8')

def decodeB64U8(b64) -> str:
    return base64.b64decode(b64.encode('utf-8'))

# [Url helpers]
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

def is_valid_url(url):
    # Regular expression pattern for matching URLs
    url_pattern = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https:// or ftp://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(url_pattern, url) is not None

def download_file_and_get_base64(url):
    try:
        # Fetch the file content
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        # Encode the content as Base64
        base64_content = base64.b64encode(response.content)
        return base64_content.decode('utf-8')  # Convert bytes to string
    except Exception as e:
        print(f"Error downloading and encoding file: {e}")
        return None

# [Functions]
def installListing(listingData=str,destinationDirPath=str,encoding="utf-8",prefix="",skipWebIncl=False,modsHaveLoadingBar=False,chibitDefaultHost=str) -> list:
    '''Returns if gdrive url was found'''
    sources = listingData.get("sources")
    webinclude = listingData.get("webInclude")

    hasGdrive = []

    # handle webinclude
    if webinclude != None and skipWebIncl == False:
        _chibitConnector = ChibitConnector(
            hostUrl = chibit_default_host,
            reqType = "fancypants",
            fancyPantsFuncs = [
                getUrlContent_HandleGdriveVirWarn,
                downloadFile_HandleGdriveVirWarn
            ]
        )
        for incl in webinclude:
            url = list(incl.keys())[0]
            relpathToDest = list(incl.values())[0]
            if relpathToDest.startswith(".\\"):
                relpathToDest = relpathToDest.replace(".\\","",1)
            elif relpathToDest.startswith("./"):
                relpathToDest = relpathToDest.replace("./","",1)
            fpath = os.path.join(destinationDirPath,relpathToDest)
            fpath = fpath.replace("\\",os.sep)
            fpath = fpath.replace("/",os.sep)
            fs.ensureDirPath(os.path.dirname(fpath))
            #downUrlFile(url,fpath)
            components = _chibitConnector.getComponents_FromPrefixedUrl(url)
            if components["valid"] == True:
                backupUrl = components["backupUrl"]
                _url = components["noBackupUrl"]
                if _url in ["",None]: _url = url
                if os.path.exists(fpath):
                    os.remove(fpath)
                try:
                    _chibitConnector.getRawFile_FromPrefixedUrl(
                        prefixedUrl = _url,
                        outputFile = fpath,
                        safe = True,
                        verbose = True,
                        check_encoding = encoding,
                        useTemp = False,
                        tempDir = None
                    )
                except Exception as e:
                    if backupUrl == None:
                        raise
                    else:
                        if "https://drive.google.com/" in url:
                            hasGdrive.append([url,fpath])
                        print(prefix+f"Error downloading chibit-webinclude, attempting to download from backup url... ({e})")
                        downloadFile_HandleGdriveVirWarn(
                            backupUrl,
                            filepath=fpath,
                            handleGdriveVirWarn=True,
                            loadingBar=True,
                            title="[cyan]Downloading webinclude...",
                            handleGdriveVirWarnText="\033[33mFound gdrive scan warning, attempting to extract link and download from there...\033[0m",
                            encoding=encoding,
                            onFileExiError="ignore-with-warn"
                        )
            else:
                if "https://drive.google.com/" in url:
                    hasGdrive.append([url,fpath])
                downloadFile_HandleGdriveVirWarn(
                    url,
                    filepath=fpath,
                    handleGdriveVirWarn=True,
                    loadingBar=True,
                    title="[cyan]Downloading webinclude...",
                    handleGdriveVirWarnText="\033[33mFound gdrive scan warning, attempting to extract link and download from there...\033[0m",
                    encoding=encoding,
                    onFileExiError="ignore-with-warn"
                )
        
    # ensure mods directory
    modsF = os.path.join(destinationDirPath,"mods")
    if fs.notExist(modsF): fs.createDir(modsF)

    # iterate over sources to extract them to the dest
    resources_zip_found = False
    listedNameOnlys = []
    downloadable = ["custom","curseforgeManifest","modrinth"]
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
                with open(destinationDirPath,'wb') as file:
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
                with open(destinationDirPath,'wb') as file:
                    file.write(zipC)
                shutil.unpack_archive(nf,modsF)
        # customB64 (non-archive)
        if _type == "customB64":
            jarC = decodeB64U8(_base64)
            nf = os.path.join(modsF,_filename)
            with open(nf,'wb') as file:
                file.write(jarC)
        # downloadable
        if _type in downloadable:
            if "<ManualUrlWaitingToBeFilledIn>" not in _url:
                #downUrlFile(_url,os.path.join(modsF,_filename))
                _filepath = os.path.join(modsF,_filename)
                downloadFile_HandleGdriveVirWarn(
                    _url,
                    filepath=_filepath,
                    handleGdriveVirWarn=True,
                    loadingBar=modsHaveLoadingBar,
                    title="",
                    handleGdriveVirWarnText="\033[33mFound gdrive scan warning, attempting to extract link and download from there...\033[0m",
                    encoding=encoding,
                    onFileExiError="ignore-with-warn"
                )
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

    # return
    return hasGdrive

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
            shutil.unpack_archive(modpack_path,dest)
    else:
        oldname = os.path.join(dest,os.path.basename(modpack_path))
        newname = os.path.join(dest,"listing.json")
        fs.copyFile(modpack_path,dest)
        fs.renameFile(oldname,newname)
    return dest

def downListingCont(extractedPackFolderPath=str,parentPath=str,encoding="utf-8",prefix="",skipWebIncl=False,modsHaveLoadingBar=False) -> list:
    '''Returns if urls if gdrive url was found'''

    hasGdrive = []

    dest = extractedPackFolderPath
    # get data
    poss = os.path.join(dest,"listing.json")
    # If there is a listing file we must install the listing content
    if fs.doesExist(poss):
        content = open(poss,'r',encoding=encoding).read()
        listing = json.loads(content)
        hasGdrive = installListing(listing,extractedPackFolderPath,encoding,prefix,skipWebIncl,modsHaveLoadingBar)
    else:
        raise FileNotFoundError(f"Could not find listing.json in {dest}!")
    return hasGdrive

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

# Function to scape minor version urls from curseforge website
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

# Function to using the previously scraped link scrape the accuallt installer links
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

# Function to remove the https://adfoc.us/serve/sitelinks/?id=<id>&url= prefix from a url
def _removeAdFocLinkPrefix(url):
    if "adfoc.us/serve" in url:
        return url.replace(url.split("&url=")[0]+"&url=","",1)
    else:
        return url

# Function to remove the https://adfoc.us/serve/sitelinks/?id=<id>&url= prefix from each url in a forge-listings directory
def _removeAdFocLinkPrefixDict(frgListings):
    newDict = {}
    for key,value in frgListings.items():
        latVal = value.get("latest")
        if latVal != None and latVal != "":
            if newDict.get(key) == None: newDict[key] = {"latest":"","recommended":""}
            newDict[key]["latest"] = _removeAdFocLinkPrefix(latVal)
        recVal = value.get("recommended")
        if recVal != None and recVal != "":
            if newDict.get(key) == None: newDict[key] = {"latest":"","recommended":""}
            newDict[key]["recommended"] = _removeAdFocLinkPrefix(recVal)
    return newDict

# Function to join together two forge-client listings
def _joinForgeListings(stdlist,newlist):
    joinedList = stdlist
    for key,value in newlist.items():
        if key not in stdlist.keys():
            joinedList[key] = value
        else:
            if joinedList[key] == None:
                joinedList[key] = value
            else:
                # prioritate std
                if newlist[key].get("latest") != "":
                    joinedList[key]["latest"] = newlist[key]["latest"]
                if newlist[key].get("recommended") != "":
                    joinedList[key]["recommended"] = newlist[key]["recommended"]
    return joinedList

# Function to get the download url for a loader
def getLoaderUrl(prefix,loaderType="fabric",tempFolder=str,fabricUrl=str,forgeUrl=str,forgeMakeUrl=True,forgeMakeUrlType="installer",forForgeMcVer=str,forForgeLdVer=str,forForgeInstType="latest",forForgeList=str,regetForge=False) -> str:
    '''Downloads a loader and return the path to it'''
    # Fabric (just return fabricURL)
    if loaderType.lower() == "fabric":
        return fabricUrl
    # Forge
    if loaderType.lower() == "forge":
        url = None
        # Compile fstring url
        if forgeMakeUrl == True:
            print(prefix+"Attempting to build list...")
            url = f"https://maven.minecraftforge.net/net/minecraftforge/forge/{forForgeMcVer}-{forForgeLdVer}/forge-{forForgeMcVer}-{forForgeLdVer}-{forgeMakeUrlType}.jar"
        # Otherwise use listing
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
                    stdlist = _removeAdFocLinkPrefixDict(stdlist)
            # return without empty listings
            if forForgeMcVer in stdlist.keys():
                urlL = stdlist[forForgeMcVer]
                late = urlL.get("latest")
                reco = urlL.get("recommended")
                if forForgeInstType.lower() == "latest":
                    print(prefix+"Found latest for (forForgeMcVer)")
                    if late != "":
                        url = late
                    elif reco != "":
                        url = reco
                else:
                    print(prefix+"Found recommended for (forForgeMcVer)")
                    if reco != "":
                        url = reco
                    elif late != "":
                        url = late
        return url

# Function to get the loader given an url 
def getLoader(basedir,loaderType="fabric",loaderLink=str) -> str:
    loader_folder = os.path.join(basedir,loaderType.lower())
    if fs.notExist(loader_folder): fs.createDir(loader_folder)
    loader_filen = os.path.basename(loaderLink)
    loader_filep = os.path.join(loader_folder,loader_filen)
    downUrlFile(loaderLink, loader_filep)
    return loader_filep

# Function to get the os-standard .minecraft path
def getLauncherDir(preset=None):
    if preset is not None:
        return preset
    else:
        user = getpass.getuser()
        system = platform.system().lower()
        if system == "windows":
            return f"C:\\Users\\{user}\\AppData\\Roaming\\.minecraft"
        elif system == "darwin":  # macOS
            return f"{getTilde()}/Library/Application Support/minecraft"
        elif system == "linux":
            return f"{getTilde()}/.minecraft"
        else:
            raise ValueError("Unsupported operating system")

# Function to run installer for a loader
def installLoader(prefix=str,java_path=str,loaderType="fabric",loaderFile=None,f_snapshot=False,f_dir=None,f_mcversion=None,f_loaderver=None,f_noprofile=False,qouteJava=False,debugLoaderCommand=False):
    if qouteJava == True:
        java_path = f"{java_path}"
    if loaderType.lower() == "fabric":
        print(prefix+"Starting fabric install...")
        commandParts = [java_path, "-jar", loaderFile, "client"]
        if f_snapshot == True:
            commandParts.append("-snapshot")
        if f_dir != None:
            commandParts.extend(["-dir",f_dir])
        if f_mcversion != None:
            commandParts.extend(["-mcversion",f_mcversion])
        if f_loaderver != None:
            commandParts.extend(["-loader",f_loaderver])
        if f_noprofile == True:
            commandParts.append("-noprofile")
        if debugLoaderCommand == True:
            print("[DEBUG]: LoaderCmd.Fabric = "+' '.join(commandParts))
            _ = input("[DEBUG]: Press any key to continue...")
        subprocess.run(commandParts, shell=True)
        print(prefix+"Continuing...")
    elif loaderType.lower() == "forge":
        print(prefix+"Starting forge install...")
        print(prefix+"Follow the forge installers instructions.")
        # set dir to forge install to make sure log is placed in right folder
        olddir = os.getcwd()
        os.chdir(os.path.dirname(loaderFile))
        # run
        command = [java_path, "-jar", loaderFile]
        if debugLoaderCommand == True:
            print("[DEBUG]: LoaderCmd.Fabric = "+' '.join(command))
            _ = input("[DEBUG]: Press any key to continue...")
        subprocess.run(command, shell=True)
        # move back to the prv dir
        os.chdir(olddir)
        #_ = input(prefix+"Once the installer is done, press any key to continue...")
        print(prefix+"Continuing...")

# Get client versionID
def getVerId(loaderType,loaderVer,mcVer):
    if loaderType.lower() == "fabric":
        return f"fabric-loader-{loaderVer}-{mcVer}"
    elif loaderType.lower() == "forge":
        return f"{mcVer}-forge-{loaderVer}"
    else:
        return mcVer

# Legacy > newFormat converter
def convFromLegacy(flavorMTAfile,legacyRepoUrl,encoding="utf-8") -> dict:
    # get flavorMTAcontent
    raw = open(flavorMTAfile,'r',encoding=encoding).read()
    mta = json.loads(raw)
    nameFound = os.path.basename(os.path.dirname(flavorMTAfile))
    # get props from name
    for segment in mta["Data"]:
        if segment.get("Name") != None:
            nameFound = segment.get("Name")
    # retrive repo for file
    lrepo = {}
    try:
        lrepo_raw = getUrlContent(legacyRepoUrl)
        lrepo = json.loads(lrepo_raw)
    except: pass
    lrepo_flavors = lrepo["Flavors"]
    listFlavorData = {}
    for flavor in lrepo_flavors:
        if list(flavor.keys())[0] == nameFound:
            listFlavorData = flavor[nameFound]
    flavorData = {}
    for item in listFlavorData:
        key = list(item.keys())[0]
        flavorData[key] = item[key]
    # create template
    listing = {
        "format": 1,
        "name": nameFound,
        "desc": f'{flavorData["desc"]} (This listing was converted from legacy by the v2 installer.)',
        "version": "0.0",
        "modloader": "fabric",
        "modloaderVer": flavorData["fabric_loader"],
        "minecraftVer": flavorData["minecraft_version"],
        "created": datetime.now().strftime('%Y-%m-%d_%H-%M-%S'),
        "launcherIcon": flavorData["launcher_icon"],
        "_legacy_fld": flavorData
    }
    return listing

# Function for Mac to get eqv to ~
def getTilde():
    user = getpass.getuser()
    system = platform.system().lower()
    if system == "darwin":
        return f"/Users/{user}"
    else:
        return f"/home/{user}"
        

# Apply user directory to a path
def applyDestPref(shortDest) -> str:
    user = getpass.getuser()
    system = platform.system().lower()
    if system == "windows":
        p = os.path.join(f"C:\\users\\{user}\\",shortDest)
    elif system == "darwin":
        p = os.path.join(getTilde(),shortDest)
    else:
        p = os.path.join(f"/home/{user}/",shortDest)
    return fs.replaceSeps(p)

# Get std final destination
def getStdInstallDest():
    p = applyDestPref("installs\\minecraft-custom-client\\v2")
    return p

# Function to handle icon
def _getIcon(icon,icon128,legacy,modded):
    if icon == "mcc:icon128":
        return icon128
    elif icon == "mcc:legacy":
        return legacy
    elif icon == "mcc:modded":
        return modded
    else:
        return icon
def getIcon(icon,icon128,legacy,modded,default):
    _icon = _getIcon(icon,icon128,legacy,modded)
    if _icon == None:
        return default
    else:
        return _icon

def getIconFromListing(listingData):
    ico = listingData.get("icon")
    if ico == None:
        return listingData.get("launcherIcon")
    else:
        return ico

# [Curseforge]
def getCFdir(ovv=None):
    if ovv != None:
        return ovv
    else:
        return applyDestPref("curseforge\\minecraft\\Instances")

def getCFinstanceDict(modld,ldver,mcver):
    if modld.lower() == "fabric":
        return {
            "baseModLoader": {
                "forgeVersion": ldver,
                "name": f"fabric-{ldver}-{mcver}",
                "minecraftVersion": mcver
            }
        }
    else:
        return {
            "baseModLoader": {
                "forgeVersion": ldver,
                "name": f"{modld.lower()}-{ldver}",
                "minecraftVersion": mcver
            }
        }

def createCFmanifest(manifestFile,mcver,modld,ldver,name,ver,encoding="utf-8"):
    manifest = {
        "minecraft": {
            "version": mcver,
            "modLoaders": [
            {
                "id": f"{modld.lower()}-{ldver}",
                "primary": True
            }
            ]
        },
        "manifestType": "minecraftModpack",
        "manifestVersion": 1,
        "name": name,
        "version": ver,
        "author": "",
        "files": [],
        "overrides": "overrides"
    }
    open(manifestFile,'w',encoding=encoding).write(json.dumps(manifest))

def zipCFexport(modpackFolder, manifest, exportZip):
    # Create a new zip file
    with zipfile.ZipFile(exportZip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add the contents of the folder to the zip file
        for folder_root, _, files in os.walk(modpackFolder):
            for file in files:
                file_to_zip = os.path.join(folder_root, file)
                arcname = os.path.relpath(file_to_zip, modpackFolder)
                arcname = os.path.join('overrides', arcname)  # Place files under "overrides" folder
                zipf.write(file_to_zip, arcname=arcname)
        # Add the specified file to the zip file
        zipf.write(manifest, arcname=os.path.basename(manifest))

# [Modrinth]
def getMRdir(system,ovv=None):
    if ovv != None:
        return ovv
    else:
        if system == "windows":
            return applyDestPref("Appdata\\Roaming\\com.modrinth.theseus\\profiles")
        elif system == "darwin":
            p = os.path.abspath(f"{getTilde()}/Library/Application Support/com.modrinth.theseus/profiles")
            fs.ensureDirPath(p)
            return p
        else:
            return applyDestPref(f"com.modrinth.theseus/profiles")

def getMRloaderURL(modld,ldver,mcver):
    if modld.lower() == "fabric":
        return f"https://meta.modrinth.com/fabric/v0/versions/{ldver}.json"
    elif modld.lower() == "forge":
        return f"https://meta.modrinth.com/forge/v0/versions/{mcver}-forge-{ldver}.json"

def getMRinstanceDict(modld,ldver,mcver,modDestF,name,icon):
    data = {
        "uuid": str(uuid.uuid4()),
        "install_stage": "installed",
        "path": os.path.basename(modDestF),
        "metadata": {
            "name": name,
            "icon": str(icon),
            "groups": [],
            "game_version": mcver,
            "loader": modld,
            "loader_version": {
                "id": ldver,
                "url": getMRloaderURL(modld,ldver,mcver),
                "stable": True
            }
        },
        "fullscreen": None,
        "projects": {},
        "modrinth_update_version": None
    }
    if modld == "forge":
        data["loader_version"]["id"] = f"{mcver}-{ldver}"
    return data

def sha1_hash_file(filepath):
    sha1 = hashlib.sha1()
    with open(filepath, "rb") as file:
        while True:
            data = file.read(65536)  # Read the file in 64k chunks
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()

def prepMRicon(modpackDestF,icon):
    iconPath = ""
    if icon == None:
        return icon
    finalPng = os.path.join(modpackDestF,"mcc_generated_icon.png")
    if os.path.exists(finalPng): os.remove(finalPng)
    # handle b64
    if "data:image/png;base64," in icon:
        icon = icon.replace("data:image/png;base64,","",1)
        icon_binary = base64.b64decode(icon)
        with open(finalPng, "wb") as f:
            f.write(icon_binary)
    else:
        if os.path.exists(icon):
            fs.copyFile(icon,finalPng)
        else:
            iconPath = icon.replace("\\","/")
    iconPath = finalPng.replace("\\","/")
    # get hash
    sha1 = sha1_hash_file(iconPath)
    cacheF = '/'.join([os.path.dirname(iconPath),"..","..","caches","icons",sha1+".png"])
    cacheF = os.path.abspath(cacheF)
    fs.copyFile(iconPath,cacheF)
    return cacheF

def resolveUrlLauncherIcon(prefix,listingData):
    icon = listingData.get("icon")
    dest = "icon"
    if icon == None:
        icon = listingData.get("launcherIcon")
        dest = "launcherIcon"

    if is_valid_url(icon.strip()):
        print(prefix+f"Resolving base64 from launcherIcon url... (icon: {os.path.basename(icon)})")
        b64 = download_file_and_get_base64(icon.strip())
        listingData[dest] = f"data:image/png;base64,{b64}"
    return listingData