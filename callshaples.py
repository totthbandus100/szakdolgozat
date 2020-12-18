import shapley2


def numberToBinary(number):
    x=[]
    a="{0:b}".format(number)
    for j in a:
        x.append(int(j))
    for j in range(len(x),5):
        x.insert(0,0)
    return x


def call_shapleys(maxnumber):

    
    #Minden átlagolt filera külön meghívja a Shapley számítást
    for i in range(maxnumber):
        data_path="eredmenyek/szetvalasztott"+str(i)+".txt"
        label=""
        for j in numberToBinary(i):
            label+=str(j)+" "
        shapley2.main(data_path, 'eredmenyek.txt',5,label)
    f=open('eredmenyek.txt','a')
    f.write('\n')
    f.close()


