# Jar Retrival Library
import requests
import json

# Modrith Jar Retrival Library
class MJRL():
    def __init__(self,UserAgent,BaseApiUrl="https://api.modrinth.com/v2/"):
        self.Headers = {
            "User-Agent": UserAgent
        }
        self.BaseApiUrl = BaseApiUrl
        self.req = requests
    def GetProjectRaw(self,Name):
        '''Name: id or slug'''
        Url = self.BaseApiUrl + f"project/{Name}"
        return self.req.get(Url, headers=self.Headers)
    def GetProjectVersionsRaw(self,Name):
        '''Name: id or slug'''
        Url = self.BaseApiUrl + f"project/{Name}/version"
        return self.req.get(Url, headers=self.Headers)
    def GetProjectVersions(self,Name):
        '''Name: id or slug'''
        Response = self.GetProjectVersionsRaw(Name)
        Content  = Response.content.decode()
        Data     = json.loads(Content)
        return Data
    def GetLinksPerMcVersion(self,Name,McVersion,McModLoader=None):
        '''Name: id or slug'''
        Content = self.GetProjectVersions(Name)
        Matches = []
        for _id in Content:
            if McVersion in _id["game_versions"]:
                valid = True
                if McModLoader != None:
                    if McModLoader in _id["loaders"]:
                        pass
                    else:
                        valid = False
                if valid == True:
                    for File in _id["files"]:
                        if File["primary"] == True:
                            Matches.append(File["url"])
        return Matches
    def GetLinksPerFilename(self,Name,Filename):
        '''Name: id or slug'''
        Content = self.GetProjectVersions(Name)
        Matches = []
        for _id in Content:
            for File in _id["files"]:
                if File["filename"] == Filename:
                    Matches.append(File["url"])
        return Matches
    def SearchForQuery(self,Query,Name=None):
        '''Name: id or slug'''
        Url = self.BaseApiUrl + f"search?query={Query}"
        Response = self.req.get(Url, headers=self.Headers)
        Content  = Response.content.decode()
        Data     = json.loads(Content)
        Hits = Data["hits"]
        if Name == None:
            return Hits
        else:
            NameHits = []
            for Hit in Hits:
                if Hit["slug"].lower() == Name.lower():
                    NameHits.append(Name)
            return NameHits



# Curseforge Jar Retrival Library
class CJRL():
    def __init__(self,manifestFilePath):
        self.manifestData = json.loads(open(manifestFilePath,'r').read())
    def GetUrlPerFilename(self,Filename):
        Addons = self.manifestData["installedAddons"] # Points to locally installed files
        Matches = []
        for Addon in Addons:
            if Addon["fileNameOnDisk"] == Filename:
                Matches.append(Addon["installedFile"]["downloadUrl"])
        return Matches

# Main class
def getJarByFilename(source="modrith",Filename=str,curseforgeManifest=None, modrithUserAgent=None,modrithProject=None) -> list:
    # Curseforge
    if source.lower() == "curseforge" and Filename != None and curseforgeManifest != None:
        RetrivalClassInstance = CJRL(curseforgeManifest)
        return RetrivalClassInstance.GetUrlPerFilename(Filename)
    # Modrith
    elif source.lower() == "modrith" and Filename != None and modrithUserAgent != None and modrithProject != None:
        RetrivalClassInstance = MJRL(modrithUserAgent)
        return RetrivalClassInstance.GetLinksPerFilename(modrithProject, Filename)