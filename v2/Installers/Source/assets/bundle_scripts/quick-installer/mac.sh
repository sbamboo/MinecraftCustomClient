#!/bin/bash

# Define variables
installerPyScript="./source.QuickInstaller.py"
tempFolder="./mac_runtime_temp"
prefix="Runtime_mac_V1.0:"

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

    # Download and run the prebuilt Python installer for macOS
    curl -L https://www.python.org/ftp/python/latest/python3.x.x-macosx10.x.pkg -o "$tempFolder/python_installer.pkg"
    sudo installer -pkg "$tempFolder/python_installer.pkg" -target /

    # Set the python variable to the installed binary
    python="/usr/local/bin/python3"
fi

# Run the installerPyScript using the python command
"$python" "$installerPyScript" "$@"

# Remove the temp folder
rm -rf "$tempFolder"

echo "$prefix Script completed."
