# Build-script: 2023-09-28(1)

import os,sys,shutil,platform
parent = os.path.dirname(__file__)
packagesF = os.path.join(parent,"packages.txt")
pkgs_str = ""
if os.path.exists(packagesF):
    packages = ','.join(open(packagesF,'r',encoding="utf-8").read().split("\n"))
    pkgs_str = f' --add-data "{packagesF};." --hidden-import={packages}'
    # ensure pkgs in build envir
    for package in packages.split(","):
        os.system(f"{sys.executable} -m pip install {package}")
excludeFiles = ["packages.txt","source.QuickInstaller.py","build.py"]
files = os.listdir(parent)
modpack = None
for file in files:
    if os.path.basename(file) not in excludeFiles:
        modpack = os.path.basename(file)

mainfile = os.path.join(parent,"source.QuickInstaller.py")
modpack = os.path.join(parent,modpack)

command = f'pyinstaller --onefile --add-data "{modpack};."{pkgs_str} {mainfile}'
os.system(command)

exeName = "source.QuickInstaller.exe"
build = os.path.join(parent,"dist",exeName)
final = os.path.join(parent,"QuickInstaller.exe")
shutil.copyfile(build, final)
# remove build folders
os.remove("source.QuickInstaller.spec")
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