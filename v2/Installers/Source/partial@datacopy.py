# IncludeInline: ./assets/ui_fs_selector.py

if action_datacopy:
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
    # [Select source]
    selTitle  = f"Welcome to MinecraftCustomClient!\n\033[90mShowing installed modpacks for:\n  {modpacks['DefaultInstallDirectory']}\033[0m\nSelect the modpack to copy data FROM:"
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
    if len(namedModpacks) < 2:
        print(f"The datacopier needs more then two installed modpacks, {len(namedModpacks)} found!")
        exit()
    if args.modpack:
        modpack = args.modpack
    else:
        modpack = showDictSel(modpacksDict,selTitle=selTitle,selSuffix=selSuffix,formatting=formatting)
    if modpack == None or modpack not in list(namedModpacks.keys()) or modpack == "[Exit]":
        args.nopause = True
        if modpack != "[Exit]":
            print(f"Modpack '{modpack}' is not installed/found.")
        exit()
    # get data
    mp_data = namedModpacks.get(modpack)
    if modpack == None:
        print(f"Failed to get modpack data for {modpack}!")
        exit()
    else:
        mp_path = mp_data.get("path")
        mp_name = mp_data.get("name")
        mp_id = mp_data.get("id")
    if os.path.exists(mp_path) == False:
        print(f"Failed to find folder for source-modpack: '{modpack}'!")
        exit()

    # [Choose files]
    selTitle  = "Welcome to MinecraftCustomClient's datacopier!\nCheck the items you want to copy using your keyboard:"
    selSuffix = "\033[90m\nUse your keyboard to select/check:\n↑ : Up\n↓ : Down\n↲ : Select/Toggle (ENTER)\nq : Quit/Done\n␛ : Quit/Done (ESC)\033[0m"
    if platform.system() == "Darwin":
        selSuffix = "\033[90m\nUse your keyboard to select/check:\na : Up\nb : Down\n↲ : Select/Toggle (ENTER)\nq : Quit/Done\n␛ : Quit/Done (ESC)\033[0m"
    ch,selbtn = displayForDir(
        mp_path,
        selTitle=selTitle,
        selSuffix=selSuffix,
        extraElems={"[Done]":"btn:prenl:Selects your checked items","[Exit]":"btn:Exits the datacopier"},
        formatting={"partial_desc":"\033[90m","box_unchecked":"\033[90m","box_checked":"\033[33m"}
    )
    if selbtn == "[Exit]":
        ch = []
    # handle no-sel
    if ch == [] or ch == None:
        print("No items selected for copy, skipping...")
        exit()

    # [Select dest]
    selTitle  = f"Welcome to MinecraftCustomClient!\n\033[90mShowing installed modpacks for:\n  {modpacks['DefaultInstallDirectory']}\n\033[90mSelected source-modpack: {modpack}\033[0m\nSelect the modpack to copy data TO:"
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
    if args.destmodpack:
        modpackd = args.destmodpack
    else:
        modpackd = showDictSel(modpacksDict,selTitle=selTitle,selSuffix=selSuffix,formatting=formatting)
    if modpackd == None or modpackd not in list(namedModpacks.keys()) or modpackd == "[Exit]":
        args.nopause = True
        if modpack != "[Exit]":
            print(f"Modpack '{modpackd}' is not installed/found.")
        exit()
    # get data
    mpd_data = namedModpacks.get(modpackd)
    if modpackd == None:
        print(f"Failed to get modpack data for {modpackd}!")
        exit()
    else:
        mpd_path = mpd_data.get("path")
        mpd_name = mpd_data.get("name")
        mpd_id = mpd_data.get("id")
    if os.path.exists(mpd_path) == False:
        print(f"Failed to find folder for dest-modpack: '{modpackd}'!")
        exit()
    
    if modpack == modpackd:
        print("Source modpack can't be the same as the destination!")
        exit()

    # [Copy]
    print(f"You have selected:")
    print(f"  Source      = '{modpack}'")
    print(f"  Destination = '{modpackd}'")
    print(f"  ToCopy: '{','.join([os.path.basename(ent) for ent in ch])}'")
    print("")
    if not args.n and not args.y:
        c = input("Is this correct? [Y/N] ")
    if args.n:
        c = "n"
    elif args.y:
        c = "y"
    if c.lower() == "n":
        print("Okay, wont copy!")
        exit()
    else:
        print("Copying...")
        for ent in ch:
            ent_n = os.path.basename(ent)
            dest = ent.replace(mp_path,mpd_path)
            print(f"\033[90m{modpack}:{ent_n} -> {modpackd}:{ent_n}\033[0m")
            if os.path.isdir(ent):
                # copy fol
                fs.copyFolder2(ent,dest)
            else:
                # copy fil
                if os.path.exists(dest) and os.path.exists(ent):
                    os.remove(dest)
                    print("Overwriting org..")
                fs.copyFile(ent,dest)
            