#MinecraftCustomClient installer
#Author: Simon Kalmi Claesson

#Version:
$app_version = "1.0"
$app_vID = "A0122-ae3dc603-abc4-44f5-9f98-43d129e779f9"
$app_mtd = "8537@ecb93f88d52e"

#Param
param(
  #Update
  [switch]$HasUpdated
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