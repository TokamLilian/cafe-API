from main import *

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
            matricule = '20250710'                          #deux étudiants ont le meme matricule
            mot_passe = 'rlPass_30'
            print(chercher(comptes, [matricule, mot_passe]))

        #test_chercher1()
        #test_chercher2()
        #test_chercher3()
        #test_chercher4()
    
    #test_chercher()
    

    def test_take_command():
        les_statuts = [ ['staff', 1], ['admin', 1], ['public', 1] ]

        for statut in les_statuts:
            take_command(statut)

    test_take_command()

test()
        