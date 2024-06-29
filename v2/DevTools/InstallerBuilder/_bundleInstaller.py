import os,sys,argparse,zipfile,importlib

parser = argparse.ArgumentParser(description='MinecraftCustomClient QuickInstaller')
parser.add_argument('-destzip', type=str, help='The final zip to bundle to')
parser.add_argument('--prepbuild', help='Should the bundler prep the script for build?', action="store_true")
parser.add_argument('--inclScripts', help='Add scripts?', action="store_true")
parser.add_argument('--skipExcludes', help='Skip excluded sections', action="store_true")
args = parser.parse_args()

parent = os.path.dirname(__file__)

def fromPath(path):
    spec = importlib.util.spec_from_file_location("module", path.replace("/",os.sep).replace("\\",os.sep))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
filesys = fromPath(os.path.join(parent,"lib_filesys.py"))
fs = filesys.filesys

installer  = os.path.abspath(os.path.join(parent,"..","..","Installers","Source","MinecraftCustomClient.py"))
ninstaller = os.path.join(os.path.dirname(installer),"source.MinecraftCustomClient.py")
ilogo = os.path.join(os.path.dirname(ninstaller),"..","Assets","instlogo.ico")
pkgs = os.path.join(os.path.dirname(ninstaller),"packages.txt")
buildScript = os.path.join(parent,"..","..","Installers","Source","assets","_bundle_buildscript.py")

inln = os.path.abspath(os.path.join(parent,"..","..","Installers","Source","assets","tool_includeInline.py"))

# copy
fs.copyFile(installer,ninstaller)

# compile ninstaller
os.system(f"{sys.executable} {inln} -path {ninstaller}")

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
    if args.skipExcludes != True:
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

# save content
open(ninstaller,'w',encoding="utf-8").write(c)
if packages != []:
    open(pkgs,'w',encoding="utf-8").write('\n'.join(packages))

# Create a ZipFile object in write mode
with zipfile.ZipFile(args.destzip, 'w') as zipf:
    # Add the file specified by the 'nquick' variable to the .zip archive
    zipf.write(ninstaller, arcname=os.path.basename(ninstaller))

    # Add packages.txt
    if packages != []:
        zipf.write(pkgs, arcname=os.path.basename(pkgs))

    # Add scripts
    if args.inclScripts:
        scriptFolder = os.path.join(parent,"..","..","Installers","Source","assets","bundle_scripts","main-installer")
        zipf.write(os.path.join(scriptFolder,"linux.sh"), arcname="linux.sh")
        zipf.write(os.path.join(scriptFolder,"mac.sh"), arcname="mac.sh")
        zipf.write(os.path.join(scriptFolder,"windows.bat"), arcname="windows.bat")
        zipf.write(os.path.join(scriptFolder,"launcher.bat"), arcname="launcher.bat")

    # Add build script
    if args.prepbuild:
        zipf.write(buildScript, arcname="build.py")
        zipf.write(ilogo, arcname="logo.ico")

#os.remove(ninstaller)
if packages != []:
    os.remove(pkgs)