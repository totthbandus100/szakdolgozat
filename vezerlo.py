import os
import sys
import federated_main
import szetvalaszto





dbteszt=15
resztvevokszama=5

def numberToBinary(number):
    x=[]
    a="{0:b}".format(number)
    for j in a:
        x.append(int(j))
    for j in range(len(x),resztvevokszama):
        x.insert(0,0)
    return x

def main():
    #Töröljük az előző teszt kimeneteit majd beállítjuk, hogy minden oda íródjon ki a konzol helyett
    open('kimenet.txt', 'w').close()
    sys.stdout=open('kimenet.txt','w')

    #Hány kísérletet akarunk végezni
    for tesztekszama in range(0,dbteszt):

        #Az összes tanítási koalíció előállítása
        for i in range(0,(2**resztvevokszama)-1):
            print("KORKEZDETE")
            print(numberToBinary(i))
            print("TRAIN NUMBER")
            print(i)
            #Megnézzük, hogy az adott tesztben kik vesznek részt, majd kiírjuk a résztvevők fileba binárisan (0 résztvesz, 1 nem vesz részt)
            open('resztvevok.txt', 'w').close()
            f = open('resztvevok.txt', "w")
            for i in numberToBinary(i):
                f.write(str(i))
                f.write(' ')
            f.close()
            #Meghívjuk a tanítást
            federated_main.main()
        print("KOR VEGE")
        print(tesztekszama)
    print("VEGE")

    open('kiertekeles.txt', 'w').close()
    sys.stdout=open('kiertekeles.txt','w')
    #Szétválasztja a teszt eredményeket, majd a szétválasztottakon meghívja az átlagolást, a Shapley érték számítást és a statisztikai kiértékelőt
    szetvalaszto.main('kimenet.txt','eredmenyek/szetvalasztott',(2**resztvevokszama)-1,"VEGE\n",resztvevokszama)


if __name__ == "__main__":

    main()

