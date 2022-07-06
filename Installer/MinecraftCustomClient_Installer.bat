@:: Powershell Installer / Runtime, Runns a script and installs powershell if needed. Created by Simon Kalmi Claesson. License/Info: https://sites.google.com/view/scofficial/projects/powershell-installerruntime    Version: 2.2
@::
@powershell "$host.ui.rawui.windowtitle = 'Pwsh Runtime v.2.2 (TOGO_SLC)'; if((Get-Command -Name Pwsh -ErrorAction Ignore)) {}else{write-host "Installing powershell..."; $script = invoke-restmethod https://raw.githubusercontent.com/PowerShell/PowerShell/master/tools/install-powershell.ps1; $script > tmp.ps1; powershell -ep bypass .\tmp.ps1 "-addtopath"; del tmp.ps1}" && start pwsh -c "Get-Content %0 | Select -Skip 12 | Invoke-Expression"
@goto :eof
#!/bin/sh
clear
echo "Pwsh Runtime v.2.2 (TOGO_SLC)"
echo "--------------------------------------------------------"
echo ""
hash pwsh 2>/dev/null || { echo >&2 ""; bash <(curl -s https://raw.githubusercontent.com/PowerShell/PowerShell/master/tools/install-powershell.sh); }; clear; pwsh -c "Get-Content $0 | Select -Skip 12 | Invoke-Expression"
exit

#===================================[Code]===================================

#MinecraftCustomClient installer
#Author: Simon Kalmi Claesson

#Version:
$app_version = "1.0"
$app_vID = "A0122-ae3dc603-abc4-44f5-9f98-43d129e779f9"
$app_mtd = "8537@ecb93f88d52e"

#variables
$lastver_url = "https://raw.githubusercontent.com/simonkalmiclaesson/MinecraftCustomClient/main/Installer/lastVer.mt"
$lastver_name = $lastver_url | split-path -leaf
$updater_url = "https://github.com/simonkalmiclaesson/MinecraftCustomClient/blob/main/Updater/MinecraftCustomClient_Updater.ps1"
$updater_name = $updater_url | split-path -leaf
$tempfolder_path = "$psscriptroot\MinecraftCustomClient_Installer_Temp"

#clear
cls

#Functions
function download($adress,$path) {
  $url = $adress
  $name = $adress | split-path -leaf
  curl -s "$adress" | Out-File "$path\$name"
}

#Create temp folder
if (test-path $tempfolder_path) {} else {md $tempfolder_path}

#Update Section
  #Assemble mt tag
  [string]$mttag = $app_vID + ":" + $app_mtd
  #Get repo lastVer.mt
  $lastVer = curl -s "$lastver_url"
  #Check
  if ($mttag -eq $lastVer) {$isLatest = $true} else {$isLatest = $false}
  #Fix
  if ($isLatest = $false) {
    $curdir = get-location
    cd $tempfolder_path
    download $updater_name $pwd
    start pwsh -file $updater_name
    exit
    cd $curdir
  }
