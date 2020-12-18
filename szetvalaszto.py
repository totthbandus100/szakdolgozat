import os
import sys
import os.path
from os import path
from atlagolo import atlagolo
from kiertekelo import kiertekelo
import threading
import time

def numberToBinary(number, lenght):
    x=[]
    a="{0:b}".format(number)
    for j in a:
        x.append(int(j))
    for j in range(len(x),lenght):
        x.insert(0,0)
    return x

def main(data_path, outputname, maxnumber, vege, number_users, korokszama):
    #Törli az előző eredményeket

    for i in range(maxnumber+1):
        out_path=outputname+str(i)+".txt"
        open(out_path, 'w').close()

    #Elkezdi olvasni a kimenetek filet
    fp = open(data_path, 'r')
    line=fp.readline()
    train_number=0
    test_number=0
    change=False
    db=0
    while line!=vege:
        #Beolvassa a teszthez tartozó adatokat
        if line=="TEST NUMBER\n":
            test_number=fp.readline()

        if line== "TRAIN NUMBER\n":
            train_number=fp.readline()
        #Kiírja a teszt eredményét a megfelelő fileba
        if line=="Test Accuracy\n":
            test_auc=fp.readline()

            out_path=outputname+str(int(test_number))+".txt"

            binary=numberToBinary(int(train_number),number_users)
            db+=1
            f=open(out_path,'a')
            for i in binary:
                f.write(str(i))
                f.write(' ')
            f.write('=')
            f.write(' ')
            f.write(test_auc.replace("%\n",""))
            f.write('\n')

            f.close()
        line=fp.readline()
    fp.close()

    #Átlagolja a teszt eredményeket, az átlagoló meghívja a shapley érték számításokat
    atlagolo(outputname,number_users,korokszama)


    #Statisztikai kiértékelő meghívása
    #kiertekelo(number_users)




