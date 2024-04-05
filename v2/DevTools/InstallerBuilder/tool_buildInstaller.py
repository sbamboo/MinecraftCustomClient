import os,sys,shutil,importlib
parent = os.path.dirname(__file__)

def fromPath(path):
    spec = importlib.util.spec_from_file_location("module", path.replace("/",os.sep).replace("\\",os.sep))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
filesys = fromPath(os.path.join(parent,"lib_filesys.py"))
fs = filesys.filesys

# Setup
destfolder = os.path.join(parent,"..","..","Installers","Builds")
fs.ensureDirPath(destfolder)
bundleScript = os.path.join(parent,"_bundleInstaller.py")

# Bundle
print("Bundling installer...")
bundleFile = os.path.join(destfolder,"bundle.zip")
# create bundle
os.system(f'{sys.executable} {bundleScript} -destzip "{bundleFile}" --inclScripts --skipExcludes')
print("Done!")

# Build src
print("Prepping build enviroment for installer...")
fs.ensureDirPath(destfolder)
bundleFile = os.path.join(destfolder,"build_source.zip")
# create bundle for build-env
os.system(f'{sys.executable} {bundleScript} -destzip "{bundleFile}" --prepbuild')
print("Done!")

# Build
print("Attempting to build quickinstaller (win_x86)...")
# extract build env
buidlenv_parent = os.path.join(destfolder,"win_x86")
fs.ensureDirPath(buidlenv_parent)
buildenv = os.path.join(buidlenv_parent,"build-env")
shutil.unpack_archive(bundleFile,buildenv)
# run build-script
possibleBuildArgs = ""
if len(sys.argv) > 1:
    possibleBuildArgs = ' '.join(sys.argv[1:])
buildScript = os.path.join(buildenv,"build.py")
if os.path.exists(buildScript) != True:
    raise Exception("No build script found, invalid build-env!")
olddir = os.getcwd()
os.chdir(buildenv)
os.system(f"{sys.executable} {buildScript} {possibleBuildArgs}")
os.chdir(buildenv)
# clean up
import time
print("Waiting 2s for process to finish...")
time.sleep(2)
print("Continuing...")
try:
    shutil.rmtree(buildenv)
except:
    print(f"Failed to remove build enviroment, please manually remove: '{os.path.abspath(buildenv)}'")
print("Done!")
