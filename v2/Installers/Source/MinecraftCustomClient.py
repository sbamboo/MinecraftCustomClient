# This is the big installer who shows and installes from repositories

# [Settings]
installer_version = "1.3.6"
installer_release = "2025-07-23(0)"
prefix    = "\033[90m[\033[35mInstaller\033[90m]\033[0m "
prefix_dl = "\033[90m[\033[34mDown-List\033[90m]\033[0m "
prefix_jv = "\033[90m[\033[33mJava-Inst\033[90m]\033[0m "
prefix_la = "\033[90m[\033[94mLnch-Agnt\033[90m]\033[0m "
title = f"MinecraftCustomClient - Installer {installer_version}: <modpack>"
temp_foldername = "MCC_Installer_Temp"

win_java_url = "https://aka.ms/download-jdk/microsoft-jdk-17.0.8.1-windows-x64.zip"
lnx_java_url = "https://aka.ms/download-jdk/microsoft-jdk-17.0.8.1-linux-x64.tar.gz"
mac_java_url = "https://aka.ms/download-jdk/microsoft-jdk-17.0.8.1-macOS-x64.tar.gz"

fabric_url = "https://maven.fabricmc.net/net/fabricmc/fabric-installer/0.11.2/fabric-installer-0.11.2.jar"
forge_url  = "https://files.minecraftforge.net/net/minecraftforge/forge"
forForgeList = "https://raw.githubusercontent.com/sbamboo/MinecraftCustomClient/main/v2/Installers/Assets/forge-links.json"

legacy_repo_url = "https://raw.githubusercontent.com/sbamboo/MinecraftCustomClient/main/v1_legacy/Repo/MinecraftCustomClient_flavors.json"

icon_base64_icon128 = "data:image/png;base64,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"
icon_base64_legacy  = "data:image/png;base64,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"
icon_base64_modded  = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAYAAADDPmHLAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADr8AAA6/ATgFUyQAABbcSURBVHhe7V1pkFRVlj75MrOy9oISSsEFEQYbxLVwZ8QFeia6jRanndYIB3VCx8BQ+WGMS2nM2KGhuIz7D2oGcQnU0NbQcBuXwXVcaC0cFwQXRDFQFBewoCorqzLzzfnuy5N16/JyeVmZ9bKs99HH9+6599z77jnnLue+l9UUIECAAAECBAgQIECAAAECBAgQIECAMYBQ5jqieKr9/PrahtSU3Wpr6nsHBmggw48y1Uej9FNff29fT3jTH9b8V6+TM7owmvrniwO8Mu/s31Ao3NEYrZ0VTw1Q0k4rfiRkUV04SjsH+taRnVp6wmv3f6IyRhlGU/+szHVEkUpHmm2io1qitXOaDQIPeSiTKT7qMJr654sDpC0eEiHq7eXRgRGiE3jIU2VGKUZT/3xxgIhl8SAIJTE1uhHynDKjE6Opf744QIDqQVU6QMi20+kBWzbPow54dvQhk6xqVKUD2CFKh8M0KkNAAM+OPmSSVQ3XMLDScezLJ5zXzmbuxK4YGyNnXWTF8ePEwhHqGehfF7JpqW2F1quMDKoljs6lH0Eobc9kB+hoiNbMSqSSlCJnuZcwsHugr4tLLT7xlbvXqAyPKKd9XB2g0nFsLgcALH6ktJ3uYZVt4uSQDlRLHJ1LPxrqWbFTrJDVkM4YHyiXA5TTPq5LgF9xrG3blOLOQHENkZpZZtuVbr9Y5NMPCM+OPqAv6FO5UU77uDqA33EsRk0indyl7ZFqvxDy6QeEZ9dHfrlRTvu4OoBfcWwoFFIEpHjkuLUNqlT7xaKQfvDsgN6fcqKc9qnKKCDAyKEkBxhunJ5Mp3lY2BFsWtwonBk1WD/d1lC/zwlyxfn686IPbn0Doe+ODkpDOc8ZSnKA4cbpVpq1YFN9Pe9YsWs1KWZF+MFy68fvc4JCcT6eHX1w6xv6jL4rHZSIcp4zuGq50nF6qWHUSJ0TlBrnA+UIY0fynMGTAwB+dhAYiXMCvx10JM8ZPDnA4PpmUS13FFcdeABMcZt7t3+WToUWzf/fFe9ksjzhlXnnTrcte2VztO4oP9pf9bfnHmGF7ZV71Y+bgbDKNADi+z44ZoYvO/1BA8RXh9KhRSe8tmKDyvCI4bdfvAOUtA5VOk5PpdjD7dzPVun2hxvn49nRh0zSM4bbvhd4cgA9rq1knG5FQ1E7ZAxvxki1P9w4H8+OPmSSnjHc9r2gpBkgwK8Hrg7gd5w+3PYrBb09P+L8SrTv6gB+x+nDbb/SQNt+xvnlbN9Vi2MpDHLDWAqDXR1gLB2EuGEsHYS5OkAh+B2n52q/0g4wWL/fcf7w2tdR0jrld5xeqP1KA237GecPt30dJSnR7zg9V/sjBb/j/OG2r8M3JQaoDpTkAGU5J9i+s+RzAiWbSqXtFE+ULoS8aq/fz+8JdJTkAMM+J+AwIbl5S8Edai4k133Vayf60zSQJDdCHspkintGxevnvkMHmeQuKGecXwgleVGpYQw6VhsKU284vS56wNSldScdtp44zPOK+JoNM1Mbv+1oCIVVGJjMjJoIjxoVJtmpdeH9Ji+ta58+JEwqFhWtn8O0+EvvzRz4+MuO+pQ1q89ODdnwlTvOL4SSHKDkcwKePkOYQtvG9dSdcPCm8NRJvWpUpQcVUBQGkvXpHfEpVsrOOJjIhxwFhkM9VlPdJopGShullarfYnVHI5T6ckt9/JUPptDW7Q12mAcyiDFSH7zoKMkBCiFXnJ5OptQUWrPvJGr9+yPVVc0AHh0Au2Q9TjYxeA5RWvcqVr9ygCj1f7WFfn7+r+oKh7AiYZUtI7yccX4hlGUdMVHwnCCdpr7+BPX2xZn6PFMfU7qfHUdbl3VCHsq4yRZDla0/rvoOHeRCOeP8QqiIAxR1TsA9TCZ5fS2BIMtxhDNzuBDyqr1+YCTi/EKoiAMEGD2oiANU6/t8v+FHnF8IlVkCcp4TILaN+P4+32+g706cLzSoo3LH+YVQkUbCVrKbzbv6l4G+LryZG6SEuvZSah1CqbDFqnBZA3+tQF/RZ/QdOtB1IgSdQXfQYUasoqiI9nOeEyDk4//VLDh0ZuyAKR1N41tm9SUS2U3Rrx3hcJhqYzHase2XdYmPNy3t/5//W6+Cew4NgUrE+YXgy/Bb+/na6Ym1X61sbmg8CqERdsZjAZFIhOpra6m7Z+fq2Ox9F83+m9kVj/MLYUTWGROJz7+rp7Q/bVcFuO9KB1UAf4yQ6IvyfnjMOoDqO+sgk/QVY3cUBlDwzQEikTCTRWGDFC/zckTFzH4eE3g8oxgS53MfcvUPfa8W+OIA9fVR3g0z1dVQbe2uVFMTIQsvToYDhJeoA4T7YkgvPwzg2dEHt76pPnPfoYNqwPB6WiL+snR5O7fc2dTYOCeuwkAnCsDY4TFEdbEa2m1iE9XV11AaZ+9eRiJ6xDKhFMvg7N5rD9EUnIBHcIhjdq+A8eO9/fTjD90UT/Rz8/jnIIxDH4SBO3d2cTuL/9TxLyV9tVxO+OIAv532j+0WWZ01VmxOyk5mDZzifwlK0rS9dqffnTqHps3Ynfr7k5SGMYuAKsWj12KZ0I4+svD2Dl0sckQ7z8HOg7i8uYGvESejSFhhjPwobfjsW3r68Xdpw+ZvKcbRfZj/AeogKBSh/nSiK03pxS9+8ejYdIBJdCQ7QKgzTNE5Nhs9Yzo2fYriNEAHT5pC5138Wzq4fQrF+/opNZD71akOVQuPQKtvgKxtveqandqLgI0Zg50gxFM1tTaTVRtT6WKBNR7T/PtrNlLnnc/T+1s2Uh3VUCTjAFA3uwD3coAdwF68hf7quwP4swfgUVGriNdDF/rV7AFc+uYQ7wHUuZ//8MUBoupfhIkjAYMUj3fJ8o5AraF8XzR5LZ+HSgVk0Ydc/XP6PoYdIED1wBcHwOuhAayETFj3dVK8JK+QmbUX//VM/B+HnAiiNOKKSgTk0Ydc/XMo+4rMV/jiAL3c+b4sJQ0acHb+at+HadjrVJwpDwOiDuURJdAwgNAVfcjVPxB0UA3w5UjqmGmHT95j3LiT95w4fnLb+AZqa22i3ZnaWhtpItP0qW0066A9aXxrHYeAHMrZ+C0l786LojRZdopCLGeFOB3h9bxIgjZCIN7AhTgCCFne1INtg2VZtKO7h37cuo1qOCzcc/w42qO1RfVvD44sJk8YRxNaGr5t263hmS+2fbIlI+obvA6vsuAvS/+jnUJ2Z1NDw5x4f4JS+Fyc4Qw+l4MglVMsuEvqIIiHv9d5XJVnsjgMDDeyM/DVU9uOA8R72AF++J7iiR5+Gnz/46g5zBvDupoY7ejp6SI7tPhPHf86Ns8B1r/wYHsoTZ0tLU1zeuJxXi8HPwiBslJsvESCV0r8kEQxPTwmjIjyEMHVi/3EAUJseLuB7/nKs0ixwNqPhsNWkmKxhLoq6czzIzJoqKujX37Z0WVbtHjm3505Nh1gzRP3tfPk2tnSzA6gPgjRHcBRZCrlbMbUA3p5SscGGXjsnu4A1EBNu0+mPQ/Yn2rYaIJUOsWGHVwaMDvhG3+dp8qoF1rK/KpalMHs4JxvhJJWONKTtu0kvhIS4MsolJEQFP0XOZNnygEZ3rdMVy1YcMJ/r1r16qBic8CjhsoDOICdsjtbmhrnOF8EFXzOkUHWAWK0x8zDaMJ+UykSjSoDAKaBYAgYROehDO5FRgwGnpCbYUXOLANIGYeHZxg8J8F7FPwEA8bP8FIs181llzHv35mXV7lOLSOManeAPWa204Rp+1O0pmaIMQoZ3+SJHO6F3OrKZfze3l76/PPPafv27dly+siX9sA78cQTszyA69nJdDvTvylGDgQOoIOV19g2ifY94niKxjgKyGMwwDQ+gLQuJ2mdV6zchg0b6IorrqA333xTlcmH77//3q2ubm6rRTFzwJdzgGrG5APa8xpflFyMEaUMCGnwi5ETHhxt27ZttHXr1oIkTmnUVfD/OMp5khFGNS8BhyxcRBZPqT0cyv30009KmTAaoCsZPChZSAwrhtbL6EbV60JaCGVAepnPPvuMrrrqKlq9ejXV1tbSkiVLVBnkY1l49tln6ZtvvlFlN23aNOQZJkyYoGSYl9fGgQPoYGMd9sdz1O2rr75K9957b9ZAgG5IkBi/mDI6DxBj62lAeJCBkWF8TO/jxo2jTz75JJsPg1944YX0zjvOX9o7++yzh9R1+eWX06xZs8BzmDmQN7NSqFoHYBz2D2er0fnggw/SRRddlOH6AzxHIvPDmdbWVvrhhx+yDvDFF1/QWWedRW+99ZYq29TUpK6Cp59+mubNmxc4gFccfMo/qan08ccfpyuvvDLD9Qf9/f1qfUc0AAf48ccflfExO2CDeM4552QdYMaMGeoquO++++jwww+naDQaOIAXHHrqWUrJUDaUjHtZkwFZu02erL+SBvSQrRg5TN0giem//PJLuummm2jNmjXU0NBAN954Y7Yc9icrV66kjRs3Kt7bb789pK7p06dTS0sL6gocwAuwBAAwDhStGwxpwORB6aJ4WfP1Mm481K87iJTR61q3bp1ahl5//XUlO3nyZMVHOcj//PPPapYAkkm8XXTk5LkzlNfGg080gkgmk/xQdiQaiajz8WoiAAoG8Fs+GEkMBYWaPKSFB8OZZdx4IqeXAel1iUxjYyM1Nzera3d3t6IdO3aoZQG7fOSB8MWx1CXyuC+EwiUqgHcfv++IUCq9cp89J80wXwb5jWkL/pgdQaJAjDZA5+Ua+TrPTQ48sx7I6TypC8vQM888k53mJR9APiC8a6+9VtUFgAfK1Dso5IK8mZVC12P3/oYvHc2NDbN6E7wEDFSPAxyycNEc02CiUFHq119/rdZnKQO4OQQ2bgceeGCW52Z8QJfTHQK/mkYoiD9IhbQA+SBdbtKkSeoqPOSjLp5FnAI5kDezUuh66j/rQz3WlJbWlvreXucDsWrBoaec1aUbAzCVis3XXXfdpfLy4fjjj6dbbrlF3UtdYkizbsCtPdPQKKPzQLnkAF4OfLHxqAUrToFHqyJWrkrjyiNS8Xg37rw1KkCnnnqqkjXrMtOA1O3GE+DeLId7PY2rzuPnyAtfNoHVDlacuuojDCRpkOCggw6iiy++WO3WQXgrV6d9P+BWl54GcvHMNNs3ywO5yaEMoPPyoXCJMQaMHFw//PBDddYOQKkgmb7feOMNev7559X9okWL6Jprrska7JFHHqGbb75ZhWg4ij3jjDN2Wb91w0jdpsFQny4nxjbrAkROT5955pm0zz77FFwCAgcwAAeAAh9++GG65JJLFM9UNF4UIRQDcB5/5513qnvkr1ixQp0g4tg2FoupM3yRA8TYAqkbKKZcsWXw/Mcee2zBk8AABliJCvfccw+0WZAuuOCCIWvw8uXL7YkTJ7qWHUl64YUX1H6B7/Mi8A4Dyoo8kvDmDSdwAvBAmIJffPFF9a4AOP/88+mOO+5Q98jHG8Srr75axfCHHHIILV682HU6xyjVR69ZRm9P4LYM5JI7+eSTaa+99kJeXhsHDmCAFYrRrIwjikUaShUe1vjLLrtM5WGdnzt3rrpHGTjOu+++q2J3jgLoscceU3l6XYA4gBgMkDJuPPMZhAfocuaz831gYy/IF3oJvISBZl0gNpJK42qGdcKTNIB8t+fS03pdAtzzc+RF4B0GoLRCo+7+++/Pbvwk3w0ICc2DIJQFQU54qFvnme25PQNg1uUmV5UngdUMVpoaNfkUj48x1q9fn1W8GBAADwQejmfxTl7kTIMBIis8sz2pS8qAAKlL6gFMOeQHYaBHsOIwnWZSQ5UKiOLzGUPSgMnTjSOENN754+MPaU/qlzIA8rCx5ChD8YppjylwAC/IrKFKeabxAfDEOIAoGmmUM+XAR1ovA+g8UEdHhzpgEoAHoIwAr3+vv/56OvLII7NygNme/gx8H9jYC9w2UvqmDFfw3MoUI5erroULF+IAChbNSY2NjSq+9/IMLJcXjpsEyEIfPaxoNaJktAJIA/lGHdK6nKTdeIDICWbPnk3nnXcenXvuuYow4vGRB+Am5/YMwiuEYHowwEpTWvv4449p1apVSqkgARSrGwxpwOTpcqhSDGTyRO7uu++mjz76SPFwuKR/4LF8+XK67rrrVB4cYv/99y/4DKeccgrtvffe4AU29gJWspo6V6xYYdfU1CiKxWJZckuXWkbnsaHgeIqWLFmSndLZuPZtt91m19XVqbxoNFpU/S+//DK6UnAKGHSZAAoYTdAbK1q91gVh8yXkli61jM6TKV6AZ8CIxoyh25ENXVT9kC3C/sESYAKjDkp///336YknnlAOoU+tolSZygE3npscKFddjz76qPopGHiY5vGKWYyPJeCGG25Qn5SddtpptN9++2XlBGgPaeHhNwNTp04NzgG8AlOvPnqgWC8bMLcySIuBdJ5eDu8NnnzyScVrb2+n+fPnqzyku7q61IspjGy8W1iwYEHW2FIPyO0ZCjlAAAOsOAU4AogNp9K4Ck9P66GXzhOAZ4ZnbnUVGwY+99xzru2ZPEmzXF4E3mEACsQVujNHGaCPMCkjo5plFQ9pkQNPLyNygF7XpZdeSq+99priSz7kBODV19erXwodffTRWTmQ3h4IkPaYHywBXoCRgyv0lkupYmjkm4YVOZQRmGUAvS4AR8H4FbBZjwDlsAHE8oCffks51INykgb0uoM9gEdgOs2nVKShWOTrPJAYLV8ZwKxL32MgDZj7DqkbkDJ6e0JmXYXeBjpPEiCLUowPnimHtFkGMHnFGB9A3YCk9fYgh6tZl7SVD8EMYICVBwxRNIC0KFUUD5hGBH3wwQfqo1ABykBGjAhA5qSTTlL3Igfo7bnxzPaQBtyMn2kzr40DBzDAymMdOsrPpVTJN8uAgNNPPz37STkgfN0W+NnY5s2bh8iZhkZ54SENfjHG1+X4Pq+NnVIBsoASQVAglMmbQkXQoyhYCBhMOz8nB/CT7Xg8rgiArNgBf/FD8kQW9QK4R1u8D9mFJ88gMkijjM4DiRyuHBSq+3wIZgAD2ARiRMFA+AtdUKqMfACKNXlIcw7znJGIUzh8OQzghyGAGOall15SXwzj9wJr165VPBmtUjfqNXkyygGkwd/1GQbrwgzj/OS9Cv9CSDWDFasshaNgnMwBomQgkz2EB+WL4oGHHnqIPv30U3UvhoEcZI477jj14QfO7vFlsS6HMiCTB0h7UgZpk6fL4ZdBODJmXmBjL2BFqtM0vA1kBZdEqEaIp+rsWz1g7ty52Tw32XIRzzSqPW4nLwLvMMCG6me9RfFyBn+lEzpkhWZyHRTiyR92AvAXPTAyJQ9n/PL3fPDbvWLqL+UZHnjgATrmmGMKzgB5M8cieLS+x0o7FH8AAobCFA6l6srOxYNRgVtvvZXee+89dY9lRMrBQHAqfFGMP/mybNmyrNH0MiCpC9DrBpAvvFxy+CS9ra0t+CzcK9gBfs8brgdYmeOgUECUKkoGdJ5uDKQXLlxITz31lMrHV7wC5OEvj+HHpdikyVfAIidk8gCzPcAM/1zq2s4OMF4VyoFBtwqgwApDAL+MldeNtKl4XE2ernikY7GYenEDwjt+Ifzlb5SRPBeD7VIXYLaH/ELGZ3RzmWWqUB4EM4ALvvtuS2TChInXsQL/mZOtrNCwGKOIUUednZ0qigDEYCAA+QCWgNtvv32InNQFQA48sz3kmw6hl2HCH1z6mcvcw9eruHzeP8AUOIAL5s8/Poz/tw1W5h84+WfeybeBL4oGcBCjG0yMAR4OcnAvxLOKKgMgD/VADjOFLid1AajfbE83PmCWydS1lXl/5rLOGhQgQIAAAQIECBAgQIAAAQIECKBA9P/X39js8+G6HQAAAABJRU5ErkJggg=="
icon_base64_default = "data:image/png;base64,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"

repo_url = "https://raw.githubusercontent.com/sbamboo/MinecraftCustomClient/main/v2/Repo/repo.json"

chibit_default_host = "https://sbamboo.github.io/theaxolot77/storage/"

legacySourceFlavorDataFile_default = "flavor.mta"

# IncludeInline: ./assets/lib_crshpiptools.py

# Handle cusPip
import sys,os
cusPip = None
for i,a in enumerate(sys.argv):
    if a == "-cusPip":
        try:
            cusPip = sys.argv[i+1]
        except: pass
if cusPip != None:
    if os.path.exists(cusPip):
        int_autopipImport = autopipImport
        def autopipImport(*args,**kwargs):
            int_autopipImport(*args,**kwargs,cusPip=cusPip)

# BuildPrep: ST-excl
# [Imports]
try:
    import platform
    if platform.system() != "Windows":
        _ = autopipImport("magic","file-magic")
    _ = autopipImport("argparse")
    _ = autopipImport("scandir",relaunch=True,relaunchCmds=sys.argv)
    _ = autopipImport("requests")
    _ = autopipImport("getpass")
    _ = autopipImport("subprocess")
    _ = autopipImport("datetime")
    _ = autopipImport("json")
    _ = autopipImport("psutil")
    _ = autopipImport("readchar")
    _ = autopipImport("urllib3") # Need modname="urllib", pipname="urllib3"?
    _ = autopipImport("bs4")
    _ = autopipImport("rich",relaunch=True,relaunchCmds=sys.argv)
    _ = autopipImport("zlib","pyzlib")
except NameError as e:
    print("\033[31mAutoPipImport failed, has the script been run through the include-inline tool?\033[0m")
    print(f"\033[90m{e}\033[0m")
    exit()
# BuildPrep: END-excl

# [Setup]
import requests,platform,os,sys,shutil,argparse,zipfile
import json,time
parent = os.path.abspath(os.path.dirname(__file__))

# Enable ansi on windows
os.system("")

# [Args]
encoding = "utf-8"
parser = argparse.ArgumentParser(description='MinecraftCustomClient QuickInstaller')
parser.add_argument('-enc', type=str, help='The file encoding to use')
parser.add_argument('--install', help='Action: Install', action="store_true")
parser.add_argument('--uninstall', help='Action: Uninstall', action="store_true")
parser.add_argument('--open', help='Action: Open', action="store_true")
parser.add_argument('--datacopy', help='Action: Data copy', action="store_true")
parser.add_argument('-mcf','-cMinecraftLoc', dest="mcf", type=str, help='MinecraftFolder (.minecraft)')
parser.add_argument('-destination','-dest', dest="dest", type=str, help='Where should the client be installed?')
parser.add_argument('--fabprofile', help='Should fabric create a profile?', action="store_true")
parser.add_argument('--dontkill', help='Should the install not kill minecraft process?', action="store_true")
parser.add_argument('--autostart', help='Should the installer attempt to start the launcher?', action="store_true")
parser.add_argument('-cLnProfFileN', type=str, help='The filename to overwrite the profile-listing file with.')
parser.add_argument('-cLnBinPath', type=str, help='If autostart and no msstore launcher if found, overwrite launcher with this.')
parser.add_argument('--lnchTmstampForceUTC', help='Should the code relating to the launcher be forced to UTC timestamps?', action="store_true")
parser.add_argument('-taskkillProcNameExcls', type=str, help='A list of process names to exclude from the taskkill (when trying to restart mc-launcher), they user URL-encoded syntax with semicolon sepparated names.')
#parser.add_argument('--curse', help='Should the installer attempt to install into curseforge instead?', action="store_true")
#parser.add_argument('-curseInstanceP', type=str, help='A custom path to curseforge/minecraft/Instances')
parser.add_argument('--rinth', help='Should the installer attempt to install into modrinth instead?', action="store_true")
parser.add_argument('-rinthInstanceP', type=str, help='A custom path to com.modrinth.theseus/profiles')
parser.add_argument('-excurse', type=str, help='Should the installer export to a curseforge pack instead of installing? (Takes a filepath to the zip to export to [non-existing])')
parser.add_argument('--excurse', dest="excurse_parent", help='Same as -excurse but takes no arguments and places in <parent>/<modpack>.zip', action="store_true")
parser.add_argument('--y', help='always answer with Yes', action="store_true")
parser.add_argument('--n', help='always answer with No', action="store_true")
parser.add_argument('-exprt', help='Exports a copy of the unpacked tempdata, takes the zip to export to. (its created so give path to non-existent file)', type=str)
parser.add_argument('-imprt', help='Imports a copy of the unpacked tempdata, takes the zip to import from.', type=str)
parser.add_argument('--nopause', help="Won't pause on exit/finish", action="store_true")
parser.add_argument('-modpack', type=str, help="Preselect modpack (str)")
parser.add_argument('-modpackFile', type=str, help="Forced custom modpack file (path)")
parser.add_argument('-destmodpack', type=str, help="Datacopy destination modpack (str)")
parser.add_argument('-cuspip', type=str, help="Custom pip binary path. (Advanced)")
parser.add_argument('--dontResolveUrlIcons', help="With this the installer won't convert launcherIcon urls to base64. (This if ignored and never done when installing to modrinth unless --resolveUrlIconMR is given)", action="store_true")
parser.add_argument('--resolveUrlIconMR', help="With this the installer will convert launcherIcon urls to base64 when installing to modrinth.", action="store_true")
parser.add_argument('--showModLoadingBar', help="Should modfile installations show a loading bar? (Will clutter terminal output but may provide usefull info for some)", action="store_true")
parser.add_argument('--noWebInclGdriveWarns', help="Hides google-drive webinclude warnings.", action="store_true")
parser.add_argument('--noQouteJava', help="ADVANCED: Won't qoute java-path when installing loader. (Might break if spaces in path, but might fix compat)", action="store_true")
parser.add_argument('--showHidden', dest="show_hidden", help='EXPERIMENTAL: Shows all entries from the repository. (Might break UI)', action="store_true")
parser.add_argument('--update', help="EXPERIMENTAL: Attepts to update installer", action="store_true")
parser.add_argument('--noPipReload', help="INTERNAL", action="store_true")
parser.add_argument('--skipPreRelWait', help='DEBUG', action="store_true")
parser.add_argument('--skipWebIncl', help='DEBUG', action="store_true")
parser.add_argument('--debugLoaderCmd', help='DEBUG', action="store_true")
args = parser.parse_args()
if args.enc:
    encoding = args.enc

# IncludeInline: MX@./partial@prep.py

# IncludeInline: ./assets/lib_filesys.py
fs = filesys

# IncludeInline: MX@./assets/flavorFunctions.py

# [Set title]
tst = title
if args.modpack:
    tst = tst.replace("<modpack>",args.modpack)
else:
    tst = tst.replace("<modpack>","MODPACK")
setConTitle(tst)

# IncludeInline: ./assets/ui_dict_selector.py

# [Show action select]
action = None
action_install = False
action_uninstall = False
action_open = False
action_datacopy = False
action_update = False
# show selector
selTitle  = "Welcome to MinecraftCustomClient!\nSelect the action you would like to do:"
selSuffix = "\033[90m\nUse your keyboard to select:\n↑ : Up\n↓ : Down\n↲ : Select (ENTER)\nq : Quit\n␛ : Quit (ESC)\033[0m"
if platform.system() != "Windows":
    selSuffix = "\033[90m\nUse your keyboard to select:\na : Up\nb : Down\n↲ : Select (ENTER)\nq : Quit (ESC)"
actionsDict = {
    "[Install]":{"desc":"ncb:Runs the installer action."},
    "[Uninstall]":{"desc":"ncb:Allowes you to uninstall clients installed by this app."},
    "[Open Install Loc]":{"desc": "ncb:Opens the default install location folder."},
    "[Datacopy]":{"desc": "ncb:Tool for copying data between modpacks. (EXPERIMENTAL)"}
}
actionsDict["[Exit]"] = {"desc": "ncb:"}
acceptedActions = ["[Update]"]
acceptedActions.extend(list(actionsDict.keys()))
if args.install:
    action = "[Install]"
elif args.uninstall:
    action = "[Uninstall]"
elif args.open:
    action = "[Open Install Loc]"
elif args.datacopy:
    action = "[Datacopy]"
elif args.update:
    action = "[Update]"
    action_update = True
else:
    action = showDictSel(actionsDict,selTitle=selTitle,selSuffix=selSuffix)
if action == None or action not in acceptedActions or action == "[Exit]":
    args.nopause = True
    exit()
if action == "[Install]":
    action_install = True
if action == "[Uninstall]":
    action_uninstall = True
if action == "[Open Install Loc]":
    action_open = True
if action == "[Datacopy]":
    action_datacopy = True

# IncludeInline: MX@./partial@installermenu.py

# IncludeInline: MX@./partial@installermain.py

# IncludeInline: MX@./partial@uninstall.py

# IncludeInline: MX@./partial@datacopy.py

# IncludeInline: MX@./partial@update.py

# [Open install loc]
if action_open == True:
    fs.openFolder(getStdInstallDest())