# MinecraftCustomClient Library, Version: 1.0
# Library backend for al things the minecraft-custom-client system needs.
# 


import json
import platform

import os, json, sys, subprocess, platform

# Ensure importlib.util
try:
    import importlib
    _ = getattr(importlib,"util")
except AttributeError:
    from importlib import util as ua
    setattr(importlib,"util",ua)
    del ua


# Python
def getExecutingPython() -> str:
    '''Returns the path to the python-executable used to start crosshell'''
    return sys.executable

def _check_pip(pipOvw=None) -> bool:
    '''Checks if PIP is present'''
    if pipOvw != None and os.path.exists(pipOvw): pipPath = pipOvw
    else: pipPath = getExecutingPython()
    try:
        with open(os.devnull, 'w') as devnull:
            subprocess.check_call([pipPath, "-m", "pip", "--version"], stdout=devnull, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        return False
    return True

def intpip(pip_args=str,pipOvw=None,pipMuteCommand=False,pipMuteEnsure=False):
    """Function to use pip from inside python, this function should also install pip if needed (Experimental)
    Returns: bool representing success or not
    
    NOTE! Might need --yes in args when using mute!"""

    if pipMuteCommand == True:
        subprocessParamsCommand = { "stdout":subprocess.DEVNULL, "stderr":subprocess.DEVNULL }
    else:
        subprocessParamsCommand = {}

    if pipMuteEnsure == True:
        subprocessParamsEnsure = { "stdout":subprocess.DEVNULL, "stderr":subprocess.DEVNULL }
    else:
        subprocessParamsEnsure = {}

    if pipOvw != None and os.path.exists(pipOvw): pipPath = pipOvw
    else: pipPath = getExecutingPython()
    if not _check_pip(pipOvw):
        print("PIP not found. Installing pip...")
        get_pip_script = "https://bootstrap.pypa.io/get-pip.py"
        try:
            subprocess.check_call([pipPath, "-m", "ensurepip"],**subprocessParamsEnsure)
        except subprocess.CalledProcessError:
            print("Failed to install pip using ensurepip. Aborting.")
            return False
        try:
            subprocess.check_call([pipPath, "-m", "pip", "install", "--upgrade", "pip"],**subprocessParamsEnsure)
        except subprocess.CalledProcessError:
            print("Failed to upgrade pip. Aborting.")
            return False
        try:
            subprocess.check_call([pipPath, "-m", "pip", "install", get_pip_script],**subprocessParamsEnsure)
        except subprocess.CalledProcessError:
            print("Failed to install pip using get-pip.py. Aborting.")
            return False
        print("PIP installed successfully.")
    try:
        subprocess.check_call([pipPath, "-m", "pip"] + pip_args.split(),**subprocessParamsCommand)
        return True
    except subprocess.CalledProcessError:
        print(f"Failed to execute pip command: {pip_args}")
        return False

# Safe import function
def autopipImport(moduleName=str,pipName=None,addPipArgsStr=None,cusPip=None,attr=None,relaunch=False,relaunchCmds=None,intpip_muteCommand=False,intpipt_mutePipEnsure=False):
    '''Tries to import the module, if failed installes using intpip and tries again.'''
    try:
        imported_module = importlib.import_module(moduleName)
    except:
        if pipName != None:
            command = f"install {pipName}"
        else:
            command = f"install {moduleName}"
        if addPipArgsStr != None:
            if not addPipArgsStr.startswith(" "):
                addPipArgsStr = " " + addPipArgsStr
            command += addPipArgsStr
        if cusPip != None:
            #os.system(f"{cusPip} {command}")
            intpip(command,pipOvw=cusPip, pipMuteCommand=intpip_muteCommand,pipMuteEnsure=intpipt_mutePipEnsure)
        else:
            intpip(command, pipMuteCommand=intpip_muteCommand,pipMuteEnsure=intpipt_mutePipEnsure)
        if relaunch == True and relaunchCmds != None and "--noPipReload" not in relaunchCmds:
            relaunchCmds.append("--noPipReload")
            if "python" not in relaunchCmds[0] and isPythonRuntime(relaunchCmds[0]) == False:
                relaunchCmds = [getExecutingPython(), *relaunchCmds]
            print("Relaunching to attempt reload of path...")
            print(f"With args:\n    {relaunchCmds}")
            subprocess.run([*relaunchCmds])
        else:
            imported_module = importlib.import_module(moduleName)
    if attr != None:
        return getattr(imported_module, attr)
    else:
        return imported_module

# Function to load a module from path
def fromPath(path, globals_dict=None):
    '''Import a module from a path. (Returns <module>)'''
    path = path.replace("/",os.sep).replace("\\",os.sep)
    spec = importlib.util.spec_from_file_location("module", path)
    module = importlib.util.module_from_spec(spec)
    if globals_dict:
        module.__dict__.update(globals_dict)
    spec.loader.exec_module(module)
    return module

def fromPathAA(path, globals_dict=None):
    '''Import a module from a path, to be used as: globals().update(fromPathAA(<path>)) (Returns <module>.__dict__)'''
    path = path.replace("/",os.sep).replace("\\",os.sep)
    spec = importlib.util.spec_from_file_location("module", path)
    module = importlib.util.module_from_spec(spec)
    if globals_dict:
        module.__dict__.update(globals_dict)
    spec.loader.exec_module(module)
    return module.__dict__

def installPipDeps(depsFile,encoding="utf-8",tagMapping=dict):
    '''Note! This takes a json file with a "deps" key, the fd function takes a deps list!'''
    deps = json.loads(open(depsFile,'r',encoding=encoding).read())["deps"]
    for dep in deps:
        for key,val in dep.items():
            for tag,tagVal in tagMapping.items():
                dep[key] = val.replace("{"+tag+"}",tagVal)
            _ = autopipImport(**dep)
    
def installPipDeps_fl(deps=list,tagMapping=dict):
    '''Note! This takes a deps list, the file function takes a json with a "deps" key!'''
    for dep in deps:
        for key,val in dep.items():
            for tag,tagVal in tagMapping.items():
                dep[key] = val.replace("{"+tag+"}",tagVal)
            _ = autopipImport(**dep)
    
def isPythonRuntime(filepath=str(),cusPip=None):
    exeFileEnds = [".exe"]
    if os.path.exists(filepath):
        try:
            # [Code]
            # Non Windows
            if platform.system() != "Windows":
                try:
                    magic = importlib.import_module("magic")
                except:
                    command = "install magic"
                    if cusPip != None:
                        #os.system(f"{cusPip} {command}")
                        intpip(command,pipOvw=cusPip)
                    else:
                        intpip(command)
                    magic = importlib.import_module("magic")
                detected = magic.detect_from_filename(filepath)
                return "application" in str(detected.mime_type)
            # Windows
            else:
                fending = str("." +''.join(filepath.split('.')[-1]))
                if fending in exeFileEnds:
                    return True
                else:
                    return False
        except Exception as e: print("\033[31mAn error occurred!\033[0m",e)
    else:
        raise Exception(f"File not found: {filepath}")

import base64, re

# Validators
def typeval(val,typeV,nm=None,allowNone=False):
    """Raises if type of 'val' does not match 'typeV'!"""
    if type(val) != typeV and (val is not None or not allowNone):
        try: typeN = typeV.__name__
        except: typeN = str(typeV)
        if nm == None: raise Exception(f"Invalid type for parameter, must be '{typeN}'!")
        else: raise Exception(f"Invalid type for parameter '{nm}', must be '{typeN}'!")
def instval(val,instV,nm=None,allowNone=False,instN=None,checkEq=False):
    """Raises if type of 'val' is not instance of 'instV'!"""
    if not isinstance(val, instV) and (val is not None and (checkEq and val != instV) or (not checkEq) or (val is None and not allowNone)) and (val is not None or not allowNone):
        try: typeN = instN if instN != None else instV.__name__
        except: typeN = str(instV)
        if nm == None: raise Exception(f"Invalid type for parameter, must be '{typeN}'!")
        else: raise Exception(f"Invalid type for parameter '{nm}', must be '{typeN}'!")

# Function to strip the comments of JSON-source
def strip_json_comments(json_string:str) -> str:
    """
    Removes both single-line (//) and multi-line (/* */) comments from a JSON string,
    while preserving the content of strings.
    
    Args:
        json_string (str): The JSON string with comments.
    
    Returns:
        str: The JSON string with comments removed.
    """
    typeval(json_string,str,"json_string")
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

# Base64 Functions
def encodeB64U8(string:str,encoding:str="utf-8") -> str:
    typeval(string,str,"string");typeval(encoding,str,"encoding")
    return base64.b64encode(string).decode(encoding)
def decodeB64U8(b64:bytes,encoding:str="utf-8") -> str:
    typeval(b64,bytes,"bytes");typeval(encoding,str,"encoding")
    return base64.b64decode(b64.encode(encoding))

# URL validator
def is_valid_url(url:str) -> bool:
    typeval(url,str,"url")
    # Regular expression pattern for matching URLs
    url_pattern = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https:// or ftp://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(url_pattern, url) is not None
# FancyPants/BeautifulPants 1.1 by Simon Kalmi Claesson
# Simple python library to download files or fetch get requests, with the possibility of a progress bar.

from bs4 import BeautifulSoup
import requests,os

from rich.progress import Progress,BarColumn,TextColumn,TimeRemainingColumn,DownloadColumn,TransferSpeedColumn,SpinnerColumn,TaskProgressColumn,RenderableColumn

def get_withProgess_rich(*args, richTitle="[cyan]Downloading...", postDownTxt=None, raise_for_status=False, **kwargs):
    """
    Wrapper function for requests.get that includes a visual loading bar made with rich.
    """
    response = requests.get(*args, **kwargs, stream=True)
    if raise_for_status == True: response.raise_for_status()
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 KB

    # Initialize the Rich progress bar
    from rich.progress import Progress,BarColumn,TextColumn,TimeRemainingColumn,DownloadColumn,TransferSpeedColumn,SpinnerColumn,TaskProgressColumn,RenderableColumn
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        DownloadColumn(),
        RenderableColumn("[cyan]ETA:"),
        TimeRemainingColumn(compact=True),
        TransferSpeedColumn(),
    ) as progress:
        task = progress.add_task(richTitle, total=total_size, expand=True)

        try:
            # Buffer to store downloaded content
            content_buffer = b''
            for data in response.iter_content(block_size):
                progress.update(task, advance=len(data))
                content_buffer += data

            # Return the response object with downloaded content
            response._content = content_buffer
            if postDownTxt not in ["",None]: print(postDownTxt)
            return response
        except Exception as e:
            # Ensure closing the progress bar and response in case of an exception
            raise e
        finally:
            # Close the progress bar and response
            progress.stop()
            response.close()

def get_withInfo(*args, prefTxt="", suffTxt="", raise_for_status=False, **kwargs):
    """
    Wrapper function for requests.get that takes strings to print before and after downloading.
    """
    if prefTxt not in ["",None]: print(prefTxt)
    response = requests.get(*args, **kwargs)
    if raise_for_status == True: response.raise_for_status()
    if suffTxt not in ["",None]: print(suffTxt)
    return response

def getFile_withProgess_rich(*args, filepath=str, richTitle="[cyan]Downloading...", postDownTxt=None, raise_for_status=True, onFileExiError="raise", stream=None, **kwargs):
    """
    Wrapper function for requests.get that includes a visual loading bar made with rich while downloading a file.
    To just wrap requests.get without a file use get_withProgess_rich().
    onFileExiError: "raise"/"ignore"/"ignore-with-warn"/"remove"/"remove-with-warn"
    """
    if os.path.exists(filepath):
        onFileExiError = onFileExiError.lower()
        if onFileExiError == "raise":
            raise FileExistsError(f"Failed to download the file: '{filepath}'! File already exists.")
        elif onFileExiError == "remove" or "-with-warn" in onFileExiError:
            if "-with-warn" in onFileExiError:
                print(f"File '{filepath}' already exists, ignoring.")
            if "remove" in onFileExiError: os.remove(filepath)
    response = requests.get(*args, **kwargs, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 KB

    # Initialize the Rich progress bar
    if response.status_code == 200:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            DownloadColumn(),
            RenderableColumn("[cyan]ETA:"),
            TimeRemainingColumn(compact=True),
            TransferSpeedColumn(),
        ) as progress:
            task = progress.add_task(richTitle, total=total_size, expand=True)
            try:
                # Download to file
                if stream == None:
                    with open(filepath, 'wb') as f:
                        for data in response.iter_content(block_size):
                            progress.update(task, advance=len(data))
                            f.write(data)
                else:
                    for data in response.iter_content(block_size):
                        progress.update(task, advance=len(data))
                        stream.write(data)
                # Return the response object
                if postDownTxt not in ["",None]: print(postDownTxt)
                return response
            except Exception as e:
                # Ensure closing the progress bar and response in case of an exception
                raise e
            finally:
                # Close the progress bar and response
                progress.stop()
                response.close()
    else:
        if raise_for_status == True:
            raise Exception(f"Failed to download the file: '{filepath}'! Invalid status code ({response.status_code}) or empty content.")
        else:
            return response

def getFile_withInfo(*args, filepath=str, prefTxt="", suffTxt="", raise_for_status=True, onFileExiError="raise", stream=None, **kwargs):
    """
    Wrapper function for requests.get that takes strings to print before and after downloading a file.
    To just wrap requests.get without a file use get_withInfo().
    onFileExiError: "raise"/"ignore"/"ignore-with-warn"/"remove"/"remove-with-warn"
    """
    if prefTxt not in ["",None]: print(prefTxt)
    response = requests.get(*args, **kwargs)
    if response.status_code == 200 and response.content not in ["",None]:
        if not os.path.exists(filepath):
            if stream == None:
                with open(filepath, 'wb') as file:
                    file.write(response.content)
            else:
                stream.write(response.content)
            if suffTxt not in ["",None]: print(suffTxt)
        else:
            onFileExiError = onFileExiError.lower()
            if onFileExiError == "raise":
                raise FileExistsError(f"Failed to download the file: '{filepath}'! File already exists.")
            elif onFileExiError == "remove" or "-with-warn" in onFileExiError:
                if "-with-warn" in onFileExiError:
                    print(f"File '{filepath}' already exists, ignoring.")
                if "remove" in onFileExiError: os.remove(filepath)
                with open(filepath, 'wb') as file:
                    file.write(response.content)
                if suffTxt not in ["",None]: print(suffTxt)
    else:
        if raise_for_status == True:
            raise Exception(f"Failed to download the file: '{filepath}'! Invalid status code ({response.status_code}) or empty content.")
    return response

def getUrlContent_HandleGdriveVirWarn(url,handleGdriveVirWarn=True, loadingBar=False, title="Downloading...", postDownText="", handleGdriveVirWarnText="Found gdrive scan warning, attempting to extract link and download from there...", raise_for_status=False, yieldResp=False):
    '''Function to send a get request to a url, and if a gdrive-virus-scan-warning appears try to extract the link and send a get request to it instead.'''
    if loadingBar == True: response = get_withProgess_rich(url,richTitle=title,postDownTxt=postDownText,raise_for_status=raise_for_status)
    else:                  response = get_withInfo(url,prefTxt=title,suffTxt=postDownText,raise_for_status=raise_for_status)
    #response = getter(url)
    if response.status_code == 200:
        # Content of the file
        if "<!DOCTYPE html>" in response.text and "Google Drive - Virus scan warning" in response.text and handleGdriveVirWarn == True:
            print(handleGdriveVirWarnText)
            # attempt extract
            soup = BeautifulSoup(response.text, 'html.parser')
            form = soup.find('form')
            linkBuild = form['action']
            hasParams = False
            inputs = form.find_all('input')
            toBeFound = ["id","export","confirm","uuid"]
            for inp in inputs:
                name = inp.attrs.get('name')
                value = inp.attrs.get('value')
                if name != None and name in toBeFound and value != None:
                    if hasParams == False:
                        pref = "?"
                        hasParams = True
                    else:
                        pref = "&"
                    linkBuild += f"{pref}{name}={value}"
            # Download from built link
            if loadingBar == True: response2 = get_withProgess_rich(linkBuild,richTitle=title,postDownTxt=postDownText,raise_for_status=raise_for_status)
            else:                  response2 = get_withInfo(linkBuild,prefTxt=title,suffTxt=postDownText,raise_for_status=raise_for_status)
            if response2.status_code == 200:
                if yieldResp == True:
                    return response2
                else:
                    return response2.content
            else:
                if yieldResp == True:
                    return response2
                else:
                    return None
        else:
            if yieldResp == True:
                return response
            else:
                return response.content
    # non 200 code
    else:
        if yieldResp == True:
            return response
        else:
            return None

def downloadFile_HandleGdriveVirWarn(url,filepath=str,handleGdriveVirWarn=True, loadingBar=False, title="Downloading...", postDownText="", handleGdriveVirWarnText="Found gdrive scan warning, attempting to extract link and download from there...", raise_for_status=True, encoding="utf-8", onFileExiError="raise", yieldResp=False, stream=None):
    """Function to try and download a file, and if a gdrive-virus-scan-warning appears try to extract the link and download it from there.
    onFileExiError: "raise"/"ignore"/"ignore-with-warn"/"remove"/"remove-with-warn"
    """
    if loadingBar == True: response = getFile_withProgess_rich(url,filepath=filepath,richTitle=title,postDownTxt=postDownText,raise_for_status=raise_for_status,onFileExiError=onFileExiError,stream=stream)
    else:                  response = getFile_withInfo(url,filepath=filepath,prefTxt=title,suffTxt=postDownText,raise_for_status=raise_for_status,onFileExiError=onFileExiError,stream=stream)
    # Get content of the file
    text_content = None
    if handleGdriveVirWarn == True and os.path.exists(filepath):
        if stream != None:
            text_content = stream.read()
        else:
            text_content = open(filepath, 'r', encoding=encoding, errors='replace').read()
        if text_content != None and "<!DOCTYPE html>" in text_content and "Google Drive - Virus scan warning" in text_content and handleGdriveVirWarn == True:
            os.remove(filepath) # clean up
            print(handleGdriveVirWarnText)
            # attempt extract
            soup = BeautifulSoup(text_content, 'html.parser')
            form = soup.find('form')
            linkBuild = form['action']
            hasParams = False
            inputs = form.find_all('input')
            toBeFound = ["id","export","confirm","uuid"]
            for inp in inputs:
                name = inp.attrs.get('name')
                value = inp.attrs.get('value')
                if name != None and name in toBeFound and value != None:
                    if hasParams == False:
                        pref = "?"
                        hasParams = True
                    else:
                        pref = "&"
                    linkBuild += f"{pref}{name}={value}"
            # Download from built link
            if loadingBar == True: response2 = getFile_withProgess_rich(linkBuild,filepath=filepath,richTitle=title,postDownTxt=postDownText,raise_for_status=raise_for_status,onFileExiError=onFileExiError,stream=stream)
            else:                  response2 = getFile_withInfo(linkBuild,filepath=filepath,prefTxt=title,suffTxt=postDownText,raise_for_status=raise_for_status,onFileExiError=onFileExiError,stream=stream)
            if not os.path.exists(filepath):
                raise Exception(f"Download of '{filepath}' seems to have failed! File does not exist.")
            else:
                if yieldResp == True:
                    return response2
        elif yieldResp == True:
            return response
    else:
        if yieldResp == True:
            return response
        else:
            raise Exception(f"Download of '{filepath}' seems to have failed! File does not exist.")

# Chibit Module 1.0 made by Simon Kalmi Claesson
#
# Modules for interacting with a chibit-store
# 

# Imports
import requests, zlib, os

# Main clas
class ChibitConnector():
    def __init__(self, hostUrl, reqType="requests", fancyPantsFuncs=None):
        """
        ChibitConnector is a class for interacting with a chibit-store.
        If 'reqType' is set to 'fancyPants', 'fancyPantsFuncs' must be given with a list of [<forDataFunc>,<forFileFunc>]
        """
        if hostUrl[-1] == '/':
            self.hostUrl = hostUrl[:-1]

        if reqType.lower() not in ["requests","fancypants"]:
            raise ValueError("reqType must be either 'requests' or 'fancypants'!")
        reqType = reqType.lower()

        if fancyPantsFuncs != None:
            valid = True
            for o in fancyPantsFuncs:
                if type(o) in [str,list,float,int,tuple,dict]:
                    valid = False
            if type(fancyPantsFuncs) != list or valid == False:
                raise ValueError("Given function instances for fancypants must be a list of objects")
        
        if reqType == "fancypants" and fancyPantsFuncs in [ None, [] ]:
            raise ValueError("For reqType = fancyPants, the fancypants functions must be given in order of [<forDataFunc>,<forFileFunc>].")
        
        self.reqType = reqType
        self.fancyPantsFuncs = fancyPantsFuncs

        self.hostUrl = hostUrl

    def _downloadChunks(self, urlList, verbose=False) -> list:
        """
        INTERNAL: Function for downloading chunks from a list of chunk-urls.
        """
        chunks = []
        max = len(urlList)
        if verbose: print(f"Downloading {max} chunks from urls...")
        ind = 0
        for url in urlList:
            if self.reqType == "requests":
                response = requests.get(url)
            else:
                if verbose: titleTx = f"Downloading {ind+1}/{max}..."
                else: titleTx = ""
                response = self.fancyPantsFuncs[0](
                    url = url,
                    handleGdriveVirWarn = True,
                    loadingBar = verbose,
                    title = titleTx,
                    postDownText = "",
                    handleGdriveVirWarnText = "Found gdrive scan warning, attempting to extract link and download from there...",
                    raise_for_status = False,
                    yieldResp = True
                )
            if response.status_code == 200:
                chunks.append(response.content)
                if verbose == True and self.reqType == "requests": print(f"Downloaded chunk {ind+1}/{max}")
                ind += 1
            else:
                raise Exception(f"Failed to download chunk from {url}! Status code: {response.status_code}")
        return chunks

    def _downloadChunksToTemp(self, fileid, urlList, tempDir, verbose=False, encoding="utf-8") -> list:
        """
        INTERNAL: Function for downloading chunks from a list of chunk-urls, using a temp folder.
        """
        chunks = []
        max = len(urlList)
        if verbose: print(f"Downloading {max} chunks from urls...")
        ind = 0
        for url in urlList:
            filepath = os.path.join(tempDir,f"{fileid}_{ind+1}.chunk")
            if self.reqType == "requests":
                response = requests.get(url)
            else:
                if verbose:
                    titleTx = f"Downloading {ind+1}/{max}..."
                    onFileExiError = "ignore-with-warn"
                else:
                    titleTx = ""
                    onFileExiError = "ignore"
                response = self.fancyPantsFuncs[1](
                    url = url,
                    filepath = filepath,
                    handleGdriveVirWarn = True,
                    loadingBar = verbose,
                    title = titleTx,
                    postDownText = "",
                    handleGdriveVirWarnText = "Found gdrive scan warning, attempting to extract link and download from there...",
                    raise_for_status = False,
                    encoding = encoding,
                    onFileExiError = onFileExiError,
                    yieldResp = True
                )
            if response.status_code == 200:
                chunks.append(filepath)
                if verbose == True and self.reqType == "requests": print(f"Downloaded chunk {ind+1}/{max}")
                ind += 1
            else:
                raise Exception(f"Failed to download chunk from {url}! Status code: {response.status_code}")
        return chunks

    def _downloadChunksToJoin(self, fileid, urlList, outputFile, verbose=False, encoding="utf-8"):
        """
        INTERNAL: Function for downloading chunks from a list of chunk-urls, appending them all to a final file.
        """
        if os.path.exists(outputFile):
            raise FileExistsError("_downloadChunksToJoin uses appending-IO so opening an existing file will append to it, ensure the file dosen't exist in forehand!")
        max = len(urlList)
        if verbose: print(f"Downloading {max} chunks from urls...")
        with open(outputFile, 'ab') as f:
            ind = 0
            for url in urlList:
                if self.reqType == "requests":
                    response = requests.get(url)
                else:
                    if verbose:
                        titleTx = f"Downloading {ind+1}/{max}..."
                        onFileExiError = "ignore-with-warn"
                    else:
                        titleTx = ""
                        onFileExiError = "ignore"
                    response = self.fancyPantsFuncs[1](
                        url = url,
                        filepath = fileid,
                        handleGdriveVirWarn = False,
                        loadingBar = verbose,
                        title = titleTx,
                        postDownText = "",
                        handleGdriveVirWarnText = "Found gdrive scan warning, attempting to extract link and download from there...",
                        raise_for_status = False,
                        encoding = encoding,
                        onFileExiError = onFileExiError,
                        yieldResp = True,
                        stream = f
                    )
                if response.status_code == 200:
                    if self.reqType == "requests":
                        f.write(response.content)
                        if verbose: print(f"Downloaded chunk {ind+1}/{max}")
                    ind += 1
                else:
                    raise Exception(f"Failed to download chunk from {url}! Status code: {response.status_code}")

    def _joinChunksData(self, chunkContents, verbose=False) -> bytes:
        """
        INTERNAL: Function for joining together chunkdata to a single byte-string.
        """
        joinedContent = b''
        if verbose: print(f"Joining {len(chunkContents)} chunks...")
        for chunk in chunkContents:
            joinedContent += chunk
        return joinedContent

    def _appendByteFiles(self, firstFile, fileList, verbose=False):
        """
        INTERNAL: Function for appending byte-files to a single final file.
        """
        try:
            # Open the first file in append mode
            with open(firstFile, 'ab') as f:
                for filePath in fileList:
                    try:
                        # Open each file in binary mode
                        with open(filePath, 'rb') as otherFile:
                            # Read the byte content of the other file
                            content = otherFile.read()
                            # Append the content to the first file
                            f.write(content)
                            otherFile.close()
                    except FileNotFoundError:
                        if verbose: print(f"File '{filePath}' not found. Skipping...")
                    except Exception as e:
                        if verbose: print(f"Error while reading '{filePath}': {e}")
                f.close()
        except Exception as e:
            if verbose: print(f"Error while opening '{firstFile}' for appending: {e}")

    def _joinChunksFile(self, chunkFiles, filepath, verbose=False):
        """
        INTERNAL: Function to join together chunk-files to a single file.
        """
        if verbose: print(f"Joining {len(chunkFiles)} chunk-files to 1...")
        self._appendByteFiles(filepath,chunkFiles,verbose)

    def _calculate_crc32(self, data) -> int:
        """
        INTERNAL: Calculate the crc32 checksum of a byte-string.
        """
        crc32Value = zlib.crc32(data)
        return crc32Value
    
    def _calculate_crc32_file(self, filepath) -> int:
        """
        INTERNAL: Calculate the crc32 checksum of a file.
        """
        crc32Value = zlib.crc32(open(filepath, "rb").read())
        return crc32Value

    def getChibit(self, fileid, verbose=False, hostOvv=None) -> dict:
        """
        Function to get a chibit for a fileid.

        Returns chibit-data.
        """
        if hostOvv != None: _host = hostOvv
        else: _host = self.hostUrl
        chibitUrl = f"{_host}/chibits/{fileid}.json"

        if self.reqType == "requests":
            response = requests.get(chibitUrl)
        else:
            if verbose: title = "Fetching chibit..."
            else: title = ""
            response = self.fancyPantsFuncs[0](
                url = chibitUrl,
                handleGdriveVirWarn = True,
                loadingBar = verbose,
                title = title,
                postDownText = "",
                handleGdriveVirWarnText = "Found gdrive scan warning, attempting to extract link and download from there...",
                raise_for_status = False,
                yieldResp = True
            )
        return response.json()

    def getRaw(self, fileid, safe=True, verbose=False, hostOvv=None) -> bytes:
        """
        Function to get the raw content of a chibit-stored file, from a fileid.
        """
        chibitData = self.getChibit(fileid, verbose, hostOvv=hostOvv)

        chunks = chibitData['chunks']

        chunkContents = self._downloadChunks(chunks,verbose=verbose)
        joinedContent = self._joinChunksData(chunkContents,verbose=verbose)

        if safe:
            algor = chibitData["checksum"]["algorithm"]
            hash_ = chibitData["checksum"]["hash"]
            if algor == "crc32":
                calculatedHash = self._calculate_crc32(joinedContent)
                if calculatedHash != hash_:
                    print(f"Checksum mismatch for {fileid}")
                    return None
                else:
                    return joinedContent
        else:
            return joinedContent

    def getRawFile(self, fileid, outputFile=None, safe=True, verbose=False, check_encoding="utf-8", hostOvv=None) -> str:
        """
        Function to get the raw content of a chibit-stored file, from a fileid, outputting to a file. (Works as a download)
        """
        chibitData = self.getChibit(fileid, verbose, hostOvv=hostOvv)

        chunks = chibitData['chunks']

        if outputFile == None or outputFile == "":
            outputFile = chibitData["filename"]

        self._downloadChunksToJoin(fileid, chunks, outputFile=outputFile, verbose=verbose, encoding=check_encoding)

        if safe:
            algor = chibitData["checksum"]["algorithm"]
            hash_ = chibitData["checksum"]["hash"]
            if algor == "crc32":
                calculatedHash = self._calculate_crc32_file(outputFile)
                if calculatedHash != hash_:
                    print(f"Checksum mismatch for {fileid}")
                    return None
                else:
                    return outputFile
        else:
            return outputFile

    def getRawFileWtemp(self, fileid, outputFile=None, safe=True, verbose=False, tempDir=None, check_encoding="utf-8", hostOvv=None) -> str:
        """
        Function to get the raw content of a chibit-stored file, from a fileid, outputting to a file. (Works as a download)

        Uses a temporary folder for chunk-files, before joining them together to the final file.
        """
        if tempDir == None: tempDir = os.path.join(os.getcwd(),".chibitTemp")
        if os.path.exists(tempDir): os.remove(tempDir)
        os.mkdir(tempDir)

        chibitData = self.getChibit(fileid, verbose, hostOvv=hostOvv)

        chunks = chibitData['chunks']

        if outputFile == None or outputFile == "":
            outputFile = os.path.join(os.getcwd(),chibitData["filename"])

        chunkFiles = self._downloadChunksToTemp(fileid, chunks, tempDir=tempDir, verbose=verbose, encoding=check_encoding)
        self._joinChunksFile(chunkFiles, outputFile, verbose)
        if os.path.exists(tempDir): os.remove(tempDir)

        if safe:
            algor = chibitData["checksum"]["algorithm"]
            hash_ = chibitData["checksum"]["hash"]
            if algor == "crc32":
                calculatedHash = self._calculate_crc32_file(outputFile)
                if calculatedHash != hash_:
                    print(f"Checksum mismatch for {fileid}/{chibitData['filename']}")
                    return None
                else:
                    return outputFile
        else:
            return outputFile

    def is_chibitPrefixedUrl(self, prefixedUrl) -> bool:
        """
        Function to check if a given url is a chibit-prefixed url.

        Format: chibit:<fileid>@<hostUrl>
        or:     chibit:<fileid>@<hostUrl>;<backupUrl>
        """
        if prefixedUrl.strip().startswith("chibit:"):
            return True
        else:
            return False

    def getComponents_FromPrefixedUrl(self, prefixedUrl) -> tuple:
        """
        Function to get the components of a chibit-prefixed url.

        Format: chibit:<fileid>@<hostUrl>
        or:     chibit:<fileid>@<hostUrl>;<backupUrl>

        Returns:
        {
            "original": <prefixedUrl>,
            "valid": <bool>,
            "fileid": <str>,
            "hostUrl": <str>,
            "backupUrl": <str>,
            "noBackupUrl": <str>
        }
        """
        data = {
            "original": prefixedUrl,
            "valid": False,
            "fileid": None,
            "hostUrl": None,
            "backupUrl": None,
            "noBackupUrl": None
        }
        if self.is_chibitPrefixedUrl(prefixedUrl):
            data["valid"] = True
            prefixedUrl = prefixedUrl.strip().replace("chibit:","")
            if ";" in prefixedUrl:
                parts = prefixedUrl.split(";")
                data["backupUrl"] = parts[-1]
                parts.pop(-1)
                prefixedUrl = ';'.join(parts)
                prefixedUrl = prefixedUrl.strip(";")
                data["noBackupUrl"] = "chibit:"+prefixedUrl
            
            if "@" in prefixedUrl:
                fileid, hostUrl = prefixedUrl.split("@")
                if hostUrl == "": hostUrl = None
                data["fileid"] = fileid
                data["hostUrl"] = hostUrl
            
            return data
        else:
            return data

    def getRaw_FromPrefixedUrl(self, prefixedUrl, safe=True, verbose=False) -> bytes:
        """
        Function to get the raw content of a chibit-stored file, from a prefixed url.

        Format: chibit:<fileid>@<hostUrl>
        or:     chibit:<fileid>@<hostUrl>;<backupUrl>
        """
        
        components = self.getComponents_FromPrefixedUrl(prefixedUrl)
        if components["valid"] == True:
            return self.getRaw(components["fileid"], safe, verbose, hostOvv=components["hostUrl"])
        else:
            raise ValueError("Inputed url did not contain the 'chibit:' prefix! (Format: chibit:<fileid>@<hostUrl> or chibit:<fileid>@<hostUrl>;<backupUrl>)")

    def getRawFile_FromPrefixedUrl(self, prefixedUrl, outputFile=None, safe=True, verbose=False, check_encoding="utf-8", useTemp=False, tempDir=None) -> str:
        """
        Function to get the raw content of a chibit-stored file, from a prefixed url.

        Format: chibit:<fileid>@<hostUrl>
        or:     chibit:<fileid>@<hostUrl>;<backupUrl>
        """
        
        components = self.getComponents_FromPrefixedUrl(prefixedUrl)
        if components["valid"] == True:
            if useTemp == True:
                if useTemp == True and (tempDir == None or not os.path.exists(tempDir)):
                    raise ValueError("When using temp, a tempDir must be given and exist!")
                return self.getRawFileWtemp(components["fileid"], outputFile, safe, verbose, tempDir, check_encoding, hostOvv=components["hostUrl"])
            else:
                return self.getRawFile(components["fileid"], outputFile, safe, verbose, check_encoding, hostOvv=components["hostUrl"])
        else:
            raise ValueError("Inputed url did not contain the 'chibit:' prefix! (Format: chibit:<fileid>@<hostUrl> or chibit:<fileid>@<hostUrl>;<backupUrl>)")



class Networking():

    class ChibitConn(ChibitConnector):
        def __init__(self,chibitHostUrl:str):
            typeval(chibitHostUrl,str,"chibitHostUrl")
            super().__init__(
                hostUrl = chibitHostUrl,
                reqType = "fancyPants",
                fancyPantsFuncs = [
                    getUrlContent_HandleGdriveVirWarn,
                    downloadFile_HandleGdriveVirWarn
                ]
            )

    @staticmethod
    def testConnection(override_url:str=None):
        typeval(override_url,str,"override_url",True)
        # If no url is given, default to google.
        if override_url == None or override_url == "":
            override_url = "https://google.com"
        # Check/Validate the connection, catch exeptions and return boolean
        try:
            req = requests.get(override_url)
            req.raise_for_status()
        except:
            return False
        return True

    @staticmethod
    def fetchContent(url:str, title:str="Downloading...", postText:str="", handleGdriveVirWarnText:str="Found gdrive scan warning, attempting to extract link and download from there..."):
        typeval(url,str,"url"); typeval(title,str,"title"); typeval(postText,str,"postText"); typeval(handleGdriveVirWarnText,str,"handleGdriveVirWarnText")
        return getUrlContent_HandleGdriveVirWarn(
            url = url,
            handleGdriveVirWarn = True,
            loadingBar = False,
            title = title,
            postDownText = postText,
            handleGdriveVirWarnText = handleGdriveVirWarnText,
            raise_for_status = True,
            yieldResp = False
        )
    @staticmethod
    def fetchContent_progress(url:str, title:str="Downloading...", postText:str="", handleGdriveVirWarnText:str="Found gdrive scan warning, attempting to extract link and download from there..."):
        typeval(url,str,"url"); typeval(title,str,"title"); typeval(postText,str,"postText"); typeval(handleGdriveVirWarnText,str,"handleGdriveVirWarnText")
        return getUrlContent_HandleGdriveVirWarn(
            url = url,
            handleGdriveVirWarn = True,
            loadingBar = True,
            title = title,
            postDownText = postText,
            handleGdriveVirWarnText = handleGdriveVirWarnText,
            raise_for_status = True,
            yieldResp = False
        )
    @staticmethod
    def fetchContent_silent(url:str):
        typeval(url,str,"url")
        return getUrlContent_HandleGdriveVirWarn(
            url = url,
            handleGdriveVirWarn = True,
            loadingBar = False,
            title = "",
            postDownText = "",
            handleGdriveVirWarnText = "",
            raise_for_status = True,
            yieldResp = False
        )

    @staticmethod
    def fetchFile(url:str,filepath:str, title:str="Downloading...", postText:str="", handleGdriveVirWarnText:str="Found gdrive scan warning, attempting to extract link and download from there...", encoding:str="utf-8", stream=None):
        typeval(url,str,"url"); typeval(filepath,str,"filepath"); typeval(title,str,"title"); typeval(postText,str,"postText"); typeval(handleGdriveVirWarnText,str,"handleGdriveVirWarnText"); typeval(encoding,str,"encoding")
        return downloadFile_HandleGdriveVirWarn(
            url = url,
            filepath = filepath,
            handleGdriveVirWarn = True,
            loadingBar = False,
            title = title,
            postDownText = postText,
            handleGdriveVirWarnText = handleGdriveVirWarnText,
            raise_for_status = True,
            encoding = encoding,
            onFileExiError = "raise",
            yieldResp = False,
            stream = stream
        )
    @staticmethod
    def fetchFile_progress(url:str,filepath:str, title:str="Downloading...", postText:str="", handleGdriveVirWarnText:str="Found gdrive scan warning, attempting to extract link and download from there...", encoding:str="utf-8", stream=None):
        typeval(url,str,"url"); typeval(filepath,str,"filepath"); typeval(title,str,"title"); typeval(postText,str,"postText"); typeval(handleGdriveVirWarnText,str,"handleGdriveVirWarnText"); typeval(encoding,str,"encoding")
        return downloadFile_HandleGdriveVirWarn(
            url = url,
            filepath = filepath,
            handleGdriveVirWarn = True,
            loadingBar = True,
            title = title,
            postDownText = postText,
            handleGdriveVirWarnText = handleGdriveVirWarnText,
            raise_for_status = True,
            encoding = encoding,
            onFileExiError = "raise",
            yieldResp = False,
            stream = stream
        )
    @staticmethod
    def fetchFile_silent(url:str,filepath:str, encoding:str="utf-8", stream=None):
        typeval(url,str,"url"); typeval(filepath,str,"filepath"); typeval(encoding,str,"encoding")
        return downloadFile_HandleGdriveVirWarn(
            url = url,
            filepath = filepath,
            handleGdriveVirWarn = True,
            loadingBar = False,
            title = "",
            postDownText = "",
            handleGdriveVirWarnText = "",
            raise_for_status = True,
            encoding = encoding,
            onFileExiError = "raise",
            yieldResp = False,
            stream = stream
        )


class Services():

    class local_JVM_Manager():
        def __init__(self,parentPath=str):
            self.platform = platform.system().lower()
            self.parentPath = parentPath

    class JVM_Manager():
        def __init__(self):
            self.platform = platform.system().lower()
        
        def checkJavaExistence(self):
            pass

        def getJavaPath(self):
            pass

        def ensureJavaExistance(self,local_JVM_Manager):
            pass

class RepositoryConnector():
    def __init__(self,repofileUrl:str=str,NetworkingClass=None):
        typeval(repofileUrl,str,"repofileUrl")
        Networking_checker = mcclib.Networking
        instval(NetworkingClass,Networking_checker,"NetworkingClass",False,"mcclib.Networking",True)
        self.url = repofileUrl
        self.net = NetworkingClass
        self.rawContent = None
        self.parsedContent = None

    def fetch(self, title="Downloading repo...", postText="", handleGdriveVirWarnText="Found gdrive scan warning, attempting to extract link and download from there..."):
        typeval(title,str,"title"); typeval(title,str,"postText"); typeval(handleGdriveVirWarnText,str,"handleGdriveVirWarnText")
        self.rawContent = self.net.fetchContent(self.url,title,postText,handleGdriveVirWarnText)
        self.parsedContent = json.loads(self.rawContent)
    def fetch_progress(self, title="Downloading repo...", postText="", handleGdriveVirWarnText="Found gdrive scan warning, attempting to extract link and download from there..."):
        typeval(title,str,"title"); typeval(title,str,"postText"); typeval(handleGdriveVirWarnText,str,"handleGdriveVirWarnText")
        self.rawContent = self.net.fetchContent_progress(self.url,title,postText,handleGdriveVirWarnText)
        self.parsedContent = json.loads(self.rawContent)
    def fetch_silent(self, *ignored,**kignored):
        self.rawContent = strip_json_comments(
            self.net.fetchContent_silent(self.url)
        )
        self.parsedContent = json.loads(self.rawContent)

    def get(self) -> dict:
        if self.rawContent == None or self.parsedContent == None:
            raise ValueError("Attempted operation on RepositorConnector without having it fetched!")
        else:
            return self.parsedContent

    def validateToFormat(self,formatVer=int) -> bool:
        typeval(formatVer,int,"formatVer")
        if self.get().get("format") != formatVer:
            return False
        else:
            return True
    
    def getRepoMeta(self) -> dict:
        _p = self.get()
        return {
            "format": _p.get("format"),
            "author": _p.get("author"),
            "version": _p.get("version"),
            "created": _p.get("created"),
            "lastUpdated": _p.get("lastUpdated")
        }
    
    def getAmntFlavors(self) -> int|None:
        _p = self.get().get("flavors")
        if _p == None:
            del _p
            return None
        else:
            return len(_p)

class Repository():
    pass

class mcclib():
    # FancyPants/BeautifulPants 1.1 by Simon Kalmi Claesson
    # Simple python library to download files or fetch get requests, with the possibility of a progress bar.
    
    from bs4 import BeautifulSoup
    import requests,os
    
    from rich.progress import Progress,BarColumn,TextColumn,TimeRemainingColumn,DownloadColumn,TransferSpeedColumn,SpinnerColumn,TaskProgressColumn,RenderableColumn
    
    def get_withProgess_rich(*args, richTitle="[cyan]Downloading...", postDownTxt=None, raise_for_status=False, **kwargs):
        """
        Wrapper function for requests.get that includes a visual loading bar made with rich.
        """
        response = requests.get(*args, **kwargs, stream=True)
        if raise_for_status == True: response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 KB
    
        # Initialize the Rich progress bar
        from rich.progress import Progress,BarColumn,TextColumn,TimeRemainingColumn,DownloadColumn,TransferSpeedColumn,SpinnerColumn,TaskProgressColumn,RenderableColumn
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            DownloadColumn(),
            RenderableColumn("[cyan]ETA:"),
            TimeRemainingColumn(compact=True),
            TransferSpeedColumn(),
        ) as progress:
            task = progress.add_task(richTitle, total=total_size, expand=True)
    
            try:
                # Buffer to store downloaded content
                content_buffer = b''
                for data in response.iter_content(block_size):
                    progress.update(task, advance=len(data))
                    content_buffer += data
    
                # Return the response object with downloaded content
                response._content = content_buffer
                if postDownTxt not in ["",None]: print(postDownTxt)
                return response
            except Exception as e:
                # Ensure closing the progress bar and response in case of an exception
                raise e
            finally:
                # Close the progress bar and response
                progress.stop()
                response.close()
    
    def get_withInfo(*args, prefTxt="", suffTxt="", raise_for_status=False, **kwargs):
        """
        Wrapper function for requests.get that takes strings to print before and after downloading.
        """
        if prefTxt not in ["",None]: print(prefTxt)
        response = requests.get(*args, **kwargs)
        if raise_for_status == True: response.raise_for_status()
        if suffTxt not in ["",None]: print(suffTxt)
        return response
    
    def getFile_withProgess_rich(*args, filepath=str, richTitle="[cyan]Downloading...", postDownTxt=None, raise_for_status=True, onFileExiError="raise", stream=None, **kwargs):
        """
        Wrapper function for requests.get that includes a visual loading bar made with rich while downloading a file.
        To just wrap requests.get without a file use get_withProgess_rich().
        onFileExiError: "raise"/"ignore"/"ignore-with-warn"/"remove"/"remove-with-warn"
        """
        if os.path.exists(filepath):
            onFileExiError = onFileExiError.lower()
            if onFileExiError == "raise":
                raise FileExistsError(f"Failed to download the file: '{filepath}'! File already exists.")
            elif onFileExiError == "remove" or "-with-warn" in onFileExiError:
                if "-with-warn" in onFileExiError:
                    print(f"File '{filepath}' already exists, ignoring.")
                if "remove" in onFileExiError: os.remove(filepath)
        response = requests.get(*args, **kwargs, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 KB
    
        # Initialize the Rich progress bar
        if response.status_code == 200:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                DownloadColumn(),
                RenderableColumn("[cyan]ETA:"),
                TimeRemainingColumn(compact=True),
                TransferSpeedColumn(),
            ) as progress:
                task = progress.add_task(richTitle, total=total_size, expand=True)
                try:
                    # Download to file
                    if stream == None:
                        with open(filepath, 'wb') as f:
                            for data in response.iter_content(block_size):
                                progress.update(task, advance=len(data))
                                f.write(data)
                    else:
                        for data in response.iter_content(block_size):
                            progress.update(task, advance=len(data))
                            stream.write(data)
                    # Return the response object
                    if postDownTxt not in ["",None]: print(postDownTxt)
                    return response
                except Exception as e:
                    # Ensure closing the progress bar and response in case of an exception
                    raise e
                finally:
                    # Close the progress bar and response
                    progress.stop()
                    response.close()
        else:
            if raise_for_status == True:
                raise Exception(f"Failed to download the file: '{filepath}'! Invalid status code ({response.status_code}) or empty content.")
            else:
                return response
    
    def getFile_withInfo(*args, filepath=str, prefTxt="", suffTxt="", raise_for_status=True, onFileExiError="raise", stream=None, **kwargs):
        """
        Wrapper function for requests.get that takes strings to print before and after downloading a file.
        To just wrap requests.get without a file use get_withInfo().
        onFileExiError: "raise"/"ignore"/"ignore-with-warn"/"remove"/"remove-with-warn"
        """
        if prefTxt not in ["",None]: print(prefTxt)
        response = requests.get(*args, **kwargs)
        if response.status_code == 200 and response.content not in ["",None]:
            if not os.path.exists(filepath):
                if stream == None:
                    with open(filepath, 'wb') as file:
                        file.write(response.content)
                else:
                    stream.write(response.content)
                if suffTxt not in ["",None]: print(suffTxt)
            else:
                onFileExiError = onFileExiError.lower()
                if onFileExiError == "raise":
                    raise FileExistsError(f"Failed to download the file: '{filepath}'! File already exists.")
                elif onFileExiError == "remove" or "-with-warn" in onFileExiError:
                    if "-with-warn" in onFileExiError:
                        print(f"File '{filepath}' already exists, ignoring.")
                    if "remove" in onFileExiError: os.remove(filepath)
                    with open(filepath, 'wb') as file:
                        file.write(response.content)
                    if suffTxt not in ["",None]: print(suffTxt)
        else:
            if raise_for_status == True:
                raise Exception(f"Failed to download the file: '{filepath}'! Invalid status code ({response.status_code}) or empty content.")
        return response
    
    def getUrlContent_HandleGdriveVirWarn(url,handleGdriveVirWarn=True, loadingBar=False, title="Downloading...", postDownText="", handleGdriveVirWarnText="Found gdrive scan warning, attempting to extract link and download from there...", raise_for_status=False, yieldResp=False):
        '''Function to send a get request to a url, and if a gdrive-virus-scan-warning appears try to extract the link and send a get request to it instead.'''
        if loadingBar == True: response = get_withProgess_rich(url,richTitle=title,postDownTxt=postDownText,raise_for_status=raise_for_status)
        else:                  response = get_withInfo(url,prefTxt=title,suffTxt=postDownText,raise_for_status=raise_for_status)
        #response = getter(url)
        if response.status_code == 200:
            # Content of the file
            if "<!DOCTYPE html>" in response.text and "Google Drive - Virus scan warning" in response.text and handleGdriveVirWarn == True:
                print(handleGdriveVirWarnText)
                # attempt extract
                soup = BeautifulSoup(response.text, 'html.parser')
                form = soup.find('form')
                linkBuild = form['action']
                hasParams = False
                inputs = form.find_all('input')
                toBeFound = ["id","export","confirm","uuid"]
                for inp in inputs:
                    name = inp.attrs.get('name')
                    value = inp.attrs.get('value')
                    if name != None and name in toBeFound and value != None:
                        if hasParams == False:
                            pref = "?"
                            hasParams = True
                        else:
                            pref = "&"
                        linkBuild += f"{pref}{name}={value}"
                # Download from built link
                if loadingBar == True: response2 = get_withProgess_rich(linkBuild,richTitle=title,postDownTxt=postDownText,raise_for_status=raise_for_status)
                else:                  response2 = get_withInfo(linkBuild,prefTxt=title,suffTxt=postDownText,raise_for_status=raise_for_status)
                if response2.status_code == 200:
                    if yieldResp == True:
                        return response2
                    else:
                        return response2.content
                else:
                    if yieldResp == True:
                        return response2
                    else:
                        return None
            else:
                if yieldResp == True:
                    return response
                else:
                    return response.content
        # non 200 code
        else:
            if yieldResp == True:
                return response
            else:
                return None
    
    def downloadFile_HandleGdriveVirWarn(url,filepath=str,handleGdriveVirWarn=True, loadingBar=False, title="Downloading...", postDownText="", handleGdriveVirWarnText="Found gdrive scan warning, attempting to extract link and download from there...", raise_for_status=True, encoding="utf-8", onFileExiError="raise", yieldResp=False, stream=None):
        """Function to try and download a file, and if a gdrive-virus-scan-warning appears try to extract the link and download it from there.
        onFileExiError: "raise"/"ignore"/"ignore-with-warn"/"remove"/"remove-with-warn"
        """
        if loadingBar == True: response = getFile_withProgess_rich(url,filepath=filepath,richTitle=title,postDownTxt=postDownText,raise_for_status=raise_for_status,onFileExiError=onFileExiError,stream=stream)
        else:                  response = getFile_withInfo(url,filepath=filepath,prefTxt=title,suffTxt=postDownText,raise_for_status=raise_for_status,onFileExiError=onFileExiError,stream=stream)
        # Get content of the file
        text_content = None
        if handleGdriveVirWarn == True and os.path.exists(filepath):
            if stream != None:
                text_content = stream.read()
            else:
                text_content = open(filepath, 'r', encoding=encoding, errors='replace').read()
            if text_content != None and "<!DOCTYPE html>" in text_content and "Google Drive - Virus scan warning" in text_content and handleGdriveVirWarn == True:
                os.remove(filepath) # clean up
                print(handleGdriveVirWarnText)
                # attempt extract
                soup = BeautifulSoup(text_content, 'html.parser')
                form = soup.find('form')
                linkBuild = form['action']
                hasParams = False
                inputs = form.find_all('input')
                toBeFound = ["id","export","confirm","uuid"]
                for inp in inputs:
                    name = inp.attrs.get('name')
                    value = inp.attrs.get('value')
                    if name != None and name in toBeFound and value != None:
                        if hasParams == False:
                            pref = "?"
                            hasParams = True
                        else:
                            pref = "&"
                        linkBuild += f"{pref}{name}={value}"
                # Download from built link
                if loadingBar == True: response2 = getFile_withProgess_rich(linkBuild,filepath=filepath,richTitle=title,postDownTxt=postDownText,raise_for_status=raise_for_status,onFileExiError=onFileExiError,stream=stream)
                else:                  response2 = getFile_withInfo(linkBuild,filepath=filepath,prefTxt=title,suffTxt=postDownText,raise_for_status=raise_for_status,onFileExiError=onFileExiError,stream=stream)
                if not os.path.exists(filepath):
                    raise Exception(f"Download of '{filepath}' seems to have failed! File does not exist.")
                else:
                    if yieldResp == True:
                        return response2
            elif yieldResp == True:
                return response
        else:
            if yieldResp == True:
                return response
            else:
                raise Exception(f"Download of '{filepath}' seems to have failed! File does not exist.")
    
    # Chibit Module 1.0 made by Simon Kalmi Claesson
    #
    # Modules for interacting with a chibit-store
    # 
    
    # Imports
    import requests, zlib, os
    
    # Main clas
    class ChibitConnector():
        def __init__(self, hostUrl, reqType="requests", fancyPantsFuncs=None):
            """
            ChibitConnector is a class for interacting with a chibit-store.
            If 'reqType' is set to 'fancyPants', 'fancyPantsFuncs' must be given with a list of [<forDataFunc>,<forFileFunc>]
            """
            if hostUrl[-1] == '/':
                self.hostUrl = hostUrl[:-1]
    
            if reqType.lower() not in ["requests","fancypants"]:
                raise ValueError("reqType must be either 'requests' or 'fancypants'!")
            reqType = reqType.lower()
    
            if fancyPantsFuncs != None:
                valid = True
                for o in fancyPantsFuncs:
                    if type(o) in [str,list,float,int,tuple,dict]:
                        valid = False
                if type(fancyPantsFuncs) != list or valid == False:
                    raise ValueError("Given function instances for fancypants must be a list of objects")
            
            if reqType == "fancypants" and fancyPantsFuncs in [ None, [] ]:
                raise ValueError("For reqType = fancyPants, the fancypants functions must be given in order of [<forDataFunc>,<forFileFunc>].")
            
            self.reqType = reqType
            self.fancyPantsFuncs = fancyPantsFuncs
    
            self.hostUrl = hostUrl
    
        def _downloadChunks(self, urlList, verbose=False) -> list:
            """
            INTERNAL: Function for downloading chunks from a list of chunk-urls.
            """
            chunks = []
            max = len(urlList)
            if verbose: print(f"Downloading {max} chunks from urls...")
            ind = 0
            for url in urlList:
                if self.reqType == "requests":
                    response = requests.get(url)
                else:
                    if verbose: titleTx = f"Downloading {ind+1}/{max}..."
                    else: titleTx = ""
                    response = self.fancyPantsFuncs[0](
                        url = url,
                        handleGdriveVirWarn = True,
                        loadingBar = verbose,
                        title = titleTx,
                        postDownText = "",
                        handleGdriveVirWarnText = "Found gdrive scan warning, attempting to extract link and download from there...",
                        raise_for_status = False,
                        yieldResp = True
                    )
                if response.status_code == 200:
                    chunks.append(response.content)
                    if verbose == True and self.reqType == "requests": print(f"Downloaded chunk {ind+1}/{max}")
                    ind += 1
                else:
                    raise Exception(f"Failed to download chunk from {url}! Status code: {response.status_code}")
            return chunks
    
        def _downloadChunksToTemp(self, fileid, urlList, tempDir, verbose=False, encoding="utf-8") -> list:
            """
            INTERNAL: Function for downloading chunks from a list of chunk-urls, using a temp folder.
            """
            chunks = []
            max = len(urlList)
            if verbose: print(f"Downloading {max} chunks from urls...")
            ind = 0
            for url in urlList:
                filepath = os.path.join(tempDir,f"{fileid}_{ind+1}.chunk")
                if self.reqType == "requests":
                    response = requests.get(url)
                else:
                    if verbose:
                        titleTx = f"Downloading {ind+1}/{max}..."
                        onFileExiError = "ignore-with-warn"
                    else:
                        titleTx = ""
                        onFileExiError = "ignore"
                    response = self.fancyPantsFuncs[1](
                        url = url,
                        filepath = filepath,
                        handleGdriveVirWarn = True,
                        loadingBar = verbose,
                        title = titleTx,
                        postDownText = "",
                        handleGdriveVirWarnText = "Found gdrive scan warning, attempting to extract link and download from there...",
                        raise_for_status = False,
                        encoding = encoding,
                        onFileExiError = onFileExiError,
                        yieldResp = True
                    )
                if response.status_code == 200:
                    chunks.append(filepath)
                    if verbose == True and self.reqType == "requests": print(f"Downloaded chunk {ind+1}/{max}")
                    ind += 1
                else:
                    raise Exception(f"Failed to download chunk from {url}! Status code: {response.status_code}")
            return chunks
    
        def _downloadChunksToJoin(self, fileid, urlList, outputFile, verbose=False, encoding="utf-8"):
            """
            INTERNAL: Function for downloading chunks from a list of chunk-urls, appending them all to a final file.
            """
            if os.path.exists(outputFile):
                raise FileExistsError("_downloadChunksToJoin uses appending-IO so opening an existing file will append to it, ensure the file dosen't exist in forehand!")
            max = len(urlList)
            if verbose: print(f"Downloading {max} chunks from urls...")
            with open(outputFile, 'ab') as f:
                ind = 0
                for url in urlList:
                    if self.reqType == "requests":
                        response = requests.get(url)
                    else:
                        if verbose:
                            titleTx = f"Downloading {ind+1}/{max}..."
                            onFileExiError = "ignore-with-warn"
                        else:
                            titleTx = ""
                            onFileExiError = "ignore"
                        response = self.fancyPantsFuncs[1](
                            url = url,
                            filepath = fileid,
                            handleGdriveVirWarn = False,
                            loadingBar = verbose,
                            title = titleTx,
                            postDownText = "",
                            handleGdriveVirWarnText = "Found gdrive scan warning, attempting to extract link and download from there...",
                            raise_for_status = False,
                            encoding = encoding,
                            onFileExiError = onFileExiError,
                            yieldResp = True,
                            stream = f
                        )
                    if response.status_code == 200:
                        if self.reqType == "requests":
                            f.write(response.content)
                            if verbose: print(f"Downloaded chunk {ind+1}/{max}")
                        ind += 1
                    else:
                        raise Exception(f"Failed to download chunk from {url}! Status code: {response.status_code}")
    
        def _joinChunksData(self, chunkContents, verbose=False) -> bytes:
            """
            INTERNAL: Function for joining together chunkdata to a single byte-string.
            """
            joinedContent = b''
            if verbose: print(f"Joining {len(chunkContents)} chunks...")
            for chunk in chunkContents:
                joinedContent += chunk
            return joinedContent
    
        def _appendByteFiles(self, firstFile, fileList, verbose=False):
            """
            INTERNAL: Function for appending byte-files to a single final file.
            """
            try:
                # Open the first file in append mode
                with open(firstFile, 'ab') as f:
                    for filePath in fileList:
                        try:
                            # Open each file in binary mode
                            with open(filePath, 'rb') as otherFile:
                                # Read the byte content of the other file
                                content = otherFile.read()
                                # Append the content to the first file
                                f.write(content)
                                otherFile.close()
                        except FileNotFoundError:
                            if verbose: print(f"File '{filePath}' not found. Skipping...")
                        except Exception as e:
                            if verbose: print(f"Error while reading '{filePath}': {e}")
                    f.close()
            except Exception as e:
                if verbose: print(f"Error while opening '{firstFile}' for appending: {e}")
    
        def _joinChunksFile(self, chunkFiles, filepath, verbose=False):
            """
            INTERNAL: Function to join together chunk-files to a single file.
            """
            if verbose: print(f"Joining {len(chunkFiles)} chunk-files to 1...")
            self._appendByteFiles(filepath,chunkFiles,verbose)
    
        def _calculate_crc32(self, data) -> int:
            """
            INTERNAL: Calculate the crc32 checksum of a byte-string.
            """
            crc32Value = zlib.crc32(data)
            return crc32Value
        
        def _calculate_crc32_file(self, filepath) -> int:
            """
            INTERNAL: Calculate the crc32 checksum of a file.
            """
            crc32Value = zlib.crc32(open(filepath, "rb").read())
            return crc32Value
    
        def getChibit(self, fileid, verbose=False, hostOvv=None) -> dict:
            """
            Function to get a chibit for a fileid.
    
            Returns chibit-data.
            """
            if hostOvv != None: _host = hostOvv
            else: _host = self.hostUrl
            chibitUrl = f"{_host}/chibits/{fileid}.json"
    
            if self.reqType == "requests":
                response = requests.get(chibitUrl)
            else:
                if verbose: title = "Fetching chibit..."
                else: title = ""
                response = self.fancyPantsFuncs[0](
                    url = chibitUrl,
                    handleGdriveVirWarn = True,
                    loadingBar = verbose,
                    title = title,
                    postDownText = "",
                    handleGdriveVirWarnText = "Found gdrive scan warning, attempting to extract link and download from there...",
                    raise_for_status = False,
                    yieldResp = True
                )
            return response.json()
    
        def getRaw(self, fileid, safe=True, verbose=False, hostOvv=None) -> bytes:
            """
            Function to get the raw content of a chibit-stored file, from a fileid.
            """
            chibitData = self.getChibit(fileid, verbose, hostOvv=hostOvv)
    
            chunks = chibitData['chunks']
    
            chunkContents = self._downloadChunks(chunks,verbose=verbose)
            joinedContent = self._joinChunksData(chunkContents,verbose=verbose)
    
            if safe:
                algor = chibitData["checksum"]["algorithm"]
                hash_ = chibitData["checksum"]["hash"]
                if algor == "crc32":
                    calculatedHash = self._calculate_crc32(joinedContent)
                    if calculatedHash != hash_:
                        print(f"Checksum mismatch for {fileid}")
                        return None
                    else:
                        return joinedContent
            else:
                return joinedContent
    
        def getRawFile(self, fileid, outputFile=None, safe=True, verbose=False, check_encoding="utf-8", hostOvv=None) -> str:
            """
            Function to get the raw content of a chibit-stored file, from a fileid, outputting to a file. (Works as a download)
            """
            chibitData = self.getChibit(fileid, verbose, hostOvv=hostOvv)
    
            chunks = chibitData['chunks']
    
            if outputFile == None or outputFile == "":
                outputFile = chibitData["filename"]
    
            self._downloadChunksToJoin(fileid, chunks, outputFile=outputFile, verbose=verbose, encoding=check_encoding)
    
            if safe:
                algor = chibitData["checksum"]["algorithm"]
                hash_ = chibitData["checksum"]["hash"]
                if algor == "crc32":
                    calculatedHash = self._calculate_crc32_file(outputFile)
                    if calculatedHash != hash_:
                        print(f"Checksum mismatch for {fileid}")
                        return None
                    else:
                        return outputFile
            else:
                return outputFile
    
        def getRawFileWtemp(self, fileid, outputFile=None, safe=True, verbose=False, tempDir=None, check_encoding="utf-8", hostOvv=None) -> str:
            """
            Function to get the raw content of a chibit-stored file, from a fileid, outputting to a file. (Works as a download)
    
            Uses a temporary folder for chunk-files, before joining them together to the final file.
            """
            if tempDir == None: tempDir = os.path.join(os.getcwd(),".chibitTemp")
            if os.path.exists(tempDir): os.remove(tempDir)
            os.mkdir(tempDir)
    
            chibitData = self.getChibit(fileid, verbose, hostOvv=hostOvv)
    
            chunks = chibitData['chunks']
    
            if outputFile == None or outputFile == "":
                outputFile = os.path.join(os.getcwd(),chibitData["filename"])
    
            chunkFiles = self._downloadChunksToTemp(fileid, chunks, tempDir=tempDir, verbose=verbose, encoding=check_encoding)
            self._joinChunksFile(chunkFiles, outputFile, verbose)
            if os.path.exists(tempDir): os.remove(tempDir)
    
            if safe:
                algor = chibitData["checksum"]["algorithm"]
                hash_ = chibitData["checksum"]["hash"]
                if algor == "crc32":
                    calculatedHash = self._calculate_crc32_file(outputFile)
                    if calculatedHash != hash_:
                        print(f"Checksum mismatch for {fileid}/{chibitData['filename']}")
                        return None
                    else:
                        return outputFile
            else:
                return outputFile
    
        def is_chibitPrefixedUrl(self, prefixedUrl) -> bool:
            """
            Function to check if a given url is a chibit-prefixed url.
    
            Format: chibit:<fileid>@<hostUrl>
            or:     chibit:<fileid>@<hostUrl>;<backupUrl>
            """
            if prefixedUrl.strip().startswith("chibit:"):
                return True
            else:
                return False
    
        def getComponents_FromPrefixedUrl(self, prefixedUrl) -> tuple:
            """
            Function to get the components of a chibit-prefixed url.
    
            Format: chibit:<fileid>@<hostUrl>
            or:     chibit:<fileid>@<hostUrl>;<backupUrl>
    
            Returns:
            {
                "original": <prefixedUrl>,
                "valid": <bool>,
                "fileid": <str>,
                "hostUrl": <str>,
                "backupUrl": <str>,
                "noBackupUrl": <str>
            }
            """
            data = {
                "original": prefixedUrl,
                "valid": False,
                "fileid": None,
                "hostUrl": None,
                "backupUrl": None,
                "noBackupUrl": None
            }
            if self.is_chibitPrefixedUrl(prefixedUrl):
                data["valid"] = True
                prefixedUrl = prefixedUrl.strip().replace("chibit:","")
                if ";" in prefixedUrl:
                    parts = prefixedUrl.split(";")
                    data["backupUrl"] = parts[-1]
                    parts.pop(-1)
                    prefixedUrl = ';'.join(parts)
                    prefixedUrl = prefixedUrl.strip(";")
                    data["noBackupUrl"] = "chibit:"+prefixedUrl
                
                if "@" in prefixedUrl:
                    fileid, hostUrl = prefixedUrl.split("@")
                    if hostUrl == "": hostUrl = None
                    data["fileid"] = fileid
                    data["hostUrl"] = hostUrl
                
                return data
            else:
                return data
    
        def getRaw_FromPrefixedUrl(self, prefixedUrl, safe=True, verbose=False) -> bytes:
            """
            Function to get the raw content of a chibit-stored file, from a prefixed url.
    
            Format: chibit:<fileid>@<hostUrl>
            or:     chibit:<fileid>@<hostUrl>;<backupUrl>
            """
            
            components = self.getComponents_FromPrefixedUrl(prefixedUrl)
            if components["valid"] == True:
                return self.getRaw(components["fileid"], safe, verbose, hostOvv=components["hostUrl"])
            else:
                raise ValueError("Inputed url did not contain the 'chibit:' prefix! (Format: chibit:<fileid>@<hostUrl> or chibit:<fileid>@<hostUrl>;<backupUrl>)")
    
        def getRawFile_FromPrefixedUrl(self, prefixedUrl, outputFile=None, safe=True, verbose=False, check_encoding="utf-8", useTemp=False, tempDir=None) -> str:
            """
            Function to get the raw content of a chibit-stored file, from a prefixed url.
    
            Format: chibit:<fileid>@<hostUrl>
            or:     chibit:<fileid>@<hostUrl>;<backupUrl>
            """
            
            components = self.getComponents_FromPrefixedUrl(prefixedUrl)
            if components["valid"] == True:
                if useTemp == True:
                    if useTemp == True and (tempDir == None or not os.path.exists(tempDir)):
                        raise ValueError("When using temp, a tempDir must be given and exist!")
                    return self.getRawFileWtemp(components["fileid"], outputFile, safe, verbose, tempDir, check_encoding, hostOvv=components["hostUrl"])
                else:
                    return self.getRawFile(components["fileid"], outputFile, safe, verbose, check_encoding, hostOvv=components["hostUrl"])
            else:
                raise ValueError("Inputed url did not contain the 'chibit:' prefix! (Format: chibit:<fileid>@<hostUrl> or chibit:<fileid>@<hostUrl>;<backupUrl>)")
    
    
    
    class Networking():
    
        class ChibitConn(ChibitConnector):
            def __init__(self,chibitHostUrl:str):
                typeval(chibitHostUrl,str,"chibitHostUrl")
                super().__init__(
                    hostUrl = chibitHostUrl,
                    reqType = "fancyPants",
                    fancyPantsFuncs = [
                        getUrlContent_HandleGdriveVirWarn,
                        downloadFile_HandleGdriveVirWarn
                    ]
                )
    
        @staticmethod
        def testConnection(override_url:str=None):
            typeval(override_url,str,"override_url",True)
            # If no url is given, default to google.
            if override_url == None or override_url == "":
                override_url = "https://google.com"
            # Check/Validate the connection, catch exeptions and return boolean
            try:
                req = requests.get(override_url)
                req.raise_for_status()
            except:
                return False
            return True
    
        @staticmethod
        def fetchContent(url:str, title:str="Downloading...", postText:str="", handleGdriveVirWarnText:str="Found gdrive scan warning, attempting to extract link and download from there..."):
            typeval(url,str,"url"); typeval(title,str,"title"); typeval(postText,str,"postText"); typeval(handleGdriveVirWarnText,str,"handleGdriveVirWarnText")
            return getUrlContent_HandleGdriveVirWarn(
                url = url,
                handleGdriveVirWarn = True,
                loadingBar = False,
                title = title,
                postDownText = postText,
                handleGdriveVirWarnText = handleGdriveVirWarnText,
                raise_for_status = True,
                yieldResp = False
            )
        @staticmethod
        def fetchContent_progress(url:str, title:str="Downloading...", postText:str="", handleGdriveVirWarnText:str="Found gdrive scan warning, attempting to extract link and download from there..."):
            typeval(url,str,"url"); typeval(title,str,"title"); typeval(postText,str,"postText"); typeval(handleGdriveVirWarnText,str,"handleGdriveVirWarnText")
            return getUrlContent_HandleGdriveVirWarn(
                url = url,
                handleGdriveVirWarn = True,
                loadingBar = True,
                title = title,
                postDownText = postText,
                handleGdriveVirWarnText = handleGdriveVirWarnText,
                raise_for_status = True,
                yieldResp = False
            )
        @staticmethod
        def fetchContent_silent(url:str):
            typeval(url,str,"url")
            return getUrlContent_HandleGdriveVirWarn(
                url = url,
                handleGdriveVirWarn = True,
                loadingBar = False,
                title = "",
                postDownText = "",
                handleGdriveVirWarnText = "",
                raise_for_status = True,
                yieldResp = False
            )
    
        @staticmethod
        def fetchFile(url:str,filepath:str, title:str="Downloading...", postText:str="", handleGdriveVirWarnText:str="Found gdrive scan warning, attempting to extract link and download from there...", encoding:str="utf-8", stream=None):
            typeval(url,str,"url"); typeval(filepath,str,"filepath"); typeval(title,str,"title"); typeval(postText,str,"postText"); typeval(handleGdriveVirWarnText,str,"handleGdriveVirWarnText"); typeval(encoding,str,"encoding")
            return downloadFile_HandleGdriveVirWarn(
                url = url,
                filepath = filepath,
                handleGdriveVirWarn = True,
                loadingBar = False,
                title = title,
                postDownText = postText,
                handleGdriveVirWarnText = handleGdriveVirWarnText,
                raise_for_status = True,
                encoding = encoding,
                onFileExiError = "raise",
                yieldResp = False,
                stream = stream
            )
        @staticmethod
        def fetchFile_progress(url:str,filepath:str, title:str="Downloading...", postText:str="", handleGdriveVirWarnText:str="Found gdrive scan warning, attempting to extract link and download from there...", encoding:str="utf-8", stream=None):
            typeval(url,str,"url"); typeval(filepath,str,"filepath"); typeval(title,str,"title"); typeval(postText,str,"postText"); typeval(handleGdriveVirWarnText,str,"handleGdriveVirWarnText"); typeval(encoding,str,"encoding")
            return downloadFile_HandleGdriveVirWarn(
                url = url,
                filepath = filepath,
                handleGdriveVirWarn = True,
                loadingBar = True,
                title = title,
                postDownText = postText,
                handleGdriveVirWarnText = handleGdriveVirWarnText,
                raise_for_status = True,
                encoding = encoding,
                onFileExiError = "raise",
                yieldResp = False,
                stream = stream
            )
        @staticmethod
        def fetchFile_silent(url:str,filepath:str, encoding:str="utf-8", stream=None):
            typeval(url,str,"url"); typeval(filepath,str,"filepath"); typeval(encoding,str,"encoding")
            return downloadFile_HandleGdriveVirWarn(
                url = url,
                filepath = filepath,
                handleGdriveVirWarn = True,
                loadingBar = False,
                title = "",
                postDownText = "",
                handleGdriveVirWarnText = "",
                raise_for_status = True,
                encoding = encoding,
                onFileExiError = "raise",
                yieldResp = False,
                stream = stream
            )
    
    
    class Services():
    
        class local_JVM_Manager():
            def __init__(self,parentPath=str):
                self.platform = platform.system().lower()
                self.parentPath = parentPath
    
        class JVM_Manager():
            def __init__(self):
                self.platform = platform.system().lower()
            
            def checkJavaExistence(self):
                pass
    
            def getJavaPath(self):
                pass
    
            def ensureJavaExistance(self,local_JVM_Manager):
                pass
    
    class RepositoryConnector():
        def __init__(self,repofileUrl:str=str,NetworkingClass=None):
            typeval(repofileUrl,str,"repofileUrl")
            Networking_checker = mcclib.Networking
            instval(NetworkingClass,Networking_checker,"NetworkingClass",False,"mcclib.Networking",True)
            self.url = repofileUrl
            self.net = NetworkingClass
            self.rawContent = None
            self.parsedContent = None
    
        def fetch(self, title="Downloading repo...", postText="", handleGdriveVirWarnText="Found gdrive scan warning, attempting to extract link and download from there..."):
            typeval(title,str,"title"); typeval(title,str,"postText"); typeval(handleGdriveVirWarnText,str,"handleGdriveVirWarnText")
            self.rawContent = self.net.fetchContent(self.url,title,postText,handleGdriveVirWarnText)
            self.parsedContent = json.loads(self.rawContent)
        def fetch_progress(self, title="Downloading repo...", postText="", handleGdriveVirWarnText="Found gdrive scan warning, attempting to extract link and download from there..."):
            typeval(title,str,"title"); typeval(title,str,"postText"); typeval(handleGdriveVirWarnText,str,"handleGdriveVirWarnText")
            self.rawContent = self.net.fetchContent_progress(self.url,title,postText,handleGdriveVirWarnText)
            self.parsedContent = json.loads(self.rawContent)
        def fetch_silent(self, *ignored,**kignored):
            self.rawContent = strip_json_comments(
                self.net.fetchContent_silent(self.url)
            )
            self.parsedContent = json.loads(self.rawContent)
    
        def get(self) -> dict:
            if self.rawContent == None or self.parsedContent == None:
                raise ValueError("Attempted operation on RepositorConnector without having it fetched!")
            else:
                return self.parsedContent
    
        def validateToFormat(self,formatVer=int) -> bool:
            typeval(formatVer,int,"formatVer")
            if self.get().get("format") != formatVer:
                return False
            else:
                return True
        
        def getRepoMeta(self) -> dict:
            _p = self.get()
            return {
                "format": _p.get("format"),
                "author": _p.get("author"),
                "version": _p.get("version"),
                "created": _p.get("created"),
                "lastUpdated": _p.get("lastUpdated")
            }
        
        def getAmntFlavors(self) -> int|None:
            _p = self.get().get("flavors")
            if _p == None:
                del _p
                return None
            else:
                return len(_p)
    
    class Repository():
        pass