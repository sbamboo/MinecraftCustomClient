#Check for same dir
if (test-path "MinecraftCustomClient_Installer.bat") {} else {
  write-host "Updater could not find a installer in the same directory, please check this." -f red
  pause
  exit
}