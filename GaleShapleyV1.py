#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import json
from pprint import pprint
import matplotlib.pyplot as plt







#######################################################
######### Fonctions outils pour Gale-shapley  #########
#######################################################

def get_les_stages_non_proposes(etu, proposes, les_stages) :
    """ Cette fonction cherche à construire la liste des stages qui n'ont 
        pas encore été proposés à un étudiant donné.
        Elle prend 3 paramètres :
         - etu : un étudiant (Str)
         - proposes : l'ensemble des propositions ayant déjà été faites, quel
           que soit l'étudiant (dictionnaire : etudiant -> liste de stages) 
         - les_stages : la liste des stages existants (Liste de Str)

        Elle renvoie la liste des stages qui n'ont pas été proposés à l'étudiant etu (Liste de Str).
        S'il n'y a pas de solution (que tous les stages ont déjà été proposés à cet étudiant), 
        alors le résultat est une liste vide.
    """
    res = []
    propositions_deja_faites = proposes.get(etu, [])
    for stage in les_stages :
        if not stage in propositions_deja_faites :
            res.append(stage)
    return res
'''
def get_next_etudiant_disponible_et_appariable(les_etudiants, paires, proposes, les_stages) :
    """ Cette fonction choisi un étudiant non-apparié à qui on peut encore proposer au moins un stage.
        Elle prend 4 paramètres :
         - les_etudiants : la liste des étudiants (Liste de Str)
         - paires : la listes des appariements déjà faits (dictionnaire : étudiant -> stage)
         - proposes : l'ensemble des propositions ayant déjà été faites, 
           quel que soit l'étudiant (dictionnaire : etudiant -> liste de stages) 
         - les_stages : la liste des stages existants (Liste de Str)
        
        Elle retourne un étudiant qui n'est pas présent dans la liste des paires déjà réalisées 
        et tel qu'il y a au moins un stage auquel il n'ait pas été proposé. 
        Si pas de solution, renvoie None
    """

    # À FAIRE ....
    test=False
    i=0
    while not test and i<len(les_etudiants):
        if paires.get(les_etudiants[i],"")=="":
            j=0 
            while j<len(les_stages) and proposes.get(les_etudiants[i],"")!="":
                j+=1
            test = (j!=len(les_stages))
        if not test:
            i+=1
    if i>len(les_etudiants):i=0
                                
    return les_etudiants[i] # Bouchon
'''
def get_next_etudiant_disponible_et_appariable(les_etudiants, paires, proposes, les_stages):
    """ Cette fonction choisi un étudiant non-apparié à qui on peut encore proposer au moins un stage.
        Elle prend 4 paramètres :
         - les_etudiants : la liste des étudiants (Liste de Str)
         - paires : la listes des appariements déjà faits (dictionnaire : étudiant -> stage)
         - proposes : l'ensemble des propositions ayant déjà été faites, 
           quel que soit l'étudiant (dictionnaire : etudiant -> liste de stages) 
         - les_stages : la liste des stages existants (Liste de Str)
        
        Elle retourne un étudiant qui n'est pas présent dans la liste des paires déjà réalisées 
        et tel qu'il y a au moins un stage auquel il n'ait pas été proposé. 
        Si pas de solution, renvoie None
    """

    # Initialisation de l'indicateur de test et de l'index de l'étudiant

    test = False
    i = 0
    
    # On parcourt la liste des étudiants
    while not test and i < len(les_etudiants):
        etudiant = les_etudiants[i]
        
        # Vérifier si l'étudiant est déjà apparié
        if paires.get(etudiant, "") == "":
            if etudiant not in proposes:
                test=True
            else:
                
                # Vérifier s'il reste des stages à proposer à cet étudiant
                j = 0
                while j < len(les_stages) and les_stages[j] in proposes.get(etudiant, []):
                    j += 1
    
                test = (j < len(les_stages))  # Si un stage est encore proposé
            
        if not test:
            i += 1  # Passer à l'étudiant suivant
    
    # Si on a dépassé la taille de la liste, cela signifie qu'il n'y a pas d'étudiant disponible
    if i >= len(les_etudiants):
        return None  # Aucun étudiant disponible
    
    return les_etudiants[i]  # Retourner l'étudiant trouvé


def get_stage_prefere_parmi(stages_possibles, prefs) :
    """ Cette fonction calcule le stage préféré d'un étudiant au sein d'une liste réduite, 
        en respectant ses préférences. 
        Elle prend 2 paramètres :
         - stages_possibles : la liste des stages que l'on peut proposer à l'étudiant (Liste de Str)
         - prefs : la listes des préférences de l'étudiant, sous la forme d'une
                   liste ordonnée par préférence décroissante. Le premier stage de la liste est le 
                   stage préféré de l'étudiant. (Liste de Str)

        Elle retourne le stage (Str) de la liste stages_possibles ayant la plus grande valeur 
        selon les préférences prefs.

        Pré-requis : la liste des stages possibles doit être non-vide.
    """
    i=0
    while i<len(prefs) and not ( prefs[i] in stages_possibles ) : 
        i += 1

    return prefs[i]


def get_etudiant_affecte(stage_choisi, les_paires) :
    """ Fonction qui recherche si un étudiant est apparié avec un stage donné.
        Elle prend 2 paramètres :
         - stage_choisi : le stage dont on veut savoir s'il est apparié à un étudiant (Str)
         - les_paires : l'ensemble des appariements actuels, sous la forme 
           d'un dictionnaire {étudiant->stage}

        Retourn l'étudiant (Str) qui est actuellement en paire avec le stage stage_choisi
        Renvoie None le stage n'est pas apparié (s'il n'y a pas d'étudiant aparié à ce stage).
    """
    
    # À FAIRE ...
    res=None
    list_etud_paire = list(les_paires.keys())
    i=0
    while i<len(list_etud_paire) and les_paires[list_etud_paire[i]]!=stage_choisi:
        i+=1
    if i!=len(list_etud_paire):
        res=list_etud_paire[i]
    return res # Bouchon






#######################################################
########## Fonction principale Gale Shapley  ##########
#######################################################

def gale_shapley(etudiants, stages, prefs_etudiants, prefs_stages):
    """Prend en paramètre un graphe biparti de préférences et construit un appariement du jeu de données en utilisant l'algorithme de Gale-Shapley
       et retourne un appariement, ainsi que la durée de calcul.
       Paramètres : 
           - etudiants : la liste des étudiants (liste de strings)
           - stages : la liste des stages (liste de strings)
           - prefs_etudiants : préférences des étudiants (liste de strings, triée par ordre décroissant de préférence)
           - prefs_stages : préférences des stages (Dictionnaire avec un nom d'étudiant en clef et le pourcentage d'intéret en valeur)
       Retour : la liste des paires construites (dictionnaire : etudiant -> stage)
    """

    ###### Structure de données de travail
    # Mémoire de l'ensemble des propositions qui ont déjà été faites à chaque étudiant
    proposes = dict() # clef : étudiant, valeur : liste des stages déjà proposés

    # Mémoire des paires actuellement formées
    paires  = dict() # clef : étudiant, valeur : un stage


    ###### Boucle de travail
    etu = get_next_etudiant_disponible_et_appariable(etudiants, paires, proposes, stages)
    while etu != None :
        stages_possibles = get_les_stages_non_proposes(etu, proposes, stages)
        stage_choisi = get_stage_prefere_parmi(stages_possibles, prefs_etudiants[etu])
    
        proposes[etu] = proposes.get(etu, [])+[stage_choisi]
    
        if not stage_choisi in paires.values() :
            paires[etu] = stage_choisi
    
        else :
            old_etu = get_etudiant_affecte(stage_choisi, paires)

            if prefs_stages[stage_choisi][old_etu] < prefs_stages[stage_choisi][etu] :
                paires.pop(old_etu)
                paires[etu]=stage_choisi
    
    
        etu = get_next_etudiant_disponible_et_appariable(etudiants, paires, proposes, stages)

    return paires



if __name__ == "__main__":
    with open("data/jeu_de_test_initial.json", "r", encoding='utf-8') as f :
        data = json.load(f)

    etudiants       = data[0] # Récupération de la liste des étudiants
    stages          = data[1] # Récupération de la liste des stages
    prefs_etudiants = data[2] # Récupération des préférences des étudiants
    prefs_stages    = data[3] # Récupération des préférences des stages

    paires = gale_shapley(etudiants, stages, prefs_etudiants, prefs_stages)

    print("Test fonctionnel :")
    print("   Attendu  : {'Dora': 'Topographie', 'Indiana Jones': 'Archéologie', 'Bob': 'Sponge factory'}")
    print(f"   Résultat : {paires}")
    print()
