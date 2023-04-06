import os
import sys
import json
#import requests

from message_section import *
#intro_Section()

#repertoire = os.getcwd()
#repertoire = os.chdir('C:\\Users\\tokam\Dropbox\\XPS School Docs\\H23\\IFT 1015\\Exercices Notés\\TP 2')
#print(repertoire)##

compte =    'C:\\Users\\tokam\Dropbox\\XPS School Docs\\H23\\IFT 1015\\Exercices Notés\\TP 2\\cafe-api\\files\\comptes.csv'
commande =  'C:\\Users\\tokam\Dropbox\\XPS School Docs\\H23\\IFT 1015\\Exercices Notés\\TP 2\\cafe-api\\files\\commandes.csv'
menu =      'C:\\Users\\tokam\Dropbox\\XPS School Docs\\H23\\IFT 1015\\Exercices Notés\\TP 2\\cafe-api\\files\\menu.json'

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

#get_argument()


def get_items():

    with open(menu) as json_file:
        the_menu = json.load(json_file)

        for type in the_menu:
            print('Type', type)                             #les differents type d'items
            category = the_menu[type]                       #les categories pour chaque type
            #print('on a', category)
            for items in category:                          
                #print(item)
                sub_category = category[items]              #les sous-categories pour chaque categories de type
                #print(sub_category)

                for item in sub_category:
                    #print(item)
                    try:
                        item_type = sub_category[item]      #les types d'items sous chaque sous-categories
                    except:                                 ##fruit et muffin n'ont pas de sous categories, donc on va acceder à "items" directement
                        item_type = sub_category
                        
                    #print(item_type)
                    for line in item_type:                  #line is "items"
                        try:
                            info = item_type[line]
                        except:                             #certaines categories n'ont pas de sous-categories,
                                                            #on va acceder aux informations directement
                            info = item_type
                        #print(info)                        #le block d'informations d'un type d'item
                    
                        for infomation in info:
                            #print(info[infomation])
                            print(infomation)
                        break
                    
                    break
                    
                    print("")
                

            print("");print("")

get_items()


def get_items_old(the_menu):
        for item in the_menu:
            item_name = item.upper()
            print(item_name)

            list = the_menu[item]

            for type in list:
                category = list[type]

                #for item in category:
                    #print(item)
                    #print(the_menu[list][category][item].get("items"))

                for i in range(len(category)):
                    item = category[i]
                    print(item)


        #print(items)
        #print(json.dumps(items,indent=5, sort_keys=True))
