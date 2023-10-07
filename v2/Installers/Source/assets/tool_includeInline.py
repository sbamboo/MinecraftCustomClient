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

def excludeCmtComments(document):
    lines = document.split("\n")
    nlines = []
    for line in lines:
        if "cmt@" not in line:
            nlines.append(line)
    document = '\n'.join(nlines)
    return document

# Function to replace inlines a document-string
def includeInline(document):
    # setup
    hasMX = False # MX@ to run content before appending
    # split
    lines = document.split("\n")
    # include to content
    for li,line in enumerate(lines):
        if line.strip(" ").startswith("#"):
            if "IncludeInline: " in line:
                line = line.strip("#")
                line = line.replace("IncludeInline: ","")
                line = line.strip(" ")
                # check MX@
                if "MX@" in line:
                    line = line.replace("MX@","")
                    hasMX = True
                oline = line
                if line.startswith("./"):
                    line = line.replace("./", os.path.dirname(args.path)+os.sep)
                elif line.startswith(".\\"):
                    line = line.replace(".\\", os.path.dirname(args.path)+os.sep)
                line = line.replace("/",os.sep)
                line = line.replace("\\",os.sep)
                if fs.doesExist(line):
                    toIncludeContent = f"#region [IncludeInline: {oline}]\n"
                    raw = open(line,'r',encoding=encoding).read()
                    raw = excludeCmtComments(raw)
                    if hasMX == True:
                        raw = includeInline(raw)
                    # fix no \n
                    if raw.endswith("\n") != True:
                        raw += "\n"
                    toIncludeContent += raw
                    toIncludeContent += f"#endregion [IncludeInline: {oline}]"
                    lines[li] = toIncludeContent
    # join
    document = '\n'.join(lines)
    return document

# Handle enc
if args.enc:
    encoding = args.enc

if args.path:
    if fs.doesExist(args.path):
        # get content
        content = open(args.path,'r',encoding=encoding).read()
        content = includeInline(content)
        # set content
        open(args.path,'w',encoding=encoding).write(content)
