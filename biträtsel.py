import pygame as pg

spalten_zahl = zeilen_zahl = 0
richtungen = {pg.K_DOWN: (0, 1), pg.K_UP: (0, -1), pg.K_LEFT: (-1, 0), pg.K_RIGHT: (1, 0)}

get_bin = lambda x, n: format(x, 'b').zfill(n)

def grunddaten(bits = 10) :
    # get_bin = lambda x, n: format(x, 'b').zfill(n)
    # print(get_bin(2 ** 11 - 1, 15))
    di = {}
    for i in range(2**bits):
        s = get_bin(i, bits)
        v = [x for x in s.split('0') if x != '']
        w = ""
        for x in v:      # BitBlöcke erstellen
            w += str(len(x)) + ' '
        w = w.strip()
        if w in di:
            di[w].append(i)
        else:
            di[w] = [i]

        # print(i, s, v, w)
    return di


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
        global spalten_zahl, zeilen_zahl
        r = {}
        self.matrix = {}
        self.spaltenkopf_matrix = {}
        self.zeilenkopf_matrix = {}
        self.spalten = {}
        self.zeilen = {}
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
        spalten_zahl = self.spaltenkopf.__len__()
        zeilen_zahl = self.zeilenkopf.__len__()
        self.baue_kopf_matrix()
        # und die eigentliche Matrix
        for ze in range(zeilen_zahl):
            for sp in range(spalten_zahl):
                 r = (self.ZeiKoB + sp * self.rasterX, self.SpaKoH + ze * self.rasterY,
                      self.rasterX, self.rasterY)
                 self.matrix[sp, ze] = cZelle((sp, ze), '0', r)


    def baue_kopf_matrix(self):
        # Spaltenkopf
        for sp in range(spalten_zahl):
            spl = self.spaltenkopf[sp].split()
            while spl.__len__() < self.spaltenmax:
                spl.insert(0, '')
            for ze in range(self.spaltenmax):
                self.spaltenkopf_matrix[sp, ze] = spl[ze]
                # print(sp, ze, spl[ze], spl)
        # Zeilenkopf
        for sp in range(spalten_zahl):
            spl = self.zeilenkopf[sp].split()
            while spl.__len__() < self.zeilenmax:
                spl.insert(0, '')
            for ze in range(self.zeilenmax):
                self.zeilenkopf_matrix[sp, ze] = spl[ze]
                # print(sp, ze, spl[ze], spl)
        pass



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
    def SpaKoH(self):
        return self.spaltenmax * self.rasterY

    @property
    def SpaKoB(self):
        return spalten_zahl * self.rasterX

    @property
    def ZeiKoB(self):
        return self.zeilenmax * self.rasterX

    @property
    def ZeiKoH(self):
        return zeilen_zahl * self.rasterY

    @property
    def SpaKo0Pos(self):
        return self.ZeiKoB, 0

    @property
    def ZeiKo0Pos(self):
        return 0, self.SpaKoH

    @property
    def Ma0Pos(self):
        return self.ZeiKoB, self.SpaKoH

    @property
    def screen_size(self):
        # raster * zeilen + rand + 400, raster * spalten + rand + 200)
        return self.ZeiKoB + self.SpaKoB + 30, self.SpaKoH + self.ZeiKoH + 50


    @property
    def matrix_rect(self):
        return *self.Ma0Pos, self.SpaKoB, self.ZeiKoH

    @property
    def zeilenkopf_rect(self):
        return *self.ZeiKo0Pos, self.ZeiKoB, self.ZeiKoH

    @property
    def spaltenkopf_rect(self):
        return *self.SpaKo0Pos, self.SpaKoB, self.SpaKoH

    def __str__(self):
        t = f"\nRätsel: Nano\nSpalten: {spalten_zahl}\tZeilen: {zeilen_zahl}\n"
        for zelle in self.matrix.values():
            t += str(zelle.__str__()).replace('\n','\t mögliche Ziele - ') + '\n'
        return t


class cZeileSpalte():

    def __init__(self, nr, orientierung):
        self.nr = nr
        self.ori = orientierung
        self.vorgabe = spiel.zeilenkopf[nr] if orientierung == 'h' else spiel.spaltenkopf[nr]
        self.möglichkeiten = vorgaben[self.vorgabe]

    @property
    def möglich(self):
        bits = zeilen_zahl if self.ori == 'h' else spalten_zahl
        rest = 2**bits - 1
        for sp in self.möglichkeiten:
            rest &= sp
        return rest

    def __str__(self):
        bez = 'Zeile' if self.ori == 'h' else 'Spalte'
        bits = zeilen_zahl if self.ori == 'h' else spalten_zahl
        return f'{bez}: {self.nr} mit den Vorgaben {self.vorgabe}\n' \
               f'\t Möglichkeiten: {self.möglichkeiten}\n' \
               f'\t möglich {self.möglich} = {get_bin(self.möglich, bits)}'


class cZelle():
    """"  """
    def __init__(self, pos, inhalt, z_rect):
        self.pos = pos
        sp, ze = pos
        self.zeichenrechteck = z_rect
        # RGB-Farben für
        self.hintergrundfarbe = (250, 250, 250)
        self.rahmenfarbe = (0, 0, 0)
        self._inhalt = '0'

    def __str__(self):
        return f"\t{self.pos}: {self.hintergrundfarbe}"

    @property
    def inhalt(self):
        return self._inhalt

    @inhalt.setter
    def inhalt(self, neu):
        self._inhalt = neu
        self.hintergrundfarbe = (0, 0, 0) if neu == '1' else (250, 250, 250)


def calc_pos_x(pos):
    sp, ze = pos
    startsp, startze, b, h = spiel.matrix_rect
    return (sp * spiel.rasterX + spiel.rand + startsp, ze * spiel.rasterY + spiel.rand,
            spiel.rasterX, spiel.rasterY)

def calc_pos_y(pos):
    sp, ze = pos
    startsp, startze, b, h = spiel.matrix_rect
    return (ze * spiel.rasterY + spiel.rand , sp * spiel.rasterX + spiel.rand + startze,
            spiel.rasterX, spiel.rasterY)


def zeichne_spiel():
    # Matrix des Rätsels zeichnen
    # spiel.calc_zeichnen()
    pg.draw.rect(screen, 'black', spiel.matrix_rect, 1)
    pg.draw.rect(screen, 'red', spiel.zeilenkopf_rect, 1)
    pg.draw.rect(screen, 'blue', spiel.spaltenkopf_rect, 1)
    for zelle in spiel.spaltenkopf_matrix:
        pos = calc_pos_x(zelle)
        pg.draw.rect(screen, 'black',  pos, 1)
        if spiel.spaltenkopf_matrix[zelle]:
            zeichne_text(spiel.spaltenkopf_matrix[zelle], pos, 'black')
    for zelle in spiel.zeilenkopf_matrix:
        pos = calc_pos_y(zelle)
        pg.draw.rect(screen, 'black', pos, 1)
        if spiel.zeilenkopf_matrix[zelle]:
            zeichne_text(spiel.zeilenkopf_matrix[zelle], pos, 'black')
        pass
    for zelle in spiel.matrix.values():
        pg.draw.rect(screen, zelle.hintergrundfarbe, zelle.zeichenrechteck)
        pg.draw.rect(screen, zelle.rahmenfarbe, zelle.zeichenrechteck, 1)



def zeichne_text(text, pos, farbe):
    x, y, b, h = pos
    font_size = b // 3
    mitte = x + b // 2, y + h // 2

    t = pg.font.SysFont('Arial', font_size).render(text, False, farbe)
    t_rect = t.get_rect(center=mitte)
    screen.blit(t, t_rect)

def zeilen_info():
    for nr in range(spalten_zahl):
        print(spiel.spalten[nr])
        ist = ''
        for ze in range(zeilen_zahl):
            ist += spiel.matrix[nr, ze].inhalt
        print('Ist  \t', ist, int(ist, 2))
        soll = int(ist, 2) | spiel.spalten[nr].möglich
        print('Soll \t', get_bin(soll, 10), soll)
        for ze in range(zeilen_zahl):
            spiel.matrix[nr, ze].inhalt = get_bin(soll, 10)[ze]




if __name__ == '__main__':
    spiel = cDaten('nono.bsp')
    vorgaben = grunddaten(zeilen_zahl)
    for sp in range(spalten_zahl):
        spiel.spalten[sp] = cZeileSpalte(sp, 'v')
    for ze in range(zeilen_zahl):
        spiel.zeilen[ze] = cZeileSpalte(ze, 'h')
    # spiel.matrix[0, 3].inhalt = '1'  # Beispiel
    zeilen_info()
    pg.init()
    screen = pg.display.set_mode(spiel.screen_size)
    pg.display.set_caption("Nanorätsel")
    print(spiel)
    # print(vorgaben)

    weitermachen = True
    clock = pg.time.Clock()
    aktiveZelle = (0, 0)
    # spiel.matrix[0, 3].inhalt = '1'  # Beispiel
    # spiel.matrix[5, 4].inhalt = '1'  # Beispiel
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
