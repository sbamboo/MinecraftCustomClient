#!/bin/bash

# Define variables
installerPyScript="./source.MinecraftCustomClient.py"
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
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y python3
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
