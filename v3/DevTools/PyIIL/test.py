import re
import json

def strip_json_comments(json_string):
    """
    Removes both single-line (//) and multi-line (/* */) comments from a JSON string,
    while preserving the content of strings.
    
    Args:
        json_string (str): The JSON string with comments.
    
    Returns:
        str: The JSON string with comments removed.
    """
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

# Example usage:
json_with_comments = """
{
    "name": "John", // This is a single-line comment
    "greeting": "Hello // this should not be removed",
    "description": "This is a /* not a comment */",
    "age": 30,
    "city": "New York" /* This is a multi-line
    comment */
}
"""

clean_json = strip_json_comments(json_with_comments)
data = json.loads(clean_json)

print(data)
