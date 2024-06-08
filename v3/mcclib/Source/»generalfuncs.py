import base64, re

# Validators
def typeval(val,typeV,nm=None,allowNone=False):
    """Raises if type of 'val' does not match 'typeV'!"""
    if type(val) != typeV and (val is not None or not allowNone):
        try: typeN = typeV.__name__
        except: typeN = str(typeV)
        if nm == None: raise Exception(f"Invalid type for parameter, must be '{typeN}'!")
        else: raise Exception(f"Invalid type for parameter '{nm}', must be '{typeN}'!")
def instval(val,instV,nm=None,allowNone=False,instN=None,checkEq=False):
    """Raises if type of 'val' is not instance of 'instV'!"""
    if not isinstance(val, instV) and (val is not None and (checkEq and val != instV) or (not checkEq) or (val is None and not allowNone)) and (val is not None or not allowNone):
        try: typeN = instN if instN != None else instV.__name__
        except: typeN = str(instV)
        if nm == None: raise Exception(f"Invalid type for parameter, must be '{typeN}'!")
        else: raise Exception(f"Invalid type for parameter '{nm}', must be '{typeN}'!")

# Function to strip the comments of JSON-source
def strip_json_comments(json_string:str) -> str:
    """
    Removes both single-line (//) and multi-line (/* */) comments from a JSON string,
    while preserving the content of strings.
    
    Args:
        json_string (str): The JSON string with comments.
    
    Returns:
        str: The JSON string with comments removed.
    """
    typeval(json_string,str,"json_string")
    def _replacer(match):
        s = match.group(0)
        if s.startswith('/'):
            return ""  # This is a comment, so replace it with an empty string
        else:
            return s   # This is a string, so keep it unchanged

    # Regex pattern to match both comments and strings
    pattern = re.compile(
        r'("(\\"|[^"])*")|(/\*.*?\*/|//[^\r\n]*)',
        re.DOTALL
    )

    # Use sub with the replacer function to handle replacements
    cleaned_json = re.sub(pattern, _replacer, json_string)

    return cleaned_json

# Base64 Functions
def encodeB64U8(string:str,encoding:str="utf-8") -> str:
    typeval(string,str,"string");typeval(encoding,str,"encoding")
    return base64.b64encode(string).decode(encoding)
def decodeB64U8(b64:bytes,encoding:str="utf-8") -> str:
    typeval(b64,bytes,"bytes");typeval(encoding,str,"encoding")
    return base64.b64decode(b64.encode(encoding))

# URL validator
def is_valid_url(url:str) -> bool:
    typeval(url,str,"url")
    # Regular expression pattern for matching URLs
    url_pattern = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https:// or ftp://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(url_pattern, url) is not None