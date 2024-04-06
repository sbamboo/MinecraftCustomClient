import os,sys,argparse,zipfile
from libs.filesys import filesys as fs

parser = argparse.ArgumentParser(description='MinecraftCustomClient QuickInstaller')
parser.add_argument('-modpack', type=str, help='The modpack to bundle')
parser.add_argument('-destzip', type=str, help='The final zip to bundle to')
parser.add_argument('-uuid', type=str, help="uuid-str to write")
parser.add_argument('--prepbuild', help='Should the bundler prep the script for build?', action="store_true")
args = parser.parse_args()

parent = os.path.dirname(__file__)

assets = os.path.abspath(os.path.join(parent,"..","..","Installers","Source"))

quick  = os.path.abspath(os.path.join(assets,"QuickInstaller.py"))
nquick = os.path.join(os.path.dirname(quick),"source.QuickInstaller.py")
qlogo = os.path.join(os.path.dirname(nquick),"..","Assets","quicklogo.ico")
pkgs = os.path.join(os.path.dirname(nquick),"packages.txt")
buildScript = os.path.join(parent,"_bundle_buildscript.py")

inln = os.path.abspath(os.path.join(assets,"assets","tool_includeInline.py"))

# uuid
usable_UUID = "<uuid>"
if args.uuid:
    usable_UUID = args.uuid

# copy
fs.copyFile(quick,nquick)

# get content
c = open(nquick,'r',encoding="utf-8").read()

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
        # Extract pip name from autopipImport calls
        # They are in the syntax of autopipImport("<modulename>","<optional:pipname",...)
        # Where ... are any additional args on how autopipImport should work, but we only want a name,
        # if pipname is defined it should use that otherwise use the modulename,
        # to get this we split by , and iterate (This will as a safecase try to inlude both the modulename and pipname)
        if "autopipImport" in line:
            if "def autopipImport" not in line and "autopipImport = " not in line and not "**kwargs" in line:
                line = line.split("autopipImport(")[-1]
                line = line.split(")")[0]
                line = line.split(",")
                _line = []
                for p in line:
                    if '"' in p or "'" in p:
                        p = p.replace('"',"")
                        p = p.replace("'","")
                        _line.append(p)
                packages.append(_line[-1])
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

# handle replace
c = c.replace("<replaceble:modpack_relative_path_to_parent>",os.path.basename(args.modpack))
c = c.replace("<replaceble:modpack_id>",usable_UUID)

# save content
open(nquick,'w',encoding="utf-8").write(c)
if packages != []:
    open(pkgs,'w',encoding="utf-8").write('\n'.join(packages))

# compile nquick
os.system(f"{sys.executable} {inln} -path {nquick}")

# Create a ZipFile object in write mode
with zipfile.ZipFile(args.destzip, 'w') as zipf:
    # Add the file specified by the 'nquick' variable to the .zip archive
    zipf.write(nquick, arcname=os.path.basename(nquick))

    # Add the file specified by the 'file' variable to the .zip archive
    zipf.write(args.modpack, arcname=os.path.basename(args.modpack))

    # Add packages.txt
    if packages != []:
        zipf.write(pkgs, arcname=os.path.basename(pkgs))

    # Add build script
    if args.prepbuild:
        zipf.write(buildScript, arcname="build.py")
        zipf.write(qlogo, arcname="logo.ico")

os.remove(nquick)
if packages != []:
    os.remove(pkgs)