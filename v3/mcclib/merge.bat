@ECHO OFF
python3 ..\DevTools\PyIIL\\pyiil.py -pyfile .\Source\mcclib.py %*
python3 ..\DevTools\PyIIL\\pyiil.py -pyfile .\Source\mcclib.py -resnameadd _clean --forceNoFileComments %*