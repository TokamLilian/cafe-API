#ce programme retourne les informations pour les différentes fonctions de L'API

def intro_Section():

    n_h_tags = 70
    top = '#'*n_h_tags

    message = ['WELCOME TO CAFE API', 
               'LET\'S GET  STARTED', 
               'THERE ARE THREE TYPES OF USERS;',
               'PUBLIC, STAFF AND ADMIN', 
               'EACH CAN PERFORM DIFFERENT TASKS',
               '',
               'IF YOUR ACCOUNT IS NOT ACTIVE,',
               'PLEASE CONTACT THE ADMINISTRATION'
            ]

    i = 0
    length = len(message)
    while i <= length:

        if i==0 or i==length:
            print(top)

        if i<length:
            longueur = len(message[i])
            espace = (n_h_tags - longueur)
            if espace%2 == 0: espace_d = espace_g = int(espace/2)-1

            else: espace_d = (espace//2); espace_g = espace_d -1
            line = ('#' + espace_g*" " + message[i] + espace_d * " " + '#')
            print(line)

        i += 1


def guides_public():
    guides= [   'ALL USERS CAN USE THE FOLLOWING', '',
        
                'TO VIEW THE LIST OF ALL ITEMS,',
                'USE THE COMMAND: \'GET /api/menu/items\'',
                '',
                
                'TO VIEW THE LIST OF ITEMS UNDER A CATEGORY,',
                'USE THE COMMAND: \'GET /api/menu/{category name}/items\'',
                '--Where \"category name\" is the category you wish to view',
                '',

                'TO VIEW INFORMATION ABOUT A GIVEN ITEM,',
                'USE THE COMMAND: \'GET /api/menu/items/{Item id}\'',
                '--Where \"Item id\" is the identification number of',
                'the item you wish to view',
                '',

                'FINALLY, TO PLACE AN ORDER,',
                'USE THE COMMAND: ',
                '\'POST /api/commandes {Item id}x{quantity} {Item id}x{quantity}\'',
                '--For example: POST /api/commandes 3x1 4x2,',
                'To order 1 time the item of id = 3 and 2 times the item of id 4',
                ' '
    ]

    for line in guides:
        print(line)


def guides_staff():

    seperator = '-'*100

    guides = [    'AS A STAFF MEMBER, YOU CAN USE THE FOLLOWING',
              
                    'TO VIEW ALL PLACED ORDERS, USE THE COMMAND:',
                    '\"GET /api/commandes\"','',

                    'TO VIEW ALL INFORMATION ABOUT A PARTICULAR ORDER,',
                    'USE THE COMAMND: GET /api/commandes/{Order Id}','',

                    'TO SET THE AVAILABILITY OR NOT OF AN ITEM,',
                    'USE THE COMMAND: \"PUT /api/menu/items/{Item id} disponible={Availability}\"',
                    '--Where \"Availability\" can be either 1 to mark the item as available'
                    'or 0 to mark the item as unavailable',
    ]

    for i in range(len(guides)):
        line = guides[i]
        print(line)
        if i==0 or len(guides)-i==1:
            print(seperator)


def guides_admin():
    guides = [  'AN ADMIN CAN PERFORM THE FOLLOWING;',''

                  'VIEW ALL THE USER ACCOUNTS',
                  'USE THE COMMAND: \"GET /api/comptes\"','',

                  'VIEW THE INFORMATION ABOUT A PARTICULAR USER',
                  'USE THE COMMAND: \"GET /api/comptes/{User id}\"','',

                  'SET THE STATUS OF A USER ACCOUNT (EITHER ACTIVE Or INACTIVE)',
                  'PUT /api/comptes/{user id} [Status]',
                  '--Where \"Status\" can be either \"actif\" or \"inactif\"',''

    ]

    for line in guides: print(line)

guides_admin()