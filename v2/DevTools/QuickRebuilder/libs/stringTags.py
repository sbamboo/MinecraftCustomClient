# StringTags: Smal library to handle some nice string formatting.
# Made by: Simon Kalmi Claesson
# Version: 1.1
#

# [Imports]
import socket
import re
import getpass

# Variables:        [<variable>]
# Ansi:             {!<AnsiCode>}  FOR COLOR DON'T FORGET m AT THE END
# GeneralTags:      {<tagName>}
# PwshCompatTags:   {<tagName>}
# Unicode:          {u.<unicode>}
# ColorsFground:    {f.<colorName>}
# ColorsBground:    {b.<colorName>}
# Reset:            {r}
# Hex Foreground:   {#<hex>}        NO OPACITY SUPPORT
# Hex Background:   {#!<hex>}       NO OPACITY SUPPORT
# RGB Foreground:   {rgb.<R>;<G>;<B>}  INTEGER ONLY
# RGB Background:   {rgb!<R>;<G>;<B>} INTEGER ONLY
# Esc Char:         {esc} / §esc§
# Newline Char:     {\n}  / §nl§
# Unformatted tags: {^<tagName>}    THESE TAGS GETS REPLACED LAST, CONTENT IS NOT FORMATTED

# Main function
def formatStringTags(inputText,allowedVariables={},customTags={}): # AllowedVariables are dict of {varName: varValue}
    '''CSlib.externalLibs.stringTags: Formats stringTags. Note! Not compatible with crosshell's old stringFormat library!
      Variables:        [<variable>]
      Ansi:             {!<AnsiCode>}      FOR COLOR DON'T FORGET m AT THE END
      GeneralTags:      {<tagName>}
      PwshCompatTags:   {<tagName>}
      Unicode:          {u.<unicode>}
      ColorsFground:    {f.<colorName>}
      ColorsBground:    {b.<colorName>}
      Reset:            {r}
      Hex Foreground:   {#<hex>}           NO OPACITY SUPPORT
      Hex Background:   {#!<hex>}          NO OPACITY SUPPORT
      RGB Foreground:   {rgb.<R>;<G>;<B>}  INTEGER ONLY
      RGB Background:   {rgb!<R>;<G>;<B>}  INTEGER ONLY
      Esc Char:         {esc} / §esc§
      Newline char:     {\\n} / §nl§
      Unformatted tags: {^<tagName>}       THESE TAGS GETS REPLACED LAST, CONTENT IS NOT FORMATTED
    '''
    _lastUsedTag = None
    placeholders = {}
    # Custom Tags
    for tag,tagValue in customTags.items():
        placehold = False
        if tag.startswith("^"):
            placehold = True
            tag = tag.replace("^","",1)
        rtext = '{' + str(tag) + '}'
        if tagValue in customTags.keys():
            tagValue = customTags[tagValue]
        if placehold == True:
            plk = "%PLC%"+tag+"%PLC%"
            placeholders[plk] = tagValue
            inputText = inputText.replace(rtext,plk)
        else:
            inputText = inputText.replace(rtext,tagValue)
    # New lines parsing
    inputText = inputText.replace("{\\n}","\n")
    inputText = inputText.replace("§nl§","\n")
    # Variable parsing
    pattern = r'\[([^]]+)\]'
    matches = re.finditer(pattern,inputText)
    for match in matches:
        matchObject = match.group()
        variableName = str(matchObject).lstrip("[")
        variableName = variableName.rstrip("]")
        # control match
        if allowedVariables.get(variableName) == None: isVar = False
        else: isVar = allowedVariables.get(variableName)
        if isVar != False:
            inputText = inputText.replace(str(matchObject),isVar)
    # Special key parse
    inputText = inputText.replace("{user}",getpass.getuser())
    inputText = inputText.replace("{hostname}",socket.gethostname())
    # ansi key parse
    pattern = r'\{\!([^}]+)\}'
    matches = re.finditer(pattern,inputText)
    for match in matches:
        matchObject = match.group()
        matchString = str(matchObject).lstrip("{!")
        matchString = matchString.rstrip("}")
        inputText = inputText.replace(str(matchObject),f"\033[{matchString}")
    # general tag parse
    inputText = inputText.replace("{reset}","\033[0m")
    inputText = inputText.replace("{blinkoff}","\033[25m")
    inputText = inputText.replace("{blink}","\033[22m")
    inputText = inputText.replace("{boldoff}","\033[22m")
    inputText = inputText.replace("{bold}","\033[1m")
    inputText = inputText.replace("{hiddenoff}","\033[28m")
    inputText = inputText.replace("{hidden}","\033[8m")
    inputText = inputText.replace("{reverseoff}","\033[27m")
    inputText = inputText.replace("{reverse}","\033[7m")
    inputText = inputText.replace("{italicoff}","\033[23m")
    inputText = inputText.replace("{italic}","\033[3m")
    inputText = inputText.replace("{underlineoff}","\033[24m")
    inputText = inputText.replace("{underline}","\033[4m")
    inputText = inputText.replace("{strikethroughoff}","\033[29m")
    inputText = inputText.replace("{strikethrough}","\033[9m")
    # powershell compatability presets (HardCoded on python)
    inputText = inputText.replace("{formataccent}","\033[32;1m")
    inputText = inputText.replace("{tableheader}","\033[32;1m")
    inputText = inputText.replace("{erroraccent}","\033[36;1m")
    inputText = inputText.replace("{error}","\033[31;1m")
    inputText = inputText.replace("{warning}","\033[33;1m")
    inputText = inputText.replace("{verbose}","\033[33;1m")
    inputText = inputText.replace("{debug}","\033[33;1m")
    inputText = inputText.replace("{p.style}","\033[33;1m")
    inputText = inputText.replace("{fi.directory}","\033[44;1m")
    inputText = inputText.replace("{fi.symboliclink}","\033[36;1m")
    inputText = inputText.replace("{fi.executable}","\033[32;1m")
    # unicode key parse
    pattern = r'\{u.([^}]+)\}'
    matches = re.finditer(pattern,inputText)
    for match in matches:
        matchObject = match.group()
        matchString = str(matchObject).lstrip("{u.")
        matchString = matchString.rstrip("}")
        evaluated = eval(f"chr(0x{matchString})")
        inputText = inputText.replace(str(matchObject),str(evaluated))
    # Colors Foreground
    inputText = inputText.replace("{f.black}","\033[30m")
    inputText = inputText.replace("{f.darkgray}","\033[90m")
    inputText = inputText.replace("{f.gray}","\033[37m")
    inputText = inputText.replace("{f.white}","\033[97m")
    inputText = inputText.replace("{f.darkred}","\033[31m")
    inputText = inputText.replace("{f.red}","\033[91m")
    inputText = inputText.replace("{f.darkmagenta}","\033[35m")
    inputText = inputText.replace("{f.magenta}","\033[95m")
    inputText = inputText.replace("{f.darkblue}","\033[34m")
    inputText = inputText.replace("{f.blue}","\033[94m")
    inputText = inputText.replace("{f.darkcyan}","\033[36m")
    inputText = inputText.replace("{f.cyan}","\033[96m")
    inputText = inputText.replace("{f.darkgreen}","\033[32m")
    inputText = inputText.replace("{f.green}","\033[92m")
    inputText = inputText.replace("{f.darkyellow}","\033[33m")
    inputText = inputText.replace("{f.yellow}","\033[93m")
    # Colors Background
    inputText = inputText.replace("{b.black}","\033[40m")
    inputText = inputText.replace("{b.darkgray}","\033[100m")
    inputText = inputText.replace("{b.gray}","\033[47m")
    inputText = inputText.replace("{b.white}","\033[107m")
    inputText = inputText.replace("{b.darkred}","\033[41m")
    inputText = inputText.replace("{b.red}","\033[101m")
    inputText = inputText.replace("{b.darkmagenta}","\033[45m")
    inputText = inputText.replace("{b.magenta}","\033[105m")
    inputText = inputText.replace("{b.darkblue}","\033[44m")
    inputText = inputText.replace("{b.blue}","\033[104m")
    inputText = inputText.replace("{b.darkcyan}","\033[46m")
    inputText = inputText.replace("{b.cyan}","\033[106m")
    inputText = inputText.replace("{b.darkgreen}","\033[42m")
    inputText = inputText.replace("{b.green}","\033[102m")
    inputText = inputText.replace("{b.darkyellow}","\033[43m")
    inputText = inputText.replace("{b.yellow}","\033[103m")
    # Reset
    inputText = inputText.replace("{r}","\033[0m")
    # hex key parse
    pattern = r'\{\#([^}]+)\}'
    matches = re.finditer(pattern,inputText)
    for match in matches:
        matchObject = match.group()
        matchString = str(matchObject).lstrip("{#")
        if matchString[0] == "!":
            matchString = matchString.lstrip("!")
            background = True
        else:
            background = False
        matchString = matchString.rstrip("}")
        lv = len(matchString)
        r,g,b = tuple(int(matchString[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
        ansi = '\033[{};2;{};{};{}m'.format(48 if background else 38, r, g, b)
        inputText = inputText.replace(str(matchObject),ansi)
    # RGB key parse
    pattern = r'\{rgb.([^}]+)\}'
    matches = re.finditer(pattern,inputText)
    for match in matches:
        matchObject = match.group()
        matchString = str(matchObject).lstrip("{rgb")
        if matchString[0] == "!":
            matchString = matchString.lstrip("!")
            background = True
        elif matchString[0] == ".":
            matchString = matchString.lstrip(".")
            background = False
        else:
            background = False
        matchString = matchString.rstrip("}")
        r,g,b = matchString.split(";")
        ansi = '\033[{};2;{};{};{}m'.format(48 if background else 38, r, g, b)
        inputText = inputText.replace(str(matchObject),ansi)
    # Replace esc chars
    inputText = inputText.replace("§esc§","\033")
    inputText = inputText.replace("{esc}","\033")
    # Put-in placeholded sections
    for k,v in placeholders.items():
        if k in inputText:
            inputText = inputText.replace(k,v)
    # Return
    return inputText