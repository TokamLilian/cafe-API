import os
import sys
import json
from datetime import date
from getpass import *

from message_section import *
intro_Section()

current_dir = os.path.join(os.path.dirname(__file__), 'files')
comptes_dir     = os.path.join(current_dir, 'comptes.csv')
commandes_dir   = os.path.join(current_dir, 'commandes.csv')
menu_dir        = os.path.join(current_dir, 'menu.json')

try:
    comptes = open(comptes_dir, "r", encoding='UTF-8')

    commandes = open(commandes_dir, "r", encoding='UTF-8')

    with open(menu_dir, encoding='utf-8') as json_file:
        menu = json.load(json_file)

except:
    print('File error')

def chercher(informations):
#cette fonction verifie si les identifiants entrés sont correctes

    statut = 'Utilisateur non trouvé'

    with open(comptes_dir) as fichier:
        for file_line in fichier:

            text = file_line.split("|")

            if informations[0] == text[0].strip():
                if informations[1] == text[3].strip():

                    user_role = []
                    for word in [text[5], text[6], text[0]]:
                        word = word.strip()
                        user_role.append(word)

                    return user_role                                                #[role, actif, matricule]
                
                else: statut = 'Mauvais mot de passe';  return statut
        
        return statut


def get_other(name,key):
#cette fontion parcour les comptes ou commandes pour l'utilisateur
    
    def order_seperate(line, message, id_present):
    #cette fonction scinde les informations de ligne commande et/ou imprimme la ligne
        order_id = line[0]
        orders = line[2].strip()
        date = line[3]
        total = line[4][:-1] +'$'

        if id_present:
            for order in orders.split(','):
                order = order.split('x')
                id = int(order[0])
                quantite = order[1]

                info = get_menu(id, replace=False, status=None)
                name = info['nom']

                message += name + ': ' + quantite + ' fois. '

            print(order_id, message, 'Date: ',date, 'Total: ', total)
            
        else:
            print(order_id, date, total)

    def account_seperate(line, id_present):
        account_id = line[0]
        first_name = line[1].strip()
        last_name  = line[2].strip()

        email = line[4].strip()
        role = line[5].strip()
        activity = line[6].strip()
        if activity == '1': msg = 'active'
        else: msg = 'incative'

        if id_present:
            print(account_id, 'Name:', first_name+',', 'Email:', email, 'is', role, 'and', msg)
        else:
            print('ID:', account_id, 'Full name:', first_name, last_name)

    def print_line(name, line,id_present):
    #cette fonction imprimme la ligne des comptes ou commandes
        message = ""
        line = line.split('|')
        if name == 'commandes' : order_seperate(line, message, id_present=id_present)
        else: account_seperate(line, id_present=id_present)
    
    callee = globals()[name+'_dir']
    with open (callee, encoding='utf-8') as file:

        if key.isdigit(): id = int(key)
                                            
        elif key != name: print('«'+key+'»','invalide'); return None            ##convert to single return
        #lorsqu'il n'y a pas d'entier qui a été spécifié

        for line in file:
            text = line.split('|')
            matricule = text[0].strip() 
            try:
                if id == int(matricule):
                    print_line(name, line, id_present=True); return None       ##convert to single return
            except:
                print_line(name, line, id_present=False)
        key.isdigit() and print(name[:-1], id,'n\'existe pas')
    

def get_menu(key, replace, status):

    way = ""
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

    if key == 'items' or type(key)== int :
        way = menu
        if key == 'items':
            print('menu') 
        elif key < 1 or key > 40:
            return 'Mauvais identifiant d\'item'

    else:
        
            for category in menu:
                if way != "": break
                if key == category :
                    way = menu[key]
                    break

                elif key in menu[category]:
                    way = menu[category][key]
                    break
                
                else:
                    try:
                        for sub_category in menu[category]:
                            if key in menu[category][sub_category]:
                                way = menu[category][sub_category][key]
                                break
                    except: pass

            if way !="": print(key)

            else: return 'Chemin non spécifié'

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
            if path[path.index(name)+1] != 'items':                  #pour s'assurer qu'on veut get items/id
                 print('Chemin specifié incorrect'); return None     ##convert to single return
            info = get_menu(id,replace=False, status=None)

            if info['disponible'] == True:
                disponibilite = 'disponible'
            else: disponibilite = 'Non disponible'

            print(info['id'], info['nom'], 'Prix:',str(info['prix'])+'$', 'est',disponibilite)

        else:
            get_other(name, id)

    except:
            if name == 'menu' and key != 'items' or key== '':            #il n'y a que 'menu' qui prend des chaines de caracteres comme chemin
                print('Chemin specifié incorrect')                       #convert to single return
                return None
            
            if name != 'menu':
                get_other(name, key)

            else:    
                key = path[2]
                info = get_menu(key, replace=False, status=None)
                info != None and print(info)
        

def POST(matricule, commande):
#cette fonction crée une commande

    prix_total = 0
    commande = commande.split(" ")
    unavailable = []                                                    #pour la liste des items non disponible

    def append_unavailable(item, msg):
        item = "x".join(item)

        if msg == 1 : print('L\'item', item_id, 'n\'est pas disponible')
        else: print('Mauvaise commande en',item)

        unavailable.append(item)

    for item in commande:
        try:

            item = item.split('x')
            if len(item) == 2: 

                quantite = int(item[1])
                item_id = int(item[0])

                info = get_menu(item_id, replace=False, status=None)

                if info["disponible"] == False : 
                    append_unavailable(item, 1)
                
                else:
                    unit_price = info["prix"]
                    prix_total += unit_price * quantite

            else:
                append_unavailable(item, 0)

        except:
            #si une commande n'est pas bonne, on l'enleve de la liste avant de continuer
            append_unavailable(item, 0)

    if prix_total == 0: print('Commande non postée');return None                        ##convert to single return
    prix_total = round(prix_total, 2)
    
    for line in globals()["commandes"]:
        pass                                               #pour recuperer la dernière ligne

    last_line = line
    start_index = int(last_line.split('|')[0]) + 1         #le numero de la commande à poster
          
    with open(commandes_dir, "a") as orders:

        current_date = date.today()
        for items in unavailable:
            commande.remove(items)

        commande = ", ".join(commande)
        order_line = str(start_index) + '  | ' + str(matricule) +  ' | ' + str(commande) +  ' | ' + str(current_date) +  ' | ' + str(prix_total) + '\n'
        
        start_index == 4 and orders.write('\n')
        orders.write(order_line)
    
    print("");print('Commande postée avec succès')              ##convert to single return


def PUT(path):
#cette fonction met à jour la valeur du champ d'un chemin donné

    def status_error():
        print('Le statut doit être soit actif ou inactif.')                 ##convert to single return
        return None

    name = path[1]
    dir = globals()[name+'_dir']    #menu_dir or comptes_dir
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

    except: print('Veuillez entrer un ID valide'); return None              ##convert to single return

    if name == "menu":
        try:
            field_status = field_status.split("=")
            if field_status[0] != 'disponible':print('«'+field_status[0]+'»','Invalide');return None      ##convert to single return

            if field_status[1] == '1': status = True
            elif field_status[1] == '0': status = False 
            else: print('Disponible doit être = 1 ou 0'); return None                                     ##convert to single return

            new_menu = get_menu(id, replace=True, status=status)

            if type(new_menu) == dict:
                with open(dir, "w", encoding='UTF-8') as menu_file:
                    json.dump(new_menu, menu_file, indent=4, ensure_ascii=False)
                print('Mise à jour éffectuée'); return None                                               ##convert to singel return
            
            else: 
                print(new_menu)
                #print('Aucune modification possible'); return None                                       ##convert to singel return      

        except: print('Disponible doit être = 1 ou 0'); return None                                       ##convert to single return

    else:
        accounts_list = []
        edit = False
        field_status = [field_status.strip('[]')]

        try:
            if field_status[0] == 'actif': status = 1
            elif field_status[0] == 'inactif': status = 0
            else: return status_error()

        except: return status_error()

        with open(dir, "r", encoding="utf-8") as file:
            for line in file:  

                line_id = line.split("|")[0].strip()             #pour trouver l"ID specifié et
                if id == int(line_id):                           #modifier le champ souhaité
                    line = line.split("|")
                    end_index = len(line)-1

                    old_status = line[end_index].strip()
                    new_status = ' '+str(status)+'\n'

                    if int(old_status) == status:
                        print('Aucun changement possible')      ##convert to single return
                        return None

                    else: line[end_index] = new_status

                    line = "|".join(line)
                    edit = True

                accounts_list.append(line)

        if edit:                                                                
            #on réécrit le contenu de accounts_list dans comptes.csv s'il y a eu une modification
            with open(dir, "w", encoding="utf-8") as account_file:
                for user in accounts_list:
                    account_file.write(user)
            print('Mise à jour éffectuée'); return None                     ##convert to single return
        
        else: print(id, 'N\'existe pas'); return None                       ##convert to single return


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
        word = command.pop(0)
        word = word.strip()
        command.append(word)

    instruction = command.pop(0)
        
    if command[0] != 'api':
        return 'Besoin d\'un chemin origin de \"api\" pour continuer'
    
    if ' ' in instruction or instruction not in ['GET', 'POST', 'PUT']:
        return 'Instruction '+str(instruction)+' non valide'
    
    if instruction == 'POST' and 'commandes' not in command[1]: 
        return 'Vous ne pouvez poster que des commandes.'
    
    if instruction == 'PUT' and 'commandes' in command[1]: 
        return 'Impossible de faire cette action.'
    
    if instruction == 'POST' or instruction == 'PUT':
        if instruction == 'POST':index = 1
        elif command[1] == 'menu': index = 3
        else: index = 2

        try:
            part_command = command[index].split(" ")
            if part_command ==[''] : return 'Besoin d\'une valeur pour ' + instruction
        except:
            return 'Chemin non spécifié'

        rem = part_command.pop(0)
        part_command = " ".join(part_command)
        command.remove(command[index])
        command.append(rem) 
        command.append(part_command) 

    if len(command) < 2 or command[1] not in ['menu', 'commandes', 'comptes']:
        return 'Le chemin spécifié n\'est pas correct'
    
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

        command = verification_command(command)
        if type(command) != list:
            print(command)
            break
        
        instruction = command.pop(0)
        
        if statut[0] != "admin" and command[0][1] == 'comptes':
            print('Vous n\'avez pas le droit d\'acceder aux', command[0][1])
            break
        
        if statut[0] == "public" and (instruction == 'GET' and command[0][1] == 'commandes' or instruction == 'PUT'):
            print('Vous n\'avez pas droit à cette fonctionalité')
            break

        process(instruction, command[0], statut[2])

    take_command(statut)


def init(matricule, mot_passe):
#cette fonction procède à la saisi de la commande si l'utilisateur est actif et s'arrete sinon

    statut = chercher([matricule, mot_passe])

    if type(statut) != list:
        print(statut)
        cont = input('Voulez-vous réessayer ? [OUI]/[NON]: ').upper()
        if cont != 'OUI': return
        else: print(""); get_inputs()
        
    elif statut[1] == '1': 
        print('Vous êtes connecté(e)');print("")
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

get_arguments()