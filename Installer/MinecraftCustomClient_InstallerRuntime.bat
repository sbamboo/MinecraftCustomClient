@:: Powershell Installer / Runtime, Runns a script and installs powershell if needed. Created by Simon Kalmi Claesson. License/Info: https://sites.google.com/view/scofficial/projects/powershell-installerruntime    Version: 2.3
@::
@powershell "$host.ui.rawui.windowtitle = 'Pwsh Runtime v.2.3'; if((Get-Command -Name Pwsh -ErrorAction Ignore)) {}else{write-host "Installing powershell..."; $script = invoke-restmethod https://raw.githubusercontent.com/PowerShell/PowerShell/master/tools/install-powershell.ps1; $script > tmp.ps1; powershell -ep bypass .\tmp.ps1 "-addtopath"; del tmp.ps1}" && start pwsh -c "set-variable -name adress -value 'https://raw.githubusercontent.com/simonkalmiclaesson/MinecraftCustomClient/main/Installer/MinecraftCustomClient_Installer.ps1'; $name = $adress | Split-Path -leaf; if (test-path $name) {. .\$name} else {curl -s $adress | Out-File -file $name; . .\$name}"
@goto :eof
#!/bin/sh
clear
echo "Pwsh Runtime v.2.3"
echo "--------------------------------------------------------"
echo ""
hash pwsh 2>/dev/null || { echo >&2 ""; bash <(curl -s https://raw.githubusercontent.com/PowerShell/PowerShell/master/tools/install-powershell.sh); }; clear; pwsh -c "set-variable -name adress -value 'https://raw.githubusercontent.com/simonkalmiclaesson/MinecraftCustomClient/main/Installer/MinecraftCustomClient_Installer.ps1'; $name = $adress | Split-Path -leaf; if (test-path $name) {. .\$name} else {curl -s $adress | Out-File -file $name; . .\$name}"