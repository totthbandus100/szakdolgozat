#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python version: 3.6


import numpy as np
import random
from torchvision import datasets, transforms


def mnist_iid(dataset, num_users):
    """
    Sample I.I.D. client data from MNIST dataset
    :param dataset:
    :param num_users:
    :return: dict of image index
    """

    num_items = int(len(dataset)/num_users)
    dict_users, all_idxs = {}, [i for i in range(len(dataset))]
    for i in range(num_users):
        dict_users[i] = set(np.random.choice(all_idxs, num_items,
                                             replace=False))
        all_idxs = list(set(all_idxs) - dict_users[i])
    return dict_users

def melyiknek(kinekmi,label):
    for i in range(len(kinekmi)):
        for j in range(len(kinekmi[i])):
            if kinekmi[i][j]==label:
                return i
def mnist_noniid(dataset, num_users):
    """
    Sample non-I.I.D client data from MNIST dataset
    :param dataset:
    :param num_users:
    :return:
    """
    # 60,000 training imgs -->  200 imgs/shard X 300 shards
    num_shards, num_imgs = 200, 300

    #Betöltjük a résztveveőket és megszámoljuk hányan vannak
    resztvevok=[]
    fp=open('resztvevok.txt', "r")
    x=fp.readline().split(' ')
    for i in x:
        if i !='':
            resztvevok.append(int(i))
    fp.close()

    db_resztvevo=0
    for i in resztvevok:
        if i==0:
            db_resztvevo+=1



    idx_shard = [i for i in range(num_shards)] #0-tól 200ig a számok egy tömbben


    #csak a résztvevők számának megfelelő méretű adathalmazt veszünk fel
    dict_users = {i: np.array([]) for i in range(db_resztvevo)}


    idxs = np.arange(num_shards*num_imgs)
    labels = dataset.train_labels.numpy()


    # sort labels
    idxs_labels = np.vstack((idxs, labels))


    idxs_labels = idxs_labels[:, idxs_labels[1, :].argsort()]

    idxs = idxs_labels[0, :] #kép indexek

    label_idxs = idxs_labels[1, :] #kép indexek


    #Megnézzük, hogy a labelek milyen index határok között mozognak
    index_hatarok=[0]
    labeltipus=0
    for i in range(len(label_idxs)):
        if label_idxs[i]!=labeltipus:
            index_hatarok.append(i)
            labeltipus+=1
    index_hatarok.append(len(label_idxs))

    #Betöltjük, hogy melyik résztvevőnek mely labelekre van szüksége
    f=open('traindataset.txt')
    kinekmi=[]
    for i in range(num_users):
        sor=f.readline().split(' ')
        tomb=[]
        for i in sor:
            tomb.append(int(i))
        kinekmi.append(tomb)
    f.close()


    #Végigmegyünk a résztveveőkön és megnézzük kinek milyen labelek jutottak, majd az adott label index határain belül sorsolunk neki egy tartományt
    hanyadiknakadunk=0
    for i in range(num_users):
        if resztvevok[i]!=1:
            num_images_for_user_i=int(num_imgs*2/len(kinekmi[i]))
            for j in range(len(kinekmi[i])):
                valasztott_kezdoindex=random.randrange(index_hatarok[kinekmi[i][j]],index_hatarok[kinekmi[i][j]+1]-num_images_for_user_i)
                dict_users[hanyadiknakadunk] = np.concatenate((dict_users[hanyadiknakadunk], idxs[valasztott_kezdoindex:valasztott_kezdoindex+num_images_for_user_i]), axis=0)
            hanyadiknakadunk+=1
    return dict_users


def mnist_noniid_unequal(dataset, num_users):
    """
    Sample non-I.I.D client data from MNIST dataset s.t clients
    have unequal amount of data
    :param dataset:
    :param num_users:
    :returns a dict of clients with each clients assigned certain
    number of training imgs
    """
    # 60,000 training imgs --> 50 imgs/shard X 1200 shards
    num_shards, num_imgs = 1200, 50
    idx_shard = [i for i in range(num_shards)]
    dict_users = {i: np.array([]) for i in range(num_users)}
    idxs = np.arange(num_shards*num_imgs)
    labels = dataset.train_labels.numpy()

    # sort labels
    idxs_labels = np.vstack((idxs, labels))
    idxs_labels = idxs_labels[:, idxs_labels[1, :].argsort()]
    idxs = idxs_labels[0, :]

    # Minimum and maximum shards assigned per client:
    min_shard = 1
    max_shard = 30

    # Divide the shards into random chunks for every client
    # s.t the sum of these chunks = num_shards
    random_shard_size = np.random.randint(min_shard, max_shard+1,
                                          size=num_users)
    random_shard_size = np.around(random_shard_size /
                                  sum(random_shard_size) * num_shards)
    random_shard_size = random_shard_size.astype(int)

    # Assign the shards randomly to each client
    if sum(random_shard_size) > num_shards:

        for i in range(num_users):
            # First assign each client 1 shard to ensure every client has
            # atleast one shard of data
            rand_set = set(np.random.choice(idx_shard, 1, replace=False))
            idx_shard = list(set(idx_shard) - rand_set)
            for rand in rand_set:
                dict_users[i] = np.concatenate(
                    (dict_users[i], idxs[rand*num_imgs:(rand+1)*num_imgs]),
                    axis=0)

        random_shard_size = random_shard_size-1

        # Next, randomly assign the remaining shards
        for i in range(num_users):
            if len(idx_shard) == 0:
                continue
            shard_size = random_shard_size[i]
            if shard_size > len(idx_shard):
                shard_size = len(idx_shard)
            rand_set = set(np.random.choice(idx_shard, shard_size,
                                            replace=False))
            idx_shard = list(set(idx_shard) - rand_set)
            for rand in rand_set:
                dict_users[i] = np.concatenate(
                    (dict_users[i], idxs[rand*num_imgs:(rand+1)*num_imgs]),
                    axis=0)
    else:

        for i in range(num_users):
            shard_size = random_shard_size[i]
            rand_set = set(np.random.choice(idx_shard, shard_size,
                                            replace=False))
            idx_shard = list(set(idx_shard) - rand_set)
            for rand in rand_set:
                dict_users[i] = np.concatenate(
                    (dict_users[i], idxs[rand*num_imgs:(rand+1)*num_imgs]),
                    axis=0)

        if len(idx_shard) > 0:
            # Add the leftover shards to the client with minimum images:
            shard_size = len(idx_shard)
            # Add the remaining shard to the client with lowest data
            k = min(dict_users, key=lambda x: len(dict_users.get(x)))
            rand_set = set(np.random.choice(idx_shard, shard_size,
                                            replace=False))
            idx_shard = list(set(idx_shard) - rand_set)
            for rand in rand_set:
                dict_users[k] = np.concatenate(
                    (dict_users[k], idxs[rand*num_imgs:(rand+1)*num_imgs]),
                    axis=0)

    return dict_users


def cifar_iid(dataset, num_users):
    """
    Sample I.I.D. client data from CIFAR10 dataset
    :param dataset:
    :param num_users:
    :return: dict of image index
    """
    num_items = int(len(dataset)/num_users)
    dict_users, all_idxs = {}, [i for i in range(len(dataset))]
    for i in range(num_users):
        dict_users[i] = set(np.random.choice(all_idxs, num_items,
                                             replace=False))
        all_idxs = list(set(all_idxs) - dict_users[i])
    return dict_users


def cifar_noniid(dataset, num_users):
    """
    Sample non-I.I.D client data from CIFAR10 dataset
    :param dataset:
    :param num_users:
    :return:
    """
    num_shards, num_imgs = 200, 200
    idx_shard = [i for i in range(num_shards)]
    dict_users = {i: np.array([]) for i in range(num_users)}
    idxs = np.arange(num_shards*num_imgs)
    # labels = dataset.train_labels.numpy()
    labels = np.array(dataset.train_labels)

    # sort labels
    idxs_labels = np.vstack((idxs, labels))
    idxs_labels = idxs_labels[:, idxs_labels[1, :].argsort()]
    idxs = idxs_labels[0, :]

    # divide and assign
    for i in range(num_users):
        rand_set = set(np.random.choice(idx_shard, 2, replace=False))
        idx_shard = list(set(idx_shard) - rand_set)
        for rand in rand_set:
            dict_users[i] = np.concatenate(
                (dict_users[i], idxs[rand*num_imgs:(rand+1)*num_imgs]), axis=0)
    return dict_users


if __name__ == '__main__':
    dataset_train = datasets.MNIST('./data/mnist/', train=True, download=True,
                                   transform=transforms.Compose([
                                       transforms.ToTensor(),
                                       transforms.Normalize((0.1307,),
                                                            (0.3081,))
                                   ]))
    num = 100
    d = mnist_noniid(dataset_train, num)
