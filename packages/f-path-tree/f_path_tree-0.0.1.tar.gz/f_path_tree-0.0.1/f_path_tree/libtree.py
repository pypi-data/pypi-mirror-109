import os
from os import path

def build (directories, catalog, k):
    for i in catalog[k]:
        if i == directories[-1]:
            if i == catalog[k][-1]:
                print(" │   " * k, "└───", i)
            else:
                print(" │   " * k, "├───", i)
            k += 1
            for j in catalog[k]:
                if i == catalog[k-1][-1]:
                    if j == catalog[k][-1]:
                        print(" │   " * (k - 1), "     " "└───", j)
                    else:
                        print(" │   " * (k - 1), "     " "├───", j)
                else:
                    if j == catalog[k][-1]:
                        print(" │   " * k, "└───", j)
                    else:
                        print(" │   " * k, "├───", j)
            k -= 1
        elif i == directories[k]:
            if i == catalog[k - 1][-1]:
                if i == catalog[k][-1]:
                    print(" │   " * (k - 1), "     " "└───", i)
                else:
                    print(" │   " * (k - 1), "     " "├───", i)
            else:
                if i == catalog[k][-1]:
                    print(" │   " * k, "└───", i)
                else:
                    print(" │   " * k, "├───", i)
            k += 1

            build(directories, catalog, k)

            k -= 1
        else:
            if i == catalog[k][-1]:
                print(" │   " * k, "└───", i)
            else:
                print(" │   " * k, "├───", i)
def tree (direct):

    if os.path.isfile(direct) != True:
        raise FileNotFoundError("Путь к файлу введён некорректно")

    directories = []
    catalog = []
    
    while direct != os.path.dirname(direct):
        direct = os.path.dirname(direct)
        os.chdir(direct)
        directories.append(os.path.basename(direct))
        catalog.append(os.listdir(direct))

    directories.pop()
    directories.reverse()
    catalog.reverse()

    print(" C:")
    build(directories, catalog, 0)
