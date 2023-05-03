import os
import sys
import json
from getpass import *

from message_section import *
#intro_Section() weeeh papa

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
    
    dir = globals()[name]
    file = open(dir, "r", encoding= 'utf-8')

    if key.isdigit(): id = int(key)
                                         
    elif key != name: print('«'+key+'»','invalide'); return None
    #lorsqu'il n'y a pas d'entier qui a été spécifié

    for line in file:
        text = line.split('|')
        matricule = text[0].strip() 
        try:
            if id == int(matricule):
                print(line); return None
        except:
            print(line)

    key.isdigit() and print(name[:-1], id,'n\'existe pas')
    

def get_menu(key, replace, status):

    def get_id_info(key, sub_category_items):
        for infomation in sub_category_items: 
        #information is the sub_category_item information
            if key == infomation["id"]:

                if replace: infomation["disponible"] = status; return way

                return infomation
            
        return False

    def print_key(sub_category):
        for line in sub_category:
            msg = str(line["id"]) +" "+ str(line["nom"])   
            print (msg)     

    with open(menu, encoding='utf-8') as json_file:
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
            if path[path.index(name)+1] != 'items': print('Chemin specifié incorrect'); return None     ##pour s'assurer qu'on veut get items/id
            info = get_menu(id,replace=False, status=None)

            if info['disponible'] == True:
                disponibilite = 'disponible'
            else: disponibilite = 'Non disponible'

            print(info['id'], info['nom'], 'Prix:',str(info['prix'])+'$', 'est',disponibilite)

        else:
            get_other(name, id)

    except:
            if name == 'menu' and key != 'items' or key== '':            #il n'y a que 'menu' qui prend des chaines de caracteres comme chemin
                print('Chemin specifié incorrect')
                return None
            
            if name != 'menu':
                get_other(name, key)

            else:    
                key = path[2]
                get_menu(key, replace=False, status=None)
        

def POST(matricule, commande):
#cette fonction crée une commande

    prix_total = 0
    commande = commande.split(" ")
    unavailable = []                                                    #pour la liste des items non disponible

    def append_unavailable(item):
        item = "x".join(item)
        unavailable.append(item)

    for item in commande:
        try:

            item = item.split('x')
            quantite = int(item[1])
            item_id = int(item[0])

            info = get_menu(item_id,replace=False, status=None)

            if info["disponible"] == False : 
                print('L\'item', item_id, 'n\'est pas disponible')
                append_unavailable(item)
            
            else:
                unit_price = info["prix"]
                prix_total += unit_price * quantite

        except:
            append_unavailable(item)
            print('Mauvaise commande en',"x".join(item))

    if prix_total == 0: print('Commande non postée');return None
    prix_total = round(prix_total, 2)
    with open(commandes) as order_file:
        for line in order_file:
            pass                                               #pour recuperer la dernière ligne

        last_line = line
        start_index = int(last_line.split('|')[0]) + 1         #le numero de la commande à poster
          
    orders= open(commandes, "a") 

    date = "2023-04-08"
    for items in unavailable:
        commande.remove(items)

    commande = ", ".join(commande)
    order_line = str(start_index) + '  | ' + str(matricule) +  ' | ' + str(commande) +  ' | ' + date +  ' | ' + str(prix_total) + '\n'
    
    orders.write(order_line)
    print("");print('Commande postée avec succès')
    orders.close


def PUT(path):
#cette fonction met à jour la valeur du champ d'un chemin donné

    def status_error():
        print('Le statut doit être soit actif ou inactif.')
        return None

    name = path[1]
    dir = globals()[name]    #menu or comptes
    try:
        id_index = path.index("items") + 1
    except: 
            try:   
                id_index = path.index("comptes") + 1
            except: return None

    try:
        id = int(path[id_index])
        field_status_index = id_index + 1
        field_status = path[field_status_index]

    except: print('Veuillez entrer un ID valide');return None

    if name == "menu":
        try:
            field_status = field_status.split("=")
            if field_status[0] != 'disponible':print('«'+field_status[0]+'»','Invalide');return None

            if field_status[1] == '1': status = True
            elif field_status[1] == '0': status = False 
            else: print('Disponible doit être = 1 ou 0');return None

            new_menu = get_menu(id, replace=True, status=status)
            if new_menu != None:
                with open(dir, "w", encoding='UTF-8') as the_menu:
                    json.dump(new_menu, the_menu, indent=4, ensure_ascii=False)
            else: print('Aucune modification possible')

        except: print('Disponible doit être = 1 ou 0');return None

    else:
        file = open(dir, "r+", encoding= 'utf-8')
        accounts_list = []
        edit = False
        field_status = [field_status.strip('[]')]

        try:
            if field_status[0] == 'actif': status = 1
            elif field_status[0] == 'inactif': status = 0
            else: status_error()

        except: status_error()

        for line in file:                                                       #pour trouver l"ID specifié et
            if id == int(line.split("|")[0].strip()):                           #modifier le champ souhaité
                line = line.split("|")
                end_index = len(line) - 1
                line[end_index] = ' '+str(status)+'\n'
                line = "|".join(line)
                print('Mise à jour éffectuée'); edit = True

            accounts_list.append(line)

        if edit:                                                                #on réécrit le contenu de accounts_list
            with open(dir, "w", encoding='UTF-8') as accounts:                  #dans comptes.csv s'il y a eu une modification
                for user in accounts_list:
                    accounts.write(user)

            file.close()
        else: print(id, 'N\'existe pas')

    return


def process(instruction, path, matricule):
    callee = globals()[instruction]

    if instruction == 'POST':
        last = len(path) - 1
        commande = path[last]
           
        callee(matricule, commande)
    else:
        callee(path)

    return 


def verification_command(command):

    command = command.split('/')

    for _ in range (len(command)):
        word = command[0]
        command.remove(word)
        word = word.strip()
        command.append(word)

    instruction = command[0]

    command.remove(instruction)
        
    if ' ' in instruction or instruction not in ['GET', 'POST', 'PUT']:
        print('Instruction',instruction,'non valide'); return None

    if instruction == 'POST' or instruction == 'PUT':
        if instruction == 'POST':index = 1
        elif command[1] == 'menu': index = 3
        else: index = 2

        try:
            part_command = command[index].split(" ")
            if part_command ==[''] : print('Besoin d\'une valeur pour', instruction); return None
        except:
            print('Chemin non spécifié')
            return None

        rem = part_command[0]
        part_command.remove(rem)
        part_command = " ".join(part_command)
        command.remove(command[index])
        command.append(rem) 
        command.append(part_command) 

    return [instruction, command]


def take_command(statut):
    
    print("""Saisissez -h ou -help pour voir le message d\'aide pour votre statut.
    Entrer une commande souhaitée, ou              
    Entrer FIN pour terminer l'execution.""")

    while True:
        print('')
        command = input('>_').strip()

        if command == "-help" or command == '-h':
            help = 'guides_' + statut[0]
            callee = globals()[help]
            callee()
            break

        if command == 'FIN' or command == 'fin': return None
        if "/" not in command: print('Entrez une commande valide');break

        line = verification_command(command)
        if line == None: break
        instruction = line[0]
        command = line[1]

        if command[0] != 'api':
            print('Besoin d\'un chemin origin de \"api\" pour continuer') 
            break

        if len(command) < 2 or command[1] not in ['menu', 'commandes', 'comptes']:
            print('Le chemin spécifié n\'est pas correct')
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

    elif statut == 'inexisting_user': print('Utilisateur non trouvé')

    else:
        print('Vous êtes connecté(e)');print("")
        
        if statut[1] == '1': 
            take_command(statut)
            
        else: print('Ce compte n\'est plus actif. Veuillez contacter les administrateurs pour modifier le statut du compte')


def get_inputs():
    matricule = input('Entrer votre matricule: ').strip()
    mot_passe = getpass('Entrer votre mot de passe: ')
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