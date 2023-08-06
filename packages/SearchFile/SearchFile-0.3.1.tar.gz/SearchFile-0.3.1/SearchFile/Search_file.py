from os import path, listdir


def search(tpath):
    list_file = []
    if path.isdir(tpath):
        try:
            for dirs in listdir(tpath):
                if path.isdir(path.join(tpath, dirs)):
                    search(path.join(tpath, dirs))
                else:
                    list_file.append(path.basename(path.join(tpath, dirs)))
                    print("\n", path.basename(path.join(tpath, dirs)))
        except PermissionError:
            list_file.append(tpath)
            print("\n""Отказано в доступе - " + tpath)
    else:
        if path.isfile(tpath):
            list_file.append(path.basename(tpath))
            print(path.basename(tpath))
        else:
            print("Неверно указан путь!")
    return list_file
