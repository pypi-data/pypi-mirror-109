import os
import time
from datetime import datetime
from random import choice
from sys import platform

from pypresence import Presence
from tqdm import tqdm

from config import *


def clear_console():
    if platform == "linux" or platform == "darwin":
        os.system('clear')
    elif platform == "win32":
        os.system('cls')


def altearn_rpc():
    clear_console()
    print("    ___  _ _                         ____________  _____")
    print("   / _ \| | |                        | ___ \ ___ \/  __ \ ")
    print("  / /_\ \ | |_ ___  __ _ _ __ _ __   | |_/ / |_/ /| /  \/")
    print("  |  _  | | __/ _ \/ _` | '__| '_ \  |    /|  __/ | |")
    print("  | | | | | ||  __/ (_| | |  | | | | | |\ \| |    | \__/\ ")
    print("  \_| |_/_|\__\___|\__,_|_|  |_| |_| \_| \_\_|     \____/")
    print("")


def main():
    error_nbr = 0
    used_names = []
    while True:
        try:
            # Choisir un élément à afficher qui ne soit pas dans la liste des statuts déjà affichés
            name = choice(names)
            while name in used_names:
                name = choice(names)
            used_names.append(name)

            # Si les deux listes sont les mêmes réinitialiser used_names, tous les statuts sont passés
            list_a = set(names)
            list_b = set(used_names)
            if list_a == list_b:
                used_names = []

            # Récupérer ses informations
            client_id = ids[name]
            st = states[name]
            bu = buttons[name]
            lt = choice(quotes)

            # Se connecter au serveur RPC Discord
            RPC = Presence(client_id)
            RPC.connect()

            # Choisir entre le logo jour et le logo nuit
            if datetime.now().hour >= 19 or datetime.now().hour <= 7:
                li = large_image_night[name]
            else:
                li = large_image[name]

            # Envoyer les informations au RPC Discord
            RPC.update(state=st,
                       buttons=bu,
                       large_image=li,
                       large_text=lt)

            # Afficher une interface basique
            altearn_rpc()
            print("En cours d'affichage: " + str(name))
            print("Citation: " + str(lt))
            print("")
            print("Prochain changement :")

            # Attendre 60 secondes avec un barre de chargement
            for i in tqdm(range(int(change_time // 0.2)), bar_format="|{bar}|{remaining}{postfix}"):
                time.sleep(0.2)

            # Fermer la connection actuelle
            RPC.close()

            error_nbr = 0

        except KeyboardInterrupt:
            print("Fermeture de la connection RPC...")
            RPC.close()
            exit()

        except ConnectionRefusedError:
            if retry_number >= 2:
                if error_nbr == retry_number:
                    altearn_rpc()
                    print(
                        "Arrêt du programme aprés" + retry_number + "tentatives infructueuses de connection à Discord.")
                    exit()
            elif retry_number == 1:
                if error_nbr == retry_number:
                    altearn_rpc()
                    print("Arrêt du programme aprés une tentative infructueuse de connection à Discord.")
                    exit()
            else:
                error_nbr += 1
                altearn_rpc()
                print("Impossible de se connecter à Discord... (Tentative n°" + str(error_nbr) + ")")
                print("Avez-vous le client allumé ?")
                print(" ")
                print("Nouvelle tentative dans :")
                for i in tqdm(range(int(retry_time // 0.2)), bar_format="|{bar}|{remaining}{postfix}"):
                    time.sleep(0.2)


if __name__ == "__main__":
    main()