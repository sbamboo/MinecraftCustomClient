#vars
$adress = "https://raw.githubusercontent.com/simonkalmiclaesson/MinecraftCustomClient/main/Installer/MinecraftCustomClient_Installer.ps1"
$name = $adress | split-path -leaf

#Check in parent dir
cd ..
if (test-path "$name") {} else {
  write-host "Updater could not find a installer in the same directory, please check this." -f red
  pause
  exit
}

#fix
del "$name"
curl -s "$adress"
start pwsh "-file $name"