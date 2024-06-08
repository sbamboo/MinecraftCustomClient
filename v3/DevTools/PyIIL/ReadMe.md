## PyIIL *(Py Include In-Line)*

### What is it?
The toolkit is made to help to clean up big projects that are used with a single file,
in otherwords to automate merging of source-files.

### How to use it?
In short call `pyiil.py` with the `-pyfile` parameter pointing to your main source file.
Then you can define some *merging-logic* with comments:
- `#include <file>` : Inserts the content of *\<file\>* into the main file at the line.
- `#exclude ST`     : Starts an exclude block. *(Excludes the lines until the next exclude-end)*
- `#exclude END`    : Ends and exclude block.

Al of theese can also contain flags, flags are noted by adding ` @<flags>` at the end of the comment line.
*(Multiple tags can be included by sepparating them with `;`, but note only one `@` should be used, so only the first one, ex: `@flag1;flag2`)*
Example `@nocom` which makes the merger not add comments where a file was included.

Another flag is the `@ontags:<comma-sepparated-tags>` which contains tags where the line should be applied to.
Handled by adding `-tags <comma-sepparated-tags>` when calling the tool.


### Configuring an enviroment
To provide automation and configuration for your project or repository,
the tool will automatically look for a `pyiil.jsonc` file in the parent of the pyfile.
To overwrite it use either `--skipconf` or `-ovvconf <config-file>`.
**If not config file is found a default one will be used.**

**Example config:**
```jsonc
{
    // PyIIL options to use for this repository
    "pyiil": { "version": "1.0+" },

    // General information about this repository
    "meta": {
        "name": "example",
        "version": "1.0",
        "desc": "Example PyIIL config file.",
        "friendly-name": "Example Project"
    },

    // Information to add at the top of the file, as a list of lines. Meta info avaliable with curly-tags.
    "included-heading": [
        "# {friendly-name}, Version: {version}",
        "# {desc}",
        "# ",
        ""
    ],

    // Information to add at the bottom of the file, as a list of lines. Meta info avaliable with curly-tags.
    "included-footer": [],

    // Config for the accuall inclusion work
    "config": {
        "include-file-comments": true,
        // Custom resolvers can be used instead of the default request.get implementation.
        // Contains enabled, a path to the py module, and the attribute to call as a function.
        "custom-fetch-resolver": {
            "enabled": true,
            "path": "./resolver.py",
            "attr": "customResolver"
        },
        // Config for heading/footer
        "padd-heading": {
            "leading": false,
            "trailing": true
        },
        "padd-footer": {
            "leading": false,
            "trailing": false
        },
        // Settings for the output file
        "output": {
            "suffix": "_merged",
            // {+} is any string added by the pyiil -resnameadd param.
            "name": "{pyfile_name}{s}{+}.{pyfile_ext}"
        },
        // The prefix to use for multi, not recomended to change
        "apply-multi-prefix": "MX@",
        // Replace ops to apply to comment lines
        "comment-lines-replacers": {
            "»": ""
        }
    }
}
``` 
