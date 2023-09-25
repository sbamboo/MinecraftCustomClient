# Read readme.txt before use!

# [Imports]
import os
import sys
import json

# [Functions]
def remExisting(path):
    if os.path.exists(path): os.remove(path)

# [Arguments]
args = sys.argv[1:]
arg_javapath = None
arg_javaargs = None
toRemove = []
for i,arg in enumerate(args):
    if arg != None:
        if arg == "-javapath":
            arg_javapath = args[i+1]
            args[i] = None
            args[i+1] = None
        elif arg == "-javaargs":
            arg_javaargs = args[i+1]
            args[i] = None
            args[i+1] = None
args2 = []
for arg in args:
    if arg != None: args2.append(arg)
args = args2

# [Settings/Defaults]
javapath = "java"
javaargs = ""

# [Setup]
if arg_javapath != None: javapath = arg_javapath
if arg_javaargs != None: javaargs = arg_javaargs
curseforgeCli_folder = os.path.join( os.path.abspath(os.path.dirname(__file__)), f"North-West-Wind_CurseForge-CLI" )
curseforgeCli = os.path.join(curseforgeCli_folder,"curseforge-cli.jar")
curseforgeCli_json = os.path.join(curseforgeCli_folder,"cf.json")
arguments = " ".join(args)
config = {"retries":0,"silentExceptions":False,"alwaysInstallOptional":False,"suppressUpdates":False,"directory":f"{curseforgeCli_folder}\\curseforge-cli","disableOptional":False,"acceptParent":False}

# Fix cf.json
remExisting(curseforgeCli_json)
configJson = json.dumps(config)
open(curseforgeCli_json,'w').write(configJson)

# [Execute]
os.system(f"{javapath} {javaargs} -jar {curseforgeCli} --args {arguments}")