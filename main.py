# https://www.raetselstunde.de/kunterbunt/roessel-sprung/roesselsprung-015.html

spalten = zeilen = 0
rätsel = {}
sprungmatrix = [(-2,-1), (-2,1), (-1,2), (1,2),(2,1), (2,-1), (-1,-2), (1,-2)]

def raetsel_laden(datei):
    global zeilen, spalten, rätsel
    with open(datei, encoding="utf-8") as f:
        ra = [x for x in f.read().split('\n')]
        zeilen = ra.__len__()
        spalten = ra[0].split().__len__()
        rätsel = {(z, s): [ra[z].split()[s], ' '] for s in range(spalten) for z in range(zeilen)}


def feld_add(sp1, ze1, sp2, ze2):
    return (sp1+sp2, ze1+ze2)


def sprungliste_erzeugen():
    for feld in rätsel:
        for delta in sprungmatrix:
            ziel = feld_add(*feld, *delta)
            if ziel in rätsel and rätsel[ziel] != '*':
                rätsel[feld].append(ziel)
        # print(feld, rätsel[feld])

def parse_zelle(pos, tiefe = 1 , teil = '', besucht = []):
    print(pos, tiefe, teil)
    teil += rätsel[pos][0] + rätsel[pos][1]
    besucht.append(pos)
    if tiefe > 0:
        for next in rätsel[pos][2:]:
            if next != pos and next not in besucht:
               parse_zelle(next, tiefe - 1, teil, besucht.copy())
    else:
        ergebnisse.append(teil)


def werGehtZu(pos, bisauf):
    # bisauf = (2, 3)

    return [ze for ze in list(rätsel.keys()) if pos in rätsel[ze][2:] and ze != bisauf]

def werKommtVon(pos):
    return rätsel[pos][2:]

def doku(von):
    ziele = rätsel[von][2:]
    print('Doku', von, rätsel[von])
    for ziel in ziele:
        print(' -- ', ziel, rätsel[ziel])

def xGehtZu(von, nach):
    doku(von)
    x = rätsel[von][:2]
    ziele = löscheTupelAusListe(rätsel[von][2:], nach)
    x.append(nach)
    rätsel[von] = x
    doku(von)

    for ohne in werGehtZu(nach, von):
        #print("    ", ohne, rätsel[ohne])
        löscheZiel(ohne, nach)
        #print("    ", ohne, rätsel[ohne])
    löscheZiel(nach, von)
    doku(von)

    if ziele.__len__() == 1:
        x = rätsel[ziele[0]][:2]
        x.append(von)
        rätsel[ziele[0]] = x
        doku(ziele[0])

    doku(von)


def wer_hat_wieviel_ziele():
    ziele0 = []
    ziele1 = []
    ziele2 = []
    ziele3 = []
    mehrziele = []
    for zelle in rätsel:
        ziele = rätsel[zelle].__len__() - 2
        if ziele == 0:
            ziele0.append(zelle)
        elif ziele == 1:
            ziele1.append(zelle)
        elif ziele == 2:
            ziele2.append(zelle)
        elif ziele == 3:
            ziele3.append(zelle)
        else:
            mehrziele.append(zelle)
    return ziele0, ziele1, ziele2, ziele3, mehrziele


def löscheTupelAusListe(liste, element):
    return [x for x in liste if element != x]


def löscheZiel(zelle, ziel):
    rätsel[zelle] = löscheTupelAusListe(rätsel[zelle], ziel)



if __name__ == '__main__':
    raetsel_laden("roesselsprung-015.bsp")
    sprungliste_erzeugen()
    ergebnisse = []
    parse_zelle(list(rätsel.keys())[0],1)
    print(ergebnisse)

    xGehtZu((0, 0), (1, 2))
    #print(werGehtZu((0, 0)))
    # print(0,0)
    #z0, z1, z2, z3, z4 = wer_hat_wieviel_ziele()
    #print(f'keine Ziele {z0}\n  1 Ziel {z1}\n    2 Ziele {z2}\n     3 Ziele {z3}\n der  Rest {z4}')
    #xGehtZu((0, 0), (1, 2))
    #z0, z1, z2, z3, z4 = wer_hat_wieviel_ziele()
    #print(f'keine Ziele {z0}\n  1 Ziel {z1}\n    2 Ziele {z2}\n    3 Ziele {z3}\n   der Rest {z4}')
    #print(werGehtZu((0, 0)))

