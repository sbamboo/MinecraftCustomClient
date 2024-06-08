import json
import platform
import shutil
import base64, re
import urllib.parse
import zipfile
import tarfile

_ = autopipImport("requests")
_ = autopipImport("bs4")
_ = autopipImport("rich")