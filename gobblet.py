"""Module Gobblet

Attributes:
    GOBBLET_REPRÉSENTATION (dict): Constante représentant
    les gobblet des joueurs.

Functions:
    * interpréteur_de_commande - Génère un interpréteur de commande.
    * formater_un_gobblet - Formater la représentation graphique d'un Gobblet.
    * formater_un_joueur - Formater la représentation graphique
        d'un joueur et de ses piles.
    * formater_plateau - Formater la représentation graphique d'un plateau.
    * formater_jeu - Formater la représentation graphique d'un jeu.
    * formater_les_parties - Formater la liste des dernières parties.
    * récupérer_le_coup - Demander le prochain coup à jouer au joueur.
"""
from argparse import ArgumentParser
import argparse
from ntpath import join
from api import récupérer_partie

# Voici la représentation des Gobblets, n'hésitez pas à l'utiliser.
# 1 pour le joueur 1, 2 pour le joueur 2.
GOBBLET_REPRÉSENTATION = {
    1: ["▫", "◇", "◯", "□"],
    2: ["▪", "◆", "●", "■"],
}


def interpréteur_de_commande():
    """Interpreteur de commande

    Returns:
        Namespace: Un objet Namespace tel que retourné par parser.parse_args().
                   Cette objet aura l'attribut IDUL représentant
                   l'idul du joueur et l'attribut lister
                   qui est un booléen True/False.
    """
    parser = ArgumentParser()

    parser.add_argument('IDUL')
    parser.add_argument(
        '--lister', '-l',
        type=bool,
        action=argparse.BooleanOptionalAction,
        help='Lister les parties existantes'
    )

    return parser.parse_args()


def formater_un_gobblet(gobblet):
    """Formater un Gobblet

    Args:
        gobblet (list): liste vide ou de 2 entier [x, y]
        représentant le Gobblet

    Returns:
        str: Représentation du Gobblet pour le bon joueur
    """
    if gobblet:
        joueur, taille = gobblet
        return " {} ".format(GOBBLET_REPRÉSENTATION[joueur][taille])
    return "   "


def formater_un_joueur(joueur):
    """Formater un joueur

    Args:
        joueur (dict): dictionnaire contenant le nom du joueurs
        et ses piles de Gobblet

    Returns:
        str: Représentation du joueur et de ses piles de Gobblet
    """

    piles = ' '.join([
        formater_un_gobblet(gobblet) for gobblet in joueur.get('piles')
        ]
    )

    return "{}: {}".format(joueur.get('nom'), piles)
    

def formater_plateau(plateau):
    """Formater un plateau

    Args:
        plateau (list): plateau de jeu 4 x 4

    Returns:
        str: Représentation du plateau avec ses Gobblet
    """
    
    return ' ───┼───┼───┼───\n'.join( ['{}'.format(3-i) + '|'.join(
        [formater_un_gobblet(gobblet) for gobblet in ligne]
        ) + '\n' for i, ligne in enumerate(plateau)]
    ) + "  0   1   2   3 "
    

def formater_jeu(plateau, joueurs):
    """Formater un jeu

    Args:
        plateau (list): plateau de jeu 4 x 4
        joueurs (list): list de dictionnaire contenant le nom du joueurs
        et ses piles de Gobblet

    Returns:
        str: Représentation du jeu
    """
    s = max(len(joueurs[0].get('nom')), len(joueurs[1].get('nom')))
    j_1 = formater_un_joueur(joueurs[0])
    j_2 = formater_un_joueur(joueurs[1])
    
    return (
        "{}   0   1   2 \n".format(' '*s) +
        "{}\n".format(j_1 if s == len(joueurs[0].get('nom')) else 
                ' '*(s - len(joueurs[0].get('nom'))) + j_1) +
        "{}\n\n".format(j_2 if s == len(joueurs[1].get('nom')) else 
                ' '*(s - len(joueurs[1].get('nom'))) + j_2) +
        "{}".format(formater_plateau(plateau))
    )


def formater_les_parties(parties):
    """Formater une liste de parties

    L'ordre doit être exactement la même que ce qui est passé en paramètre.

    Args:
        parties (list): Liste des parties

    Returns:
        str: Représentation des parties
    """
    args = interpréteur_de_commande()
    
    return '\n\n'.join(
        [
            f"ID : {partie.get('id')}\nDate : {partie.get('date')}\n"
            f"Joueurs : {' & '.join(partie.get('joueurs'))}\n "
            f"Gagnant : {partie.get('gagnant')}"
            for partie in parties.get('parties')
        ]
    )


def récupérer_le_coup():
    """Récupérer le coup

    Returns:
        tuple: Un tuple composé d'un origine et de la destination.
                L'origine est soit un entier représentant le numéro de la pile
                du joueur ou une liste de 2 entier [x, y] représentant
                le Gobblet sur le plateau. La destination est une liste
                de 2 entier [x, y] représentant le Gobblet sur le plateau

    Examples:
        Quel Gobblet voulez-vous déplacer:
        Donnez le numéro de la pile (p) ou la position sur le plateau (x,y): 0
        Où voulez-vous placer votre Gobblet (x,y): 0,1

        Quel Gobblet voulez-vous déplacer:
        Donnez le numéro de la pile (p) ou la position sur le plateau (x,y): 2,3
        Où voulez-vous placer votre Gobblet (x,y): 0,1
    """
    
    print('Quel Gobblet voulez-vous déplacer:')
    org = input('Donnez le numéro de la pile (p) ou la position sur le plateau (x,y): ')
    dst = input('Où voulez-vous placer votre Gobblet (x,y): ')

    if len(org) > 1:
        org = [int(coord) for coord in org.split(',')]
    else:
        org = int(org)

    dst = [int(coord) for coord in dst.split(',')]

    return (org, dst)


if __name__ == '__main__':
    pass
