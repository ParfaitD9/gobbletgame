"""Module d'API du jeu Gobblet

Attributes:
    URL (str): Constante représentant le début de l'url du serveur de jeu.

Functions:
    * lister_parties - Récupérer la liste des parties reçus du serveur.
    * débuter_partie - Créer une nouvelle partie et retourne l'état de cette dernière.
    * récupérer_partie - Retrouver l'état d'une partie spécifique.
    * jouer_coup - Exécute un coup et retourne le nouvel état de jeu.
"""

import requests

URL = "https://pax.ulaval.ca/gobblet/api/"


def lister_parties(idul, secret):
    """Lister les parties

    Args:
        idul (str): idul du joueur
        secret (str): secret récupérer depuis le site de PAX

    Raises:
        PermissionError: Erreur levée lorsque le serveur retourne un code 401.
        RuntimeError: Erreur levée lorsque le serveur retourne un code 406.
        ConnectionError: Erreur levée lorsque le serveur retourne un code autre que 200, 401 ou 406

    Returns:
        list: Liste des parties reçues du serveur,
             après avoir décodé le json de sa réponse.
    """
    url = URL + 'parties/'
    
    r = requests.get(url, auth= (idul, secret))

    if r.status_code == 200:
        return r.json()
    elif r.status_code == 401:
        raise PermissionError(r.text)
    elif r.status_code == 406:
        raise RuntimeError(r.text)
    else:
        raise requests.exceptions.ConnectionError
    
def débuter_partie(idul, secret):
    """Débuter une partie

    Args:
        idul (str): idul du joueur
        secret (str): secret récupérer depuis le site de PAX

    Raises:
        PermissionError: Erreur levée lorsque le serveur retourne un code 401.
        RuntimeError: Erreur levée lorsque le serveur retourne un code 406.
        ConnectionError: Erreur levée lorsque le serveur retourne un code autre que 200, 401 ou 406

    Returns:
        tuple: Tuple constitué de l'identifiant de la partie,
            de l'état du plateau de jeu et de la liste des joueurs,
            après avoir décodé le JSON de sa réponse.
    """
    r = requests.post(URL + 'partie', auth=(idul, secret))

    if r.status_code == 200:
        data  : dict = r.json()
        id_partie, plateau, joueurs = data.get('id'), data.get('plateau'), data.get('joueurs')
        return (id_partie, plateau, joueurs)
    elif r.status_code == 401:
        raise PermissionError(r.text)
    elif r.status_code == 406:
        raise RuntimeError(r.text)
    else:
        raise requests.exceptions.ConnectionError

def récupérer_partie(id_partie, idul, secret):
    """Récupérer une partie

    Args:
        id_partie (str): identifiant de la partie à récupérer
        idul (str): idul du joueur
        secret (str): secret récupérer depuis le site de PAX

    Raises:
        PermissionError: Erreur levée lorsque le serveur retourne un code 401.
        RuntimeError: Erreur levée lorsque le serveur retourne un code 406.
        ConnectionError: Erreur levée lorsque le serveur retourne un code autre que 200, 401 ou 406

    Returns:
        tuple: Tuple constitué de l'identifiant de la partie,
            de l'état du plateau de jeu et de la liste des joueurs,
            après avoir décodé le JSON de sa réponse.
    """
    r = requests.get(URL + 'partie/{}'.format(id_partie), auth= (idul, secret))
    if r.status_code == 200:
        data : dict = r.json()
        return (data.get('id'), data.get('plateau'), data.get('joueurs'))
    elif r.status_code == 401:
        raise PermissionError(r.json().get('message'))
    elif r.status_code == 406:
        raise PermissionError(r.json().get('message'))
    else:
        raise requests.exceptions.ConnectionError

def jouer_coup(id_partie, origine, destination, idul, secret):
    """Jouer un coup

    Args:
        id_partie (str): identifiant de la partie
        origine (int ou list): l'origine est soit un entier représentant
                               le numéro de la pile du joueur ou une liste de 2 entier [x, y]
                               représentant le Gobblet sur le plateau.
        destination (list): la destination estune liste de 2 entier [x, y]
                            représentant le Gobblet sur le plateau
        idul (str): idul du joueur
        secret (str): secret récupérer depuis le site de PAX

    Raises:
        StopIteration: Erreur levée lorsqu'il y a un gagnant dans la réponse du serveur.
        PermissionError: Erreur levée lorsque le serveur retourne un code 401.
        RuntimeError: Erreur levée lorsque le serveur retourne un code 406.
        ConnectionError: Erreur levée lorsque le serveur retourne un code autre que 200, 401 ou 406

    Returns:
        tuple: Tuple constitué de l'identifiant de la partie,
            de l'état du plateau de jeu et de la liste des joueurs,
            après avoir décodé le JSON de sa réponse.
    """
    r = requests.put(
        URL + 'jouer/',
        auth= (idul, secret),
        json= {'id' : id_partie, 'origine': origine, 'destination' : destination},
    )

    if r.status_code == 200:
        if r.json().get('gagnant'):
            raise StopIteration(r.json().get('gagnant'))
        else:
            data = r.json()
            return (data.get('id'), data.get('plateau'), data.get('joueurs'))
    elif r.status_code == 401:
        raise PermissionError(r.json().get('message'))
    elif r.status_code == 406:
        raise PermissionError(r.json().get('message'))
    else:
        raise requests.exceptions.ConnectionError


    