# https://www.raetselstunde.de/kunterbunt/roessel-sprung/roesselsprung-015.html
import pygame as pg


spalten = zeilen = 0
rätsel = {}
sprungmatrix = [(-2,-1), (-2,1), (-1,2), (1,2),(2,1), (2,-1), (-1,-2), (1,-2)]
richtungen = {pg.K_DOWN: (0, 1), pg.K_UP: (0, -1), pg.K_LEFT: (-1, 0), pg.K_RIGHT: (1, 0)}



def raetsel_laden(datei):
    global zeilen, spalten, rätsel
    with open(datei, encoding="utf-8") as f:
        ra = [x for x in f.read().split('\n')]
        zeilen = ra.__len__()
        spalten = ra[0].split().__len__()
        rätsel = {(s, z): [ra[s].split()[z], ' '] for s in range(zeilen) for z in range(spalten)}


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

def zeichne_brett(board):
  br = hö = raster - rand
  for sp, ze in board:
    x, y = sp*raster+rand, ze*raster+rand
    a, rahmen = (1, (255, 50, 50)) if aktiveZelle == (sp, ze) else (2, (255, 255, 255))

    pg.draw.rect(screen, "lightblue",(x, y, br, hö))
    pg.draw.rect(screen, rahmen, (x, y, br, hö), 2)
    if board[(ze,sp)][0] == '': continue
    zeichne_text(str(board[(ze,sp)][0]), raster//3, (x+br//2, y+hö//2), (25, 25, 25))


def zeichne_text(text, font_size, pos, farbe):
  t = pg.font.SysFont('Arial', font_size).render(text, False, farbe)
  t_rect = t.get_rect(center=pos)
  screen.blit(t, t_rect)

def aktiveZelleVerschieben(key):
    global aktiveZelle, zeilen, spalten
    sp, ze = aktiveZelle

    if key == pg.K_DOWN:
        if ze < zeilen - 1:
            ze += 1
        else:
            ze = 0
    elif key == pg.K_UP:
        if ze > 0:
            ze -= 1
        else:
            ze = zeilen - 1
    elif key == pg.K_RIGHT:
        if sp < spalten - 1:
            sp += 1
        else:
            sp = 0
    elif key == pg.K_LEFT:
        if sp > 0:
            sp -= 1
        else:
            sp = spalten - 1
    aktiveZelle = (sp, ze)

if __name__ == '__main__':
    raetsel_laden("roesselsprung-015.bsp")
    sprungliste_erzeugen()
    ergebnisse = []

    pg.init()
    raster = 100
    rand = 2  # raster // 8
    screen = pg.display.set_mode((raster * zeilen + rand + 400, raster * spalten + rand + 200))
    pg.display.set_caption("Rösselsprung Texträtsel")
    weitermachen = True
    clock = pg.time.Clock()
    aktiveZelle = (0, 0)


    while weitermachen:
        clock.tick(40)
        for ereignis in pg.event.get():
            if ereignis.type == pg.QUIT:
                weitermachen = False
            if ereignis.type == pg.KEYDOWN and ereignis.key in richtungen:
                aktiveZelleVerschieben(ereignis.key)
                print(aktiveZelle)
            elif ereignis.type == pg.MOUSEBUTTONDOWN:
                (x1, y1) = pg.mouse.get_pos()
                aktiveZelle = (x1 // raster, y1 // raster)
                print(x1 // raster, y1 // raster)
        screen.fill((180,180,190))
        zeichne_brett(rätsel)

        pg.display.flip()
    pg.quit()