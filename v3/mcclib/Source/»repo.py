#exclude ST
import json
from typing import Callable
Networking:object
mcclib = object
strip_json_comments:Callable[[str],str]
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
#exclude END

class RepositoryConnector():
    def __init__(self,repofileUrl:str=str,NetworkingClass=None):
        typeval(repofileUrl,str,"repofileUrl")
        Networking_checker = mcclib.Networking
        Networking_checker = Networking #excludeThis
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