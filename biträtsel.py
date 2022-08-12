import pygame as pg
from time import perf_counter as pfc

spalten_zahl = zeilen_zahl = 0
alle_vorgaben = []
richtungen = {pg.K_DOWN: (0, 1), pg.K_UP: (0, -1), pg.K_LEFT: (-1, 0), pg.K_RIGHT: (1, 0)}

get_bin = lambda x, n: format(x, 'b').zfill(n)
get_invert = lambda x: (2**zeilen_zahl - 1) ^ x

def bitblöcke(bits = 10) :
    # get_bin = lambda x, n: format(x, 'b').zfill(n)
    # print(get_bin(2 ** 11 - 1, 15))
    di = {}
    di['0'] = [0]
    for i in range(2**bits):
        s = get_bin(i, bits)
        v = [x for x in s.split('0') if x != '']
        w = ""
        for x in v:      # BitBlöcke erstellen
            w += str(len(x)) + ' '
        w = w.strip()
        # if w in alle_vorgaben:
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
    global alle_vorgaben
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
        """ die max. Anzahl von Vorgaben, für die Berechnung der Kopfhöhe/breite """
        self.spaltenmax = max_anzahl_einträge(self.spaltenkopf)
        self.zeilenmax = max_anzahl_einträge(self.zeilenkopf)
        spalten_zahl = self.spaltenkopf.__len__()
        zeilen_zahl = self.zeilenkopf.__len__()
        # alle_vorgaben = [] - gobal
        for sp in self.spaltenkopf:
            if sp not in alle_vorgaben:
                alle_vorgaben.append(sp)
        for sp in self.zeilenkopf:
            if sp not in alle_vorgaben:
                alle_vorgaben.append(sp)


        self.baue_kopf_matrix()

        # und die eigentliche Matrix
        for ze in range(zeilen_zahl):
            for sp in range(spalten_zahl):
                 r = (self.ZeiKoB + sp * self.rasterX, self.SpaKoH + ze * self.rasterY,
                      self.rasterX, self.rasterY)
                 self.matrix[sp, ze] = cZelle((sp, ze), '0', r)
        self.status = 0     # Schleifenzähler für Lösungen
        self.status_max = spalten_zahl + zeilen_zahl - 1

    def nächste_spalte_zeile(self):
        spze = self.spalten[self.status].löse_spalte_zeile() if self.status in range(spalten_zahl) else \
            self.zeilen[self.status - spalten_zahl].löse_spalte_zeile()
        self.status += 1
        if self.status > self.status_max:
            self.status = 0
        print(f'Statuszähler: {self.status} max = {self.status_max}')



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
        for sp in range(zeilen_zahl):
            spl = self.zeilenkopf[sp].split()
            while spl.__len__() < self.zeilenmax:
                spl.insert(0, '')
            for ze in range(self.zeilenmax):
                self.zeilenkopf_matrix[sp, ze] = spl[ze]
                # print(sp, ze, spl[ze], spl)
        pass



    @property
    def anzahl_möglichkeiten(self):
        zahl = 0
        for i in range(zeilen_zahl):
            zahl += self.zeilen[i].möglichkeiten.__len__() - 1
        for i in range(spalten_zahl):
            zahl += self.spalten[i].möglichkeiten.__len__() - 1
        return zahl



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



class cZeileSpalte():

    def __init__(self, nr, orientierung):
        self.nr = nr
        self.ori = orientierung
        self.vorgabe = spiel.zeilenkopf[nr] if orientierung == 'h' else spiel.spaltenkopf[nr]
        self.möglichkeiten = vorgaben[self.vorgabe]

    @property
    def is_zeile(self):
        return self.ori == 'h'

    @property
    def möglich(self):
        bits = zeilen_zahl if self.is_zeile else spalten_zahl
        rest = 2**bits - 1
        for sp in self.möglichkeiten:
            rest &= sp
        return rest

    def zeilen_alt(self):
        ist = ''
        null = ''
        for sp in range(spalten_zahl):
            ist += spiel.matrix[sp, self.nr].inhalt
            null += spiel.matrix[sp, self.nr].null
        return ist, null

    def spalten_alt(self):
        ist = ''
        null = ''
        for ze in range(zeilen_zahl):
            ist += spiel.matrix[self.nr, ze].inhalt
            null += spiel.matrix[self.nr, ze].null
        return ist, null

    def zeilen_neu(self, neu, null):
        neu = get_bin(neu, spalten_zahl)
        for sp in range(spalten_zahl):
            spiel.matrix[sp, self.nr].inhalt = neu[sp]
            print(sp, self.nr, neu, null[sp], null)
            if null[sp] == '1':
                spiel.matrix[sp, self.nr].null = '1'
        return True

    def spalten_neu(self, neu, null):
        neu = get_bin(neu, zeilen_zahl)
        for ze in range(zeilen_zahl):
            spiel.matrix[self.nr, ze].inhalt = neu[ze]
            if null[ze] == '1':
                spiel.matrix[self.nr, ze].null = '1'
        return True

    def löse_spalte_zeile(self):
        print(self)
        ist, nullzellen = self.zeilen_alt() if self.is_zeile else self.spalten_alt()
        print(f'Ist  \t{ist}\t{int(ist, 2)} und Leerzellen: {nullzellen}')
        n = []   # temporäre möglichkeiten
        i = 2**zeilen_zahl - 1
        for m in self.möglichkeiten:
            print(self.nr, m, int(nullzellen, 2), m & int(nullzellen, 2))
            if m & int(ist,2) == int(ist, 2) and not(m & int(nullzellen, 2)):
                i &= get_invert(m)
                n.append(m)
        i
        print(f'\talt: {self.möglichkeiten} \n\tneu: {n}\n\toder\t{i} - {get_bin(i, 10)} - {get_bin(get_invert(i),10)}')
        self.möglichkeiten = n
        soll = int(ist, 2) | self.möglich
        i |= int(nullzellen, 2)
        print('Soll\t', get_bin(soll, 10), soll)
        jetzt = self.zeilen_neu(soll, get_bin(i, zeilen_zahl)) if self.is_zeile else self.spalten_neu(soll, get_bin(i, spalten_zahl))
        print(self)

    def __str__(self):
        bez = 'Zeile' if self.ori == 'h' else 'Spalte'
        bits = zeilen_zahl if self.ori == 'h' else spalten_zahl
        s = ''
        for x, m in enumerate(self.möglichkeiten):
            s += f'\t\tNr{x} - {m} - {get_bin(m,10)} - not - {get_bin(m ^ (2**10-1),10)}\n'
        return f'{bez}: {self.nr} mit den Vorgaben {self.vorgabe}\n' \
               f'\t Möglichkeiten: {self.möglichkeiten}\n{s}' \
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
        self._null = '0'

    def __str__(self):
        return f"\t{self.pos}: {self.hintergrundfarbe}"

    @property
    def inhalt(self):
        return self._inhalt

    @inhalt.setter
    def inhalt(self, neu):
        self._inhalt = neu
        self.hintergrundfarbe = (0, 0, 0) if neu == '1' else (250, 250, 250)

    @property
    def null(self):
        return self._null

    @null.setter
    def null(self, neu):
        self._null = neu
        self.hintergrundfarbe = (180, 180, 180) if neu == '1' else self.hintergrundfarbe



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
        # print(zelle)
        pg.draw.rect(screen, zelle.hintergrundfarbe, zelle.zeichenrechteck)
        pg.draw.rect(screen, zelle.rahmenfarbe, zelle.zeichenrechteck, 1)


def zeichne_text(text, pos, farbe):
    x, y, b, h = pos
    font_size = b // 3
    mitte = x + b // 2, y + h // 2

    t = pg.font.SysFont('Arial', font_size).render(text, False, farbe)
    t_rect = t.get_rect(center=mitte)
    screen.blit(t, t_rect)




if __name__ == '__main__':
    spiel = cDaten('nono.bsp')
    start = pfc()
    vorgaben = bitblöcke(max(zeilen_zahl, spalten_zahl))
    print(f'Dauer : {pfc() - start}')
    for sp in range(spalten_zahl):
        spiel.spalten[sp] = cZeileSpalte(sp, 'v')
    for ze in range(zeilen_zahl):
        spiel.zeilen[ze] = cZeileSpalte(ze, 'h')
    print(f'Ausawahlmöglichkeiten: {spiel.anzahl_möglichkeiten}')

    pg.init()
    screen = pg.display.set_mode(spiel.screen_size)
    pg.display.set_caption("Nanorätsel")
    print(spiel)
    # print(vorgaben)

    weitermachen = True
    automatik = False
    clock = pg.time.Clock()
    # aktiveZelle = (0, 0)
    # spiel.matrix[0, 3].inhalt = '1'  # Beispiel
    # spiel.matrix[5, 4].inhalt = '1'  # Beispiel
    while weitermachen:
        clock.tick(40)
        if automatik:
            if spiel.anzahl_möglichkeiten:
                spiel.nächste_spalte_zeile()
            else:
                automatik = False

        for ereignis in pg.event.get():
            if ereignis.type == pg.QUIT:
                weitermachen = False
            elif ereignis.type == pg.KEYDOWN: # and ereignis.key in richtungen:
                if ereignis.key == pg.K_n:
                    print('n Taste gedrückt')
                    spiel.nächste_spalte_zeile()
                elif ereignis.key == pg.K_a:
                    automatik = True
                elif ereignis.key == pg.K_s:
                    for s in range(spalten_zahl):
                        spiel.spalten[s].löse_spalte_zeile()
                elif ereignis.key == pg.K_z:
                    for z in range(zeilen_zahl):
                        spiel.zeilen[z].löse_spalte_zeile()
                elif ereignis.key == pg.K_1:
                    spiel.spalten[1].löse_spalte_zeile()
                    spiel.zeilen[1].löse_spalte_zeile()
                    pass
                elif ereignis.key == pg.K_2:
                    spiel.spalten[2].löse_spalte_zeile()
                    spiel.zeilen[2].löse_spalte_zeile()
                    pass
                elif ereignis.key == pg.K_0:
                    spiel.spalten[0].löse_spalte_zeile()
                    spiel.zeilen[0].löse_spalte_zeile()
                print(f'Ausawahlmöglichkeiten: {spiel.anzahl_möglichkeiten}')

            elif ereignis.type == pg.MOUSEBUTTONDOWN:
                (x1, y1) = pg.mouse.get_pos()
                b1, b2, b3 = pg.mouse.get_pressed()  # welche Maustaste
                # print(b1, b2, b3)
                # sp, ze = x1 // test.rasterX, y1 // test.rasterY
                """if (sp, ze) in test.matrix:
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
                            # ziele = test.matrix[aktiveZelle].ziele
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
"""
            # elif ereignis.type == pg.MOUSEMOTION:
                # print('mausbewegung', pg.mouse.get_pos())

        screen.fill((180,180,190))
        zeichne_spiel()

        pg.display.flip()

    pg.quit()
