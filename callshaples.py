import shapley2


def numberToBinary(number, lenght):
    x=[]
    a="{0:b}".format(number)
    for j in a:
        x.append(int(j))
    for j in range(len(x),lenght):
        x.insert(0,0)
    return x


def call_shapleys(number_users):
    #Törli az eddigi eredményeket
    open('eredmenyek.txt', 'w').close()
    #Minden átlagolt filera külön meghívja a Shapley számítást
    for i in range(2**number_users-1):
        data_path="eredmenyek/szetvalasztott"+str(i)+".txt"
        label=""
        for j in numberToBinary(i,number_users):
            label+=str(j)+" "
        shapley2.main(data_path, 'eredmenyek.txt',number_users,label)
    f=open('eredmenyek.txt','a')
    f.write('\n')
    f.close()


