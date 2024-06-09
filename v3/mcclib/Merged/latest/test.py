import os
from mcclib_merged import mcclib

#repoconn = mcclib.RepositoryConnector("https://raw.githubusercontent.com/sbamboo/MinecraftCustomClient/main/v2/Repo/repo.json",mcclib.Networking)
#repoconn.fetch_progress()
#print(repoconn.getRepoMeta())

#print(mcclib.Services.JVM_Manager().ensureJavaExistance(mcclib.Services.local_JVM_Manager()))

localJDKMan = mcclib.Services.local_JDK_Manager(
    parentPath = os.path.join(os.path.dirname(os.path.abspath(__file__)),"java"),
    winUrl = "https://aka.ms/download-jdk/microsoft-jdk-17.0.8.1-windows-x64.zip",
    lnxUrl = "https://aka.ms/download-jdk/microsoft-jdk-17.0.8.1-linux-x64.tar.gz",
    macUrl = "https://aka.ms/download-jdk/microsoft-jdk-17.0.8.1-macOS-x64.tar.gz",
    NetworkingClass=mcclib.Networking
)
javaBin = mcclib.Services.JDK_Manager( localJDKMan ).ensureJavaExistance(
    silentEnsure = False,
    encoding = "utf-8"
)
print(javaBin)