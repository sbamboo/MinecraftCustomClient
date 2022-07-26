#vars
$host.ui.rawui.windowtitle = "Updating..."
$adress = "https://raw.githubusercontent.com/simonkalmiclaesson/MinecraftCustomClient/main/Installer/MinecraftCustomClient.bat"
$name = $adress | split-path -leaf

#Check in parent dir
cd ..
if (test-path "$name") {} else {
  write-host "Updater could not find a installer in the same directory, please check." -f red
  pause
  exit
}

#fix
del "$name"
curl -s "$adress" | Out-File -file $name
start pwsh "-file $name -HasUpdated"