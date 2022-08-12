from pathlib import Path
from time import sleep
import locale

def text_ab(text, von):
    v = text.find(von)
    if v >= 0:
        return text[v + len(von):]
    else:
        return ""


def text_bis(text, bis):
    return text[:text.find(bis)]


def text_zwischen(text : str, von, bis):
    v = text_ab(text, von)
    if v != "":
        return v[:v.find(bis)]
    else:
        return ""


def msgbox(titel, msg, sle=3 ):
    from tkinter import messagebox
    messagebox.showinfo(titel, msg)
    sleep(sle)


def dateiexist(dateiname): # inclusive Pfad
    fileObj = Path(dateiname)
    return fileObj.is_file()


def s2d(s):
    from datetime import datetime
    return datetime.date(datetime.strptime(s, "%Y-%m-%d"))



def i2s(i):
    return locale.format_string("%d", i, grouping=True)


import pickle

def laden(datei):
    if dateiexist(datei):
        f = open(datei, 'rb')
        p = pickle.Unpickler(f)
        inhalt = p.load()
        f.close()
    else:
        inhalt = {}
    return inhalt

def update(datei, inhalt):
    # print(inhalt)
    f = open(datei, 'wb')
    p = pickle.Pickler(f)
    p.dump(inhalt)
    f.close()


locale.setlocale(locale.LC_ALL, '')
if __name__ == '__main__':
    print('__name__ == "__main__"')
    # msgbox('__name__ == "__main__"', 'Schau mal auf meinen Titel')

