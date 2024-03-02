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
