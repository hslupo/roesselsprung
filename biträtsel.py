import pygame as pg

spalten = zeilen = 0
# sprungmatrix = [(-2,-1), (-2,1), (-1,2), (1,2),(2,1), (2,-1), (-1,-2), (1,-2)]
richtungen = {pg.K_DOWN: (0, 1), pg.K_UP: (0, -1), pg.K_LEFT: (-1, 0), pg.K_RIGHT: (1, 0)}



def grunddaten() :
    get_bin = lambda x, n: format(x, 'b').zfill(n)
    # print(get_bin(2 ** 11 - 1, 15))
    di = {}
    for i in range(2**10):
        s = get_bin(i, 10)
        v = [x for x in s.split('0') if x != '']
        w = ""
        for x in v:
            w += str(len(x)) + ' '
        w = w.strip()
        if w in di:
            di[w].append(i)
        else:
            di[w] = [i]

        print(i, s, v, w)
    for k in di:
        w = 2**10 - 1
        for u in di[k]:

            w = w & u
        di[k].append(w)

    print(di)
    print(di.keys())
    for x in di['3 4']:
        print(get_bin(x, 11))

def max_anzahl_einträge(liste):
    max = 0
    for s in liste:
        max = s.split().__len__() if s.split().__len__() > max else max
    return max



class cDaten():

    def __init__(self, datei, raster=40, rand=0):
        """
        :param datei: Dateiname incl. eventuell notwendigem Pfad
        ließt die Datei ein und erstellt daraus ein Dict für Zellenobjekte
        """
        global spalten, zeilen
        r = {}
        self.matrix = {}
        self.spaltenkopf_matrix = {}
        self.raster = raster  # x/y Dimension der Zellen
        self.rand = rand      # ohne diesen Rand
        with open(datei, encoding="utf-8") as f:
            rs, rz = [x for x in f.read().split('\n')]

        """ die Vorgaben für die Spalten und Zeilen """
        self.spaltenkopf = [z for z in [str(x).strip() for x in rs.split(',')]]
        self.zeilenkopf = [z for z in [str(x).strip() for x in rz.split(',')]]
        """ die max. Azahl von Vorgaben """
        self.spaltenmax = max_anzahl_einträge(self.spaltenkopf)

        self.zeilenmax = max_anzahl_einträge(self.zeilenkopf)
        spalten = self.spaltenkopf.__len__()
        zeilen = self.zeilenkopf.__len__()
        self.baue_spaltenkopf_matrix()

    def baue_spaltenkopf_matrix(self):
        for sp in range(spalten):
            spl = self.spaltenkopf[sp].split()
            while spl.__len__() < self.spaltenmax:
                spl.insert(0, '')
            for ze in range(self.spaltenmax):
                self.spaltenkopf_matrix[sp, ze] = spl[ze]
                # print(sp, ze, spl[ze])


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
    def screen_size(self):
        # raster * zeilen + rand + 400, raster * spalten + rand + 200)
        return self.rasterX * (spalten + self.spaltenmax + 1) + self.rand, \
               self.rasterY * (zeilen + self.zeilenmax + 1) + self.rand

    @property
    def matrix_rect(self):
        ssx, ssy = self.screen_size
        mrx = self.rasterX * (self.spaltenmax + 1) + self.rand
        mry = self.rasterY * (self.zeilenmax + 1) + self.rand
        return mrx, mry, ssx - mrx, ssy - mry

    @property
    def zeilenkopf_rect(self):
        mrx, mry, mx, my = self.matrix_rect
        return 0, mry, mrx - 1, my

    @property
    def spaltenkopf_rect(self):
        mrx, mry, mx, my = self.matrix_rect
        return mrx, 0, mx, mry - 1

    def __str__(self):
        t = f"\nRätsel: Nano\nSpalten: {spalten}\tZeilen: {zeilen}\n"
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


def calc_pos(pos):
    sp, ze = pos
    startsp, startze, b, h = spiel.matrix_rect
    return (sp * spiel.rasterX + spiel.rand + startsp, ze * spiel.rasterY + spiel.rand,
            spiel.rasterX, spiel.rasterY)

def zeichne_spiel():
    # Matrix des Rätsels zeichnen
    # spiel.calc_zeichnen()
    pg.draw.rect(screen, 'black', spiel.matrix_rect, 1)
    pg.draw.rect(screen, 'red', spiel.zeilenkopf_rect, 1)
    pg.draw.rect(screen, 'blue', spiel.spaltenkopf_rect, 1)
    for zelle in spiel.spaltenkopf_matrix:
        pos = calc_pos(zelle)
        pg.draw.rect(screen, 'black',  pos, 1)
        if spiel.spaltenkopf_matrix[zelle]:
            zeichne_text(spiel.spaltenkopf_matrix[zelle], pos, 'black')
    for zelle in spiel.matrix.values():
        pg.draw.rect(screen, zelle.hintergrundfarbe, zelle.zeichenrechteck)
        pg.draw.rect(screen, zelle.rahmenfarbe, zelle.zeichenrechteck, 3)
        if zelle.text:
            zeichne_text(zelle.text, zelle.zeichenrechteck, zelle.textfarbe)


def zeichne_text(text, pos, farbe):
    x, y, b, h = pos
    font_size = b // 3
    mitte = x + b // 2, y + h // 2

    t = pg.font.SysFont('Arial', font_size).render(text, False, farbe)
    t_rect = t.get_rect(center=mitte)
    screen.blit(t, t_rect)

def zeichne_spalten_matrix():

    pass

if __name__ == '__main__':
    spiel = cDaten('nono.bsp')
    pg.init()
    screen = pg.display.set_mode(spiel.screen_size)
    pg.display.set_caption("Nanorätsel")
    zeichne_spalten_matrix()
    print(spiel)

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
