# snit

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Python command line application to backup IDE / code editor settings. 
**Currently only VSCode is supported**.

Motivation: I have most of my projects in Github, but don't want to put editor settings there.  This lets me save the important information in *launch.json*, *settings.json*, to some central location. 


## Project Features

* Simply copies files to given destination 
* files are numgered sequentially, like old-school [VMS](https://en.wikipedia.org/wiki/Versioning_file_system#Files-11_(RSX-11_and_OpenVMS))
* files are compared so only changed files are backed up.
* numbering preserves the extension so the OS still recognizes the file type.


## Alternatives

VSCode offers settings sync, but not for workspaces, only for user settings.

Git, Hg, etc. seem too heavy.

## Installation

    $ pip install snit

## Usage
    $ snit [OPTIONS] COMMAND

    Options:
       -a, --archive PATH    Specify the directory for the archive.  Can be set with
                             the SNIT_DIR environment variable.  [required]
       --help                Show this message and exit.

    Commands:
        backup  Backup editor settings.  
        list    List any found backups.  

## Example:
(Windows, with `SNIT_DIR` set)

    D:\Code\MyBigProject>snit backup

Copies workspace settings to `$SNIT_DIR\D__Code_MyBigProject\vscode`

## ToDo
Verify Unix compatibility.