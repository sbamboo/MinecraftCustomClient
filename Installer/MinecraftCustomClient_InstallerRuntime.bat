@:: Powershell Installer / Runtime, Runns a script and installs powershell if needed. Created by Simon Kalmi Claesson. License/Info: https://sites.google.com/view/scofficial/projects/powershell-installerruntime    Version: 2.3
@::
@powershell "$host.ui.rawui.windowtitle = 'Pwsh Runtime v.2.3'; if((Get-Command -Name Pwsh -ErrorAction Ignore)) {}else{write-host "Installing powershell..."; $script = invoke-restmethod https://raw.githubusercontent.com/PowerShell/PowerShell/master/tools/install-powershell.ps1; $script > tmp.ps1; powershell -ep bypass .\tmp.ps1 "-addtopath"; del tmp.ps1}" && start pwsh -c "Get-Content %0 | Select -Skip 12 | Out-File pwshRuntime_Tempscript.ps1; .\pwshRuntime_Tempscript.ps1; del pwshRuntime_Tempscript.ps1"
@goto :eof
#!/bin/sh
clear
echo "Pwsh Runtime v.2.3"
echo "--------------------------------------------------------"
echo ""
hash pwsh 2>/dev/null || { echo >&2 ""; bash <(curl -s https://raw.githubusercontent.com/PowerShell/PowerShell/master/tools/install-powershell.sh); }; clear; pwsh -c "Get-Content $0 | Select -Skip 12 | Out-File pwshRuntime_Tempscript.ps1; .\pwshRuntime_Tempscript.ps1; del pwshRuntime_Tempscript.ps1"
exit

#Bundled Powershell script

#Varibles
$app_adress = "https://github.com/simonkalmiclaesson/MinecraftCustomClient/releases/download/test/MinecraftCustomClient_Installer.bat"
$app_name = $app_adress | split-path -leaf

#Check for vdat file
if (Test-path $app_name) {
    start pwsh "-file $app_name"
    exit
} else {
    curl -s "$app_adress" | Out-File -file "$app_name"
    start pwsh "-file $app_name"
    exit
}