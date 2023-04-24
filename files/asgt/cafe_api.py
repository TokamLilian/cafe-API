#Ange Lilian Tchomtchoua Tokam, Matricule: 20230129
#Sarah Jolia Enombo Ngosso, Matricule: 20241121
#Date de création: 8 Avril 2023

#Le programme cafe-api.py permet d'envoyer des requêtes aux cafés étudiants
#telles que, recuperer les informations d'un ou plusieurs item(s) diponible(s) et placer une commande

#Ce programme permet aussi à un administrateur de mettre à jour des champs dans le fichier comptes
#et au staff de le faire pour le menu

import os
import sys
import json
from datetime import date


current_dir = os.path.dirname(__file__)
comptes     = os.path.join(current_dir, 'comptes.csv')
commandes   = os.path.join(current_dir, 'commandes.csv')
menu        = os.path.join(current_dir, 'menu.json')


def chercher(repertoire, informations):
#cette fonction verifie si les identifiants entrés sont correctes

    statut = 'Utilisateur non trouvé'

    with open(repertoire) as fichier:
        for file_line in fichier:

            text = file_line.split("|")

            if informations[0] == text[0].strip():                                  #on verifie le matricule
                if informations[1] == text[3].strip():                              #verifier si le mot de passe est correct

                    user_role = []
                    for word in [text[5], text[6], text[0]]:
                        word = word.strip()
                        user_role.append(word)

                    return user_role                                                #[role, actif, matricule]
                
                else: statut = 'Mauvais mot de passe';  return statut
    
    return statut


def get_other(name,key):
#cette fontion parcour les comptes ou commandes pour l'utilisateur

    def seperate_line(line, id_present):
    #cette fonction scinde les informations de ligne commande et/ou imprimme la ligne
        message = ""
        line = line.split('|')
        order_id = line[0]
        orders = line[2].strip()
        date = line[3]
        total = line[4][:-1] +'$'

        if id_present == True:
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

    def print_line(name, line,id_present):
    #cette fonction imprimme la ligne des comptes ou commandes
        if name == 'commandes' : seperate_line(line, id_present=id_present)
        else: print(line)

    dir = globals()[name]
    file = open(dir, "r", encoding= 'utf-8')

    if key.isdigit(): id = int(key)
                                         
    elif key != name: print('«'+key+'»','invalide'); return None
    #lorsqu'il n'y a pas d'entier qui a été spécifié

    for line in file:
        text = line.split('|')
        identifiant = text[0].strip() 

        try:        
            if id == int(identifiant):
                print_line(name, line, id_present=True); return None                #imprimmer la ligne de l'ID souhaité
            
        except:     
            #on imprimme les lignes une après l'autre s'il n'y a pas d'ID spécifié                                
            print_line(name, line, id_present=False)                                                                                                 

    key.isdigit() and print(name[:-1], id,'n\'existe pas')                          #dans le cas où on ne trouve pas l'ID
    

def get_menu(key, replace, status):
#cette fonction parcour tout les elements d'un dictionnaire

    def get_id_info(key, sub_category_items):
    #cette fonction retourne les information de l'item par son ID
        for infomation in sub_category_items: 
        #information est les données sub_category_item
            if key == infomation["id"]:

                if replace: infomation["disponible"] = status; return way

                return infomation
            
        return False

    def print_key(sub_category):
    #cette fonction imprimme les informations sous une sous-categorie
        for line in sub_category:
            msg = str(line["id"]) +" "+ str(line["nom"])   
            print (msg)     

    with open(menu, encoding='utf-8') as json_file:
        the_menu = json.load(json_file)
        way = ""
        if key == 'items' or type(key)== int :                                        #pour imprimmer tout le menu ou rechercher un ID,
            way = the_menu                                                            #on parcour tout le menu 
            if key == 'items':
                print('menu') 
            elif key < 1 or key > 40:
                return 'Mauvais identifiant d\'item'

        else:                                                                         #on cherche la categorie ou sous-categorie à parcourir
            
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

                else:return 'Chemin non spécifié'

        for item_name in way:                                                       #les differents type d'items
            if item_name!='items' and type(key)!=int :print(item_name)
            categories = way[item_name]                                             #les categories pour chaque type

            try:                                                                    #fruit et muffin n'ont pas de sous categories, 
                sub_category_items = categories["items"]                            #donc on va acceder à "items" directement

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
                                    sub_category_items = sub_category["items"]                     #on recupere les items de la categorie
                            
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
            if path[path.index(name)+1] != 'items': print('Chemin specifié incorrect'); return None     #pour s'assurer qu'on veut get items/id
            info = get_menu(id,replace=False, status=None)

            if type(info) != dict: print(info); return None
 
            if info['disponible'] == True:
                disponibilite = 'disponible'
            else: disponibilite = 'Non disponible'

            print(info['id'], info['nom'], 'Prix:',str(info['prix'])+'$', 'est',disponibilite)

        else:
            get_other(name, id)

    except:
            if name == 'menu' and key != 'items' or key== '':            #'menu' doit prendre items comme chemin finale s'il n'y a pas de ID
                print('Chemin specifié incorrect')
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
    break_line = '\n'

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

    current_date = date.today()
    for items in unavailable:
        commande.remove(items)

    commande = ", ".join(commande)
    order_line = str(start_index) + '  | ' + str(matricule) +  ' | ' + str(commande) +  ' | ' + str(current_date) +  ' | ' + str(prix_total) + break_line

    start_index == 4 and orders.write('\n')                    #pour la premiere modification
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
            else: print('Disponible doit être =1 ou 0');return None

            new_menu = get_menu(id, replace=True, status=status)
            if new_menu != None:
                print('Mise à jour éffectuée')
                with open(dir, "w", encoding='UTF-8') as the_menu:
                    json.dump(new_menu, the_menu, indent=4, ensure_ascii=False)
            else: print('Aucune modification possible')

        except: print('Disponible doit être =1 ou 0');return None

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
#cette fonction appelle GET, PUT ou POST

    callee = globals()[instruction]

    if instruction == 'POST':
        last = len(path) - 1
        commande = path[last]
           
        callee(matricule, commande)                                              #on a besoin du matricule pour poster une commande
    else:
        callee(path)

    return 


def verification_command(command):
#cette fonction verifie si une commande est valide

    command = command.split('/')

    for _ in range (len(command)):
    #on enleve les espace entre les barres obliques
        word = command[0]
        command.remove(word)
        word = word.strip()
        command.append(word)

    instruction = command[0]

    command.remove(instruction)
        
    if ' ' in instruction or instruction not in ['GET', 'POST', 'PUT']:
        return 'Instruction '+instruction+' non valide'

    if instruction == 'POST' or instruction == 'PUT':
    #POST et PUT prennent des argument qui vont etre séparés du reste d'une façaon spécifique 
        if instruction == 'POST':index = 1
        elif command[1] == 'menu': index = 3
        else: index = 2

        try:
            part_command = command[index].split(" ")
            if part_command ==[''] : return 'Besoin d\'une valeur pour '+ instruction
        except:
            return 'Chemin non spécifié'

        #on scinde de les arguments respectifs
        rem = part_command[0]
        part_command.remove(rem)
        part_command = " ".join(part_command)
        command.remove(command[index])
        command.append(rem) 
        command.append(part_command) 

    return [instruction, command]


def take_command(statut):
#cette fonction scinde la command de l'utilisateur recupere aussi le mots-clé
    
    print("Entrer une commande souhaitée ou Entrer FIN pour terminer l'execution.")

    while True:
        print('')
        command = input('>_').strip()

        if command == 'FIN': print('Vous êtes déconnecté'); return None
        if "/" not in command: print('Entrez une commande valide');break

        line = verification_command(command)
        if type(line) != list: print(line); break
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

take_command(['admin', '1' , '45678'])
def init(matricule, mot_passe):
#cette fonction procède à la saisi de la commande si l'utilisateur est actif et s'arrete sinon

    statut = chercher(comptes, [matricule, mot_passe])

    if type(statut) != list: print(statut); return

    else:
        print('Vous êtes connecté(e)');print("")
        
        if statut[1] == '1': 
            take_command(statut)
            
        else: print('Ce compte n\'est plus actif. Veuillez contacter les administrateurs pour modifier le statut du compte')


def get_inputs():
#cette fonction recupère les entrés pour le login
    matricule = input('Entrer votre matricule: ').strip()
    mot_passe = input('Entrer votre mot de passe: ')
    init(matricule, mot_passe)


def get_arguments():
#cette fonction recupère les arguments qui vont etre utilisés pour se connecter à l'API
#sinon, on demande à l'utilisateur de les entrer

    if len(sys.argv) == 3:
        try:
            matricule = sys.argv[1]
            mot_passe = sys.argv[2]                            
            init(matricule, mot_passe)

        except :
            get_inputs()

    else: get_inputs()

get_arguments()


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
            assert chercher(comptes, [matricule, mot_passe]) == ['public', '0', '20209230'], 'Mauvais parametre'

        def test_chercher4():
            matricule = '1052138'
            mot_passe = 'mpPass_26'
            assert chercher(comptes, [matricule, mot_passe]) == ['staff', '1', '1052138' ], 'Mauvais parametre'

        def test_chercher5():
            matricule = '20458102'
            mot_passe = 'rlPass_30'
            assert chercher(comptes, [matricule, mot_passe]) == ['admin', '1', '20458102'], 'Mauvais parametre'

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
            command = 'put /api/menu/cafe/items'
            assert verification_command(command) == 'Instruction put non valide'


        test_verification_GET_menu()
        test_verification_GET_comptes()
        test_verification_POST()
        test_verification_PUT()
        test_verification_None()

    test_verification()


#test()