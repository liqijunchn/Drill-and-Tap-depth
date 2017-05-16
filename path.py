import sys,os
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS,
        # and places our data files in a folder relative to that temp
        # folder named as specified in the datas tuple in the spec file
        base_path = sys._MEIPASS
    except Exception:
        # sys._MEIPASS is not defined, so use the original path
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

path=resource_path('test.txt')
print(path)
print(type(path))