"""
Par Erwan Boukerche ( aka. Ebium )
Date de début : 25 Octobre 2020
Date de fin : 1er Novembre 2020
Sujet du programme : Type " Escape Game "
But : Atteindre la fin du labyrinthe en répondant à des questions
présentées sous formes de portes et collecter tous les objets
( qui vous aiderons à répondre à certaines questions )

! Avant de compiler le script !
N'oubliez pas de placer les 3 fichiers chateau, objets et portes
pour que le programme fonctionne
"""

# Librairies --------------|---------------

import turtle
import time


# Variables ---------------|---------------

L = -1 # Ligne pour tracer le château
C = -1 # Colonne pour tracer le château
list_murs = [(-1,1),(27,17)]#Cases déjà présentes = Cases hors château pour eviter toute sortie de celui-ci
tuple_arrivee = () #Case de l'arrivée
LM = 0 # Ligne dans la position du joueur
CM = 1 # Colonne dans la position du joueur
coo_prec = () # Coordonnées précédente du joueur
indentation_objet = 0 # Utilisée pour descendre dans la fenêtre pour afficher les indices
num_objet = 1 # Utilisée pour modifier le nombre après " N° " pour les indices
rep = '' # enregistre la réponse de chaque question
valangleprec = 3 # position initiale du curseur et utilisée pour le tourner
chateau = 'plan_chateau.txt' # Nom plus simple à utiliser , pareil pour les 2 suivants
fichier_objets = 'dico_objets.txt'
fichier_portes = 'dico_portes.txt'
# Fonctions ---------------|---------------


#Première partie : Lecture du fichier de la zone de jeu et fonctions de traçage

def lire_matrice(fichier_chateau):
    """
    Arguments : Fichier avec les numéros de chaque case correspondant à un mur ou autre 
    But : retourne une matrice représentant le château
    """
    lfin = []
    lperm = []
    with open(fichier_chateau,encoding='utf-8') as f:
        grid = f.read().strip() # enregistre la matrice sous forme de str ( plus simple à étudier )
        for elem in grid:
            if elem == "\n":
                lfin.append(lperm)
                lperm = []
            else:
                if elem.isalnum() == True:
                    lperm.append(int(elem))
    lfin.append(lperm)
    return lfin
matrice = lire_matrice(chateau) #Constante représentant le château et utilisée pour le reste du programme


def calculer_pas(grid):
    """
    Arguments : Grid = matrice représentant le château
    But : Calcule le pas qui sera utlisé dans toutes les fonctions utilisant l'argument '' Pas ''
    """
    ligne = len(grid[0])
    colonne = len(grid)
    return min((290/ligne),(440/colonne))


def coordonnees(case, pas):
    """
    Arguments : Case = numéro de la case du joueur, Pas 
    But : Calcule et retourne les coordonnées d'une case choisie
    """
    ncase = len(lire_matrice(chateau)) - 1
    un = -240 + ((ncase - case[0]) * pas)
    deux = -240 + (case[1]*pas)
    return (deux,un)


def tracer_carre(dimension):
    """
    Arguments : Dimension du carré voulu ( longueur d'un côté )
    But : Trace le carré d'une dimension choisie
    """
    i = 0
    turtle.begin_fill()
    turtle.down()
    while i <= 3:
        turtle.forward(dimension)
        turtle.left(90)
        i += 1
    turtle.end_fill()
    turtle.up()


def tracer_case(case, couleur, pas):
    """
    Arguments : Case = numéro de la case du joueur , Couleur = couleur de la case , Pas 
    But : Trace la case voulue 
    """
    turtle.color(couleur)
    turtle.goto(coordonnees(case,pas))
    tracer_carre(pas)


#Deuxième partie : Gestion objets, portes et fin de jeu

def dic_objets(fichier_des_objets):
    """
    Arguments : Fichier contenant coordonnées et indices des objets
    But : Créer un dictionnaire correspondant au fichier
    """
    dfin = {}
    a = ''
    b = ''
    with open(fichier_des_objets, encoding='utf-8') as f:
        for ligne in f:
            a, b = eval(ligne)
            dfin[a] = b
    return dfin
dict_objets = dic_objets(fichier_objets) # dictionnaire modifiable pour la gestion des objets


def dic_portes(fichier_des_portes):
    """
    Arguments : Fichier contenant coordonnées, questions et réponses des portes
    But : Créer un dictionnaire correspondant au fichier
    """
    dfin = {}
    a = ''
    b = ''
    with open(fichier_des_portes, encoding='utf-8') as f:
        for ligne in f:
            a, b = eval(ligne) # pour chaque ligne, la question est stockée dans a et la réponse dans b
            dfin[a] = b
    return dfin
dict_portes = dic_portes(fichier_portes) # dictionnaire modifiable pour la gestion des portes


def shutdown():
    """
    But : Ferme la fenêtre lorsque la partie est terminée
    """
    turtle.color("black")
    turtle.onkeypress(None, "Left") # Ces 4 fonctions permettent d'arrêter les déplacements
    turtle.onkeypress(None, "Right")
    turtle.onkeypress(None, "Up")
    turtle.onkeypress(None, "Down")
    turtle.goto(-240,240)
    turtle.write("Bravo, vous avez trouvé la sortie !", font=("Arial", 11, "bold"))
    time.sleep(2)
    turtle.undo()
    for i in range(10,0,-1): # Compteur de 10 à 1 pour la fermeture de la fenêtre
        turtle.goto(-240,240)
        turtle.write("Cette fenêtre va se fermer automatiquement dans " + str(i) + " secondes !", font=("Arial", 11, "bold"))
        time.sleep(0.5) # créer une pause d'1 seconde dans le jeu 
        turtle.undo() # annule la dernière action, ici, ce sera la phrase de fermeture de la fenêtre
    turtle.bye() # Ferme la fenêtre turtle


#Troisième partie : Gestion déplacements

def tourner(valangle):
    """
    Arguments : Angle voulu ( chaque angle correspond à une direction, ex : 1 pour la gauche )
    But : Tourne la tortue pour avancer dans la direction voulue
    """
    global valangleprec # global permet de rendre une variable utilisable dans le script entier
    angle = valangleprec - valangle # Calcul la différence entre l'angle voulu et le dernier angle utilisé
    turtle.right(angle*90) # Calcul l'angle dont il faut tourner pour se trouver dans la bonne direction
    valangleprec = valangle # On stock le dernier angle utilisé 


def deplacement_moitie(pas):
    """
    Arguments : Pas 
    But : Permet d'avancer de rendre le joueur au milieu de la case où il se trouve
    """
    turtle.forward(pas/2)
    turtle.left(90)
    turtle.forward(pas/2)
    turtle.right(90)


def deplacement_passage():
    """
    But : Efface la case précédente, avance le pion sur la prochaine puis trace le pion du joueur
    """
    tracer_case(coo_prec,"wheat",calculer_pas(matrice)) # Trace la case sur la quelle se trouve le personnage
    turtle.color("black")
    deplacement_moitie(calculer_pas(lire_matrice(chateau))) # Replace le personnage au milieu de la case
    turtle.forward(calculer_pas(lire_matrice(chateau))) # Avance sur la prochaine case
    turtle.dot(calculer_pas(matrice)-(calculer_pas(matrice)/4),"red") # Redessine le personnage


def deplacement_objet(tup):
    """
    Arguments : Case où veux se rendre le joueur ( devant ,derrière ou sur les côtés )
    But : Récupère l'objet pour l'afficher dans l'inventaire
    """
    global indentation_objet, num_objet
    turtle.goto(70,140 - indentation_objet)
    turtle.write("N° " + str(num_objet) + ": " + str(dic_objets(fichier_objets)[tup]), font=("Arial", 10, "normal"))
    indentation_objet += 25
    num_objet += 1
    dict_objets.pop(tup,None)


def deplacement_porte(tup):
    """
    Arguments : Case où veux se rendre le joueur ( devant ,derrière ou sur les côtés )
    But : affiche la question de la porte voulue et affiche le résultat qui en dépend 
    """
    global rep
    turtle.goto(-240,240)
    turtle.write("Porte Fermée !", font=("Arial", 9, "bold"))
    time.sleep(0.5)
    turtle.undo()
    rep = turtle.textinput("Question :",dic_portes(fichier_portes)[tup][0]) # récupère le résultat de la question dans rep
    turtle.listen() # réenclenche l'écoute du clavier
    if rep != dic_portes(fichier_portes)[tup][1]: # cas où la réponse est fausse
        turtle.goto(-240,240)
        turtle.write("Mauvaise réponse, la porte reste fermée !", font=("Arial", 9, "bold"))
        time.sleep(0.5)
        turtle.undo()
    else: # cas où elle est correcte
        turtle.goto(-240,240)
        turtle.write("Bonne réponse, porte ouverte !", font=("Arial", 9, "bold"))
        time.sleep(0.5)
        turtle.undo()
        dict_portes.pop(tup,None) # retire la question du dictionnaire des portes sinon renvoie rien / None


def deplacement_arrivee():
    """
    But : Regarde si le joueur possède tous les objets pour mettre fin au jeu ou non
    """
    global LM, CM, coo_prec, tuple_arrivee
    if len(dict_objets) != 0: # N'arrête pas le jeu si tous les objets ne sont pas collectés
        turtle.goto(-240,240)
        turtle.write("Vous devez rassembler tous les objets !", font=("Arial", 10, "bold"))
        time.sleep(0.5)
        turtle.undo()
        turtle.onkeypress(deplacer_bas, "Down")
        return
    elif len(dict_objets) == 0: # Si tous les objets sont collectés
        coo_prec = (LM-1,CM) # On fait avancer le personnage sur la case d'arrivée puis on démarre la fonction d'arrêt
        tourner(2)
        deplacement_passage()
        shutdown()
        return

    
def deplacer_gauche():
    """
    But : Réalise le déplacement voulu
    """
    turtle.onkeypress(None, "Left") # Désactive la touche le temps d'éffectuer toute la fonction
    global LM, CM, coo_prec, list_murs, rep
    tuple_gauche = (LM,CM-1) # Case où veut se rendre le joueur ( à gauche de la position actuelle dans ce cas )
    if tuple_gauche in dict_portes: # Section pour passer une porte
        deplacement_porte(tuple_gauche)
        if rep != dic_portes(fichier_portes)[tuple_gauche][1]:
            turtle.onkeypress(deplacer_gauche, "Left") # Réactive la touche avant car fonction return juste après
            return # Sortie de fonction anticipée si la réponse est fausse
    if tuple_gauche in dict_objets: # Section pour ramasser un objet
        deplacement_objet(tuple_gauche)
    if tuple_gauche not in list_murs: # Section pour avancer 
        coo_prec = (LM-1,CM+1) # Case précédente
        tourner(1)
        deplacement_passage()
        CM -= 1 # Met à jour la position du joueur ( ici la colonne car on va à gauche )
    turtle.onkeypress(deplacer_gauche, "Left") # Réactive la touche à la fin de la fonction

# Les trois prochaines fonctions sont presque pareils que celle-ci sauf pour la dernière qui gère l'arrivée

def deplacer_droite():
    turtle.onkeypress(None, "Right")
    global LM, CM, coo_prec, list_murs, rep
    tuple_droit = (LM,CM+1)
    if tuple_droit in dict_portes:
        deplacement_porte(tuple_droit)
        if rep != dic_portes(fichier_portes)[tuple_droit][1]:
            turtle.onkeypress(deplacer_droite, "Right")
            return
    if tuple_droit in dict_objets:
        deplacement_objet(tuple_droit)
    if tuple_droit not in list_murs:
        coo_prec = (LM,CM)
        tourner(3)
        deplacement_passage()
        CM += 1
    turtle.onkeypress(deplacer_droite, "Right")


def deplacer_haut():
    turtle.onkeypress(None, "Up")
    global LM, CM, coo_prec, list_murs, rep
    tuple_haut = (LM-1,CM)
    if tuple_haut in dict_portes:
        deplacement_porte(tuple_haut)
        if rep != dic_portes(fichier_portes)[tuple_haut][1]:
            turtle.onkeypress(deplacer_haut, "Up")
            return
    if tuple_haut in dict_objets:
        deplacement_objet(tuple_haut)
    if tuple_haut not in list_murs:
        coo_prec = (LM,CM+1)
        tourner(4)
        deplacement_passage()
        LM -= 1
    turtle.onkeypress(deplacer_haut, "Up")


def deplacer_bas():
    turtle.onkeypress(None, "Down")
    global LM, CM, coo_prec, list_murs, rep, tuple_arrivee
    tuple_bas = (LM+1,CM)
    if tuple_bas == tuple_arrivee: # Section arrivée à la fin
        deplacement_arrivee()
    if tuple_bas in dict_portes:
        deplacement_porte(tuple_bas)
        if rep != dic_portes(fichier_portes)[tuple_bas][1]:
            turtle.onkeypress(deplacer_bas, "Down")
            return
    if tuple_bas in dict_objets:
        deplacement_objet(tuple_bas)
    if tuple_bas not in list_murs:
        coo_prec = (LM-1,CM)
        tourner(2)
        deplacement_passage()
        LM += 1
    turtle.onkeypress(deplacer_bas, "Down")


# Code global ---------------|---------------

#Affichage du chateau
turtle.up()
turtle.hideturtle()
turtle.tracer(0)
for liste in matrice: # Pour chaque ligne de la matrice
    L += 1
    for numero in liste: # Pour chaque colonne de la matrice
        C += 1
        if numero == 0: # 0 pour les passages
            tracer_case((L,C),"white",calculer_pas(matrice)) # Trace la case avec la couleur correspondante
        if numero == 1: # 1 pour les murs
            tracer_case((L,C),"grey",calculer_pas(matrice))
            list_murs.append((L,C))
        if numero == 2: # 2 pour l'arrivée
            tracer_case((L,C),"yellow",calculer_pas(matrice))
            tuple_arrivee = (L,C)
        if numero == 3: # 3 pour les portes
            tracer_case((L,C),"orange",calculer_pas(matrice))
        if numero == 4: # 4 pour les objets
            tracer_case((L,C),"green",calculer_pas(matrice))
    C = -1
    

#Affichage de l'inventaire
turtle.color("black")
turtle.goto(70,160)
turtle.write('Inventaire :', font=("Arial", 10, "bold"))


#Positionnement du joueur à l'entrée du château et le place au milieu de la case
turtle.goto(coordonnees((LM,CM),calculer_pas(lire_matrice(chateau)))) 
deplacement_moitie(calculer_pas(lire_matrice(chateau)))
turtle.dot(calculer_pas(matrice)-(calculer_pas(matrice)/4),"red")


#Fonctions d'écoute du clavier
turtle.listen() # Enclenche l'écoute des touches
turtle.onkeypress(deplacer_gauche, "Left") # Active la touche correspondante
turtle.onkeypress(deplacer_droite, "Right")
turtle.onkeypress(deplacer_haut, "Up")
turtle.onkeypress(deplacer_bas, "Down")
turtle.mainloop() # Créer une boucle infinie jusqu'à fermeture de la fenêtre
