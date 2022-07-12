#MinecraftCustomClient installer
#Author: Simon Kalmi Claesson

#Version:
$app_version = "1.0"
$app_vID = "A0122-ae3dc603-abc4-44f5-9f98-43d129e779f9"
$app_mtd = "8537@ecb93f88d52e"

#Param
param(
  #Update
  [switch]$HasUpdated,

  #Java
  [switch]$script:customJava,
  [string]$script:javaPath
)

#variables
$lastver_url = "https://raw.githubusercontent.com/simonkalmiclaesson/MinecraftCustomClient/main/Installer/lastVer.mt"
$lastver_name = $lastver_url | split-path -leaf
$updater_url = "https://raw.githubusercontent.com/simonkalmiclaesson/MinecraftCustomClient/main/Updater/MinecraftCustomClient_Updater.ps1"
$updater_name = $updater_url | split-path -leaf
$tempfolder_path = "MinecraftCustomClient_Installer_Temp"

#Create temp folder
if (test-path $tempfolder_path) {} else {md $tempfolder_path}

#Has Updated check
if ($HasUpdated) {
  $tp = Get-Location
  cd $tempfolder_path
  if (Test-path $updater_name) {del $updater_name}
  cd $tp
}

#Update Section
  #Assemble mt tag
  [string]$mttag = $app_vID + ":" + $app_mtd
  #Get repo lastVer.mt
  $lastVer = curl -s "$lastver_url"
  #Check
  if ($mttag -eq $lastVer) {$isLatest = $true} else {$isLatest = $false}
  #Fix
  if ($isLatest -eq $false) {
    $curdir = get-location
    cd $tempfolder_path
    curl -s $updater_url | Out-File -file "$updater_name"
    start pwsh "-file $updater_name"
    exit
  }

#Functions
Function MinecraftLauncherAgent {
    #Minecraft Install Agent
    #This script helps to add/remove/list or replace minecraft launcher installs.
    #
    #Made by Simon Kalmi Claesson
    #Version:  2022-07-04(3) 2.0
    #


    #Parameters
    param(
        #Option
        [switch]$startLauncher,
        [switch]$suppressMsgs,
        [switch]$dontkill,

        #Prio inputs
        [switch]$add,
        [switch]$remove,
        [switch]$list,
        [switch]$get,
        [switch]$replace,

        #Later inputs
        [string]$OldInstall,
        [string]$gameDir,
        [string]$icon,
        [string]$versionId,
        [string]$name,
        [string]$overWriteLoc,
        [string]$overWriteFile
    )


    #Variables
    #Settings
    $doExitOnMsg = $false
    $doPause = $false

    #Presets
    $defa_MCFolderLoc = "$env:appdata\.minecraft\"
    $defa_MCProfFileN = "launcher_profiles.json"
    $backupFolderName = ".installAgentBackups"
    $script:familyName = "Microsoft.4297127D64EC6_8wekyb3d8bbwe"
    $script:binlauncdir = "C:\Program Files (x86)\Minecraft Launcher\MinecraftLauncher.exe"

    #Text
    $text_MissingParam = "You have not supplied one or more of the required parameters for this action!"
    $text_NoLauncher = "No launcher found! Wont auto start"
    $text_OPhasRun = "Operation has been run."

    #Defaults
    $opHasRun = $false
    $script:returnPath = Get-Location



    #Kill launcher processes to apply launcher changes
    if ($dontkill) {} else { foreach ($proc in ($processes = Get-Process | where -property processname -like "*Minecraft*")) {Stop-Process $proc -force} }

    #returnPath function
    function returnPath {
        cd $returnPath
        #Auto startLauncher when done
        if ($startLauncher) {
            
            if ((get-appxpackage | ?{$_.PackageFamilyName -like "$familyName"}).installlocation) {
                start "shell:AppsFolder\$familyName!Minecraft"
            } else {
                if (Test-path "$binlauncdir") {
                    start "$binlauncdir"
                } else {
                    write-host "$text_NoLauncher" -f red
                }
            }
        }
    }
        
    #Add Install
    if ($add) {
        #Missing param fix
        $paramMissing = $false
        #GameDir
        if ($gameDir) {} else {$paramMissing = $true}
        #versionId
        if ($versionId) {} else {$paramMissing = $true}
        #name
        if ($name) {} else {$paramMissing = $true}
        if ($paramMissing) {
            if ($suppressMsgs) {} else { write-host $text_MissingParam -f red}
            if ($doPause) {pause}
            if ($doExitOnMsg) {exit} else {break}
        }

        #OverWrite Fix for file location
        if ($overWriteLoc) {
            $loc = $overWriteLoc
        } else {
            $loc = $defa_MCFolderLoc
        }
        #OverWrite Fix for file name
        if ($overWriteFile) {
            $file = $overWriteFile
        } else {
            $file = $defa_MCProfFileN
        }

        #Get file content add change to PSobject
        cd $loc
        $jsonFile = gc $file
        $psobject = ConvertFrom-Json "$jsonFile"
        $profiles = $psobject.profiles

        #Create tempalate profile
        $template = @{
            created = Get-Date
            gameDir = "$gameDir"
            icon = "$icon"
            lastVersionId = "$versionId"
            name = "$name"
            type = "custom"
        }

        #Create temporary variables and fix add profile to data
        $NewProfiles = $profiles
        $NewProfiles | Add-Member -MemberType NoteProperty -Name $template.name -Value $template
        $newPsobject = $psobject
        $newPsobject.profiles = $newProfiles
        #Convert to JSON
        $endJson = ConvertTo-Json $newPsobject

        #Prep Backup
        [string]$newFileName = "(" + $(Get-Date) + ")_" + $file
        $newFileName = $newFileName -replace "/","_"
        $newFileName = $newFileName -replace ':',"-"
        #Backup
        if (Test-Path "$backupFolderName") {} else {md "$backupFolderName"}
        $cl = Get-Location
        copy "$file" ".\$backupFolderName\$newFileName" -force
        cd $cl

        #Set content to file
        Set-Content $file $endJson

        #Done
        if ($suppressMsgs) {} else { write-host "$text_OPhasRun" -f blue}
        returnPath
        if ($doPause) {pause}
        if ($doExitOnMsg) {exit} else {break}
        $opwRun = $true
    }
        
    #Remove Install
    if ($remove) {
        #Missing param fix
        $paramMissing = $false
        #name
        if ($name) {} else {$paramMissing = $true}
        if ($paramMissing) {
            write-host $text_MissingParam -f red
            if ($doPause) {pause}
            if ($doExitOnMsg) {exit} else {break}
        }

        #OverWrite Fix for file location
        if ($overWriteLoc) {
            $loc = $overWriteLoc
        } else {
            $loc = $defa_MCFolderLoc
        }
        #OverWrite Fix for file name
        if ($overWriteFile) {
            $file = $overWriteFile
        } else {
            $file = $defa_MCProfFileN
        }

        #Get file content add change to PSobject
        cd $loc
        $jsonFile = gc $file
        $psobject = ConvertFrom-Json "$jsonFile"
        $profiles = $psobject.profiles

        #Create temporary variables and fix add profile to data
        $newProfiles = $profiles | Select-Object -Property * -ExcludeProperty "$name"
        $newPsobject = $psobject
        $newPsobject.profiles = $newProfiles
        $endJson = ConvertTo-Json $newPsobject

        #Prep Backup
        [string]$newFileName = "(" + $(Get-Date) + ")_" + $file
        $newFileName = $newFileName -replace '/',"-"
        $newFileName = $newFileName -replace ':',"-"
        #Backup
        if (Test-Path "$backupFolderName") {} else {md "$backupFolderName"}
        $cl = Get-Location
        copy "$file" ".\$backupFolderName\$newFileName" -force
        cd $cl

        #Set content to file
        Set-Content $file $endJson

        #Done
        if ($suppressMsgs) {} else { write-host "$text_OPhasRun" -f blue}
        returnPath
        if ($doPause) {pause}
        if ($doExitOnMsg) {exit} else {break}
        $opHasRun = $true
    }

    #List Profiles
    if ($list) {
        #OverWrite Fix for file location
        if ($overWriteLoc) {
            $loc = $overWriteLoc
        } else {
            $loc = $defa_MCFolderLoc
        }
        #OverWrite Fix for file name
        if ($overWriteFile) {
            $file = $overWriteFile
        } else {
            $file = $defa_MCProfFileN
        }

        #Get file content add change to PSobject
        cd $loc
        $jsonFile = gc $file
        $psobject = ConvertFrom-Json "$jsonFile"
        $profiles = $psobject.profiles

        #Print profiles to console
        $profiles

        #Done
        if ($suppressMsgs) {} else { write-host "$text_OPhasRun" -f blue}
        returnPath
        if ($doPause) {pause}
        if ($doExitOnMsg) {exit} else {break}
        $opHasRun = $true
    }

    #Get Profiles
    if ($get) {
        #OverWrite Fix for file location
        if ($overWriteLoc) {
            $loc = $overWriteLoc
        } else {
            $loc = $defa_MCFolderLoc
        }
        #OverWrite Fix for file name
        if ($overWriteFile) {
            $file = $overWriteFile
        } else {
            $file = $defa_MCProfFileN
        }

        #Get file content add change to PSobject
        cd $loc
        $jsonFile = gc $file
        $psobject = ConvertFrom-Json "$jsonFile"
        $profiles = $psobject.profiles

        #Send profiles to variable
        $script:MinecraftLauncherLatestProfiles = $profiles

        #Done
        if ($suppressMsgs) {} else { write-host "$text_OPhasRun" -f blue}
        returnPath
        if ($doPause) {pause}
        if ($doExitOnMsg) {exit} else {break}
        $opHasRun = $true
    }

    #Replace Profiles
    if ($replace) {
        #Missing param fix
        $paramMissing = $false
        #OldInstall
        if ($OldInstall) {} else {$paramMissing = $true}
        #GameDir
        if ($gameDir) {} else {$paramMissing = $true}
        #versionId
        if ($versionId) {} else {$paramMissing = $true}
        #name
        if ($name) {} else {$paramMissing = $true}
        if ($paramMissing) {
            write-host $text_MissingParam -f red
            if ($doPause) {pause}
            if ($doExitOnMsg) {exit} else {break}
        }

        #OverWrite Fix for file location
        if ($overWriteLoc) {
            $loc = $overWriteLoc
        } else {
            $loc = $defa_MCFolderLoc
        }
        #OverWrite Fix for file name
        if ($overWriteFile) {
            $file = $overWriteFile
        } else {
            $file = $defa_MCProfFileN
        }

        #Get file content add change to PSobject
        cd $loc
        $jsonFile = gc $file
        $psobject = ConvertFrom-Json "$jsonFile"
        $profiles = $psobject.profiles

        #Create tempalate profile
        $template = @{
            created = Get-Date
            gameDir = "$gameDir"
            icon = "$icon"
            lastVersionId = "$versionId"
            name = "$name"
            type = "custom"
        }

        #Create temporary variables and fix add profile to data
        $NewProfiles = $profiles
        if ($NewProfiles."$OldInstall") {$NewProfiles."$OldInstall" = $template}
        $newPsobject = $psobject
        $newPsobject.profiles = $newProfiles
        #Convert to JSON
        $endJson = ConvertTo-Json $newPsobject

        #Prep Backup
        [string]$newFileName = "(" + $(Get-Date) + ")_" + $file
        $newFileName = $newFileName -replace '/',"-"
        $newFileName = $newFileName -replace ':',"-"
        #Backup
        if (Test-Path "$backupFolderName") {} else {md "$backupFolderName"}
        $cl = Get-Location
        copy "$file" ".\$backupFolderName\$newFileName" -force
        cd $cl

        #Set content to file
        Set-Content $file $endJson

        #Done
        if ($suppressMsgs) {} else { write-host "$text_OPhasRun" -f blue}
        returnPath
        if ($doPause) {pause}
        if ($doExitOnMsg) {exit} else {break}
        $opHasRun = $true
    }

    #If no param is given show help
    if ($opHasRun) {} else {
        write-host "  MinecraftLauncher InstallAgent (GameInstalls)"
        write-host "-------------------------------------------------"
        write-host "This script helps to add/remove/list or replace minecraft launcher installs."
        write-host "This script is written by Simon Kalmi Claesson"
        write-host ""
        write-host "Operation parameters"
        write-host "  Add:"
        write-host "    Adds a install to the launcher (Specify params: gameDir, versionID, name. Or optionaly icon)"
        write-host "  Remove:"
        write-host "    Removes a install from the launcher (Specify params: name)"
        write-host "  List:"
        write-host "    Lists installs in the launcher"
        write-host "  Get:"
        write-host "    Sends the installs to the MinecraftLauncherLatestProfiles variable in the script scope"
        write-host "  Replace:"
        write-host "    Replaces a install with a new one (Specify params: oldInstall, gameDir, versionID, name. Or optionaly icon)"
        write-host ""
        write-host "Install data"
        write-host "  GameDir:"
        write-host "    The directory of a new install"
        write-host "  Icon:"
        write-host "    The filepath/data of the icon to the new install"
        write-host "  VersionID:"
        write-host "    The versionID for the jar/version to be used by the new install"
        write-host "  Name:"
        write-host "    The name of the new install or the name of an install to remove"
        write-host "  OldInstall:"
        write-host "    The name of the install to replace with the replace operation"
        write-host ""
        write-host "Flags"
        write-host "  StartLauncher:"
        write-host "    Automaticly starts the minecraft launcher after the action has completed."
        write-host "  SuppressMsgs:"
        write-host "    Suppreses messages from the script to the console (Warns/Error will still get sent)"
        write-host "  DontKill:"
        write-host "    Stops the script from killing the launcher before an action/operation (May break things)"
        write-host ""
        write-host "Overwrite Flags"
        write-host "  OverwriteLoc:"
        write-host "    Overwrite the location of the minecraft folder (the folder were the launcher_profiles.json is stored)"
        write-host "  OverwriteFile:"
        write-host "    Overwrite the filename of the launcher_profiles json file." 
        write-host ""
        if ($doPause) {pause}
        if ($doExitOnMsg) {exit} else {break}
    }

    #Go return path
    returnPath

}
#Fabric Installer
Function FabricInstaller {

    #SYNTAX:
    #FabricInstaller (-forceBaseJava) -installerName "fabric-installer.jar" -client/-server (-snapshot) -dir <mc_dir> -mcversion <mcver> -loader <fabric_loader_version> (-noprofile)

    param(
        #Java
        [switch]$forceBaseJava,

        #Installer
        [string]$installerName,

        #Modes
        [switch]$client,
        [switch]$server,

        #Params
        [switch]$snapshot,
        [string]$dir,
        [string]$mcversion,
        [string]$loader,
        [string]$noprofile
    )

    #Java
    if ($forceBaseJava) {$java = "java"} else {
        if ($script:customJava) {
            if ($script:javapath) {
                $java = $script:javapath
            } else {
                write-host "No custom java path given! When using the -customJava flag a -javaPath parameter must be given and used, will try to continue with default java." -f red
                $java = "java"
            }
        } else {
            $java = "java"
        }
    }

    #Client
    if ($client) {
        #Begin StringBuild
        $command = $java + " -jar "
        #InstallerName
        if ($InstallerName) {$command = $command + "$InstallerName "} else {write-host "The script needs a fabric installer to be presented, please provide a filename/path to the -installerName flag, the script will instead try and use 'fabric-installer.jar' as a name." -f red; $command = $command + "fabric-installer.jar "}
        #Client tag
        $command = $command + "client "
        #snapshot
        if ($snapshot) {$command = $command + "-snapshot "}
        #dir
        if ($dir) {
            $command = $command + "-dir " + "'" + $dir + "'" + " "
        } else {
            write-host "A install directory must be provided! (flag -dir is required)" -f red
            break
        }
        #mcversion
        if ($mcversion) {
            $command = $command + "-mcversion " + "'" + $mcversion + "'" + " "
        } else {
            write-host "A minecraft version must be provided! (flag -mcversion is required)" -f red
            break
        }
        #loader
        if ($loader) {
            $command = $command + "-loader " + "'" + $loader + "'" + " "
        } else {
            write-host "A fabric-loader version must be provided! (flag -loader is required)" -f red
            break
        }
        #noprofile
        if ($noprofile) {$command = $command + "-noprofile"}

        iex($command)
    }
}

#clear & Title
cls
$host.ui.rawui.windowtitle = "MinecraftCustomClient Installer"

#Path setup
$core_path = Get-Location
cd $tempfolder_path
$temp_path = Get-Location
cd $core_path


#Installer code
$core_path
$temp_path
pause

#show menu were to choose install or copyData or more
#if install
  #check and get java
  #get fabric-installer
  #get flavorlist
  #display flavorlist
  #get chosen flavors data
  #pass to fabric installer
  #pass to launcherProfile creator
  #^^^ launch mc-launcher (if wanted)

#if copyData
  #show menu copyData ui
  #show choice for copy_from and allow custom path/folder or from standard dir
  #show choice for copy_to and allow custom path/folder or from standard dir
  #show options (checkboxes) for what to copy:  Saves, modConfig, settins, resourcepacks, servers, shaders
  #show choice if user want to keep remove files from copy_from
  #copy data