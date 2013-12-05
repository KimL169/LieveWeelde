def verdeelVrijstand(vrijstand):
    m = Maison()
    e = Eengezins()
    b = Bungalow()
    Mvrijstand = 0
    Bvrijstand = 0
    Evrijstand = 0
    total = 0

    while True:

        if total == vrijstand:
            print "\nMaison: %d\n Bungalow: %d\n Eengezins:%d\n" % (Mvrijstand, Bvrijstand, Evrijstand)
            return

        MvrijstandNew = (Mvrijstand + 1)
        Mold = float(m.waarde + (((Mvrijstand)- (m.verplichte_vrijstand/4)) * (m.waarde * 0.06)))
        Mnew = float(m.waarde + (((MvrijstandNew/4) - (m.verplichte_vrijstand/4)) * (m.waarde * 0.06)))
        Mextra = Mnew - Mold

        BvrijstandNew = (Bvrijstand + 1)
        Bold = float(b.waarde + (((Bvrijstand/4) - (b.verplichte_vrijstand/4)) * (b.waarde * 0.04)))
        Bnew = float(b.waarde + (((BvrijstandNew/4) - (b.verplichte_vrijstand/4)) * (b.waarde * 0.04)))
        Bextra = Bnew - Bold

        EvrijstandNew = (Evrijstand + 1)
        Eold = float(e.waarde + (((Evrijstand/4) - (e.verplichte_vrijstand/4)) * (e.waarde * 0.03)))
        Enew = float(e.waarde + (((EvrijstandNew/4) - (e.verplichte_vrijstand/4)) * (e.waarde * 0.03)))
        Eextra = Enew - Eold

        if Mextra >= Bextra and Mextra >= Eextra:
            Mvrijstand += 1
        elif Bextra >= Mextra and Bextra >= Eextra:
            Bvrijstand += 1
        elif Eextra >= Mextra and Eextra >= Bextra: 
            Evrijstand += 1

        total = Mvrijstand + Bvrijstand + Evrijstand

