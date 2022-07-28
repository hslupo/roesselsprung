# https://www.raetselstunde.de/kunterbunt/roessel-sprung/roesselsprung-015.html
import pygame as pg

spalten = zeilen_zahl = 0
sprungmatrix = [(-2,-1), (-2,1), (-1,2), (1,2),(2,1), (2,-1), (-1,-2), (1,-2)]
richtungen = {pg.K_DOWN: (0, 1), pg.K_UP: (0, -1), pg.K_LEFT: (-1, 0), pg.K_RIGHT: (1, 0)}
aktiveZelle = (0, 0)
protokoll = []

class cRätsel():

    def __init__(self, datei, raster=100, rand=0):
        """
        :param datei: Dateiname incl. eventuell notwendigem Pfad
        ließt die Datei ein und erstellt daraus ein Dict für Zellenobjekte
        """
        global spalten, zeilen_zahl
        r = {}
        self.matrix = {}
        self.raster = raster
        self.rand = rand
        with open(datei, encoding="utf-8") as f:
            ra = [x for x in f.read().split('\n')]
            zeilen = ra.__len__()
            spalten = ra[0].split().__len__()
            # Koordinaten, Text-Fragmente ermitteln
            r = {(z, s): ra[s].split()[z] for s in range(zeilen) for z in range(spalten)}
        # und entsprechende Objekte generieren
        for z in r:
            self.matrix[z] = cZelle(z, r[z])
        # originale sprungliste in die Objekte generieren
        self.original_sprungliste()

    @property
    def rasterX(self):
        return self._rasterX

    @property
    def rasterY(self):
        return self._rasterY

    @property
    def raster(self):
        return self._rasterX, self._rasterY

    @raster.setter
    def raster(self, wert):
        if wert.__class__.__name__ == 'int':
            self._rasterX = wert
            self._rasterY = wert
        else:
            self._rasterX, self._rasterY = wert

    @property
    def screen_rect(self):
        # raster * zeilen + rand + 400, raster * spalten + rand + 200)
        return self.rasterX * spalten + self.rand + 100, self.rasterY * zeilen_zahl + self.rand + 50

    def __str__(self):
        t = f"\nRätsel: Rösselsprung\nSpalten: {spalten}\tZeilen: {zeilen_zahl}\n"
        for zelle in self.matrix.values():
            t += str(zelle.__str__()).replace('\n','\t mögliche Ziele - ') + '\n'
        return t


    def original_sprungliste(self):
        """ alle möglichen Rösselsprünge als potentielles Ziel eintragen """
        for zelle in self.matrix:
            for delta in sprungmatrix:
                ziel = (zelle[0] +  delta[0], zelle[1] +  delta[1])
                if ziel in self.matrix and self.matrix[ziel].text != '*':
                    self.matrix[zelle].ziele.append(ziel)
            if ziel in self.matrix:
                # print(self.rätsel[zelle])
                pass


    def setze_ziel(self, von_zelle, zu_zelle):
        global  aktiveZelle
        protokoll.append((von_zelle, zu_zelle))
        print(protokoll)
        """  setzt eindeutiges Ziel, liefert nicht genutzte mögliche Ziele  """
        restziele = self.matrix[von_zelle].mein_ziel(zu_zelle)
        """  die eindeutige Zelle darf nicht zurück springen  """
        self.matrix[zu_zelle].loesche_ziel(von_zelle)
        """  auf die Zielzelle dürfen keine anderen Zellen springen  """
        for zelle in self.matrix[zu_zelle].ziele:
            self.matrix[zelle].loesche_ziel(zu_zelle)
        """ wenn nur noch eine Zielzelle nicht genutzt wurde
            diese dann als Start für Sprung zur von_zelle setzen """
        if restziele and restziele.__len__() == 1 and restziele != self.matrix[restziele[0]].ziele:
            print(restziele, self.matrix[restziele[0]].ziele)
            self.setze_ziel(restziele[0], von_zelle)
        aktiveZelle = zu_zelle

    def calc_zeichnen(self):
        br = self.rasterX - self.rand
        hö = self.rasterY - self.rand
        az = self.matrix[aktiveZelle]
        aziele = az.ziele
        for zelle in self.matrix.values():
            sp, ze = zelle.pos
            x, y = sp * self.rasterX + self.rand, ze * self.rasterY + self.rand
            zelle.zeichenrechteck = (x, y, br, hö)
            if az.pos == zelle.pos:
                zelle.rahmenfarbe = (250, 50, 10)
            elif zelle.pos in aziele:
                zelle.rahmenfarbe  = (10, 50, 50)
            else:
                zelle.rahmenfarbe = (200, 200, 200)
            anzahl_ziele = zelle.ziele.__len__()
            if anzahl_ziele == 1:
                zelle.hintergrundfarbe = (50, 250, 50)
            elif anzahl_ziele == 2:
                zelle.hintergrundfarbe = (50, 250, 250)
            elif anzahl_ziele == 3:
                zelle.hintergrundfarbe = (250, 250, 50)
            else:
                zelle.hintergrundfarbe = (250, 250, 250)



class cZelle():

    def __init__(self, pos, inhalt):
        self.pos = pos
        self.text = inhalt
        self.space = ' '
        self.ziele = []
        self.zeichenrechteck = (0, 0, 0, 0)
        # RGB-Farben für
        self.textfarbe = (10, 10, 10)
        self.hintergrundfarbe = (250, 250, 250)
        self.rahmenfarbe = (200, 200, 200)

    def __str__(self):
        return f"\t{self.pos}: {str('-' + self.text + self.space + '-').ljust(9)}\t{self.ziele}"

    def toggle_space(self):
        if self.space == '':
            self.space = ' '
        else:
            self.space = ''

    def loesche_ziel(self, pos):
        if pos in self.ziele:
            self.ziele.remove(pos)
            return self.ziele
        else:
            return False


    def mein_ziel(self, pos):
        """ setze ein eindeutiges Ziel, liefert nicht genutzte mögliche Ziele """
        if pos in self.ziele:
            restziele = []
            restziele.extend(self.ziele)
            restziele.remove(pos)
            self.ziele = [pos]
            # print(self, '\n\t', restziele)
            return restziele
        else:
            return False


def zeichne_brett():
    # Matrix des Rätsel zeichnen
    test.calc_zeichnen()
    for zelle in test.matrix.values():
        pg.draw.rect(screen, zelle.hintergrundfarbe, zelle.zeichenrechteck)
        pg.draw.rect(screen, zelle.rahmenfarbe, zelle.zeichenrechteck, 3)
        if zelle.text:
            zeichne_text(zelle.text, zelle.zeichenrechteck, zelle.textfarbe)


def zeichne_text(text, pos, farbe):
    x, y, b, h = pos
    font_size = b // 4
    mitte = x + b // 2, y + h // 2

    t = pg.font.SysFont('Arial', font_size).render(text, False, farbe)
    t_rect = t.get_rect(center=mitte)
    screen.blit(t, t_rect)


if __name__ == '__main__':
    test = cRätsel('roesselsprung-015.bsp')
    # print(test)
    zelle = test.matrix[(3, 4)]
    pg.init()
    screen = pg.display.set_mode(test.screen_rect)
    pg.display.set_caption("Rösselsprung Texträtsel")
    weitermachen = True
    clock = pg.time.Clock()
    aktiveZelle = (0, 0)

    while weitermachen:
        clock.tick(40)
        for ereignis in pg.event.get():
            if ereignis.type == pg.QUIT:
                weitermachen = False
            elif ereignis.type == pg.KEYDOWN: # and ereignis.key in richtungen:
                if ereignis.key == pg.K_n:
                    test.original_sprungliste()
                #aktiveZelleVerschieben(ereignis.key)
                #print(aktiveZelle)
                #print(zellentexte(aktiveZelle))
                pass
            elif ereignis.type == pg.MOUSEBUTTONDOWN:
                (x1, y1) = pg.mouse.get_pos()
                b1, b2, b3 = pg.mouse.get_pressed()
                # print(b1, b2, b3)
                sp, ze = x1 // test.rasterX, y1 // test.rasterY
                if (sp, ze) in test.matrix:
                    # print(sp, ze, ' im Rätsel')
                    if test.matrix[(sp, ze)].text == '*':
                        # print('Leerzelle')
                        pass
                    elif (sp, ze) == aktiveZelle:
                        if b2:
                            test.matrix[aktiveZelle].toggle_space()
                            # print('aktive Zelle toggle_space')
                    # andere Zelle
                    elif b1:
                        aktiveZelle = (sp, ze)
                        # print(f'linke Maustaste auf {(sp, ze)} gedrückt!')
                    elif b3:
                        # print(f'rechte Maustaste auf {(sp, ze)} gedrückt!')
                        # testen ob diese pos in den Zielen der aktiven Zelle ist
                        ziele = test.matrix[aktiveZelle].ziele
                        if (sp, ze) in ziele:
                            # print('ist drin - setze das als einziges Ziel')
                            test.setze_ziel(aktiveZelle, (sp, ze))
                        else:
                            # print('ist NICHT drin')
                            pass
                    elif b2:
                        pass
                        # print(f'Mausrad auf {(sp, ze)} gedrückt!')
                        # (sp, ze) ist Ziel von aktiver Zelle

                else:
                    print('Außerhalb des Rätsels')
                # print(x1 // raster, y1 // raster)
                # print(zellentexte(aktiveZelle))
            # elif ereignis.type == pg.MOUSEMOTION:
                # print('mausbewegung', pg.mouse.get_pos())

        screen.fill((180,180,190))
        zeichne_brett()

        pg.display.flip()
    print(protokoll)
    print(test)
    pg.quit()


    """# print(az)
    test.setze_ziel((1, 2), (0, 0))
    test.rätsel[(1, 2)].toggle_space()
    test.rätsel[(0, 0)].toggle_space()
    print(test.rätsel[(1, 2)])
    print(test.rätsel[(0, 0)])
    print(test.rätsel[(2, 1)])
    print(test)
"""
