#exclude ST
Networking:object
RepositoryConnector:object
Repository:object
#exclude END

#include ./»deps-setup.py

#include ./libs/importa.py

#include ./»generalfuncs.py
#include MX@./»networking.py
#include MX@./»services.py
#include MX@./»repo.py

class mcclib():
    pass #excludeThis
    #include MX@./»networking.py
    #include MX@./»services.py
    #include MX@./»repo.py