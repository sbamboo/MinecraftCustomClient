<# : Bat/powershell polygot block

@echo off
REM set env: variable
setlocal
set "POWERSHELL_BAT_ARGS=%*"
REM Launch file in powershell
powershell -noprofile -command "[System.IO.File]::ReadAllText('%~f0') | Out-string | Invoke-Expression"
exit /b %errorlevel%

: End of runtime block #>

# Check if either "python" or "python3" is available in the PATH

$prefix = "Runtime_windows_V1.0:"
$pythonWingetId = "Python.Python.3.12"
$pythonInstallerUrl = "https://www.python.org/ftp/python/3.12.2/python-3.12.2-amd64.exe"
$pythonScript = "source.MinecraftCustomClient.py"

# Make it reload path so it won't fallback to failed manual-install even after successfull install.

function getPython() {
    $pythonExecutable = $null
    if (Test-Path "$((Get-Command py.exe -ErrorAction SilentlyContinue).Path)") {
        $pythonExecutable = "py.exe"
    } elseif (Test-Path "$((Get-Command python -ErrorAction SilentlyContinue).Path)") {
        $pythonExecutable = "python"
    } elseif (Test-Path "$((Get-Command python3 -ErrorAction SilentlyContinue).Path)") {
        $pythonExecutable = "python3"
    }
    return $pythonExecutable
}

# If python executable is still $null, check if winget exists and use it to install python
$pythonExecutable = getPython
$wingetValid = $False
if ($pythonExecutable -eq $null) {
    # Check if winget exists
    if (Test-Path "$((Get-Command winget.exe -ErrorAction SilentlyContinue).Path)") {
        Write-Host "$prefix Installing Python via winget..."
        # Install Python using winget
        winget install $pythonWingetId -e
        # Check if installation was successful
        if (getPython -eq $null) {} else {
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
        $pythonInstallerPath = "$env:TEMP\python-installer.exe"
        Invoke-WebRequest -Uri $pythonInstallerUrl -OutFile $pythonInstallerPath -UseBasicParsing

        # Run Python installer silently
        Start-Process -FilePath $pythonInstallerPath -ArgumentList "/quiet", "/passive", "/norestart" -Wait

        # Update $pythonExecutable after installation
        $pythonExecutable = getPython # make this work even after successful install
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
#$pythonScript = $MyInvocation.MyCommand -replace "\[System\.IO\.File\]::ReadAllText\(\'", "" -replace "\'\) \| Out-string \| Invoke-Expression",""
$command = "$pythonExecutable $pythonScript $env:POWERSHELL_BAT_ARGS"
Invoke-Expression $command