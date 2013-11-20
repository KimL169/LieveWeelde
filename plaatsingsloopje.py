        huizen = []

        Hvariant = TwintigH()
        for i in range(1, Hvariant.eengezins):
            name =  "e%d" % (i)
            e = Eengezin()
            e.name(name)
            e.render(x, y)
            #append de huizen in een list
            huizen.append(e)
        for i in range(1, Hvariant.bungalow):
            name = "b%d" % (i)
            b = Bungalow()
            b.name(name)
            b.render(x, y)
            #append de huizen in een list
            huizen.append(b)
        for i in range(1, Hvariant.maison):
            name= "m%d" % (i)
            m = Maison()
            m.name(name)
            m.render(x, y)
            #append de huizen in een list
            huizen.append(m)
    
    


'''
        # Loop voor het plaatsen van huizen
        # Komt straks in plaats van de handmatige plaatsing die er nu nog staat
        # voor de x en y coordinaten in 'render(x, y)'  moet een functie komen die een random x en y produceert maar zorgt dat ze niet overlappen.
    #list voor om de huisjes in te appenden.
    huizen = []

    Hvariant = TwintigH()
    for i in range(1, Hvariant.eengezins):
        name =  "e%d" % (i)
        e = Eengezin()
        e.name(name)
        e.render(x, y)
        #append de huizen in een list
        huizen.append(e)
    for i in range(1, Hvariant.bungalow):
        name = "b%d" % (i)
        b = Bungalow()
        b.name(name)
        b.render(x, y)
        #append de huizen in een list
        huizen.append(b)
    for i in range(1, Hvariant.maison):
        name= "m%d" % (i)
        m = Maison()
        m.name(name)
        m.render(x, y)
        #append de huizen in een list
        huizen.append(m)
    x+=movex
y+=movey

'''
