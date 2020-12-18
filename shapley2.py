from numpy import double
import math



def osszegez(adatok,hanyadiknaklepbe, melyiket):
    osszeg=0;
    for i in adatok:

        if i[0][melyiket]==0 and i[2]==hanyadiknaklepbe:
            ellentett=ellentettErteke(adatok,i,melyiket)
            if ellentett == None:
                ellentett=[[1,1],[0],0]


            hozzaadni=i[1][melyiket]-ellentett[1][melyiket]

            osszeg+=hozzaadni
    return osszeg



def hanyelem(binaris):
    x=0
    for i in binaris:
        if i==0:
            x+=1
    return x

def szorzo(n,k):
    x=1
    x*=math.factorial(k-1)
    x*=math.factorial(n-k)
    x/=math.factorial(n)
    return x

def osszehasonlito(mit, mivel, hanyadikbanelteres):
    if mit[hanyadikbanelteres]==mivel[hanyadikbanelteres]:
        return False
    for i in range(0,len(mit)):
        if i==hanyadikbanelteres:
            continue
        if mit[i]!=mivel[i]:
            return False
    return True

def ellentettErteke(adatok, minek,hanyadikelem):
    for i in adatok:
        if osszehasonlito(i[0],minek[0],hanyadikelem):
            return i

def main(eredmenyek_path, out_path,number_users , label):
    melyiket=0
    adatok=[]
    ossz=0
    fp=open(eredmenyek_path,"r")
    line="1"

    f=open(out_path,'a')
    f.write(label)
    f.write("= ")

    while line!="":
        line=fp.readline()
        line1=line.split('=')

        x=[]
        for j in range(0,len(line1)):
            line1[j]=line1[j].split(' ')
            for i in line1[j]:
                if i !=' ' and i !='':

                    x.append(double(i))
            line1[j]=[]

            line1[j]+=x
            x.clear()
        x.clear()
        if len(line1)>1:
            adatok.append(line1)

    for i in adatok:
        suly=0
        for j in i[0]:
            if j==0:
                suly+=1
        i.append(suly)


    for i in range(0,number_users):
        shapley=0
        for hanyadiknaklepbe in range(1,number_users+1):
            osszeg=osszegez(adatok, hanyadiknaklepbe, melyiket)
            shapley+=szorzo(number_users,hanyadiknaklepbe)*osszeg
        f.write("{:.3f}".format(shapley))
        f.write(" ")

        ossz+=shapley

    f.write('\n')
    f.close()
    fp.close()
