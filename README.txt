MNIST dataseten non-iid elosztású federált tanulás elosztott kiértékelésére alkotott teszt környezet.
Alapul szolgáló federált tanulási környezet: https://github.com/AshwinRJ/Federated-Learning-PyTorch

Követelmények a kísérlethez:
    Python3
    Pytorch
    Torchvision


A kísérlet beállításaihoz:
	options.py-ban megadni: epochs: szabadon választható pozitív egész szám
	                        num_users: szabadon választható pozitív egész szám
	                        model: kötelezően: mlp
	                        dataset: kötelezően: mnist
	                        iid: kötelezően: 0

    vezerlo.py-ban megadni: resztvevokszama: ugyanannyinak kell lennie mint az options.py-ban a num_users értéke
                            dbteszt: szabadon választható pozitív egész, megadja, hogy hányszor szeretnénk a kísérletet elvégezni

    traindataset.txt: soronként megadni, hogy a résztvevők milyen cimkével ellátott képekkel rendelkeznek.



A kísérlet futtatása:
    A beállítások elvégzése után az alábbi parancs kiadása a forrás filok mappájában: python vezerlo.py




A kísérlet kimenetelei:
    eredmények.txt: A résztvevők Shaplyes értékeik a teszt koalíciók alapján.
    kiertekeles.txt: Statisztikai adatok a kísérletekről.
    etalon.txt, konszenzus.txt: Kísérletenként a résztvevők Shapley értékei.
    kimenet.txt: Az összes kísérlet kimenete és minden teszteredmény. Végig lehet vele követni a teljes kísérletet.








