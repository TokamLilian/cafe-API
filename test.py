import os
import sys

current_dir = os.path.join(os.path.dirname(__file__), 'asgt')
sys.path.append(current_dir)

from cafe_api import *


def test():

    def test_chercher():
        def test_chercher1():
            matricule = '20230129'
            mot_passe = 'm@mi22'
            assert chercher(comptes, [matricule, mot_passe]) == 'Utilisateur non trouvé'

        def test_chercher2():
            matricule = '20031977'
            mot_passe = 'vqdv@5'
            assert chercher(comptes, [matricule, mot_passe]) == 'Mauvais mot de passe'

        def test_chercher3():
            matricule = '20209230'
            mot_passe = 'rnPass_25'
            assert chercher(comptes, [matricule, mot_passe]) == ['public', '0', '20209230']

        def test_chercher4():
            matricule = '1052138'
            mot_passe = 'mpPass_26'
            assert chercher(comptes, [matricule, mot_passe]) == ['staff', '1', '1052138' ]

        def test_chercher5():
            matricule = '20458102'
            mot_passe = 'rlPass_30'
            assert chercher(comptes, [matricule, mot_passe]) == ['admin', '1', '20458102']

        test_chercher1()
        test_chercher2()
        test_chercher3()
        test_chercher4()
        test_chercher5()
    
    test_chercher()


    def test_get_menu():

        def test_get_nom():
            key = 2
            assert get_menu(key, replace=False, status=[])['nom'] == 'Café filtre (grand)'

        def test_get_none():
            key = 46
            assert (get_menu(key, replace=False, status=[])) == 'Mauvais identifiant d\'item'

        def test_get_prix():
            key = 24
            assert get_menu(key, replace=False, status=[])['prix'] == 2.7
        
        def test_get_disponible():
            key = 8
            assert get_menu(key, replace=False, status=[])['disponible'] == True

        def test_get_len():
            key = 35
            assert len(get_menu(key, replace=False, status=[])) == 4


        test_get_nom()
        test_get_none()
        test_get_prix()
        test_get_disponible()
        test_get_len()  

    test_get_menu()


    def test_verification():

        def test_verification_GET_menu():
            command = 'GET /api/menu/items'
            assert verification_command(command) == ['GET', ['api', 'menu', 'items']]

        def test_verification_GET_comptes():
            command = 'GET/api / comptes'
            assert verification_command(command) == ['GET', ['api', 'comptes']]

        def test_verification_POST():
            command = 'POST /api/commandes 4x5 32x4'
            assert verification_command(command) == ['POST', ['api', 'commandes', '4x5 32x4']]

        def test_verification_PUT():
            command = 'PUT /api/menu/items/25 disponible=1'
            assert verification_command(command) == ['PUT', ['api', 'menu', 'items', '25', 'disponible=1']]

        def test_verification_None():
            command = 'get /api/menu/cafe/items'
            assert verification_command(command) == 'Instruction get non valide'


        test_verification_GET_menu()
        test_verification_GET_comptes()
        test_verification_POST()
        test_verification_PUT()
        test_verification_None()

    test_verification()


test()