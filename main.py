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
                    for word in [text[5], text[6], text[0]]:
                        word = word.strip()
                        user_role.append(word)

                    return user_role #[role, actif, matricule]
                
                else: statut = 'mdp_error';  return statut
    
    return statut


def get_other(name,key):
#cette fontion parcour les comptes ou commandes pour l'utilisateur
    #with open(comptes) as accounnt_file:
        dir = globals()[name]
        file = open(dir, "r", encoding= 'utf-8')
        for line in file:
            try:
                id = int(key)
                text = line.split('|')
                matricule = text[0].strip() 

                if id == int(matricule):
                    print(line);break
            except:
                print(line)


def get_menu(key):

    def get_id_info(key, sub_category_items):
        for infomation in sub_category_items: 
        #information is the sub_category_item information
            if key == infomation["id"]:
                return infomation
            
        return False

    def print_key(sub_category):
        for line in sub_category:
            msg = str(line["id"]) +" "+ str(line["nom"])   
            print (msg)     

    with open(menu) as json_file:
        the_menu = json.load(json_file)
        way = ""
        if key == 'items' or type(key)== int :
            way = the_menu
            if key == 'items':
                print('menu') 
            elif key < 1 or key > 40:
                print('Mauvais identifiant d\'item')
                return None

        else:
            
                for category in the_menu:
                    if way != "": break
                    if key == category :
                        way = the_menu[key]
                        break

                    elif key in the_menu[category]:
                        way = the_menu[category][key]
                        break
                    
                    else:
                        try:
                            for sub_category in the_menu[category]:
                                if key in the_menu[category][sub_category]:
                                    way = the_menu[category][sub_category][key]
                                    break
                        except: pass

                if way !="": print(key)

                else:print('Chemin non spécifié'); return None

        for item_name in way:                                                       #les differents type d'items
            if item_name!='items' and type(key)!=int :print(item_name)
            categories = way[item_name]                                             #les categories pour chaque type

            try:                                                                    #fruit et muffin n'ont pas de sous categories, donc on va acceder à "items" directement
                sub_category_items = categories["items"]

                if type(key)== int:
                    found = get_id_info(key, sub_category_items)
                    if found != False:
                        return found
                else:print_key(sub_category_items)

            except: 
                try:
                    for category_name in categories:  
                                                 
                        sub_category = categories[category_name]                                   #les sous-categories pour chaque categories de type
                        if type(key)!=int:print(category_name)

                        for sub_category_name in sub_category:
                            if type(key)!=int and category_name!='items' and sub_category_name != 'items': print(sub_category_name)##
                            try:
                                sub_category_items = sub_category[sub_category_name]["items"]      #les types d'items sous chaque sous-categories

                            except: 
                                    sub_category_items = sub_category["items"]
                            
                            if type(key) == int:
                                found = get_id_info(key, sub_category_items)
                                if found != False:
                                    return found
                                
                            else: print_key(sub_category_items)
                                
                        type(key)!= int and print("")
                except:
                        sub_category_items = way["items"]
                        if type(key)== int:get_id_info(key, sub_category_items)
                        else:print_key(sub_category_items)
        
            type(key)!= int and print("")


def GET(path):
#cette fonction affiche la liste d'une categorie
    last = len(path) - 1
    key = path[last] 

    name = path[1]
    try:
        id = int(key)
        if name == 'menu':
            if path[last-1] != 'items': print('Chemin specifié incorrect'); return None     ##pour s'assurer qu'on veut get items/id
            info = get_menu(id)

            if info['disponible'] == True:
                disponibilite = 'disponible'
            else: disponibilite = 'Non disponible'

            print(info['id'], info['nom'], 'Prix:',str(info['prix'])+'$', 'est',disponibilite)

        else:
            get_other(name, id)

    except:
            if len(path) > 2 and name != 'menu' or key== '': 
                print('Chemin specifié incorrect')
                return None
            
            if name != 'menu':
                get_other(name, key)

            else:    
                key = path[2]
                get_menu(key)
        

def POST(matricule, commande):
#cette fonction crée une commande

    prix_total = 0
    for item in commande.split(" "):
        try:
            item = item.split('x')
            quantite = int(item[0])

            item_id = int(item[1])
            info = get_menu(item_id)

            if info["disponible"] == False : 
                print('L\'item', item_id, 'n\'est pas disponible')
            
            else:
                unit_price = info["prix"]
                prix_total += unit_price * quantite
        except:
            print('Mauvaise commande en',"x".join(item))

    if prix_total == 0: print('Commande non postée');return None
    prix_total = round(prix_total, 2)
    with open(commandes) as order_file:
        for line in order_file:
            pass

        last_line = line
        start_index = int(last_line[0])
          
    orders= open(commandes, "a") 

    date = "2023-04-08"

    order_line = str(start_index+1) + ' | ' + str(matricule) +  ' | ' + str(commande) +  ' | ' + date +  ' | ' + str(prix_total)
    
    #orders.write('\n')
    #orders.write(order_line)
    print("");print('Commande postée avec succès')
    orders.close


def PUT(path):
#cette fonction met à jour la valeur du champ d'un chemin donné
    pass


def process(instruction, path, matricule):
    callee = globals()[instruction]

    if instruction == 'POST':
        last = len(path) - 1
        commande = path[last]
           
        callee(matricule, commande)
    else:
        callee(path)

    return 


def take_command(statut):
    
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
            break

        if command == 'FIN' or command == 'fin': return None

        if "/" not in command: break
        command = command.split('/')

        for _ in range (len(command)):
            word = command[0]
            command.remove(word)
            word = word.strip().lower()
            command.append(word)

        instruction = command[0]

        command.remove(instruction)
        instruction = instruction.upper()
        if ' ' in instruction or instruction not in ['GET', 'POST', 'PUT']:print('Instruction',instruction,'non valide');break

        if instruction == 'POST':
            part_command = command[1].split(" ")
            rem = part_command[0]
            part_command.remove(rem)
            part_command = " ".join(part_command)
            command.remove(command[1])
            command.append(rem) 
            command.append(part_command) 

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

        process(instruction, command, statut[2])

    take_command(statut)


def init(matricule, mot_passe):

    statut = chercher(comptes, [matricule, mot_passe])

    if statut == 'mdp_error': print('Mauvais mot de passe')

    elif statut == 'inexisting_user': print('Utilisateur non touvé')

    else:
        print('Vous êtes connecté');print("")
        
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