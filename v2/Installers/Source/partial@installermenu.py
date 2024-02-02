if action_install == True:
    # [Show repo]
    modpack_path = None
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
                    flavorsDict[n] = fl + " \033[33m[NoSup]\033[0m"
                else:
                    flavorsDict[n] = fl
        flavorsDict["[Exit]"] = {"desc": "ncb:"}
        # show os-dep keybinds:
        selTitle  = "Welcome to MinecraftCustomClient installer!\nSelect a flavor to install:"
        if args.modpack:
            key = args.modpack
        else:
            key = showDictSel(flavorsDict,selTitle=selTitle,selSuffix=selSuffix)
        if key == None or key not in list(flavorsDict.keys()) or key == "[Exit]":
            args.nopause = True
            exit()
        # get modpack url
        modpack_url = flavorsDict[key]["source"]
        # download url
        modpack_path = os.path.join(parent,os.path.basename(modpack_url))
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
    title = title.replace("<modpack>", modpack)
    system = platform.system().lower()