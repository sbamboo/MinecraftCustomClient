# [Uninstall]
if action_uninstall == True:

    def safeNone(v):
        if type(v) == str:
            v = v.replace("<uuid>","Unknown")
        if v == None:
            return str("None")
        else:
            return str(v)
    # get modpacks
    mcc_installed_file = os.path.join(getStdInstallDest(),"modpacks.json")
    if not os.path.exists(mcc_installed_file):
        print("No modpacks.json file found, can't read installed modpacks!")
        exit()
    else:
        try:
            modpacks = json.loads(open(mcc_installed_file,'r',encoding=encoding).read())
        except:
            modpacks = {
                "DefaultInstallDirectory": getStdInstallDest(),
                "Installs":[]
            }
    # show modpacks
    selTitle  = f"Welcome to MinecraftCustomClient!\n\033[90mShowing installed modpacks for:\n  {modpacks['DefaultInstallDirectory']}\033[0m\nSelect the modpack to uninstall:"
    formatting={"item_selected":"\x1b[33m","item_normal":"","selector":""}
    modpacksDict = {}
    installs = modpacks.get("Installs")
    namedModpacks = {}
    if installs != None and installs != [] and type(installs) == list:
        for iter_modpack in modpacks["Installs"]:
            # add to lists
            name = safeNone(iter_modpack.get('name'))
            if "-quickcompile." in name:
                _name = name.split("_")
                _name.pop(-1)
                _name.pop(-1)
                name = '_'.join(_name)
            namedModpacks[name] = iter_modpack
            modpacksDict[name] = {"desc":f"ID: {safeNone(iter_modpack.get('id'))}"}
    modpacksDict["[Exit]"] = {"desc": "ncb:"}
    if args.modpack:
        modpack = args.modpack
    else:
        modpack = showDictSel(modpacksDict,selTitle=selTitle,selSuffix=selSuffix,formatting=formatting)
    if modpack == None or modpack not in list(namedModpacks.keys()) or modpack == "[Exit]":
        args.nopause = True
        if modpack != "[Exit]":
            print(f"Modpack '{modpack}' is not installed/found.")
        exit()
    print(f"Attempting uninstallation of '{modpack}'.")
    # get path
    mp_data = namedModpacks.get(modpack)
    if modpack == None:
        print(f"Failed to get modpack data for {modpack}!")
        exit()
    else:
        mp_path = mp_data.get("path")
        mp_name = mp_data.get("name")
        mp_id = mp_data.get("id")
        # are you sure with --y & --n support
        if args.n:
            exit()
        if not args.y:
            c = input(f"Are you sure you want to uninstall '{modpack}'? (THIS ACTION IS IRREVERSIBLE) [y/n]: ")
            if c.lower() != "y":
                exit()
        # remove folder
        try:
            if os.path.exists(mp_path):
                shutil.rmtree(mp_path)
            else:
                print("Modpack path dosen't exist, wont attempt removal.")
        except Exception as e:
            print("Failed to remove modpack, this might lead to a partially-installed modpack.")
            print(e)
            exit()
        # remove from modpacks.json
        try:
            cur_modpacks_d = json.loads(open(mcc_installed_file,'r',encoding=encoding).read())
            cur_modpacks = cur_modpacks_d.get("Installs")
            if cur_modpacks == None:
                cur_modpacks_d["Installs"] = []
        except Exception as e:
            print(f"Failed to get current modpacks!\n{e}")
            exit()
        try:
            if cur_modpacks != None:
                for i,pack in enumerate(cur_modpacks):
                    if pack.get("name") == mp_name:
                        cur_modpacks_d["Installs"].pop(i)
                        break
        except Exception as e:
            print(f"Failed to remove path from installed-modpack data!\n{e}")
            exit()
        try:
            open(mcc_installed_file,'w',encoding=encoding).write(json.dumps(cur_modpacks_d))
        except Exception as e:
            print(f"Failed to remove path from installed-modpack file!\n{e}")
            exit()
        # done
        print(f"Uninstalled {modpack}!")
        exit()