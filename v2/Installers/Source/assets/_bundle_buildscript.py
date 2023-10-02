# Build-script: 2023-10-02(1)


import os,sys,shutil,platform
parent = os.path.dirname(__file__)
packagesF = os.path.join(parent,"packages.txt")
pkgs_str = ""
if os.path.exists(packagesF):
    packages = ','.join(open(packagesF,'r',encoding="utf-8").read().split("\n"))
    pkgs_str = f'--add-data "{packagesF};." --hidden-import={packages}'
    # ensure pkgs in build envir
    for package in packages.split(","):
        os.system(f"{sys.executable} -m pip install {package}")

mainfile = os.path.join(parent,"source.MinecraftCustomClient.py")
logo = os.path.join(parent,"logo.ico")

command = f'pyinstaller --onefile {pkgs_str} --icon="{logo}" "{mainfile}"'
if "--debug" in sys.argv:
    print(command)
os.system(command)

exeName = "source.MinecraftCustomClient.exe"
build = os.path.join(parent,"dist",exeName)
final = os.path.join(parent,"..","MinecraftCustomClient.exe")
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