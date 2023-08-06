# SearchFile
#### Table of contents
1. [Installation](#Installation)
2. [Description](#Description)
3. [Using](#Using)
4. [Code](#Code)
## Installation
Installation using a terminal:

```pip install SearchFile```
## Description
This library searches for files by the specified parameters.
## Using
```import SearchFile```

or

```from SearchFile import search```

The `search` function accepts three parameters.

tpath: directory path

name_parameter: file name or the first match of a substring with the name

extension_parameter: file extension

returns a list sorted by the specified parameters
#### For Windows
Also, the directory separator should be written in the form `\\`, so as not to form control characters (\n, \t, \r, etc.). Examples:
```
search("C:\\Users")
search("D:\\Downloads\\test.txt", "t")
search("D:\\Git\\cmd", "t", ".txt")
search("C:\\Users", extension_parameter=".txt")
```
#### Linux
The directory separator should be used `/`. Examples:
```
search("/home/artem/desktop/tmp/")
search("/home/artem/desktop/", "t")
search("/home/artem/tmp/file1", "f", ".txt")
search("/home/artem/desktop/tmp/", extension_parameter=".txt")
```
#### Mac OS
The directory separator should be used `/`. Examples:
```
search("/Library/Desktop Pictures")
search("/Library/Desktop Pictures/pictures1.jpg", "pictures1")
search("/Library/Desktop Pictures/gallery", "f", ".jpg")
search("/Library/Desktop Pictures", extension_parameter=".png")
```
## Code
```
from os import path, listdir


def search(tpath: str, name_parameter: str = None, extension_parameter: str = None) -> list:
    list_all_files = []

    def search_all_files(transmission_path):
        if path.isdir(transmission_path):
            for dirs in listdir(transmission_path):
                if path.isdir(path.join(transmission_path, dirs)):
                    search_all_files(path.join(transmission_path, dirs))
                else:
                    list_all_files.append(path.basename(path.join(transmission_path, dirs)))
            return list_all_files
        else:
            if path.isfile(transmission_path):
                list_all_files.append(path.basename(transmission_path))
            else:
                return "The path is specified incorrectly!"
            return list_all_files

    if name_parameter is not None:
        list_needed_files = [files for files in search_all_files(tpath)
                             if files.find(name_parameter) == 0]
        if extension_parameter is not None:
            list_needed_files = [files for files in list_needed_files
                                 if files.rfind(extension_parameter) == files.rfind(".")]
        return list_needed_files

    if extension_parameter is not None:
        list_needed_files = [files for files in search_all_files(tpath)
                             if files.rfind(extension_parameter) == files.rfind(".")]
        return list_needed_files

    return search_all_files(tpath)
```