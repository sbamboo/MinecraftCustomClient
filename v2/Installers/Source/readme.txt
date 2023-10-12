The installer build-script inline-includes content into the file to avoid mutli-coding.

Since the code is split up in multiple partials, the installer-code can be used in both installers, 
so the bulk of the installer-code is in partial@installermain.py

Note! Multiple partials exists since the big installer has some other tools and utils in it.

The MinecraftCustomClient.py file is the big-installer.
The QuickInstaller.py file is the to-be-bundled installer.