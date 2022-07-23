spalten = zeilen = 0
sprungmatrix = [(-2,-1), (-2,1), (-1,2), (1,2),(2,1), (2,-1), (-1,-2), (1,-2)]
aktiveZelle = (0, 0)

class cRätsel():

    def __init__(self, datei):
        """
        :param datei: Dateiname incl. eventuell notwendigem Pfad
        ließt die Datei ein und erstellt daraus ein Dict für Zellenobjekte
        """
        global spalten, zeilen
        r = {}
        self.rätsel = {}
        with open(datei, encoding="utf-8") as f:
            ra = [x for x in f.read().split('\n')]
            zeilen = ra.__len__()
            spalten = ra[0].split().__len__()
            # Koordinaten, Text-Fragmente ermitteln
            r = {(z, s): ra[s].split()[z] for s in range(zeilen) for z in range(spalten)}
        # und entsprechende Objekte generieren
        for z in r:
            self.rätsel[z] = cZelle(z, r[z])
        # originale sprungliste in die Objekte generieren
        self.original_sprungliste()

    def __str__(self):
        t = f"\nRätsel: Rösselsprung\nSpalten: {spalten}\tZeilen: {zeilen}\n"
        for zelle in self.rätsel.values():
            t += str(zelle.__str__()).replace('\n','\t mögliche Ziele - ') + '\n'
        return t


    def original_sprungliste(self):
        """ alle möglichen Rösselsprünge als potentielles Ziel eintragen """
        for zelle in self.rätsel:
            for delta in sprungmatrix:
                ziel = (zelle[0] +  delta[0], zelle[1] +  delta[1])
                if ziel in self.rätsel and self.rätsel[ziel].text != '*':
                    self.rätsel[zelle].ziele.append(ziel)
            if ziel in self.rätsel:
                # print(self.rätsel[zelle])
                pass




class cZelle():

    def __init__(self, pos, inhalt):
        self.pos = pos
        self.inhalt = inhalt
        self.text = inhalt
        self.space = ' '
        self.ziele = []

    def __str__(self):
        return f"\t{self.pos}: {str('-' + self.text + self.space + '-').ljust(7)}\n\t{self.ziele}"

    def toggle_space(self):
        if self.space == '':
            self.space = ' '
        else:
            self.space = ''


    def mein_ziel(self, pos):
        if pos in self.ziele:
            pass
        # else:
            # raise ValueError('gewähltes Ziel ist ungültig')


if __name__ == '__main__':
    test = cRätsel('roesselsprung-015.bsp')
    print(test)
    zelle = test.rätsel[(3, 4)]
    aZ = test.rätsel[(5, 5)]
    aZ.mein_ziel((3, 4))