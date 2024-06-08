from mcclib_merged import mcclib

repoconn = mcclib.RepositoryConnector("https://raw.githubusercontent.com/sbamboo/MinecraftCustomClient/main/v2/Repo/repo.json",mcclib.Networking)
repoconn.fetch_progress()
print(repoconn.getRepoMeta())