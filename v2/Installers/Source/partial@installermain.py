# [Code]
setConTitle(title)

print(prefix+f"Starting install for '{modpack}'...")

# IncludeInline: ./assets/lib_filesys.py

# IncludeInline: ./assets/flavorFunctions.py

# IncludeInline: ./assets/minecraftLauncherAgent.py

# Create tempfolder
fs = filesys
print(prefix+"Creating temp folder...")
tempFolder = os.path.join(parent,temp_foldername)
try:
    if os.path.exists(tempFolder): shutil.rmtree(tempFolder)
except:
    if os.path.exists(tempFolder):
        if platform.system() == "Windows":
            os.system(f'rmdir /s /q "{tempFolder}"')
        else:
            os.system(f'rm -rf "{tempFolder}"')
fs.createDir(tempFolder)

# IMPORT
if args.imprt:
    pass
else:
    # get type
    listingType = fs.getFileExtension(modpack_path)

    # extract archive to temp
    print(prefix+f"Extracting listing... (type: {listingType})")
    dest = extractModpackFile(modpack_path,tempFolder,encoding)

    if listingType != "package":
        # get listing data
        listingFile = os.path.join(dest,"listing.json")
        if fs.doesExist(listingFile) == True:
            listingData = json.loads(open(listingFile,'r',encoding=encoding).read())
        else:
            print("Failed to retrive listing content!")
            cleanUp(tempFolder,modpack_path)
            exit()
    else:
        try:
            mtaFile = os.path.join(dest,"flavor.mta")
            listingData = convFromLegacy(mtaFile,legacy_repo_url,encoding=encoding)
        except Exception as e:
            print("Failed to retrive listing content!",e)
            cleanUp(tempFolder,modpack_path)
            exit()

    # get data
    print(prefix+f"Downloading listing content... (type: {listingType})")
    try:
        downListingCont(dest,tempFolder,encoding,prefix_dl)
    except Exception as e:
        print(prefix+"Failed to download listing content!",e)
        cleanUp(tempFolder,modpack_path)
        exit()

    # get java
    print(prefix+f"Checking java...")
    try:
        javapath = getjava(prefix_jv,tempFolder,lnx_java_url,mac_java_url,win_java_url)
    except Exception as e:
        print(prefix+"Failed to get java!",e)
        cleanUp(tempFolder,modpack_path)
        exit()

    # handle install dest
    install_dest = getStdInstallDest(system)
    if listingData.get("_legacy_fld") != None:
        _legacy_fld_isntLoc = listingData["_legacy_fld"].get("install_location")
        if _legacy_fld_isntLoc != None and listingData["_legacy_fld"].get("install_location") != "":
            install_dest = applyDestPref(_legacy_fld_isntLoc)
    if args.dest:
        install_dest = args.dest
    fs.ensureDirPath(install_dest)
    ## handle curse
    #if args.curse == True:
    #    install_dest = getCFdir(
    #        args.curseInstanceP
    #    )
    #    fs.ensureDirPath(install_dest)
    ## create subfolder
    ## handle modrinth
    if args.rinth == True:
        install_dest = getMRdir(
            system,
            args.rinthInstanceP
        )
        ## handle modrinth profile already existing
        if args.rinth == True:
            _p = os.path.join(install_dest,fs.getFileName(modpack))
            if os.path.exists(_p):
                if args.y:
                    c = args.y
                elif args.n:
                    c = args.n
                else:
                    c = input("Modrith profile already exists, overwrite it? [y/n]")
                if c.lower() == "n":
                    cleanUp(tempFolder,modpack_path)
                    exit()
        fs.ensureDirPath(install_dest)
    ## get modpack destination folder
    modpack_destF = os.path.join(install_dest,fs.getFileName(modpack))
    if os.path.exists(modpack_destF) != True: os.mkdir(modpack_destF)

    # get mod info
    try:
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
            cleanUp(tempFolder,modpack_path)
            exit()
    except Exception as e:
        print(prefix+"Failed to get loader!",e)
        cleanUp(tempFolder,modpack_path)
        exit()

# EXPORT
infoFile = os.path.join(tempFolder,"modpack_info.json")
if args.exprt:
    if args.exprt.endswith(".zip"):
        args.exprt = args.exprt[::-1].replace("piz.","",1)[::-1]
    modpackInfo = {
        "modpack": modpack,
        "modpack_path": modpack_path,
        "dest": dest,
        "listingData": listingData,
        "listingType": listingType,
        "listingFile": listingFile,
        "loaderFp": loaderFp,
        "javapath": javapath,
        "install_dest": install_dest,
        "modpack_destF": modpack_destF,
        "f_snapshot": f_snapshot,
        "loaderURL": loaderURL
    }
    open(infoFile,'w',encoding=encoding).write(json.dumps(modpackInfo))
    print(f"Exporting to '{args.exprt}'")
    shutil.make_archive(args.exprt, "zip", tempFolder)
    cleanUp(tempFolder,modpack_path)
    exit()
elif args.imprt:
    print(f"Importing from '{args.imprt}'")
    try:
        if not os.path.exists(tempFolder):
            os.makedirs(tempFolder)
        # Extract the contents of the zip file to the tempFolder
        with zipfile.ZipFile(args.imprt, 'r') as zip_ref:
            zip_ref.extractall(tempFolder)
        impData = json.loads( open(infoFile,'r',encoding=encoding).read() )
    except:
        print("Failed to import tempfolder!")
        cleanUp(tempFolder)
        exit()
    modpack = impData["modpack"]
    modpack_path = impData["modpack_path"]
    dest = impData["dest"]
    listingData = impData["listingData"]
    listingType = impData["listingType"]
    listingFile = impData["listingFile"]
    loaderFp = impData["loaderFp"]
    javapath = impData["javapath"]
    install_dest = impData["install_dest"]
    modpack_destF = impData["modpack_destF"]
    f_snapshot = impData["f_snapshot"]
    loaderURL = impData["loaderURL"]
    modld = listingData["modloader"]
    ldver = listingData["modloaderVer"]
    mcver = listingData["minecraftVer"]

# Install loader
print(prefix+f"Starting install of loader... ({loaderFp})")
f_dir = getLauncherDir(args.mcf)
f_mcversion = mcver
f_loaderver = ldver
f_noprofile = args.fabprofile
try:
    installLoader(prefix,javapath,modld,loaderFp,f_snapshot,f_dir,f_mcversion,f_loaderver,True)
except Exception as e:
    print(prefix+"Failed to install loader!",e)
    cleanUp(tempFolder,modpack_path)
    exit()

# Copy content to final dest
fs.copyFolder2(dest,modpack_destF)

# Create profile
print(prefix+f"Creating profile for: {modpack}")
# Export to curse file
if (args.excurse != None and args.excurse != False and args.excurse != "") or args.excurse_parent == True:
    # Handle --excurse
    if args.excurse_parent == True:
        if "MinecraftCustomClient" in str(sys.executable):
            _parent = os.path.dirname(str(sys.executable))
        else:
            _parent = os.path.dirname(__file__)
        args.excurse = os.path.join(_parent,listingData["name"]+"_excurse.zip")
        if os.path.exists(args.excurse): os.remove(args.excurse)
    # Msg
    print(prefix+f"Exporting to curseforge file: '{args.excurse}'")
    # fix .zip double
    if args.excurse.endswith(".zip") != True:
        args.excurse = args.excurse + ".zip"
    # create manifest file
    print(prefix+f"Creating manifest...")
    manifest = os.path.join(tempFolder,"manifest.json")
    createCFmanifest(manifest,mcver,modld,ldver,listingData["name"],listingData["version"],encoding)
    # export
    print(prefix+f"Exporting...")
    zipCFexport(dest,manifest,args.excurse)
    print(prefix+f"Done!")
    # cleanup
    cleanUp(tempFolder,modpack_path)
    exit()
elif args.rinth == True:
    try:
        gicon = getIcon(
            getIconFromListing(listingData),
            icon_base64_icon128,
            icon_base64_legacy,
            icon_base64_modded,
            icon_base64_default
        )
        gicon = prepMRicon(modpack_destF,gicon)
        mrInstanceFile = os.path.join(modpack_destF,"profile.json")
        mrInstanceDict = getMRinstanceDict(modld,ldver,mcver,modpack_destF,listingData["name"],gicon)
        if os.path.exists(mrInstanceFile): os.remove(mrInstanceFile)
        open(mrInstanceFile,'w',encoding=encoding).write(
            json.dumps(mrInstanceDict)
        )
    except Exception as e:
        print(prefix+"Failed to create profile in modrinth app!",e)
else:
    try:
        gicon = getIcon(
            getIconFromListing(listingData),
            icon_base64_icon128,
            icon_base64_legacy,
            icon_base64_modded,
            icon_base64_default
        )
        MinecraftLauncherAgent(
            prefix=prefix_la,
            add=True,

            name=listingData["name"],
            gameDir=modpack_destF,
            icon=gicon,
            versionId=getVerId(modld,ldver,mcver),

            dontkill=args.dontkill,
            startLauncher=args.autostart,
            overWriteLoc=args.mcf,
            overWriteFile=args.cLnProfFileN,
            overWriteBinExe=args.cLnBinPath,

            excProcNameList=["minecraftcustomclient.exe"]
        )
    except Exception as e:
        print(prefix+"Failed to create profile in minecraft launcher",e)
        cleanUp(tempFolder,modpack_path)
        exit()
    #elif args.curse:
    #    cfInstanceFile = os.path.join(modpack_destF,"minecraftinstance.json")
    #    cfInstanceDict = getCFinstanceDict(modld,ldver,mcver)
    #    if os.path.exists(cfInstanceFile): os.remove(cfInstanceFile)
    #    open(cfInstanceFile,'w',encoding=encoding).write(
    #        json.dumps(cfInstanceDict)
    #    )

# Add to installed-list
mcc_installed_file = os.path.join(getStdInstallDest(system),"modpacks.json")
mcc_installed = {
    "DefaultInstallDirectory": getStdInstallDest(system),
    "Installs":[]
}
## handle existing
if fs.doesExist(mcc_installed_file):
    raw = open(mcc_installed_file,'r',encoding=encoding).read()
    mcc_installed = json.loads(raw)
## get id
mcc_installed_id = "<uuid>"
if listingData.get("_legacy_fld") != None:
    mcc_installed_id = listingData["_legacy_fld"].get("ID")
## add client
mcc_installed_current = {
    "id": mcc_installed_id,
    "name": os.path.basename(modpack),
    "path": modpack_destF
}
mcc_installed["Installs"].append(mcc_installed_current)
## write
raw = json.dumps(mcc_installed)
open(mcc_installed_file,'w',encoding=encoding).write(raw)


# Clean up
print(prefix+"Cleaning up...")
try:
    if os.path.exists(tempFolder): shutil.rmtree(tempFolder)
except:
    if os.path.exists(tempFolder):
        if platform.system() == "Windows":
            os.system(f'rmdir /s /q "{tempFolder}"')
        else:
            os.system(f'rm -rf "{tempFolder}"')
if args.autostart:
    print(prefix+"Done, Enjoy!")
else:
    print(prefix+"Done, now start your launcher and enjoy!")

cli_pause("Received exit, press any key to continue...")