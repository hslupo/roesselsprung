# https://www.raetselstunde.de/kunterbunt/roessel-sprung/roesselsprung-015.html
import pygame as pg

spalten = zeilen = 0
sprungmatrix = [(-2,-1), (-2,1), (-1,2), (1,2),(2,1), (2,-1), (-1,-2), (1,-2)]
richtungen = {pg.K_DOWN: (0, 1), pg.K_UP: (0, -1), pg.K_LEFT: (-1, 0), pg.K_RIGHT: (1, 0)}


class cDaten():

    def __init__(self, datei, raster=100, rand=0):
        """
        :param datei: Dateiname incl. eventuell notwendigem Pfad
        ließt die Datei ein und erstellt daraus ein Dict für Zellenobjekte
        """
        global spalten, zeilen
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
        # self.original_sprungliste()

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
        return self.rasterX * spalten + self.rand + 100, self.rasterY * zeilen + self.rand + 50

    def __str__(self):
        t = f"\nRätsel: Rösselsprung\nSpalten: {spalten}\tZeilen: {zeilen}\n"
        for zelle in self.matrix.values():
            t += str(zelle.__str__()).replace('\n','\t mögliche Ziele - ') + '\n'
        return t



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




def zeichne_spiel():
    # Matrix des Rätsels zeichnen
    # spiel.calc_zeichnen()
    for zelle in spiel.matrix.values():
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
    spiel = cDaten('roesselsprung-015.bsp')
    pg.init()
    screen = pg.display.set_mode(spiel.screen_rect)
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
                    pass

            elif ereignis.type == pg.MOUSEBUTTONDOWN:
                (x1, y1) = pg.mouse.get_pos()
                b1, b2, b3 = pg.mouse.get_pressed()  # welche Maustaste
                # print(b1, b2, b3)
                # sp, ze = x1 // test.rasterX, y1 // test.rasterY
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

            # elif ereignis.type == pg.MOUSEMOTION:
                # print('mausbewegung', pg.mouse.get_pos())

        screen.fill((180,180,190))
        zeichne_spiel()

        pg.display.flip()

    pg.quit()
