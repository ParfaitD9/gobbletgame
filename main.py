# -*- coding: utf-8 -*-
"""Jeu Gobblet

Ce programme permet de joueur au jeu Gobblet.
"""
from api import débuter_partie, jouer_coup, lister_parties
from gobblet import (
    formater_jeu,
    formater_les_parties,
    interpréteur_de_commande,
    récupérer_le_coup,
)

# Mettre ici votre secret récupérer depuis le site de PAX
SECRET = "<your_secret>"


if __name__ == "__main__":
    args = interpréteur_de_commande()
    if args.lister:
        parties = lister_parties(args.IDUL, SECRET)
        print(formater_les_parties(parties))
    else:
        id_partie, plateau, joueurs = débuter_partie(args.IDUL, SECRET)
        while True:
            # Afficher la partie
            print(formater_jeu(plateau, joueurs))
            # Demander au joueur de choisir son prochain coup
            origine, destination = récupérer_le_coup()
            # Envoyez le coup au serveur
            id_partie, plateau, joueurs = jouer_coup(
                id_partie, origine, destination, args.IDUL, SECRET)
