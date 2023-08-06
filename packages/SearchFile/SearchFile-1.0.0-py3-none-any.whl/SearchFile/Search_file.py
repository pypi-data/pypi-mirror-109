from os import path, listdir


def search(tpath: str, name_parameter: str = None, extension_parameter: str = None) -> list:
    """
    Documentation. This function searches for files by the specified parameters.
    :param tpath: directory path
    :param name_parameter: file name or the first match of a substring with the name
    :param extension_parameter: file extension
    :return: list: returns a list sorted by the specified parameters
    """
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
