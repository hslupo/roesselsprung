# https://www.raetselstunde.de/kunterbunt/roessel-sprung/roesselsprung-015.html
import pygame as pg


richtungen = {pg.K_DOWN: (0, 1), pg.K_UP: (0, -1), pg.K_LEFT: (-1, 0), pg.K_RIGHT: (1, 0)}



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
        rahmen = (255, 50, 50) if aktiveZelle == (sp, ze) else (255, 255, 255)
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


