import math
from callshaples import call_shapleys


#Felnyitja az összes szétválasztott teszt eredményeket tartalmazó filet és a benne található eredményeket a binárisok szerint átlagolja
#Majd az átlagolt értékekre meghívja a shapley értékszámolót
def atlagolo(path, number, kornumber):
    for i in range(number):
        file_path=path+str(i)+".txt"
        fp=open(file_path, 'r')
        line=fp.readline()
        binaries=[]
        values = []
        count=0
        while line!="":
            split_line=line.split('=')
            if split_line[0] in binaries:
                index = binaries.index(split_line[0])

                values[index]=[values[index][0]+float(split_line[1])]

            else:
                binaries.append(split_line[0])


                values.append([float(split_line[1])])

            line=fp.readline()

        fp.close()
        for j in range(len(values)):

            values[j]=[values[j][0]/kornumber]

        last_binary=""
        for k in range(int(math.log(len(values)+1,2))):
            last_binary+="1"
            last_binary+=" "
        binaries.append(last_binary)
        values.append([0])

        ki_path='atlagolt/tocalculateshapley'+str(i)+".txt"
        open(ki_path,"w").close()
        f=open(ki_path,"w")
        for i in range(len(values)):
            f.write(binaries[i])
            f.write("= ")
            f.write("0 ")
            f.write(str(values[i][0]))

            f.write("\n")
        f.close()
    #Shapley érték számítások meghívásai
    call_shapleys(number)

