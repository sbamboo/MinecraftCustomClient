#::   PythonRuntimeBootstrapper 1.0 by SimonKalmiClaesson  > nul


echo \" <<'BATCH_SCRIPT' >/dev/null ">NUL "\" \`" <#"
@ECHO OFF
cls
REM =====[WinBatch RuntimeWrapper Start]=====
REM set env: variable
setlocal
set "POWERSHELL_BAT_ARGS=%*"
REM Launch file in powershell
powershell -noprofile -command "[System.IO.File]::ReadAllText('%~f0') | Out-string | Invoke-Expression"
exit /b %errorlevel%
REM ======[WinBatch RuntimeWrapper End]======
GOTO :eof
TYPE CON >NUL
BATCH_SCRIPT
#> | Out-Null



#::   [WINDOWS CODE BELLOW]  > nul

echo \" <<'POWERSHELL_SCRIPT' >/dev/null # " | Out-Null
# ===== PowerShell Script Begin =====
#region [IncludeInline: ./parts/_multi.ps1]
$prefix = "Runtime_windows_V1.1:"
$pythonWingetId = "Python.Python.3.12"
$pythonInstallerUrl = "https://www.python.org/ftp/python/3.12.2/python-3.12.2-amd64.exe"
$pythonScript = "source.QuickInstaller.py"

$arguments = $env:POWERSHELL_BAT_ARGS
$flag_quietManualInstall = $false
if ($arguments -match "--qmaninst") {
    $arguments = $arguments -replace "--qmaninst",""
    $flag_quietManualInstall = $true
}
$param_customManualExe = $false
$parts = $arguments -split '\s+(?=(?:[^"]*"[^"]*")*[^"]*$)'
# Iterate over the array
for ($i = 0; $i -lt $parts.Length; $i++) {
    if ($parts[$i] -eq "-cusmanexe") {
        # Set $param_customManualExe to the next element
        $param_customManualExe = $parts[$i + 1]
        
        # Remove both elements
        $parts = $parts | Where-Object { $_ -ne "-cusmanexe" -and $_ -ne $param_customManualExe }
    }
}
$arguments = $parts -join " "

if ($flag_quietManualInstall -eq $true) {
    Write-Host "$prefix Manual python installation set to quiet."
}
if ($param_customManualExe -eq $false) {} else {
    Write-Host "$prefix Using custom manual python exe: $param_customManualExe"
}

# Make it reload path so it won't fallback to failed manual-install even after successfull install.
function testPythonForMsStoreOrBroken() {
    param( [string]$pythonPath )
    $output = Invoke-Expression -Command "$pythonPath -c 'print(5)'"
    if (-not $output -or $output -eq "") {
        return $False
    } else {
        if ($output -eq "5") {
            return $True
        } else {
            return $False
        }
    }
}

function getPython() {
    Write-Host "$prefix Attempting to get python..."
    $pythonExecutable = $null
    $pyc = Get-Command py.exe -ErrorAction SilentlyContinue
    $python3c = Get-Command python3 -ErrorAction SilentlyContinue
    $pythonc = Get-Command python -ErrorAction SilentlyContinue
    if ($pyc -and (Test-Path $pyc.Path)) {
        $pythonExecutable = "py.exe"
	Write-Host "$prefix Found py.exe..."
    } elseif ($python3c -and (Test-Path $python3c.Path)) {
        $pythonExecutable = "python3"
	Write-Host "$prefix Found python3..."
    } elseif ($pythonc -and (Test-Path $pythonc.Path)) {
        $pythonExecutable = "python"
	Write-Host "$prefix Found python..."
    }
    Write-Host "$prefix Checking python validity..."
    if ((testPythonForMsStoreOrBroken -pythonPath $pythonExecutable) -eq $False) {
        $pythonExecutable = $null
        Write-Host "$prefix Python was invalid..."
    } else {
        Write-Host "$prefix Python was valid..."
    }
    if ($pythonExecutable -eq $null) {
        Write-Host "$prefix No python found..."
    }
    return $pythonExecutable
}

# Reload the environment to reflect changes in the PATH variable
$machinePath = [System.Environment]::GetEnvironmentVariable("PATH", "Machine")
$userPath = [System.Environment]::GetEnvironmentVariable("PATH", "User")
$combinedPath = $machinePath + ";" + $userPath
$env:PATH = $combinedPath

# If python executable is still $null, check if winget exists and use it to install python
$pythonExecutable = getPython
$wingetValid = $False
if ($pythonExecutable -eq $null) {
    # Check if winget exists
    Write-Host "$prefix Checking if winget is avaliable..."
    $wingetc = Get-Command winget.exe -ErrorAction SilentlyContinue
    if ($wingetc -and (Test-Path $wingetc.Path)) {
        Write-Host "$prefix Installing Python via winget..."
        # Install Python using winget
        winget install $pythonWingetId -e --accept-package-agreements --accept-source-agreements
        # Reload the environment to reflect changes in the PATH variable
        $machinePath = [System.Environment]::GetEnvironmentVariable("PATH", "Machine")
        $userPath = [System.Environment]::GetEnvironmentVariable("PATH", "User")
        $combinedPath = $machinePath + ";" + $userPath
        $env:PATH = $combinedPath
        # Check if installation was successful
        $pythonExecutable = getPython
        if ($pythonExecutable -eq $null) {} else {
            $wingetValid = $True
        }
    }
} else {
    $wingetValid = $True
}

if ($wingetValid -eq $True) {} else {
    Write-Host "$prefix Winget install failed attempting manual install..."
    
    # URL to download Python installer (adjust as needed)

    try {
        # Download Python installer
        if ($param_customManualExe -eq $false) {
            $pythonInstallerPath = "$env:TEMP\python-installer.exe"
            Invoke-WebRequest -Uri $pythonInstallerUrl -OutFile $pythonInstallerPath -UseBasicParsing
        } else {
            $pythonInstallerPath = $param_customManualExe
            $pythonInstallerPath = $pythonInstallerPath -replace '"',""
        }

        # Run Python installer silently
        if ($flag_quietManualInstall -eq $true) {
            # ,"Include_doc=0","Include_debug=0","Include_dev=1","Include_exe=1","Include_launcher=0","Include_lib=1","Include_pip=1","Include_symbols=0","Include_tctk=0","Include_test=0","Include_tools=1"
            Start-Process -FilePath $pythonInstallerPath -ArgumentList "/norestart", "/passive", "/quiet" -Wait
        } else {
            Start-Process -FilePath $pythonInstallerPath -ArgumentList "/norestart", "/passive" -Wait
        }

        # Reload the environment to reflect changes in the PATH variable
        $machinePath = [System.Environment]::GetEnvironmentVariable("PATH", "Machine")
        $userPath = [System.Environment]::GetEnvironmentVariable("PATH", "User")
        $combinedPath = $machinePath + ";" + $userPath
        $env:PATH = $combinedPath

        # Update $pythonExecutable after installation
        $pythonExecutable = getPython
        if ($pythonExecutable -eq $null) {
            throw "Failed"
        }

        Write-Host "$prefix Python installed successfully."

        # Clean up the temporary Python installer file
        Remove-Item -Path $pythonInstallerPath -Force
    } catch {
        Write-Host "$prefix Error occurred while installing Python. Please install Python manually."
        Write-Host "$prefix You can download Python from https://www.python.org/downloads/ or from Microsoft Store.`n`n Install python and then restart the app..."
        Pause
        exit
    }
}

# Execute the command
$parent = Split-Path -Path ($MyInvocation.MyCommand -replace "\[System\.IO\.File\]::ReadAllText\(\'", "" -replace "\'\) \| Out-string \| Invoke-Expression","") -Parent
$pythonScript = Join-Path -Path $parent -ChildPath $pythonScript
$command = "$pythonExecutable $pythonScript $arguments"
Write-Host "$prefix Starting application...`n  Python: $pythonExecutable`n  Script: $pythonScript`n  Args: $arguments`n  Command: $command"
Invoke-Expression $command
#endregion [IncludeInline: ./parts/_multi.ps1]
# ====== PowerShell Script End ======
exit
<#
POWERSHELL_SCRIPT



#::   [UNIX CODE BELLOW]  > nul

set +o histexpand 2>/dev/null
# ===== Bash Script Begin =====
#region [IncludeInline: ./parts/_multi.sh]
#!/bin/bash

# Define variables
installerPyScript="./source.QuickInstaller.py"
tempFolder="./linux_runtime_temp"
prefix="Runtime_linux_V1.0:"

# Remove the temp folder if it already exists
if [ -d "$tempFolder" ]; then
    rm -rf "$tempFolder"
fi

# Create the temp folder
mkdir -p "$tempFolder"

# Check if Python is installed and available in PATH
if command -v python3 &> /dev/null; then
    python="python3"
else
    echo "$prefix Python not found. Installing Python..."

    # Check the distribution package manager (apt, yum, etc.) and install Python
    if command -v apt &> /dev/null; then
        sudo apt update
        sudo apt install -y python3
    elif command -v yum &> /dev/null; then
        sudo yum install -y python3
    else
        echo "$prefix Unsupported distribution. Please install Python manually."
        exit 1
    fi

    # Set the python variable to the installed binary
    python="python3"
fi

# Run the installerPyScript using the python command
"$python" "$installerPyScript" "$@"

# Remove the temp folder
rm -rf "$tempFolder"

echo "$prefix Script completed."
#endregion [IncludeInline: ./parts/_multi.sh]
# ====== Bash Script End ======
case $- in *"i"*) cat /dev/stdin >/dev/null ;; esac
exit
#>
