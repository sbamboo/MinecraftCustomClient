# New MinecraftCustomClient System
## Listings:
A listing is a file containing pack-information and sourceURLs to the mods or similar sources.

*Example*:

```
{
    "format":  "1",               //The format version for future proofing
    "name":    "My Example ModPack",
    "desc":    "Just a modpack",
    "version": "1.0",
    "modLoader": "Fabric",        //The modloader to use, alternatives: "Fabric"
    "modLoaderVer": "0.14.21",    
    "minecraftVer": "1.20.1",
    "created: "yyyy-mm-dd",
    "launcherIcon": "<base64_or_url>",
    "sources": [
        {
            "type": "custom",
            "url":  "https://www.example.com/mod.jar",
            "filename": "mod.jar"
        },
        {
            "type": "customArchive",
            "url":  "https://www.example.com/legacyPackage.zip",
            "filename": "legacyPackage.zip"
        },
        {
            "type": "customArchive",
            "url":  "https://www.example.com/legacyPackage.package", //Same as above but in .package
            "filename": "legacyPackage.package"                      //Same as above but in .package
        },
        {
            "type": "customB64",
            "url": None,
            "base64":  "<base64>",          //A custom field is included
            "filename": "mod.jar"
        },
        {
            "type": "customArchiveB64",
            "url": None,
            "base64":  "<base64>",          //A custom field is included
            "filename": "legacyPackage.zip" //Also works with .package
        },
        {
            "type": "curseforgeManifest",
            "url":  "https://www.curseforge.com/.../mod.jar",
            "filename": "mod.jar"
        },
        {
            "type": "modrith",
            "url":  "https://www.modrith.com/.../mod.jar",
            "filename": "mod.jar"
        },
        {
            "type": "filenameOnly", // This exist to allow for listing just filenames, these won't be installed.
            "url": null,
            "filename": "mod.jar"
        }
    ],
    "sourceLength": 6
}
```
<br>
<br>

## PackageFormats:

### .Package (Legacy)
The new system will support the legacy packageformat being ZIP archive of finalSource.

### .listing
This format uses only a listing file (JSON). *A listing file may include external resources via base64 or url*

### .modListing / .mlisting
This is an archive of source/resources just like *legacyPackages* aswell as a listing file in **modpack.json**

<br>
<br>

## Repositories:
A repository can contain either listings in full or a link to a listing.

*The legacy sourceType allowes for inclusion of data that would normally be in the listing file being included here*

Modpacks are since old called *Flavors*

*Example*:
```
{
    "format": 1,
    "author": "Simon Kalmi Claesson",
    "version": "1.0",
    "created":     "yyyy-mm-dd",
    "lastUpdated": "yyyy-mm-dd",
    "flavors": [
        {
            "name": "My Example ModPack",
            "desc": "My Amazing modpack!",
            "id":   "<uuid>",
            "hidden": false,
            "supported": true,
            "sourceType": "urlListing",
            "source": "https://example.com/modpack.listing"
        },
        {
            "name": "My Example ModPack",
            "desc": "My Amazing modpack!",
            "id":   "<uuid>",
            "hidden": false,
            "supported": true,
            "sourceType": "included",
            "source": { // This includes a full listing file
                ...
            }
        },
        {
            "name": "My Example ModPack",
            "desc": "My Amazing modpack!",
            "id":   "<uuid>",
            "hidden": false,
            "supported": true,
            "sourceType": "legacy",
            "source": {
                "url": "https://example.com/modpack.package",
                "archiveType": "package-zip",
                "flavorDataFile": "flavor.mta",
                "launcherIcon": "<base64_or_url>",
                "modLoader": "Fabric",
                "modLoaderVer": "0.14.21",
                "minecraftVer": "1.20.1"
            }
        },
        {
            "name": "My Example ModPack",
            "desc": "My Amazing modpack!",
            "id":   "<uuid>",
            "hidden": false,
            "supported": true,
            "sourceType": "legacyB64",
            "source": {
                "base64": "<base64>",
                "archiveType": "package-zip",
                "flavorDataFile": "flavor.mta",
                "launcherIcon": "<base64_or_url>",
                "modLoader": "Fabric",
                "modLoaderVer": "0.14.21",
                "minecraftVer": "1.20.1"
            }
        }
    ]
}
```
<br>
<br>

## ArchiveTypes
### ArchiveTypes are supported with the *legacy* sourceType and can be in theese formats:
> **zip**: Just a standard zip file

> **package-zip**: A .package file with the zip format

<br>
<br>

## InstalledPacks
### MinecraftCustomClient creates a file with installed modpacks
Theese files use this format:
```
{
    "DefaultInstallDirectory": "<path>",
    "Installs":[
        {
            "id": "<uuid>",
            "name": "My Example Modpack",
            "location": "<path>"
        }
    ]
}
```