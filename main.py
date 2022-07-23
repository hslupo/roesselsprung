# https://www.raetselstunde.de/kunterbunt/roessel-sprung/roesselsprung-015.html
import pygame as pg


richtungen = {pg.K_DOWN: (0, 1), pg.K_UP: (0, -1), pg.K_LEFT: (-1, 0), pg.K_RIGHT: (1, 0)}

class cZelle():

    def __init__(self, pos):
        self.pos = pos
        self.inhalt = rätsel[pos]
        self.text = str(self.inhalt[0])
        self.space = self.inhalt[1]
        self.ziele = self.inhalt[2:]

    def toggle_space(self):
        if self.space == '':
            self.space = ' '
        else:
            self.space = ''

        self.sichere_zelle()


    def baue_zelle(self):
        zelle = []
        zelle.append(self.text)
        zelle.append(self.space)
        zelle.extend(self.ziele)
        return zelle

    def sichere_zelle(self):
        rätsel[self.pos] = self.baue_zelle()

    def seperator(self):
        return self.space



def raetsel_laden(datei):
    global zeilen, spalten, rätsel
    with open(datei, encoding="utf-8") as f:
        ra = [x for x in f.read().split('\n')]
        zeilen = ra.__len__()
        spalten = ra[0].split().__len__()
        rätsel = {(z, s): [ra[s].split()[z], ' '] for s in range(zeilen) for z in range(spalten)}


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

def zellentexte(pos, tiefe = 0):
    e = ''
    t = rätsel[pos][0] + rätsel[pos][1]
    # texte.append(t)
    ziele = rätsel[pos][2:]
    for ziel in ziele:
        e += t + rätsel[ziel][0] + rätsel[ziel][1] + '\n'
    return(t, e)



def zeichne_brett(board):
    br = hö = raster - rand
    for sp, ze in board:
        zelle = board[sp, ze]
        ziele = zelle[2:]
        anz = ziele.__len__()
        if anz > 5:
            anz = 5
        bg = ((80 + 30 * anz, 200, 200))
        x, y = sp * raster + rand, ze * raster + rand
        a, rahmen = (1, (255, 50, 50)) if aktiveZelle == (sp, ze) else (2, (255, 255, 255))
        # print((sp, ze), bg, anz, zelle)
        pg.draw.rect(screen, bg, (x, y, br, hö))
        pg.draw.rect(screen, rahmen, (x, y, br, hö), 2)
        if board[(ze,sp)][0] == '': continue
        zeichne_text(str(board[(sp, ze)][0]), raster//3, (x+br//2, y+hö//2), (25, 25, 25))

    br = raster * 2
    hö = raster // 2
    deltay = zeilen * raster + 20

    for sp in range(3):
        for ze in range(3):
            x, y = sp * br + rand, ze * hö + rand + deltay
            pg.draw.rect(screen, (255, 255, 255), (x, y, br,  hö), 1)
            # print(sp, br, br + (sp * br // 2))
        # print()

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

def i2pos(index, spalten):
    return (index % spalten, index // spalten)

def pos2i(pos, spalten):
    sp, ze = pos
    return ze * spalten + sp


if __name__ == '__main__':
    raetsel_laden("roesselsprung-015.bsp")
    print(rätsel)
    sprungliste_erzeugen()
    print(rätsel)
    ergebnisse = []
    for i, zelle in enumerate(rätsel):
        print(i, zelle, i2pos(i, spalten), pos2i(zelle, spalten))

    # quit(1954)

    pg.init()
    raster = 100
    rand = 2  # raster // 8
    screen = pg.display.set_mode((raster * zeilen + rand + 400, raster * spalten + rand + 200))
    pg.display.set_caption("Rösselsprung Texträtsel")
    weitermachen = True
    clock = pg.time.Clock()
    aktiveZelle = (0, 0)
    print(zellentexte(aktiveZelle))

    while weitermachen:
        clock.tick(40)
        for ereignis in pg.event.get():
            if ereignis.type == pg.QUIT:
                weitermachen = False
            elif ereignis.type == pg.KEYDOWN and ereignis.key in richtungen:
                aktiveZelleVerschieben(ereignis.key)
                print(aktiveZelle)
                print(zellentexte(aktiveZelle))
            elif ereignis.type == pg.MOUSEBUTTONDOWN:
                (x1, y1) = pg.mouse.get_pos()
                b1, b2, b3 = pg.mouse.get_pressed()
                print(b1, b2, b3)
                sp, ze = x1 // raster, y1 // raster
                if (sp, ze) in rätsel:
                    print(sp, ze, ' im Rätsel')
                    if rätsel[(sp, ze)] == '*':
                        print('Leerzelle')
                    elif (sp, ze) == aktiveZelle:
                        if b2:
                            cz = cZelle(aktiveZelle)
                            cz.toggle_space()
                        print('aktive Zelle')
                    # andere Zelle
                    elif b1:
                        aktiveZelle = (sp, ze)
                        print(f'linke Maustaste auf {(sp, ze)} gedrückt!')
                    elif b3:
                        print(f'rechte Maustaste auf {(sp, ze)} gedrückt!')
                        # testen ob diese pos in den Zielen der aktiven Zelle ist
                        ziele = rätsel[aktiveZelle][2:]
                        if (sp, ze) in ziele:
                            print('ist drin - setze das als einziges Ziel')
                        else:
                            print('ist NICHT drin')
                    elif b2:
                        print(f'Mausrad auf {(sp, ze)} gedrückt!')
                        # (sp, ze) ist Ziel von aktiver Zelle

                else:
                    print('Außerhalb des Rätsels')
                # print(x1 // raster, y1 // raster)
                print(zellentexte(aktiveZelle))
            # elif ereignis.type == pg.MOUSEMOTION:
                # print('mausbewegung', pg.mouse.get_pos())

        screen.fill((180,180,190))
        zeichne_brett(rätsel)

        pg.display.flip()
    pg.quit()