@ECHO OFF

if exist .\launcher.bat (
    del .\launcher.bat
)
copy .\parts\_multi.main.bat .\launcher.bat
python3 ..\..\Installers\Source\assets\tool_includeInline.py -path .\launcher.bat -enc utf-8