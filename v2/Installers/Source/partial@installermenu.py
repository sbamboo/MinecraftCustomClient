if action_install == True:
    # [Show repo]
    modpack_path = None
    modpack_source = None
    if args.modpackFile:
        if os.path.exists(args.modpackFile):
            modpack_path = args.modpackFile
    if args.imprt:
        modpack_path = args.imprt
    elif modpack_path == None:
        # get repo
        try:
            repoContent = requests.get(repo_url).text
            repoData = json.loads(repoContent)
        except:
            print("Failed to get repository")
            exit()
        # show select
        flavors = repoData.get("flavors")
        flavorsDict = {}
        notShowFlavors = {}
        for fl in flavors:
            n = fl["name"]
            fl.pop("name")
            if fl["supported"] == False:
                fl["desc"] += " \033[33m[NoSup]\033[0m"
            if fl["hidden"] == False:
                flavorsDict[n] = fl
            else:
                notShowFlavors[n] = fl
        flavorsDict["[Exit]"] = {"desc": "ncb:"}
        # show os-dep keybinds:
        selTitle  = "Welcome to MinecraftCustomClient installer!\n\033[90mAny clients with [NoSup] have no support offered, use on your own risk.\033[0m\nSelect a flavor to install:"
        if args.modpack:
            key = args.modpack
        else:
            if args.show_hidden == True:
                toDisplay = flavorsDict.copy()
                toDisplay.update(notShowFlavors)
                del toDisplay["[Exit]"]
                toDisplay["[Exit]"] = {"desc": "ncb:"}
                key = showDictSel(toDisplay,selTitle=selTitle,selSuffix=selSuffix)
            else:
                key = showDictSel(flavorsDict,selTitle=selTitle,selSuffix=selSuffix)
        validKeys = list(flavorsDict.keys())
        validKeys.extend( list(notShowFlavors.keys()) )
        if key == None or key not in validKeys or key == "[Exit]":
            args.nopause = True
            exit()
        # get modpack url
        if flavorsDict.get(key) != None:
            modpack_source = flavorsDict[key]["source"]
            modpack_id = flavorsDict[key]["id"]
        else:
            modpack_source = notShowFlavors[key]["source"]
            modpack_id = notShowFlavors[key]["id"]
        __modpack = key
        # download url
        ## check for legacy
        if type(modpack_source) == dict:
            modpack_url = modpack_source["url"]
        else:
            modpack_url = modpack_source
        ## download & install
        modpack_path = os.path.join(parent,os.path.basename(modpack_url))
        ## fix for invalid urls
        if "." not in modpack_url.split("/")[-1]:
            modpack_path = os.path.join(parent,key+".zip")
        print(prefix+"Downloading modpack file...")
        #response = requests.get(modpack_url)
        #if response.status_code == 200:
        #    # Content of the file
        #    cont = response.content
        #else:
        #    cont = None
        #if cont != None and cont != "":
        #    if os.path.exists(modpack_path) == False:
        #        open(modpack_path,'wb').write(cont)
        #else:
        #    print(prefix+"Failed to get modpack!")
        #    exit()
        try:
            downloadFile_HandleGdriveVirWarn(
                modpack_url,
                filepath=modpack_path,
                handleGdriveVirWarn=True,
                loadingBar=True,
                title=f"[cyan]Downloading {__modpack}...",
                handleGdriveVirWarnText="\033[33mFound gdrive scan warning, attempting to extract link and download from there...\033[0m",
                encoding=encoding,
                onFileExiError="remove"
            )
        except Exception as e:
            print(prefix+"Failed to get modpack!",e)
            exit()

    # [Prep selected package]
    modpack = os.path.basename(modpack_path)
    modpack_source = modpack_source
    modpack_id = modpack_id
    title = title.replace("<modpack>", modpack)
    system = platform.system().lower()