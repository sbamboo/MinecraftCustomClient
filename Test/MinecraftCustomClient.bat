<# : Start of runtime block

REM Shell things
@echo off & setlocal
set "POWERSHELL_BAT_ARGS=%*"
REM Install Pwsh and start it
powershell $old_ErrorActionPreference = $ErrorActionPreference; $ErrorActionPreference = 'SilentlyContinue'; $title = $host.ui.rawui.windowtitle; $host.ui.rawui.windowtitle = 'Pwsh runtime V.3.1 [win_batch]'; $env:path = [System.Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [System.Environment]::GetEnvironmentVariable('Path','User'); if(Get-Command 'pwsh') {} else { $curdir = $pwd; cd $env:temp; if (test-path 'pwsh_runtime_install') {} else {mkdir 'pwsh_runtime_install'}; cd 'pwsh_runtime_install'; $tempLoc = $pwd; cd $curdir; Invoke-RestMethod 'https://aka.ms/install-powershell.ps1' -outfile $tempLoc/inst.ps1; . $tempLoc/inst.ps1 -AddToPath; rmdir $tempLoc -recurse -force }; $ErrorActionPreference = $old_ErrorActionPreference; $env:path = [System.Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [System.Environment]::GetEnvironmentVariable('Path','User'); $host.ui.rawui.windowtitle = $title; cls; write-host '[Runtime]: Installed!' -f green; pwsh -noprofile -NoLogo -Command 'iex (${%~f0} ^| out-string)'
REM Exit prompt
exit /b %errorlevel%

: End of runtime block #>


#MinecraftCustomClient installer
#Author see $app_author bellow:

#Version:
$app_author = "Simon Kalmi Claesson"
$app_version = "1.0"
$app_vID = "A0222-3cfbb7a8-4594-4141-9f49-38e44a2a6a20"
$app_mtd = "9f49@38e44a2a6a20"

#Param
function ParamHandle {
  param(
    [switch]$help,
    
    #Update
    [switch]$HasUpdated,

    #Java
    [switch]$customJava,
    [string]$javaPath,

    #Other
    [switch]$startLauncher,
    [string]$customDrive,
    [string]$customInstallLoc,

    #Support
    [switch]$dontcheckdownloads,
    [switch]$forceLegacyDownload
  )
  #Redir
  $script:help = $help
  $script:HasUpdated = $HasUpdated
  $script:customJava = $customJava
  $script:javaPath = $javaPath
  $script:startLauncher = $startLauncher
  $script:customDrive = $customDrive
  $script:customInstallLoc = $customInstallLoc
  $script:dontcheckdownloads = $dontcheckdownloads
  $script:forceLegacyDownload = $forceLegacyDownload
}
$pc = "ParamHandle " + "$env:POWERSHELL_BAT_ARGS"
iex("$pc")


#variables
$old_ProgressPreference = $ProgressPreference
$ProgressPreference = "SilentlyContinue"
$new_ProgressPreference = $ProgressPreference

$lastver_url = "https://raw.githubusercontent.com/simonkalmiclaesson/MinecraftCustomClient/main/Installer/lastVer.mt"
$lastver_name = $lastver_url | split-path -leaf
$updater_url = "https://raw.githubusercontent.com/simonkalmiclaesson/MinecraftCustomClient/main/Updater/MinecraftCustomClient_Updater.ps1"
$updater_name = $updater_url | split-path -leaf
$flavorlist_url = "https://raw.githubusercontent.com/simonkalmiclaesson/MinecraftCustomClient/main/Repo/MinecraftCustomClient_flavors.json"
$flavorlist_name = $flavorlist_url | split-path -leaf
$tempfolder_path = "MinecraftCustomClient_Installer_Temp"
$javaURI = "https://aka.ms/download-jdk/microsoft-jdk-17.0.3-windows-x64.zip"
$fabricURI = "https://maven.fabricmc.net/net/fabricmc/fabric-installer/0.11.0/fabric-installer-0.11.0.jar"

$helpfile_url = "https://raw.githubusercontent.com/simonkalmiclaesson/MinecraftCustomClient/main/Assets/_HelpAndInfo.bip"
$helpfile_name = $helpfile_url | split-path -leaf

#Create temp folder
if (test-path $tempfolder_path) {} else {md $tempfolder_path > $null}

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
  $lastVer = (iwr $lastver_url).content
  #no internet fallback
  if ($lastVer -eq "") {
    write-host "Could not check for an update from the repository, please check your internet connection." -f red
    write-host 'Write "Y" to continue without updates, or press any other key to exit.' -f blue
    $no_internet_or_invalid_lastVer_message_input = Read-Host
    if ($no_internet_or_invalid_lastVer_message_input -ne "Y") {exit} else {$lastVer = $mttag}
  }
  #Check
  if ($mttag -eq $lastVer) {$isLatest = $true} else {$isLatest = $false}
  #Fix
  if ($isLatest -eq $false) {
    $curdir = get-location
    cd $tempfolder_path
    iwr $updater_url -outfile "$updater_name"
    start pwsh "-file $updater_name"
    exit
  }

#Functions
#ShowInfo
Function ShowInfo {
  $VerificationHeader = "# Verification Header --918a-- #"
  $WebHelp = (iwr $helpfile_url).content
    cls
    write-host "  Minecraft Custom Client Installer help and info:"
    write-host "--------------------------------------------------------------"
    Write-host "  Version: $app_version  ($app_vid)"
    write-host "  Author: $app_author"
    write-host "--------------------------------------------------------------"
    write-host ""
  if ($WebHelp -like "*$verificationHeader*") {
    iex($WebHelp)
  } else {
    write-host "WebHelp couldn't be downloaded please check it for more information." -f red
    write-host ""
    write-host "MCC installer is an app to install my minecraft clients with more simplicity then zipping files here and there"
    write-host "It needs java but if not found it will download a binary"
    write-host "MCC installer also installs fabric and other client dependencies."
    write-host ""
    write-host "The app can be used from the command line so here is some cli help:"
    write-host ""
    write-host "  help: Shows this help menu."
    write-host ""
    write-host "  customJava: Flag to allow the use of custom Java paths other then the pathed 'java' command."
    write-host ""
    write-host "  javaPath: Path to custom java binary, used with the -customJava flag."
    write-host ""
    write-host "  startLauncher: Flag to autostart the minecraft launcher after installation."
    write-host ""
    write-host "  customDrive: Overwrite install drive for clients (default: C:\) specify in path format."
    write-host ""
    write-host "  customInstallLoc: Overwrite the installlocation for clients."
    write-host ""
    write-host "  dontcheckdownloads: Using this flag will diable the download package-id check."
    write-host ""
    write-host "  forceLegacyDownload: Forces the app to use InvokeWebRequest istead of Start-BitsTransfer"
    write-host ""
    write-host ""
    write-host "SYNTAX"
    write-host "MinecraftCustomClient.bat [params/flags]"
    write-host ""
    pause
    #Refix Progress Pref
    $ProgressPreference = $old_ProgressPreference
    #Remove temp files
    cd $temp_path
    cd ..
    if (test-path $tempfolder_path) {del $tempfolder_path -recurse -force}
    exit
  }
}
#GetJava
Function GetJava {
  param(
    #os
    [switch]$win,
    [switch]$unx,
    
    #other
    [string]$workdir,
    [string]$javaURI
  )

  if ($workdir) {$wdir = $workdir} else {$wdir = $pwd}
  cd $wdir  

  if ($javaURI) {} else {$javaURI = "https://aka.ms/download-jdk/microsoft-jdk-17.0.3-windows-x64.zip"}
  $javaName = $javaURI | split-path -leaf

  if($win) {
    #Check Java
    if(Get-Command 'Java') {} else {
      #No Java
      if (test-path $javaName) {} else {
        iwr $javaURI -OutFile $javaName
      }
      #Extract Java
      if ($javaName -like "*.zip*") {
        #Archive Java
        $ProgressPreference = $old_ProgressPreference
        Expand-Archive $javaName
        cd $javaName.TrimEnd(".zip")
        $script:customJava = $True
        $script:javaPath = Get-Location
        $ProgressPreference = $new_ProgressPreference
      } else {
        $script:customJava = $True
        $script:javaPath = $pwd + "\java.exe"
      }
    }
  }
}

#GetJava
Function GetFabric {
  param(
    #os
    [switch]$win,
    [switch]$unx,
    
    #other
    [string]$workdir,
    [string]$fabricURI
  )

  if ($workdir) {$wdir = $workdir} else {$wdir = $pwd}
  cd $wdir 

  if ($fabricURI) {} else {$fabricURI = "https://maven.fabricmc.net/net/fabricmc/fabric-installer/0.11.0/fabric-installer-0.11.0.jar"}
  $fabricName = $fabricURI | split-path -leaf

  if($win) {
    #Get fabricInstaller file if needed
    if (test-path $fabricName) {} else {
      iwr $fabricURI -OutFile $fabricName
      [string]$script:fabricInstallerPath = "$pwd" + '\' + "$fabricName"
    }
  }
}

#MinecraftLauncherAgent
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
        [string]$overWriteFile,

        #extraAdditions
        [switch]$dontbreak
    )


    #Variables
    #Settings
    $doExitOnMsg = $false
    $doPause = $false

    #DontBreak
    if ($dontbreak) {$doExitOnMsg = $false}

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
            if ($dontbreak) {} else {if ($doExitOnMsg) {exit} else {break}}
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
        if ($dontbreak) {} else {if ($doExitOnMsg) {exit} else {break}}
        $opHasRun = $true
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
            if ($dontbreak) {} else {if ($doExitOnMsg) {exit} else {break}}
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
        if ($dontbreak) {} else {if ($doExitOnMsg) {exit} else {break}}
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
        if ($dontbreak) {} else {if ($doExitOnMsg) {exit} else {break}}
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
        if ($dontbreak) {} else {if ($doExitOnMsg) {exit} else {break}}
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
            if ($dontbreak) {} else {if ($doExitOnMsg) {exit} else {break}}
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
        if ($dontbreak) {} else {if ($doExitOnMsg) {exit} else {break}}
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
        if ($dontbreak) {} else {if ($doExitOnMsg) {exit} else {break}}
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
        [switch]$noprofile
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
#FlavorObjectFix
Function FlavorObjectFix {
  param($in)
  $in = $in.TrimEnd(" ")
  $in = $in.TrimStart(" ")
  return $in
}

#UI
#Built-in UI System
  #settings
  $cursorColor = "Magenta"
  $selectColor = "Green"
  $commntColor = "Green"
  $objectColor = "White"

  #Import Menu Functions
  #DrawMenu
  function DrawMenu {
    param ($menuItems, $menuPosition, $Multiselect, $selection)
    $l = $menuItems.length
    for ($i = 0; $i -le $l;$i++) {
      if ($menuItems[$i] -ne $null) {
        $item = $menuItems[$i]
        if ($Multiselect) {
          if ($selection -contains $i) {
            $item = '[x] ' + $item
          } else {
            $item = '[ ] ' + $item
          }
        }
        if ($i -eq $menuPosition) {
          Write-Host -nonewline ">" -f $cursorColor
          Write-Host " $($item)" -f $selectColor
        } else {
          Write-Host "  $($item)" -f $objectColor
        }
      }
    }
  }
  #ToggleSelection
  function Toggle-Selection {
    param ($pos, [array]$selection)
    if ($selection -contains $pos) { 
      $result = $selection | where {$_ -ne $pos}
    } else {
      $selection += $pos
      $result = $selection
    }
    $result
  }
  #Main
  function def_ui_Menu {
    param ([array]$menuItems, [switch]$ReturnIndex=$false, [switch]$Multiselect)
    $vkeycode = 0
    $pos = 0
    $selection = @()
    if ($menuItems.Length -gt 0) {
      try {
        [console]::CursorVisible=$false #prevents cursor flickering
        DrawMenu $menuItems $pos $Multiselect $selection
        While ($vkeycode -ne 13 -and $vkeycode -ne 27) {
          $press = $host.ui.rawui.readkey("NoEcho,IncludeKeyDown")
          $vkeycode = $press.virtualkeycode
          If ($vkeycode -eq 38 -or $press.Character -eq 'k') {$pos--}
          If ($vkeycode -eq 40 -or $press.Character -eq 'j') {$pos++}
          If ($vkeycode -eq 36) { $pos = 0 }
          If ($vkeycode -eq 35) { $pos = $menuItems.length - 1 }
          If ($press.Character -eq ' ') { $selection = Toggle-Selection $pos $selection }
          if ($pos -lt 0) {$pos = 0}
          If ($vkeycode -eq 27) {$pos = $null }
          if ($pos -ge $menuItems.length) {$pos = $menuItems.length -1}
          if ($vkeycode -ne 27) {
            $startPos = [System.Console]::CursorTop - $menuItems.Length
            [System.Console]::SetCursorPosition(0, $startPos)
            DrawMenu $menuItems $pos $Multiselect $selection
          }
        }
      }
      finally {
        [System.Console]::SetCursorPosition(0, $startPos + $menuItems.Length)
        [console]::CursorVisible = $true
      }
    } else {
      $pos = $null
    }
    if ($ReturnIndex -eq $false -and $pos -ne $null) {
      if ($Multiselect) {
        return $menuItems[$selection]
      } else {
        return $menuItems[$pos]
      }
    } else {
      if ($Multiselect) {
        return $selection
      } else {
        return $pos
      }
    }
  }

#=====================================================================================================================================================================================================

#clear & Title
cls
$host.ui.rawui.windowtitle = "MinecraftCustomClient Installer"

#terminal size
  #sizes
  $toAdd_width = 3
  $toAdd_height = 2
  #Get window
  $pswindow = $host.ui.rawui
  $newbuffer = $pswindow.buffersize
  $newsize = $pswindow.windowsize
  #setnew
  $newbuffer.width = $newbuffer.width + $toAdd_width
  $newbuffer.height = $newbuffer.height + $toAdd_height
  $newsize.width = $newsize.width + $toAdd_width
  $newsize.height = $newsize.height + $toAdd_height
  #apply
  $pswindow.buffersize = $newbuffer
  $pswindow.windowsize = $newsize

#Path setup
$core_path = Get-Location
cd $tempfolder_path
$temp_path = Get-Location
cd $core_path


#Installer code
if ($help) {ShowInfo}

#variables
$splitter = "  {"
[int]$lengthAllow = "73"

#show menu were to choose install or copyData or more
write-host "  Choose an option bellow:"
write-host "----------------------------"
$menuarray = "[Install]","[dataCopy]","[UnInstall]","[Help]","[Exit]"
$menuOption = (def_ui_Menu $menuarray).Trim("[","]")
#if help
if ($menuOption -eq "Help") {
  ShowInfo
}
#if install
if ($menuOption -eq "Install") { 
  #check and get java
  GetJava -win -workdir "$temp_path"
  #get fabric-installer
  GetFabric -win -workdir "$temp_path"
  #get flavorlist
  $Flavors = (iwr $flavorlist_url).content
  $FlavorList = ConvertFrom-Json "$Flavors"
  #display flavorlist
  $menuarray = $null
  foreach ($flavor in $FlavorList.Flavors) {
    [string]$flavorname = (("$($flavor)").trim("@{") -split "=")[0]
    [string]$flavornameO = $flavorname
    [string]$flavordesc = $FlavorList.Flavors."$flavornameO".desc
    [string]$flavordesc = FlavorObjectFix -in $flavordesc
    if ($flavordesc.length -gt $lengthAllow) {
      [array]$flavordescA = $flavordesc[0..$lengthAllow]
      $flavordesc = ""
      foreach ($a in $flavordescA) {
        [string]$flavordesc += $a
      }
      [string]$flavordesc = "$flavordesc" + "..."
    } 
    [string]$flavorname = "[" + $flavorname + "]"
    $hidden = $FlavorList.Flavors.$flavornameO.Hidden
    if ($hidden -like "*false*") {
      [array]$menuarray = $menuarray + "$flavorname  {$flavordesc}"
    }
  }
  #Fix length sync
    #Get longest itemname
    $lastLength = 0
    foreach ($item in $menuarray) {
      [array]$itemA = $item -split "$splitter"
      [string]$item_name = $itemA[0]
      if ("$item_name".length -gt $lastLength) {
        $lastLength = "$item_name".length
      }
    }
    #Fix items
    foreach ($item in $menuarray) {
      [array]$itemA = $item -split "$splitter"
      [string]$item_name = $itemA[0]
      [string]$item_desc = $itemA[1]
      [string]$item_desc = "{" + "$item_desc"
      if ("$item_name".length -ne "$lastLength") {
        [int]$tmp_value = $lastLength - "$item_name".length
        [string]$spaces = " "*$tmp_value
        [string]$rebuild = "$item_name" + "$spaces" + "$item_desc"
        [array]$newmenuarray += "$rebuild"
      }
    }
    #Change array
    $menuarray = $newmenuarray

  [array]$menuarray = $menuarray + "[Cancel&Exit]"
  cls
  write-host "  Choose an option bellow:"
  write-host "----------------------------"
  $flavorOption = (def_ui_Menu $menuarray).Trim("[","]")
  if ($flavorOption -like "*  {*") {
    [array]$flavorOptionA = $flavorOption -split "$splitter"
    $flavorOption = $flavorOptionA[0]
  }
  if ($flavorOption -eq "Cancel&Exit") {exit}
  $choosenFlavor = $FlavorList.Flavors."$flavorOption"
  #Get client location
  if ($IsWindows) {
    $drive = "C:/"
    $InstallLoc = $choosenFlavor.install_location -replace " ",""
    if ($customDrive -ne "") {$drive = $customDrive}
    if ($customInstallLoc -ne "") {$InstallLoc = $customInstallLoc}
    #StringBuild
    [string]$installpath = "$drive" + "$InstallLoc" + "/" + "$flavorOption"
    #FolderCreate
    $folders = $installpath | split-path -NoQualifier
    $folders = $folders.TrimStart("/").TrimEnd("/")
    [array]$folders = $folders -split "/"
    $curpath = Get-Location
    cd $drive
    foreach ($folder in $folders) {
      $folder = $folder.TrimStart(" ")
      $folder = $folder.TrimEnd(" ")
      if (test-path $folder) {} else {mkdir $folder > $null}
      cd $folder
    }
    $clientLocation = Get-Location
    cd $curpath
  }
  #Download and extract client
  $curpath = Get-Location
  cd $clientLocation
  [string]$type = $choosenFlavor.archive_type
  [string]$type = FlavorObjectFix -in $type
  [string]$url = $choosenFlavor.url
  [string]$url = FlavorObjectFix -in $url
  [string]$name = "$url" | split-path -leaf
  #non filename ending link fix
  if ($name -notlike ".zip*") {
    if ($name -notlike ".package*") {
      $name = $flavorOption + ".unknownpackage"
    }
  }
  #Use best method
  if ($forceLegacyDownload) {
    iwr "$url" -outfile $name | Out-Null
  } else {
    if ($IsWindows) {
      $ProgressPreference = $old_ProgressPreference
      Start-BitsTransfer -source "$url" -destination "$name"
    } else {
      iwr "$url" -outfile $name | Out-Null
    }
  }
  if ($type -like "*zip*") {
    $ProgressPreference = $old_ProgressPreference
    Expand-Archive $name . -force
    del $name -force
    if ($dontcheckdownloads) {} else {
      [string]$flavorData_file = $FlavorList.Flavors.$FlavorOption.flavorData_file
      [string]$flavorData_file = FlavorObjectFix -in $flavorData_file
      if (Test-path "$flavorData_file") {
        [string]$flavorData_json = get-content "$flavorData_file"
        $flavorData_data = ConvertFrom-Json "$flavorData_json"
        [string]$flavorid = $Flavorlist.Flavors.$FlavorOption.ID
        [string]$flavorid = FlavorObjectFix -in $flavorid
        [string]$flavordataid = $flavorData_data.data.id
        [string]$flavordataid = FlavorObjectFix -in $flavordataid
        #Verify download
        if ("$flavorid" -ne "$flavordataid") {
          write-host "Id of downloaded package dosen't match id in repository! Removing Package and aborting. (to continue anyway please use the -dontcheckdownloads flag)" -f red
          pause
          cd $temp_path
          cd ..
          if (test-path $tempfolder_path) {del $tempfolder_path -recurse -force}
          exit
        } else {
          write-host "Downloaded package didn't contain flavordata file so download id could not be checked, continuing but errors may happen." -f yellow
        }
      }
    }
    $ProgressPreference = $new_ProgressPreference
  }
  cd $curpath
  #pass to fabric installer
  [string]$mcversion = $choosenFlavor.minecraft_version
  [string]$mcversion = FlavorObjectFix -in $mcversion
  [string]$loader = $choosenFlavor.fabric_loader
  [string]$loader = FlavorObjectFix -in $loader
  FabricInstaller -installerName $fabricInstallerPath -client -snapshot -dir "$env:appdata\.minecraft" -mcversion $mcversion -loader $loader -noprofile
  #pass to launcherProfile creator
  $fabricversionid = "fabric-loader-" + $choosenFlavor.fabric_loader + "-" + $choosenFlavor.minecraft_version
  $fabricversionid = $fabricversionid -replace " ",""
  $icon = $choosenFlavor.launcher_icon -replace " ",""
  #Should you start lancher?
  cls
  write-host "  Start the launcher after adding the profile?"
  write-host "------------------------------------------------"
  $menuarray = $null
  $menuarray = "[Yes]","[No]"
  $startlauncherOption = (def_ui_Menu $menuarray).Trim("[","]")
  if ($startlauncherOption -eq "Yes") {
    MinecraftLauncherAgent -add -gameDir "$clientLocation" -icon $icon -versionID "$fabricversionid" -name "$flavorOption" -startLauncher -dontbreak
  } else {
    MinecraftLauncherAgent -add -gameDir "$clientLocation" -icon $icon -versionID "$fabricversionid" -name "$flavorOption" -dontbreak
  }
}

#if Uninstall
if ($menuOption -eq "UnInstall") {
  cls
  write-host "  Write name of client to remove (use repository names)"
  write-host "---------------------------------------------------------"
  $clientname = Read-Host "client.name"
  #get flavorlist
  $Flavors = (iwr $flavorlist_url).content
  $FlavorList = ConvertFrom-Json "$Flavors"
  #check name
  Foreach ($flavor in $FlavorList.Flavors) {
    if ($flavor -like "*$clientname*") {
      [string]$installpath = $FlavorList.Flavors.$clientname.install_location
      [string]$installpath = FlavorObjectFix -in $installpath
      cd $drive
      cd $installpath
      rmdir "$clientname" -force -recurse
      MinecraftLauncherAgent -remove -name "$clientname"
    }
  }
}

#if copyData
if ($menuOption -eq "dataCopy") { 
  #show menu copyData ui
  cls
  write-host "  Client data copy assistant"
  write-host "------------------------------"
  write-host ""
  write-host "The data copier has not been inplomented yet" -f red
  write-host ""
  write-host "(the data copier will allow you to move resourcepacks and saves between clients)" -f blue
  write-host ""
  pause
  #show choice for copy_from and allow custom path/folder or from standard dir
  #show choice for copy_to and allow custom path/folder or from standard dir
  #show options (checkboxes) for what to copy:  Saves, modConfig, settins, resourcepacks, servers, shaders
  $menuarray = $null
  $menuarray = "saves", "modConfig", "settings", "resourcepacks", "servers", "shaders"
  #  def_ui_Menu $menuarray -Multiselect
  #show choice if user want to keep remove files from copy_from
  #copy data
}

#EOF
  #Refix Progress Pref
  $ProgressPreference = $old_ProgressPreference
  #Remove temp files
  cd $temp_path
  cd ..
  if (test-path $tempfolder_path) {del $tempfolder_path -recurse -force}