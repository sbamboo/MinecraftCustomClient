import os
import sys
import readchar

# Function to clear the terminal screen
def clear_screen():
    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')

def getItemFormatting(stripAnsi=bool,checked=bool,selected=bool,formatting=dict):
    v = None
    if stripAnsi == True:
        v = ""
    else:
        if checked == True:
            if selected == True:
                v = formatting.get("item_selected_checked")
            else:
                v = formatting.get("item_normal_checked")
        else:
            if selected == True:
                v = formatting.get("item_selected")
            else:
                v = formatting.get("item_normal")
        if formatting.get("partial_name") != None and formatting.get("partial_name") != "" and selected == False:
            v += formatting.get("partial_name")
    if v == None:
        v = ""
    return v

def getDescFormatting(stripAnsi=bool,selected=bool,formatting=dict):
    v = None
    if stripAnsi == True:
        v = ""
    else:
        if formatting.get("partial_desc") != None and formatting.get("partial_desc") != "" and selected == False:
            v = formatting.get("partial_desc")
    if v == None:
        v = ""
    return v

def getBoxFormatting(stripAnsi=bool,checked=bool,selected=bool,formatting=dict):
    v = None
    if stripAnsi == True:
        v = ""
    else:
        if selected == False:
            if checked == True:
                v = formatting.get("box_checked")
            else:
                v = formatting.get("box_unchecked")
    if v == None:
        v = ""
    return v

# Function to display the list of items with checkboxes
def multisel_display_items(selected_index, items, selkey, checked_states, selTitle="Select options (press Enter to toggle):", selSuffix=None, dispWidth="vw", stripAnsi=False, formatting=None):
    def_formatting = {"item_selected":"\x1b[32m","item_selected_checked":"\x1b[32m","item_normal":"","item_normal_checked":"","box_unchecked":"","box_checked":""}
    if formatting != None and type(formatting) == dict:
        _formatting = def_formatting.copy()
        _formatting.update(formatting)
        formatting = _formatting
    # Get terminal width
    width, _ = os.get_terminal_size()
    if dispWidth == "vw":
        dispWidth = width

    clear_screen()
    if selTitle != None:
        print(selTitle)
    max_key_length = max(len(key) for key in items.keys())
    for i, key in enumerate(list(items.keys())):
        selected = i==selected_index
        if checked_states[i]:
            checkbox = f"{getBoxFormatting(stripAnsi,True,selected,formatting)}[x] "
        else:
            checkbox = f"{getBoxFormatting(stripAnsi,False,selected,formatting)}[ ] "
        if selkey == "" or selkey == None:
            item_desc = items[key]
        else:
            item_desc = items[key]["desc"]
        # check for ncb:
        ncb = False
        if "ncb:" in item_desc:
            ncb = True
            item_desc = item_desc.replace("ncb:","")
        else:
            item_desc = '{'+item_desc+'}'
        # check for btn:
        if "btn:" in item_desc:
            item_desc = "    " + item_desc.replace("btn:","")
            checkbox = ""
        # create string
        checked = True if checked_states[i] else False
        if stripAnsi == False:
            checkbox += "\033[0m"
        string = f"{checkbox}{getItemFormatting(stripAnsi,checked,selected,formatting)}{key.ljust(max_key_length)}  {getDescFormatting(stripAnsi,selected,formatting)}{item_desc}"
        if stripAnsi == False:
            string += "\033[0m"

        # Truncate and fill with ellipsis if the string is too long
        off = 12 + max_key_length  # Numerical amount to cut (12 is what worked)
        if len(string) > dispWidth - 2:
            string = string.replace(item_desc, f"{item_desc[:dispWidth - off]}...")
            if ncb == False and string.endswith("..."):
                string += "}"

        # handle newline
        if "prenl:" in item_desc:
            string = "\n" + string[::-1].replace(":lnerp","",1)[::-1]
        if "posnl:" in item_desc:
            string = string[::-1].replace(":lnsop","",1)[::-1] + "\n"

        if i == selected_index:
            print(f"\x1b[32m{string}\x1b[0m")
        else:
            print(string)
    if selSuffix is not None:
        print(selSuffix)

# Function to get a single keypress
def get_keypress():
    return readchar.readchar()

# Function to get the up-key
def getup(keylow):
    if os.name == 'nt':
        return keylow == "h"
    else:
        return keylow == "a"

# Function to get the down-key
def getdown(keylow):
    if os.name == 'nt':
        return keylow == "p"
    else:
        return keylow == "b"

# Function to get the enter-key
def getent(keylow):
    if os.name == 'nt':
        return keylow == "\r"
    else:
        return keylow == "\n"

# Function to get the space-key
def getspc(keylow):
    if os.name == 'nt':
        return keylow == " "
    else:
        return keylow == " "

# Main function to show a dictionary and allow multiple selections
def showMultiSelectMenu(nameDescDict=dict, selKey="desc", sti=0, selTitle="Select an option:", selSuffix=None, dispWidth="vw", prechecked=[], stripAnsi=False, formatting=None):
    checked_states = [False] * len(nameDescDict)
    selected_index = sti

    for i in prechecked:
        if i >= 0 and i < len(nameDescDict):
            checked_states[i] = True
    disp = True
    while True:
        if disp == True:
            multisel_display_items(selected_index, nameDescDict, selKey, checked_states, selTitle, selSuffix, dispWidth, stripAnsi, formatting)
        else:
            disp = True
        key = get_keypress()

        if getup(key.lower()):
            selected_index -= 1
            # roll-over
            if selected_index < 0: selected_index = len(nameDescDict)-1
        elif getdown(key.lower()):
            selected_index += 1
            # roll-over
            if selected_index > len(nameDescDict)-1: selected_index = 0
        elif getent(key.lower()) or getspc(key.lower()):
            idx = selected_index
            if "btn:" in list(nameDescDict.values())[idx]:
                # handle button
                return [key for i, key in enumerate(nameDescDict.keys()) if checked_states[i]],list(nameDescDict.keys())[idx]
            else:
                checked_states[idx] = not checked_states[idx]
        elif key.lower() == "q" or key.lower() == "\x1b":
            break
        else:
            disp = False

    selected_options = [key for i, key in enumerate(nameDescDict.keys()) if checked_states[i]]
    return selected_options,None

def format_size(size):
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB']
    suffix_index = 0
    while size >= 1024 and suffix_index < len(suffixes)-1:
        suffix_index += 1   # increment the index of the suffix
        size /= 1024.0      # apply the division
    return f"{size:.2f}{suffixes[suffix_index]}"

def displayForDir(dirpath, sti=0, selTitle="Select an option:", selSuffix=None, dispWidth="vw", prechecked=[], stripAnsi=False, formatting=None, extraElems=None):
    if os.path.exists(dirpath):
        items = os.listdir(dirpath)
        ditems = {}
        for item in items:
            itempath = os.path.join(dirpath,item)
            if os.path.isdir(itempath):
                subitems = os.listdir(itempath)
                subs = {"files":[],"folders":[]}
                for i in subitems:
                    ip = os.path.join(itempath,i)
                    if os.path.isfile(ip):
                        subs["files"].append(ip)
                    else:
                        subs["folders"].append(ip)
                files_str = None
                folders_str = None
                files_len = len(subs["files"])
                folders_len = len(subs["folders"])
                if files_len > 0:
                    if files_len == 1:
                        files_str = " 1 file"
                    else:
                        files_str = f" {files_len} files"
                if folders_len > 0:
                    if folders_len == 1:
                        folders_str = " 1 folder"
                    else:
                        folders_str = f" {folders_len} folders"
                final_str = ""
                if files_str != None:
                    if folders_str != None:
                        final_str = f"ncb:Has{files_str} and{folders_str}."
                    else:
                        final_str = f"ncb:Has{files_str}."
                else:
                    if folders_str != None:
                        final_str = f"ncb:Has{folders_str}."
                ditems[item] = final_str
            else: ditems[item] = f"ncb:Size: {str(format_size(os.path.getsize(itempath)))}"

        if extraElems != None:
            ditems.update(extraElems)

        sels,selbtn = showMultiSelectMenu(
            nameDescDict=ditems,
            selKey=None,
            selTitle=selTitle,
            selSuffix=selSuffix,
            dispWidth=dispWidth,
            prechecked=prechecked,
            stripAnsi=stripAnsi,
            formatting=formatting
        )
        nsels = []
        for sel in sels:
            nsels.append(os.path.join(dirpath,sel))
        return nsels,selbtn
    else:
        return [],selbtn