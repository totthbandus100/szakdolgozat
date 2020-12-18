import math

#A kiértékelésekhez végez számításokat
def statisztikus(number_users,values, vegso_etalon_atlaghoz_osszeg, vegso_konszenzus_atlaghoz_osszeg,max_szazalekos_elteres_lefele,max_szazalekos_elteres_felfele,sorrendcsere_szazalekos_elteres,osszes_etalon_Shapley_erteke,osszes_konszenzus_Shapley_erteke):
    #A konszenzusi eredmények összegzése
    osszegek=[]
    for i in range(number_users):
        osszegek.append(0)
    print(values)
    print(osszegek)
    for i in range(1, len(values)):
        for j in range(0,len(values[i])):
            osszegek[j]=osszegek[j]+values[i][j]

    #Konszenzus és etalon összegek kiszámítása a százalékoláshoz
    konszenzusosszeg=0
    for i in osszegek:
        konszenzusosszeg+=i
    etalonosszegek=0

    osszes_etalon_Shapley_erteke.append(values[0])
    seged=[]
    for i in osszegek:
        seged.append(i/len(osszegek))
    osszes_konszenzus_Shapley_erteke.append(seged)

    for i in values[0]:
        etalonosszegek+=i

    #Konszenzusi és etalonos százalékok kiszámítása
    etalonszazalekok=[]
    for i in range(len(values[0])):
        etalonszazalekok.append(values[0][i]*100/etalonosszegek)
        vegso_etalon_atlaghoz_osszeg[i]=vegso_etalon_atlaghoz_osszeg[i]+values[0][i]

    konszenzusszazalekok=[]
    for i in range(len(osszegek)):
        if(konszenzusosszeg) ==0:
            konszenzusszazalekok.append(0)
        else:
            konszenzusszazalekok.append(osszegek[i]*100/konszenzusosszeg)
        vegso_konszenzus_atlaghoz_osszeg[i]=vegso_konszenzus_atlaghoz_osszeg[i]+osszegek[i]



    #A konszenzusi és az etalonos százalékok összehasonlítása
    szazalakelteresek=[]
    for i in range(0,len(konszenzusszazalekok)):
        elteres=etalonszazalekok[i]-konszenzusszazalekok[i]
        szazalakelteresek.append(elteres)
        if elteres <0 and abs(elteres) > max_szazalekos_elteres_lefele:
            max_szazalekos_elteres_lefele=abs(elteres)
        if elteres >0 and elteres > max_szazalekos_elteres_felfele:
            max_szazalekos_elteres_felfele=elteres



    #Sorrendcserék detektálása és a százalékos eltérések összeadása
    for i in range(0, len(konszenzusszazalekok)):
        for j in range(i+1, len(konszenzusszazalekok)):
            if konszenzusszazalekok[i]<konszenzusszazalekok[j] and etalonszazalekok[i]> etalonszazalekok[j]:
                sorrendcsere_szazalekos_elteres.append(abs(szazalakelteresek[i])+abs(szazalakelteresek[j]))


    return max_szazalekos_elteres_lefele, max_szazalekos_elteres_felfele


def kiertekelo(number_users):
    fp=open('eredmenyek.txt','r')
    line=fp.readline()
    values=[]
    max_szazalekos_elteres_lefele=0
    max_szazalekos_elteres_felfele=0
    vegso_etalon_atlaghoz_osszeg=[]
    vegso_konszenzus_atlaghoz_osszeg=[]
    vegso_etalon_atlag=[]
    vegso_konszenzus_atlag=[]
    for i in range(number_users):
        vegso_etalon_atlaghoz_osszeg.append(0)
        vegso_konszenzus_atlaghoz_osszeg.append(0)
        vegso_etalon_atlag.append(0)
        vegso_konszenzus_atlag.append(0)
    sorrendcsere_szazalekos_elteres=[]
    osszes_etalon_Shapley_erteke=[]
    osszes_konszenzus_Shapley_erteke=[]
    futasokszama=0


    #Adatok beolvasása
    while line!="":
        if line=="\n":
            #Az egyes futások eredménye enterrel van elválasztva, ha entert talál, az éppen beolvasott eredményeket hozzáadja a meglévőkhöz
            max_szazalekos_elteres_lefele, max_szazalekos_elteres_felfele=statisztikus(number_users,values,vegso_etalon_atlaghoz_osszeg,vegso_konszenzus_atlaghoz_osszeg, max_szazalekos_elteres_lefele,max_szazalekos_elteres_felfele, sorrendcsere_szazalekos_elteres,osszes_etalon_Shapley_erteke,osszes_konszenzus_Shapley_erteke)
            futasokszama+=1
            values=[]
            line=fp.readline()
            continue

        split_line=line.split(" = ")
        ezasor=[]
        for i in split_line[1].split(' '):
            if i!='\n':
                ezasor.append(float(i))
        values.append(ezasor)
        line=fp.readline()

    fp.close()

    #Az eredmények átlagolása
    for i in range(len(vegso_konszenzus_atlaghoz_osszeg)):
        vegso_konszenzus_atlag[i]=vegso_konszenzus_atlaghoz_osszeg[i]/futasokszama/len(vegso_konszenzus_atlaghoz_osszeg)
        vegso_etalon_atlag[i]=vegso_etalon_atlaghoz_osszeg[i]/futasokszama

    #Százalékos eltérések kiszámolása
    vegso_szazalekos_elteresek=[]
    if(sum(vegso_konszenzus_atlag)!=0 and sum(vegso_etalon_atlag!=0)):
        for i in range(0,len(vegso_konszenzus_atlag)):
            vegso_szazalekos_elteresek.append(100*(vegso_etalon_atlag[i]/sum(vegso_etalon_atlag)-vegso_konszenzus_atlag[i]/sum(vegso_konszenzus_atlag)))

    etalon_szazalekok=[]
    konszenzus_szazalekok=[]
    if(sum(vegso_konszenzus_atlag)!=0 and sum(vegso_etalon_atlag!=0)):
        for i in range(len(vegso_konszenzus_atlag)):
            etalon_szazalekok.append(100*vegso_etalon_atlag[i]/sum(vegso_etalon_atlag))
            konszenzus_szazalekok.append(100*vegso_konszenzus_atlag[i]/sum(vegso_konszenzus_atlag))

    #Eredmények kiírása
    print("ETALON SZAZALEKOK")
    print(etalon_szazalekok)
    print("KONSZENZSU SZAZALEKOK")
    print(konszenzus_szazalekok)
    print("VEGSO SZAZALEKOS ELTERES")
    print(vegso_szazalekos_elteresek)
    print("SORRENDVALTOZAS DB")
    print(len(sorrendcsere_szazalekos_elteres))
    if len(sorrendcsere_szazalekos_elteres)!=0:
        print("SORRENVALTOZAS ATLAG ELTERES")
        print(sum(sorrendcsere_szazalekos_elteres)/len(sorrendcsere_szazalekos_elteres))
        print("LEGNAGYOBB ELTERES SORREND VALTOZASNAL")
        print(max(sorrendcsere_szazalekos_elteres))
    print("MAX SZAZALEKOS ELTERES LEFELE")
    print(max_szazalekos_elteres_lefele)
    print("MAX SZAZALEKOS ELTERES FELFELE")
    print(max_szazalekos_elteres_felfele)


    #Fileokba kiírja hogy körönként a könszenzus és az etalon miket gondoltak a résztvevőkről.
    open('etalon010145.txt',"w").close()
    etalon_file=open('etalon010145.txt',"w")
    open('konszenzus010145.txt',"w").close()
    konszenzus_file=open('konszenzus010145.txt',"w")
    for i in range(len(osszes_konszenzus_Shapley_erteke)):
        osszkonszenzus=sum(osszes_konszenzus_Shapley_erteke[i])
        osszetalon=sum(osszes_etalon_Shapley_erteke[i])
        for j in range(len(osszes_konszenzus_Shapley_erteke[0])):
            if osszetalon!=0:
                etalon_file.write(str(100*osszes_etalon_Shapley_erteke[i][j]/osszetalon))
            else:
                etalon_file.write('0')
            etalon_file.write('\t')
            if osszkonszenzus!=0:
                konszenzus_file.write(str(100*osszes_konszenzus_Shapley_erteke[i][j]/osszkonszenzus))
            else:
                konszenzus_file.write('0')
            konszenzus_file.write('\t')
        konszenzus_file.write('\n')
        etalon_file.write('\n')
    konszenzus_file.close()
    etalon_file.close()
    print()
