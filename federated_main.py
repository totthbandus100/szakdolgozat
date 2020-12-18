#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python version: 3.6


import os
import copy
import time
import pickle
import numpy as np
from tqdm import tqdm
from random import randint

import torch
from tensorboardX import SummaryWriter

from options import args_parser
from update import LocalUpdate, test_inference
from models import MLP, CNNMnist, CNNFashion_Mnist, CNNCifar
from utils import get_dataset, average_weights, exp_details


def numberToBinary(number, lenght):
    x=[]
    a="{0:b}".format(number)
    for j in a:
        x.append(int(j))
    for j in range(len(x),lenght):
        x.insert(0,0)
    return x

def main():
    start_time = time.time()

    # define paths
    path_project = os.path.abspath('..')
    logger = SummaryWriter('../logs')

    args = args_parser()
    exp_details(args)

    if args.gpu:
        torch.cuda.set_device(0)
    device = 'cuda' if args.gpu else 'cpu'

    # load dataset and user groups
    train_dataset, test_dataset, user_groups = get_dataset(args)

    args.num_users=len(user_groups)

    # BUILD MODEL
    if args.model == 'cnn':
        # Convolutional neural netork
        if args.dataset == 'mnist':
            global_model = CNNMnist(args=args)
        elif args.dataset == 'fmnist':
            global_model = CNNFashion_Mnist(args=args)
        elif args.dataset == 'cifar':
            global_model = CNNCifar(args=args)

    elif args.model == 'mlp':
        # Multi-layer preceptron
        img_size = train_dataset[0][0].shape
        len_in = 1
        for x in img_size:
            len_in *= x
            global_model = MLP(dim_in=len_in, dim_hidden=64,
                               dim_out=args.num_classes)
    else:
        exit('Error: unrecognized model')


    # Set the model to train and send it to device.
    global_model.to(device)
    global_model.train()

    # copy weights
    global_weights = global_model.state_dict()

    # Training
    train_loss, train_accuracy = [], []
    val_acc_list, net_list = [], []
    cv_loss, cv_acc = [], []
    print_every = 2
    val_loss_pre, counter = 0, 0

    #Beolvassuk, hogy éppen mely résztvevők vesznek részt a tanításban (0 jelentése, hogy benne van, 1 az hogy nincs)
    resztvevok=[]
    fp=open('resztvevok.txt',"r")
    x=fp.readline().split(' ')
    for i in x:
        if i !='':
            resztvevok.append(int(i))
    fp.close()


    #for epoch in tqdm(range(args.epochs)):
    for epoch in range(args.epochs):
        local_weights, local_losses = [], []
        #print(f'\n | Global Training Round : {epoch+1} |\n')


        global_model.train()
        m = max(int(args.frac * args.num_users), 1)
        idxs_users = np.random.choice(range(args.num_users), m, replace=False)




        for idx in idxs_users:
            local_model = LocalUpdate(args=args, dataset=train_dataset,idxs=user_groups[idx], logger=logger)
            w, loss = local_model.update_weights(model=copy.deepcopy(global_model), global_round=epoch)
            local_weights.append(copy.deepcopy(w))
            local_losses.append(copy.deepcopy(loss))


        global_weights = average_weights(local_weights)

            # update global weights
        global_model.load_state_dict(global_weights)

        loss_avg = sum(local_losses) / len(local_losses)
        train_loss.append(loss_avg)

            # Calculate avg training accuracy over all users at every epoch
        list_acc, list_loss = [], []
        global_model.eval()
        for c in range(args.num_users):
            local_model = LocalUpdate(args=args, dataset=train_dataset,idxs=user_groups[idx], logger=logger)
            acc, loss = local_model.inference(model=global_model)
            list_acc.append(acc)
            list_loss.append(loss)
        train_accuracy.append(sum(list_acc)/len(list_acc))

            # print global training loss after every 'i' rounds
        '''if (epoch+1) % print_every == 0:
            print(f' \nAvg Training Stats after {epoch+1} global rounds:')
            print(f'Training Loss : {np.mean(np.array(train_loss))}')
            print('Train Accuracy: {:.2f}% \n'.format(100*train_accuracy[-1]))'''

    # Test inference after completion of training

    #Beolvassuk hogy mely résztvevőnek mely labeleket osztottuk ki.
    ftrain=open('traindataset.txt')
    testlabels=[]
    line=ftrain.readline()
    while line!="":
        sor=line.split(' ')
        tomb=[]
        for i in sor:
            tomb.append(int(i))
        testlabels.append(tomb)
        line=ftrain.readline()
    ftrain.close()

    print("KINEK MI")
    print(testlabels)

    #Minden lehetséges koalícióra lefut a tesztelés
    for j in range((2**args.num_users)-1):
        binary =numberToBinary(j,len(resztvevok))



        test_acc, test_loss = test_inference(args, global_model, test_dataset, testlabels,binary, len(binary))

        #Teszt eredmények kiírása
        print("RESZTVEVOK")
        print(resztvevok)
        print("TEST NUMBER")
        print(j)
        print("TEST BINARY")
        print(binary)
        print("TEST LABELS")
        print(testlabels)
        print("Test Accuracy")
        print("{:.2f}%".format(100*test_acc))
        print()

    # Saving the objects train_loss and train_accuracy:
    '''file_name = '../save/objects/{}_{}_{}_C[{}]_iid[{}]_E[{}]_B[{}].pkl'.\
        format(args.dataset, args.model, args.epochs, args.frac, args.iid,
               args.local_ep, args.local_bs)

    with open(file_name, 'wb') as f:
        pickle.dump([train_loss, train_accuracy], f)
'''
    #print('\n Total Run Time: {0:0.4f}'.format(time.time()-start_time))

    # PLOTTING (optional)
    # import matplotlib
    # import matplotlib.pyplot as plt
    # matplotlib.use('Agg')

    # Plot Loss curve
    # plt.figure()
    # plt.title('Training Loss vs Communication rounds')
    # plt.plot(range(len(train_loss)), train_loss, color='r')
    # plt.ylabel('Training loss')
    # plt.xlabel('Communication Rounds')
    # plt.savefig('../save/fed_{}_{}_{}_C[{}]_iid[{}]_E[{}]_B[{}]_loss.png'.
    #             format(args.dataset, args.model, args.epochs, args.frac,
    #                    args.iid, args.local_ep, args.local_bs))
    #
    # # Plot Average Accuracy vs Communication rounds
    # plt.figure()
    # plt.title('Average Accuracy vs Communication rounds')
    # plt.plot(range(len(train_accuracy)), train_accuracy, color='k')
    # plt.ylabel('Average Accuracy')
    # plt.xlabel('Communication Rounds')
    # plt.savefig('../save/fed_{}_{}_{}_C[{}]_iid[{}]_E[{}]_B[{}]_acc.png'.
    #             format(args.dataset, args.model, args.epochs, args.frac,
    #                    args.iid, args.local_ep, args.local_bs))
if __name__ == '__main__':
    main()
