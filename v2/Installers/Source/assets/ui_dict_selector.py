import os
import sys
import readchar

# Function to clear the terminal screen
def clear_screen():
    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')

# Function to display the list of items
def display_items(selected_index, items, selkey, selTitle="Select an option:", selSuffix=None, dispWidth="vw", stripAnsi=False):
    # get dispWidth
    width,height = os.get_terminal_size()
    if dispWidth == "vw": dispWidth = width
    if dispWidth == "vh": dispWidth = height
    # clear screen (use function for os-indep)
    clear_screen()
    # get the length of the longest key
    max_key_length = max(len(key) for key in items.keys())
    # print
    if stripAnsi == True:
        print(selTitle)
    else:
        print("\x1b[0m"+selTitle) # include reset to fix wrong-coloring
    for i, key in enumerate(list(items.keys())):
        # get the org-value based on selkey
        if selkey == "" or selkey == None:
            ovalue = items[key]
        else:
            ovalue = items[key][selkey]
        if "ncb:" not in ovalue:
            value = "{" + ovalue + "}"
        else: value = ""
        # concat a string using left-adjusted keys
        string = f"  {key.ljust(max_key_length)}   {value}"
        # if over dispwidth cut with ... to correct size (indep of key-length)
        if len(string) > dispWidth-2:
            off = 12+max_key_length                                               # numerical amnt to cut (12 is what worked and the next is so it reacts on key-len)
            string = string.replace(value,"{"+ovalue[:dispWidth-off] + "..."+"}") # chn string basaed on cutoff
        # print the string with formatting if enabeld
        if i == int(selected_index):
            string = ">" + string[1:] # add the >
            if stripAnsi == True:
                print(f"{string}")
            else:
                print(f"\x1b[32m{string}\x1b[0m")
        else:
            print(f"{string}")
    # print suffix msg
    if selSuffix != None:
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

# Main function to show a dictionary based on the dict.value.<key> / or dict.value (if selkey = ""/None)
def showDictSel(nameDescDict=dict, selKey="desc", sti=0, selTitle="Select an option:", selSuffix=None, dispWidth="vw", stripAnsi=False):
    '''
    Add "ncb:" to your value to ommit the curly brackets.
    '''
    selected_index = sti # start index
    disp = True
    while True:
        # display the items if disp = True
        if disp == True:
            display_items(selected_index, nameDescDict, selKey, selTitle, selSuffix, dispWidth, stripAnsi)
        else:
            disp = True
        # check keys and change selected index depends on keys
        key = get_keypress()
        if getup(key.lower()):
            selected_index = selected_index - 1
            # roll-over
            if selected_index < 0: selected_index = len(nameDescDict)-1
        elif getdown(key.lower()):
            selected_index = selected_index + 1
            # roll-over
            if selected_index > len(nameDescDict)-1: selected_index = 0
        elif getent(key.lower()):
            return list(nameDescDict.keys())[selected_index]
        elif key.lower() == "q" or key.lower() == "\x1b":
            return None
        # if no key pressed set disp to false, so it wont redisp on an-uncaught key
        else:
            disp = False