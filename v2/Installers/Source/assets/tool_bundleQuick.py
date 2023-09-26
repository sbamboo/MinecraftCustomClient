import os,sys,argparse,zipfile
from lib_filesys import filesys as fs

parser = argparse.ArgumentParser(description='MinecraftCustomClient QuickInstaller')
parser.add_argument('-modpack', type=str, help='The modpack to bundle')
parser.add_argument('-destzip', type=str, help='The final zip to bundle to')
args = parser.parse_args()

parent = os.path.dirname(__file__)

quick  = os.path.abspath(os.path.join(parent,"..","QuickInstaller.py"))
nquick = os.path.join(os.path.dirname(quick),"source.QuickInstaller.py")

inln = os.path.abspath(os.path.join(parent,"tool_includeInline.py"))

# copy
fs.copyFile(quick,nquick)

# handle replace
c = open(nquick,'r',encoding="utf-8").read()
c = c.replace("<replaceble:modpack_relative_path_to_parent>",os.path.basename(args.modpack))
open(nquick,'w',encoding="utf-8").write(c)

# compile nquick
os.system(f"{sys.executable} {inln} -path {nquick}")

# Create a ZipFile object in write mode
with zipfile.ZipFile(args.destzip, 'w') as zipf:
    # Add the file specified by the 'nquick' variable to the .zip archive
    zipf.write(nquick, arcname=os.path.basename(nquick))

    # Add the file specified by the 'file' variable to the .zip archive
    zipf.write(args.modpack, arcname=os.path.basename(args.modpack))

os.remove(nquick)