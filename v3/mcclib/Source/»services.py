#exclude ST
import platform, shutil
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

class Services():

    class local_JDK_Manager():
        def __init__(self,parentPath:str,winUrl:str,lnxUrl:str,macUrl:str,NetworkingClass=None):
            Networking_checker = mcclib.Networking
            Networking_checker = Networking #excludeThis
            instval(NetworkingClass,Networking_checker,"NetworkingClass",False,"mcclib.Networking",True)
            self.NetworkingClass = NetworkingClass
            typeval(parentPath,str,"parentPath")
            self.platform = platform.system().lower()
            self.parentPath = parentPath
            if self.platform == "windows":
                typeval(winUrl,str,"winUrl")
                self.platformUrl = winUrl
            elif self.platform == "linux":
                typeval(lnxUrl,str,"lnxUrl")
                self.platformUrl = lnxUrl
            elif self.platform == "darwin":
                typeval(macUrl,str,"macUrl")
                self.platformUrl = macUrl
        def ensureDir(self):
            os.makedirs(self.parentPath)
        @staticmethod
        def getPossibleJDKBinInFolder(folderPath:str) -> str|None:
            typeval(folderPath,str,"folderPath")
            java_binary = os.path.join(folderPath, "java")
            if platform.system().lower() == "windows":
                java_binary += ".exe"
            if os.path.exists(java_binary):
                return java_binary
            else:
                return None
        @staticmethod
        def findJavaInFolder(folderPath:str) -> str:
            typeval(folderPath,str,"folderPath")
            # Check in root folder
            jvb = getPossibleJDKBinInFolder(folderPath)
            if jvb != None: return jvb
            # Else check other folders in the root folder
            for elem in os.listdir(folderPath):
                elem = os.path.join(folderPath,elem)
                if os.path.isdir(elem):
                    jvb = getPossibleJDKBinInFolder(elem)
                    if jvb != None: return jvb

        def downloadJava(self,silent=False,textEncoding="utf-8") -> str:
            typeval(silent,bool,"silent")
            typeval(textEncoding,str,"textEncoding")
            if os.path.exists(self.parentPath):
                raise FileNotFoundError("Error on Java-JDK download, destination dosen't exist, run ensureDir() first!")
            filename = get_filename_from_url(self.platformUrl)
            filepath = os.path.join(self.parentPath,filename)
            # Download
            if not os.path.exists(filepath):
                # Silent
                if silent == True:
                    self.NetworkingClass.fetchFile_silent(
                        url = self.platformUrl,
                        filepath = filepath,
                        encoding = textEncoding,
                        stream = None
                    )
                # Progressbar
                else:
                    self.NetworkingClass.fetchFile_progress(
                        url = self.platformUrl,
                        filepath = filepath,
                        title = f"Downloading {filename}...",
                        postText = "",
                        handleGdriveVirWarnText="Found gdrive scan warning, attempting to extract link and download from there...",
                        encoding = textEncoding,
                        stream = None
                    )
            # Already-existing archive
            else:
                if silent != True:
                    print("Warn! Local JDK-archive already exists, skipping download.")
            # Extract
            if filename.endswith(".zip"):
                with zipfile.ZipFile(filepath, 'r') as zip_ref:
                    zip_ref.extractall(self.parentPath)
            elif filename.endswith(".tar.gz"):
                with tarfile.open(filepath, 'r:gz') as tar_ref:
                    tar_ref.extractall(self.parentPath)
            else:
                raise NotImplementedError("Unsupported archive format!")
            # Find the binary from the extracted archive
            java_binary = findJavaInFolder(self.parentPath)
            if not java_binary:
                raise RuntimeError("Java binary not found in the extracted folder")
            # Mark the binary as executable on macOS and Linux
            if self.platform in ["linux","darwin"]:
                os.chmod(java_binary, 0o755)
            # Return the path
            return java_binary

    class JDK_Manager():
        def __init__(self,customJdkBin:str=None):
            typeval(customJdkBin,str,"customJdkBin",True)
            self.platform = platform.system().lower()
            self.localJdkCliCmd = "java"
            self.customJdkBin = customJdkBin
        
        def checkJavaExistence(self) -> bool:
            if self.customJdkBin != None:
                return os.path.exists(self.customJdkBin)
            else:
                # Check if avaliable in cli
                if shutil.which(self.localJdkCliCmd):
                    return True
                else:
                    return False

        def getJavaPath(self) -> str|None:
            if self.customJdkBin != None:
                if os.path.exists(self.customJdkBin) == True:
                    return self.customJdkBin
                else:
                    return None
            else:
                toret = shutil.which(self.localJdkCliCmd)
                if toret:
                    return toret
                else:
                    return None

        def ensureJavaExistance(self,local_JDK_Manager,silentEnsure=False,encoding="utf-8") -> str:
            Networking_checker = mcclib.Services.local_JDK_Manager
            Networking_checker = Services.local_JDK_Manager #excludeThis
            instval(local_JDK_Manager,Networking_checker,"local_JDK_Manager",False,"mcclib.Services.local_JDK_Manager",False)
            currentJava = self.getJavaPath()
            if currentJava != None:
                return currentJava
            else:
                # Ensure java
                return local_JDK_Manager.downloadJava(silentEnsure,encoding)