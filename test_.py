from main import *
from random import *

def test():

    def test_chercher():
        def test_chercher1():
            matricule = '20230129'
            mot_passe = 'm@mi22'
            print(chercher(comptes, [matricule, mot_passe]))

        def test_chercher2():
            matricule = '20031977'
            mot_passe = 'vqdv@5'
            print(chercher(comptes, [matricule, mot_passe]))

        def test_chercher3():
            matricule = '20209230'
            mot_passe = 'rnPass_25'
            print(chercher(comptes, [matricule, mot_passe]))

        def test_chercher4():
            matricule = '20250710'
            mot_passe = 'rlPass_30'
            print(chercher(comptes, [matricule, mot_passe]))

        #test_chercher1()
        #test_chercher2()
        #test_chercher3()
        #test_chercher4()
    
    #test_chercher()
    

    def test_take_command():
        les_statuts = [  ['admin', 1,'20230129'], ['staff', 1,'20230129'], ['public', 1,'20230129'] ]

        for statut in les_statuts:
            take_command(statut)

    test_take_command()


    def test_process():
        command = 'POST'
        path = ['api', 'commandes', '3x1 1x22']
        statut = '20230129'
        process(command, path, statut)

    #test_process()


    def test_POST():
        path = ['API', 'COMMANDES', '5X4 3x6 3x4 7x1 28x3']
        statut = ['public', 1, '20230129']
        prix = 4
        POST(statut[2], path[2])

    #test_POST()

    def test_get_items1():
        number = 40
        indices = []
        index = ""
        
        while len(indices) < number:
            index = int(40*random())
            if index not in indices:
                indices.append(index)
                print(index, get_menu(index))

    def test_get_items2():
        ma_list = ['fruit', 'boisson_chaude', 'muffin', 'the', 'viennoiserie', 'lait', 'chocolat', 'wrap', 'boisson','items','croissant','boisson_froide']
        for nom in ma_list:
            print('on a',nom)
            get_menu(nom)
            print("-"*30)

    #test_get_items1()
    #test_get_items2()


test()