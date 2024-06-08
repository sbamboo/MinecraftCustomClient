# Imports
import os
import re
import argparse
import requests
import json
import importlib

# Setup
encoding = "utf-8"
configFilename = "pyiil.jsonc"
parent = os.path.dirname( os.path.abspath(__file__) )
defaultConf = os.path.join(parent, configFilename)
loadedConfig = {}

# Argparse
parser = argparse.ArgumentParser(description='PyIIL - Python Include In-line')
parser.add_argument('-pyfile', type=str, help='The pyfile to run include on.')
parser.add_argument('-destdir', type=str, help='Where to put the final file, defaults relative to pyfile at ./pyiils/latest')
parser.add_argument('-ovvconf', type=str, help='Force to use the given config file.')
parser.add_argument('-encoding', type=str, help='Encoding to use, defaults to "utf-u".')
parser.add_argument('--skipconf', help='If given, will skip any in-dir config files.', action='store_true')
parser.add_argument('--force', help='Overwrites destination errors etc.', action='store_true')
parser.add_argument('--ignoreIndents', help='Ignores idents on #include statements.', action='store_true')
args = parser.parse_args()

# Define functions
def strip_json_comments(json_string):
    """
    Removes both single-line (//) and multi-line (/* */) comments from a JSON string,
    while preserving the content of strings.
    
    Args:
        json_string (str): The JSON string with comments.
    
    Returns:
        str: The JSON string with comments removed.
    """
    def _replacer(match):
        s = match.group(0)
        if s.startswith('/'):
            return ""  # This is a comment, so replace it with an empty string
        else:
            return s   # This is a string, so keep it unchanged

    # Regex pattern to match both comments and strings
    pattern = re.compile(
        r'("(\\"|[^"])*")|(/\*.*?\*/|//[^\r\n]*)',
        re.DOTALL
    )

    # Use sub with the replacer function to handle replacements
    cleaned_json = re.sub(pattern, _replacer, json_string)

    return cleaned_json

def count_indents(line,ret=False):
    indent_count = 0
    index = 0
    bstr = ""
    while index < len(line):
        if line[index] == '\t':
            indent_count += 1
            index += 1
            bstr += "\r"
        elif line[index:index+4] == ' ' * 4:
            indent_count += 1
            index += 4
            bstr += " "*4
        else:
            break
    if ret == True:
        return indent_count,bstr
    else:
        return indent_count

def requestsFetcher(url) -> str:
    return requests.get(url).content

def check_string_type(s):
    # Regular expression to match a URL
    url_pattern = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if re.match(url_pattern, s):
        return "URL"
    elif os.path.exists(s):
        return "File path"
    else:
        return "Invalid"

def includer(lines,parentFolder=None,includeFileComments=False,fetchResolver=requestsFetcher,fetchResolverArgs=[],fetchResolverKwargs={},encoding="utf-8",multiPrefix="MX@"): 
    newlines = []
    for line in lines:
        # Setup
        indents = 0
        indentStr = ""
        multi = False
        fileToInclude = ""
        preParsedLine = ""
        contentToInclude = None
        flags = []
        # Check for prefix and count indents
        if line.lstrip().startswith("#include "):
            # Parse out filepath
            preParsedLine = line.lstrip()
            if preParsedLine.replace("#include ","",1).strip().startswith(multiPrefix):
                multi = True
                fileToInclude = preParsedLine.split(multiPrefix)[-1].strip()
            else:
                fileToInclude = preParsedLine.replace("#include ","",1).strip()
            # Handle flags
            if "@" in fileToInclude:
                flags = fileToInclude.split("@")[-1].split(";")
                fileToInclude = fileToInclude.replace( fileToInclude.split("@")[-1], "", 1 ).rstrip()
            # Handle relative paths
            fileToInclude_o = fileToInclude
            if parentFolder != None and fileToInclude.startswith("./"):
                fileToInclude = fileToInclude.replace("./",parentFolder+os.sep,1)
            # Handle some tags
            fileToInclude = fileToInclude.replace("{pyiil_root}",parent)
            # Get strType and fetch content
            contentTypeToInclude = check_string_type(fileToInclude)
            if contentTypeToInclude == "URL":
                contentToInclude = fetchResolver(fileToInclude,*fetchResolverArgs,**fetchResolverKwargs).decode(encoding)
            elif contentTypeToInclude == "File path":
                with open(fileToInclude,'r',encoding=encoding) as file:
                    contentToInclude = file.read()
                    file.close()

            # If file exists continue
            if contentToInclude != None:
                # Handle multi
                if multi == True:
                    secondParDir = None
                    if contentTypeToInclude == "File path":
                        secondParDir = os.path.dirname(fileToInclude)
                    contentToInclude = '\n'.join( includer( contentToInclude.split("\n"), secondParDir, includeFileComments, fetchResolver, fetchResolverArgs, fetchResolverKwargs, encoding, multiPrefix ) )
                # Indents?
                if not args.ignoreIndents == True:
                    indents,indentStr = count_indents(line,True)
                # Add file comments (pre)
                if includeFileComments == True and "nocom" not in flags:
                    newlines.append( indentStr + f'#region [IncludeInline: {fileToInclude_o}]' )
                # Add content
                for line2 in contentToInclude.split("\n"):
                    newlines.append( indentStr + line2 )
                # Add file comments (post)
                if includeFileComments == True and "nocom" not in flags:
                    newlines.append( indentStr + f'#endregion [IncludeInline: {fileToInclude_o}]' )

        # No file just add the line
        else:
            newlines += line
    return newlines

def noneTo(value,default=None):
    if value == None:
        return default
    else:
        return value

def normPathSep(path):
    """CSlib: Normalises path sepparators to the current OS."""
    return path.replace("/",os.sep).replace("\\",os.sep)

## Cred: Importa by Simon Kalmi Claesson.
def fromPath(path, globals_dict=None):
    '''Import a module from a path. (Returns <module>)'''
    path = path.replace("/",os.sep).replace("\\",os.sep)
    spec = importlib.util.spec_from_file_location("module", path)
    module = importlib.util.module_from_spec(spec)
    if globals_dict:
        module.__dict__.update(globals_dict)
    spec.loader.exec_module(module)
    return module

# Handle encoding
if args.encoding:
    encoding = args.encoding

# Abs pyfile
args.pyfile = os.path.abspath(args.pyfile)

# Check so the pyfile exists
if not os.path.exists(args.pyfile):
    raise Exception(f"Pyfile '{args.pyfile}' dosen't exist!")

# Get config
configFile = defaultConf
## Check for in-dir config file
possibleConfFile = os.path.join(os.path.dirname(args.pyfile),configFilename)
if os.path.exists(possibleConfFile) and args.skipconf != True:
    configFile = possibleConfFile
del possibleConfFile
## Check for overwriting config file
if args.ovvconf:
    if os.path.exists(args.ovvconf):
        configFile = args.ovvconf

# Read config to a dictionary
with open(configFile,'r',encoding=encoding) as configFile_:
    content = strip_json_comments(configFile_.read())
    loadedConfig = json.loads(content)
    configFile_.close()
    del content

## Load subkeys
config_pyiil = noneTo(loadedConfig.get("pyiil"),{})
config_meta = noneTo(loadedConfig.get("meta"),{})
config_heading = noneTo(loadedConfig.get("included-heading"),[])
config_footer = noneTo(loadedConfig.get("included-footer"),[])
config_config = noneTo(loadedConfig.get("config"),{})

# Check so the dest exists if given
destdir = os.path.dirname(args.pyfile)
confDestdir = noneTo(config_config.get("output"),{}).get("destdir")

if args.destdir:
    if not os.path.exists(args.destdir):
        raise Exception(f"Destination directory '{args.destdir}' dosen't exist!")
    destdir = args.destdir

elif confDestdir != None and confDestdir != "":
    # ./ -> conf.dirname+sep+..
    if confDestdir.startswith("./"):
        confDestdir = normPathSep(confDestdir.replace("./",os.path.dirname(configFile)+os.sep,1))
        if not os.path.exists(confDestdir):
            print(f"Ensuring dest directory '{confDestdir}'...")
            os.makedirs(confDestdir)
    # ../ -> conf.dirname.dirname+sep+..
    elif confDestdir.startswith("../"):
        confDestdir = normPathSep(confDestdir.replace("../",os.path.dirname( os.path.dirname(configFile) )+os.sep,1))
        if not os.path.exists(confDestdir):
            print(f"Ensuring dest directory '{confDestdir}'...")
            os.makedirs(confDestdir)
    else:
        if not os.path.exists(confDestdir):
            raise Exception(f"Destination directory '{confDestdir}' dosen't exist!")
    destdir = confDestdir
del confDestdir

destdir = os.path.abspath(destdir)


# Handle fetchResolver
fetchResolver_ = requestsFetcher
fetchResolver_args = []
fetchResolver_kwargs = {}
if type(config_config.get("custom-fetch-resolver")) == dict:
    customFetchResolver = config_config.get("custom-fetch-resolver")
    if customFetchResolver.get("enabled") == True:
        customFetchResolver_path = customFetchResolver.get("path")
        customFetchResolver_attr = customFetchResolver.get("attr")
        fetchResolver_args = noneTo(customFetchResolver.get("args"), fetchResolver_args)
        fetchResolver_kwargs = noneTo(customFetchResolver.get("kwargs"), fetchResolver_kwargs)
        if customFetchResolver_path != None and customFetchResolver_attr != None :
            # Handle ./
            if customFetchResolver_path.startswith("./"):
                customFetchResolver_path = normPathSep(customFetchResolver_path.replace("./", os.path.dirname(configFile)+os.sep, 1))
            # load
            if os.path.exists(customFetchResolver_path):
                mod = fromPath(customFetchResolver_path)
                fetchResolver__ = getattr(mod,customFetchResolver_attr,None) # def = None
                if fetchResolver__ != None:
                    fetchResolver_ = fetchResolver__
                del fetchResolver__, mod
        del customFetchResolver_path,customFetchResolver_attr
    del customFetchResolver

# Convert the file
splitContent = []
with open(args.pyfile,'r',encoding=encoding) as pyfile_:
    splitContent = pyfile_.read().split("\n")
    pyfile_.close()
convertedLines = includer(splitContent, os.path.dirname(args.pyfile), noneTo(config_config.get("include-file-comments"),False), fetchResolver_, fetchResolver_args, fetchResolver_kwargs, encoding, noneTo(config_config.get("apply-multi-prefix"),"MX@"))
convertedContent = '\n'.join(convertedLines)

# Add in heading text
if len(config_heading) > 0:
    preAdditionalContent = '\n'.join(config_heading)
    padd_heading = noneTo(config_config.get("padd-heading"),{})
    padd_heading_leading = noneTo(padd_heading.get("leading"),False)
    padd_heading_trailing = noneTo(padd_heading.get("trailing"),False)
    
    for k,v in config_meta.items():
        preAdditionalContent = preAdditionalContent.replace('{'+k+'}',v)
    
    if padd_heading_leading:
        preAdditionalContent = "\n" + preAdditionalContent

    if padd_heading_trailing:
        preAdditionalContent = preAdditionalContent + "\n"

    convertedContent = preAdditionalContent + convertedContent

    del preAdditionalContent, padd_heading, padd_heading_leading, padd_heading_trailing

# Add in footer text
if len(config_footer) > 0:
    postAdditionalContent = '\n'.join(config_footer)
    padd_footer = noneTo(config_config.get("padd-footer"),{})
    padd_footer_leading = noneTo(padd_footer.get("leading"),False)
    padd_footer_trailing = noneTo(padd_footer.get("trailing"),False)
    
    for k,v in config_meta.items():
        postAdditionalContent = postAdditionalContent.replace('{'+k+'}',v)
    
    if padd_footer_leading:
        postAdditionalContent = "\n" + postAdditionalContent

    if padd_footer_trailing:
        postAdditionalContent = postAdditionalContent + "\n"
    
    convertedContent = convertedContent + postAdditionalContent

    del postAdditionalContent, padd_footer, padd_footer_leading, padd_footer_trailing

# Add to output
_fn,_ext = os.path.splitext(os.path.basename(args.pyfile))
_ext = _ext.lstrip(".")
output = noneTo(config_config.get("output"),{})
suffix = noneTo(output.get("suffix"),"")
name = noneTo(output.get("name"),"")
name = name.replace("{pyfile_name}",_fn)
name = name.replace("{pyfile_ext}",_ext)
name = name.replace("{s}",suffix)
outputFile = os.path.join(destdir,name)
del _fn, _ext, output, suffix, name

if os.path.exists(outputFile):
    if args.force == True:
        os.remove(outputFile)
    else:
        raise Exception(f"Output file '{outputFile}' already exists!")


with open(outputFile, 'w') as file:
    file.write(convertedContent)
    file.close()

print(f"Merged '{os.path.basename(args.pyfile)}' to '{os.path.basename(outputFile)}'!")