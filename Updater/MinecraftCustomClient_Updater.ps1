#vars
$adress = ""
$name = $adress | split-path -leaf

#Check for same dir
if (test-path "$name") {} else {
  write-host "Updater could not find a installer in the same directory, please check this." -f red
  pause
  exit
}

#fix
del "$name"
curl -s "$adress"
start pwsh -file $name