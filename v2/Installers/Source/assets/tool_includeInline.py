# Smal tool to include content of script in file

import argparse,os

from lib_filesys import filesys as fs

# Create an ArgumentParser object
encoding = "utf-8"
parser = argparse.ArgumentParser(description='IncludeInline')
parser.add_argument('-path', type=str, help='The path to file (its basedir is used as relative-pointer)')
parser.add_argument('-enc', type=str, help='The file encoding to use')
args = parser.parse_args()

def injectStringAtIndex(listToInjectTo=list,index=int,string=str) -> list:
    return listToInjectTo[:index] + [string] + listToInjectTo[index:]


# Handle enc
if args.enc:
    encoding = args.enc

if args.path:
    if fs.doesExist(args.path):
        # get content
        content = open(args.path,'r',encoding=encoding).read()
        lines = content.split("\n")
        # append content
        for li,line in enumerate(lines):
            if line.strip(" ").startswith("#"):
                if "IncludeInline: " in line:
                    line = line.strip("#")
                    line = line.replace("IncludeInline: ","")
                    line = line.strip(" ")
                    oline = line
                    if line.startswith("./"):
                        line = line.replace("./", os.path.dirname(args.path)+os.sep)
                    elif line.startswith(".\\"):
                        line = line.replace(".\\", os.path.dirname(args.path)+os.sep)
                    line = line.replace("/",os.sep)
                    line = line.replace("\\",os.sep)
                    if fs.doesExist(line):
                        toIncludeContent = f"#region [IncludeInline: {oline}]: START\n"
                        toIncludeContent += open(line,'r',encoding=encoding).read()
                        toIncludeContent += f"#endregion [IncludeInline: {oline}]: END"
                        lines[li] = toIncludeContent
        # set content
        content = '\n'.join(lines)
        open(args.path,'w',encoding=encoding).write(content)
