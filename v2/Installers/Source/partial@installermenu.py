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
        for fl in flavors:
            if fl["hidden"] == False:
                n = fl["name"]
                fl.pop("name")
                if fl["supported"] == False:
                    fl["desc"] += " \033[33m[NoSup]\033[0m"
                flavorsDict[n] = fl
        flavorsDict["[Exit]"] = {"desc": "ncb:"}
        # show os-dep keybinds:
        selTitle  = "Welcome to MinecraftCustomClient installer!\n\033[90mAny clients with [NoSup] have no support offered, use on your own risk.\033[0m\nSelect a flavor to install:"
        if args.modpack:
            key = args.modpack
        else:
            key = showDictSel(flavorsDict,selTitle=selTitle,selSuffix=selSuffix)
        if key == None or key not in list(flavorsDict.keys()) or key == "[Exit]":
            args.nopause = True
            exit()
        # get modpack url
        modpack_source = flavorsDict[key]["source"]
        # download url
        ## check for legacy
        if type(modpack_source) == dict:
            modpack_url = modpack_source["url"]
        else:
            modpack_url = modpack_source
        ## download & install
        modpack_path = os.path.join(parent,os.path.basename(modpack_url))
        print(prefix+"Downloading modpack file...")
        response = requests.get(modpack_url)
        if response.status_code == 200:
            # Content of the file
            cont = response.content
        else:
            cont = None
        if cont != None and cont != "":
            if os.path.exists(modpack_path) == False:
                open(modpack_path,'wb').write(cont)
        else:
            print(prefix+"Failed to get modpack!")
            exit()

    # [Prep selected package]
    modpack = os.path.basename(modpack_path)
    modpack_source = modpack_source
    title = title.replace("<modpack>", modpack)
    system = platform.system().lower()