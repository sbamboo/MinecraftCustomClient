import os,sys,argparse,zipfile
from lib_filesys import filesys as fs

parser = argparse.ArgumentParser(description='MinecraftCustomClient QuickInstaller')
parser.add_argument('-destzip', type=str, help='The final zip to bundle to')
parser.add_argument('--prepbuild', help='Should the bundler prep the script for build?', action="store_true")
args = parser.parse_args()

parent = os.path.dirname(__file__)

installer  = os.path.abspath(os.path.join(parent,"..","MinecraftCustomClient.py"))
ninstaller = os.path.join(os.path.dirname(installer),"source.MinecraftCustomClient.py")
ilogo = os.path.join(os.path.dirname(ninstaller),"..","Assets","instlogo.ico")
pkgs = os.path.join(os.path.dirname(ninstaller),"packages.txt")
buildScript = os.path.join(parent,"_bundle_buildscript.py")

inln = os.path.abspath(os.path.join(parent,"tool_includeInline.py"))

# copy
fs.copyFile(installer,ninstaller)

# get content
c = open(ninstaller,'r',encoding="utf-8").read()

# prep build?
packages = []
if args.prepbuild:
    lines = c.split("\n")
    sti = None
    excludes = []
    toExclude = []
    # exclude
    for i,line in enumerate(lines):
        # if no sti is found check for sti
        if sti == None:
            if "BuildPrep: ST-excl" in line:
                sti = i
                toExclude.append(i)
        # if sti found check for excludes and eni
        else:
            if "BuildPrep: END-excl" in line:
                sti = None
                toExclude.append(i)
            else:
                excludes.append(line)
                toExclude.append(i)
    # check for sp (save-pkg)
    for line in excludes:
        if "autopipImport" in line:
            line = line.split("autopipImport(")[-1]
            line = line.split(")")[0]
            line = line.split(",")
            for i,p in enumerate(line):
                p = p.replace('"',"")
                p = p.replace("'","")
                line[i] = p
            packages.append(line[-1])
    # include includes
    toinclude = []
    for i,line in enumerate(lines):
        if i not in toExclude:
            if "oexit()" in line and "#repl-exit" in line:
                line = line.replace("oexit()","raise Exception('EXIT')")
            if "exit()" in line and "#repl-exit" in line:
                line = line.replace("exit()","raise Exception('EXIT')")
            toinclude.append(line)
    c = '\n'.join(toinclude)

# save content
open(ninstaller,'w',encoding="utf-8").write(c)
if packages != []:
    open(pkgs,'w',encoding="utf-8").write('\n'.join(packages))

# compile ninstaller
os.system(f"{sys.executable} {inln} -path {ninstaller}")

# Create a ZipFile object in write mode
with zipfile.ZipFile(args.destzip, 'w') as zipf:
    # Add the file specified by the 'nquick' variable to the .zip archive
    zipf.write(ninstaller, arcname=os.path.basename(ninstaller))

    # Add packages.txt
    if packages != []:
        zipf.write(pkgs, arcname=os.path.basename(pkgs))

    # Add build script
    if args.prepbuild:
        zipf.write(buildScript, arcname="build.py")
        zipf.write(ilogo, arcname="logo.ico")

os.remove(ninstaller)
if packages != []:
    os.remove(pkgs)