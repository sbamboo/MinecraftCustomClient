# PyIIL Merger-Tool 1.0
#

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
version = "1.0+"
parent = os.path.dirname( os.path.abspath(__file__) )
defaultConf = os.path.join(parent, configFilename)
loadedConfig = {}

# Enable ANSI on windows
os.system("")

# Argparse
parser = argparse.ArgumentParser(description='PyIIL - Python Include In-line')
parser.add_argument('-pyfile', type=str, help='The pyfile to run include on.')
parser.add_argument('-destdir', type=str, help='Where to put the final file, defaults relative to pyfile at ./pyiils/latest')
parser.add_argument('-ovvconf', type=str, help='Force to use the given config file.')
parser.add_argument('-encoding', type=str, help='Encoding to use, defaults to "utf-u".')
parser.add_argument('-tags', type=str, help='A comma sepparated list of tags to apply to the merge. Ex: "-tags dev"')
parser.add_argument('-resnameadd', type=str, help='Text to fill in the output-file {+} tag.')
parser.add_argument('--skipconf', help='If given, will skip any in-dir config files.', action='store_true')
parser.add_argument('--force', help='Overwrites destination errors etc.', action='store_true')
parser.add_argument('--ignoreIndents', help='Ignores idents on #include statements.', action='store_true')
parser.add_argument('--forceNoFileComments', help='Forces no-comments', action="store_true")
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

def includer(lines,parentFolder=None,includeFileComments=False,fetchResolver=requestsFetcher,fetchResolverArgs=[],fetchResolverKwargs={},encoding="utf-8",multiPrefix="MX@",tagFilter=[],commentReplacers={}): 
    newlines = []
    inExclude = False
    for line in lines:
        # Setup
        indents = 0
        indentStr = ""
        multi = False
        fileToInclude = ""
        preParsedLine = ""
        contentToInclude = None
        flags = []
        ontags = []

        # Check for exclude-prefix
        if line.lstrip().startswith("#exclude "):
            preParsedLine = line.lstrip().replace("#exclude ","",1)
            prem = ""
            inExclude_ = inExclude
            if preParsedLine.startswith("ST"):
                prem = preParsedLine.replace("ST","",1).lstrip()
                inExclude_ = True
            elif preParsedLine.lower().startswith("start"):
                prem = preParsedLine.replace("start","",1).lstrip()
                inExclude_ = True
            elif preParsedLine.startswith("END"):
                prem = preParsedLine.replace("END","",1).lstrip()
                inExclude_ = False
            elif preParsedLine.startswith("end"):
                prem = preParsedLine.replace("end","",1).lstrip()
                inExclude_ = False
                
            # handle
            if "@" in prem:
                flags = prem.split("@")[-1].split(";")
            allowedInTagFilter = False
            for fl in flags:
                if fl.startswith("ontags:"):
                    ontags = fl.replace("ontags:","",1).split(",")
            if len(ontags) > 0:
                for ta1 in tagFilter:
                    if ta1 in ontags:
                        allowedInTagFilter = True
                        break
            else:
                allowedInTagFilter = True
            # Set if allowed in filter
            if allowedInTagFilter == True:
                inExclude = inExclude_

        # Single line exlude
        elif line.rstrip().endswith("#excludeThis"):
            pass

        # Check for include-prefix and count indents
        elif line.lstrip().startswith("#include ") and inExclude != True:
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
                fileToInclude = fileToInclude.replace( "@"+fileToInclude.split("@")[-1], "", 1 ).rstrip()
            # Handle tags
            allowedInTagFilter = False
            for fl in flags:
                if fl.startswith("ontags:"):
                    ontags = fl.replace("ontags:","",1).split(",")
            if len(ontags) > 0:
                for ta1 in tagFilter:
                    if ta1 in ontags:
                        allowedInTagFilter = True
                        break
            else:
                allowedInTagFilter = True
            # If allowed continue
            if allowedInTagFilter == True:
                # Handle relative paths
                fileToInclude_o = fileToInclude
                if parentFolder != None and fileToInclude.startswith("./"):
                    fileToInclude = fileToInclude.replace("./",parentFolder+os.sep,1)
                # Handle some tags
                fileToInclude = fileToInclude.replace("{pyiil_root}",parent)
                # Get strType and fetch content
                contentTypeToInclude = check_string_type(fileToInclude)
                if contentTypeToInclude == "URL":
                    try:
                        contentToInclude = fetchResolver(fileToInclude,*fetchResolverArgs,**fetchResolverKwargs).decode(encoding)
                    except Exception as e:
                        print("\033[31m[Fetch-Error] {e}\n\033[0m")
                        exit()
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
                        contentToInclude = '\n'.join( includer( contentToInclude.split("\n"), secondParDir, includeFileComments, fetchResolver, fetchResolverArgs, fetchResolverKwargs, encoding, multiPrefix, tagFilter, commentReplacers ) )
                    # Indents?
                    if not args.ignoreIndents == True:
                        indents,indentStr = count_indents(line,True)
                    # Add file comments (pre)
                    if includeFileComments == True and "nocom" not in flags:
                        strb = f'#region [IncludeInline: {fileToInclude_o}]'
                        for k,v in commentReplacers.items():
                            strb = strb.replace(k,v)
                        newlines.append( indentStr + strb )
                    # Add content
                    for line2 in contentToInclude.split("\n"):
                        newlines.append( indentStr + line2 )
                    # Add file comments (post)
                    if includeFileComments == True and "nocom" not in flags:
                        strb = f'#endregion [IncludeInline: {fileToInclude_o}]'
                        for k,v in commentReplacers.items():
                            strb = strb.replace(k,v)
                        newlines.append( indentStr + strb )
            
            # Otherwise just add the original line
            else:
                newlines.append(line)

        # No file just add the line
        else:
            if inExclude != True:
                newlines.append(line)
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

try:
    # Handle encoding
    if args.encoding:
        encoding = args.encoding

    # Abs pyfile
    args.pyfile = os.path.abspath(args.pyfile)

    # Check so the pyfile exists
    if not os.path.exists(args.pyfile):
        print(f"\033[31m[Error] Pyfile '{args.pyfile}' dosen't exist!\033[0m")
        exit()

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

    ## handle pyiil subkey
    config_pyiil = noneTo(loadedConfig.get("pyiil"),{})
    if config_pyiil.get("version") != version:
        print(f"\033[33m[Warn] Invalid config version '{config_pyiil.get('version')}', use '{version}' or compatible! Expect errors.\033[0m")

    ## Load subkeys
    config_meta = noneTo(loadedConfig.get("meta"),{})
    config_heading = noneTo(loadedConfig.get("included-heading"),[])
    config_footer = noneTo(loadedConfig.get("included-footer"),[])
    config_config = noneTo(loadedConfig.get("config"),{})

    # Check so the dest exists if given
    destdir = os.path.dirname(args.pyfile)
    confDestdir = noneTo(config_config.get("output"),{}).get("destdir")

    if args.destdir:
        if not os.path.exists(args.destdir):
            print(f"\033[31m[Error] Destination directory '{args.destdir}' dosen't exist!\033[0m")
            exit()
        destdir = args.destdir

    elif confDestdir != None and confDestdir != "":
        # ./ -> conf.dirname+sep+..
        if confDestdir.startswith("./"):
            confDestdir = normPathSep(confDestdir.replace("./",os.path.dirname(configFile)+os.sep,1))
            if not os.path.exists(confDestdir):
                print(f"\033[34m[Info] Ensuring dest directory '{confDestdir}'...\033[0m")
                os.makedirs(confDestdir)
        # ../ -> conf.dirname.dirname+sep+..
        elif confDestdir.startswith("../"):
            confDestdir = normPathSep(confDestdir.replace("../",os.path.dirname( os.path.dirname(configFile) )+os.sep,1))
            if not os.path.exists(confDestdir):
                print(f"\033[34m[Info] Ensuring dest directory '{confDestdir}'...\033[0m")
                os.makedirs(confDestdir)
        else:
            if not os.path.exists(confDestdir):
                print(f"\033[31m[Error] Destination directory '{confDestdir}' dosen't exist!\033[0m")
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
    if args.tags:
        tagFilter = args.tags.strip().split(",")
    else:
        tagFilter = []
    try:
        if args.forceNoFileComments == True:
            includeFileComments = False
        else:
            includeFileComments = noneTo(config_config.get("include-file-comments"),False)
        convertedLines = includer(splitContent, os.path.dirname(args.pyfile), includeFileComments, fetchResolver_, fetchResolver_args, fetchResolver_kwargs, encoding, noneTo(config_config.get("apply-multi-prefix"),"MX@"),tagFilter,noneTo(config_config.get("comment-lines-replacers"),{}))
    except Exception as e:
        print(f"\033[31m[Includer-Error]\n\n{e}\033[0m]\n")
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
    if args.resnameadd:
        name = name.replace("{+}",args.resnameadd)
    else:
        name = name.replace("{+}","")
    outputFile = os.path.join(destdir,name)
    del _fn, _ext, output, suffix, name

    if os.path.exists(outputFile):
        if args.force == True:
            os.remove(outputFile)
        else:
            print(f"\033[31m[Error] Output file '{outputFile}' already exists!\033[0m")
            exit()

    with open(outputFile, 'w') as file:
        file.write(convertedContent)
        file.close()

    print(f"\033[32m[Done] Merged '{os.path.basename(args.pyfile)}' to '{os.path.basename(outputFile)}'!\033[0m")

except Exception as e:
    print(f"\033[31m[Toolkit-Error]\n\n{e}\033[0m\n")