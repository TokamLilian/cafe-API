import os
import sys
import json

from message_section import *
#intro_Section()

current_dir = os.path.join(os.path.dirname(__file__), 'files')
comptes     = os.path.join(current_dir, 'comptes.csv')
commandes   = os.path.join(current_dir, 'commandes.csv')
menu        = os.path.join(current_dir, 'menu.json')


def chercher(repertoire, informations):
    statut = 'inexisting_user'

    with open(repertoire) as fichier:
        for file_line in fichier:

            text = file_line.split("|")

            if informations[0] == text[0].strip():
                if informations[1] == text[3].strip(): 

                    user_role = []
                    for word in [text[5], text[6]]:
                        word = word.strip()
                        user_role.append(word)

                    return user_role #[role, actif]
                
                else: statut = 'mdp_error';  return statut
    
    return statut


def GET(path):
#cette fonction affiche la liste d'une categorie
    pass


def POST(path):
#cette fonction crée une commande
    pass


def PUT(path):
#cette fonction met à jour la valeur du champ d'un chemin donné
    pass


def process(comamnd, path):
    print('La commande', comamnd)   ##
    print('Le chemin', path)        ##

    callee = globals()[comamnd]
    callee(path)

    return 


def take_command(statut):
    #print(statut[0])   ##
    print("""Saisissez -h ou -help pour voir le message d\'aide pour votre statut.
    Entrer une commande souhaitée, ou              
    Entrer FIN pour terminer l'execution.""")

    while True:
        print('')
        command = input('>_').strip()

        if command == "-help" or command in '-h':
            help = 'guides_' + statut[0]
            callee = globals()[help]
            callee()

        if command == 'FIN' or command == 'fin': return None

        if "/" not in command: break
        command = command.split('/')

        for _ in range (len(command)):
            word = command[0]
            command.remove(word)
            word = word.strip()
            command.append(word)

        instruction = command[0]
        if ' ' in instruction :break

        else:
            command.remove(instruction)
            instruction = instruction.upper()

            if len(command) < 2: break
            if command[0] != 'api':
                print('Besoin d\'un chemin origin de l\'API pour continuer') 
                break

            if command[1] not in ['menu', 'commandes', 'comptes']:
                print('Le chemin spécifé n\'est pas correct')
                break

            if instruction == 'POST' and command[1] != 'commandes': 
                print('Vous ne pouvez que poster des commandes.')
                break
            
            if statut[0] != "admin" and command[1] == 'comptes':
                print('Vous n\'avez pas le droit d\'acceder aux', command[1])
                break
            
            if statut[0] == "public" and (instruction == 'GET' and command[1] == 'commandes' or instruction == 'PUT'):
                print('Vous n\'avez pas droit à cette fonctionalité')
                break
            
            if instruction == 'PUT' and command[1] == 'commandes': 
                print('Impossible de faire cette action.')
                break

            process(instruction, command)

    take_command(statut)


def init(matricule, mot_passe):

    statut = chercher(comptes, [matricule, mot_passe])

    if statut == 'mdp_error': print('Mauvais mot de passe')

    elif statut == 'inexisting_user': print('Utilisateur non touvé')

    else:
        if statut[1] == '1': 
            take_command(statut)
            
        else: print('Ce compte n\'est plus actif. Veuillez contacter les administrateurs pour modifier le statut du compte')


def get_inputs():
    matricule = input('Entrer votre matricule: ').strip()
    mot_passe = input('Entrer votre mot de passe: ')
    init(matricule, mot_passe)


def get_arguments():
    if len(sys.argv) == 3:
        try:
            matricule = sys.argv[1]                            #ces arguments vont etre utilisés pour se connecter à l'API
            mot_passe = sys.argv[2]                            
            init(matricule, mot_passe)

        except :
            get_inputs()

    else: get_inputs()

#get_arguments()


def get_items():

    with open(menu) as json_file:
        the_menu = json.load(json_file)

        for item_name in the_menu:
            print('Type', item_name)                             #les differents type d'items
            categories = the_menu[item_name]                       #les categories pour chaque type
            #print('on a', categories)
            for category_name in categories:                          
                #print(sub_category_name)
                sub_category = categories[category_name]              #les sous-categories pour chaque categories de type
                #print(sub_category)

                for sub_category_name in sub_category:
                    i = 0
                    #print(sub_category_name)
                    try:
                        sub_category_items = sub_category[sub_category_name]["items"]      #les types d'items sous chaque sous-categories

                    except TypeError: 
                        try:                                ##fruit et muffin n'ont pas de sous categories, donc on va acceder à "items" directement
                            sub_category_items = sub_category["items"]
                        
                        except:
                            sub_category_items = sub_category
                        
                    #print(sub_category_items)
                    while i <= len(sub_category_items):
                    #for line in sub_category_items:                  #line is "items", we can use "sub_category_item.get("items")
                        #try:
                        #category_info = sub_category_items["items"]
                        category_info = sub_category_items
                    #    except:
                        #certaines categories n'ont pas de sous-categories,
                        #on va acceder aux informations directement
                        #    category_info = sub_category_items

                            #for infomation in category_info:
                            #    print(infomation)
                            #    i += 1

                        #print(category_info)                        #le block d'informations d'un type d'item
                    
                        for infomation in category_info:             #information is the sub_category_item information
                            #print(category_info[infomation])
                            print(infomation)
                            i += 1

                        break
                    #i+=1
                    print("")
                   
            print("")