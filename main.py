import os
import sys
#import requests

from message_section import *
#intro_Section()

#repertoire = os.getcwd()
#repertoire = os.chdir('C:\\Users\\tokam\Dropbox\\XPS School Docs\\H23\\IFT 1015\\Exercices Notés\\TP 2')
#print(repertoire)##

compte =    'C:\\Users\\tokam\Dropbox\\XPS School Docs\\H23\\IFT 1015\\Exercices Notés\\TP 2\\cafe-api\\files\\comptes.csv'
commande =  'C:\\Users\\tokam\Dropbox\\XPS School Docs\\H23\\IFT 1015\\Exercices Notés\\TP 2\\cafe-api\\files\\commandes.csv'
menu =      'C:\\Users\\tokam\Dropbox\\XPS School Docs\\H23\\IFT 1015\\Exercices Notés\\TP 2\\cafe-api\\files\\menu.csv'

def chercher(repertoire, informations):
    statut = 'inexisting_user'

    with open(repertoire) as fichier:
        for file_line in fichier:

            code_line = []
            text = file_line.split("|")

            for word in text:
                word = word.strip()
                code_line.append(word)

            if informations[0] not in code_line:
                continue

            else:
                if informations[1] == code_line[3]: 
                    return [ code_line[5], code_line[6] ] #[role, actif]
                
                else: statut = 'mdp_error'
    
    return statut


def init(email, mot_passe):

    statut = chercher(compte, [email, mot_passe])

    if statut == 'mdp_error': print('Mauvais mot de passe')

    elif statut == 'inexisting_user': print('Utilisateur non touvé')

    else:
        if statut[1] == '1': message = "actif"
        else: message = 'inactif'  
    
        print('Vous etes du', statut[0], 'avec un compte', message)


def get_inputs():
    email = input('Entrer votre email: ').strip()
    mot_passe = input('Entrer votre mot de passe: ')
    init(email, mot_passe)


def get_argument():

    try:
        email = sys.argv[1]                            #cet argument va etre utilisé pour se connecter à l'API

        try:
            mot_passe = sys.argv[2]

        except:
            mot_passe = input('Entrer le mot de passe: ')

        init(email, mot_passe)

    except :
        get_inputs()

get_argument()