import os
import sys


def numberToBinary(number, lenght):
    x=[]
    a="{0:b}".format(number)
    for j in a:
        x.append(int(j))
    for j in range(len(x),lenght):
        x.insert(0,0)
    return x

def main(data_path, outputname, maxnumber, vege, number_users):

    out_path=outputname+".txt"
    open(out_path, 'w').close()
    fp = open(data_path, 'r')
    line=fp.readline()
    train_number=0
    test_number=0
    change=False
    db=0
    while line!=vege:


        if line=="TEST NUMBER\n":
            test_number=fp.readline()

        if line== "TRAIN NUMBER\n":
            train_number=fp.readline()

        if line=="Test Accuracy\n":
            test_auc=fp.readline()

            binary_train=numberToBinary(int(train_number),number_users)
            binary_test=numberToBinary(int(test_number),number_users)
            db+=1
            f=open(out_path,'a')
            f.write("train binary= ")
            for i in binary_train:
                f.write(str(i))
                f.write(' ')
            f.write("test binary= ")
            for i in binary_test:
                f.write(str(i))
                f.write(' ')
            f.write('=')
            f.write(' ')
            f.write(test_auc.replace("%\n",""))
            f.write('\n')

            f.close()
        line=fp.readline()
    fp.close()

if __name__ == '__main__':
    main('kimenet0101010101.txt','eredmenyek0101010101',30,"VEGE\n",5)



