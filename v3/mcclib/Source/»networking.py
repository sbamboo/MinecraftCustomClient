#include ./libs/fancyPants.py
#include ./libs/chibit.py

#exclude ST
from typing import Callable
from libs.fancyPants import *
from libs.chibit import ChibitConnector
from typing import Optional,Union
def typeval(val,typeV,nm:Optional[str]=None,allowNone=False) -> None:
    """Raises if type of 'val' does not match 'typeV'!"""
    if type(val) != typeV and (val is not None or not allowNone):
        try: typeN = typeV.__name__
        except: typeN = str(typeV)
        if nm == None: raise Exception(f"Invalid type for parameter, must be '{typeN}'!")
        else: raise Exception(f"Invalid type for parameter '{nm}', must be '{typeN}'!")
def instval(val,instV,nm:Optional[str]=None,allowNone=False,instN:Optional[str]=None,checkEq=False) -> None:
    """Raises if type of 'val' is not instance of 'instV'!"""
    if not isinstance(val, instV) and (val is not None and (checkEq and val != instV) or (not checkEq) or (val is None and not allowNone)) and (val is not None or not allowNone):
        try: typeN = instN if instN != None else instV.__name__
        except: typeN = str(instV)
        if nm == None: raise Exception(f"Invalid type for parameter, must be '{typeN}'!")
        else: raise Exception(f"Invalid type for parameter '{nm}', must be '{typeN}'!")
#exclude END

class Networking():

    class ChibitConn(ChibitConnector):
        def __init__(self,chibitHostUrl:str) -> None:
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
    def testConnection(override_url:Optional[str]=None) -> bool:
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
