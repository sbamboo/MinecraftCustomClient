# Build-script: 2023-10-14(1)

import os,sys,shutil,platform

pyinst = "pyinstaller"
if "--pyinstallerPath" in sys.argv:
    ind = sys.argv.index("--pyinstallerPath")
    try:
        pyinst = sys.argv[ind+1]
        sys.argv.pop(ind+1)
        sys.argv.pop(ind)
    except:
        pass

parent = os.path.dirname(__file__)
packagesF = os.path.join(parent,"packages.txt")
pkgs_str = ""
if os.path.exists(packagesF):
    packages = ','.join(open(packagesF,'r',encoding="utf-8").read().split("\n"))
    if platform.system() == "Windows":
        pkgs_str = f'--add-data "{packagesF};." --hidden-import={packages}'
    else:
        pkgs_str = f'--add-data "{packagesF}:." --hidden-import={packages}'
    # ensure pkgs in build envir
    for package in packages.split(","):
        os.system(f"{sys.executable} -m pip install {package}")
        # Handle --copy-metadata for specific packages
        if package in ["readchar"]:
            pkgs_str += f" --copy-metadata {package}"

mainfile = os.path.join(parent,"source.MinecraftCustomClient.py")
logo = os.path.join(parent,"logo.ico")

command = f'{pyinst} --onefile {pkgs_str} --icon="{logo}" "{mainfile}"'
if "--debug" in sys.argv:
    print(command)
os.system(command)

if platform.system() == "Windows":
    exeName = "source.MinecraftCustomClient.exe"
    build = os.path.join(parent,"dist",exeName)
    final = os.path.join(parent,"..","MinecraftCustomClient.exe")
else:
    exeName = "source.MinecraftCustomClient"
    build = os.path.join(parent,"dist",exeName)
    final = os.path.join(parent,"..","MinecraftCustomClient")

shutil.copyfile(build, final)
# remove build folders
os.remove("source.MinecraftCustomClient.spec")
tor = ["dist","build"]
for f in tor:
    f = os.path.join(parent,f)
    try:
        shutil.rmtree(f)
    except:
        if os.path.exists(f):
            if platform.system() == "Windows":
                os.system(f'rmdir /s /q "{f}"')
            else:
                os.system(f'rm -rf "{f}"')