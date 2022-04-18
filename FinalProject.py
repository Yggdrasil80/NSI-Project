from EncryptMethods import *
from time import sleep
import json
import os


class Options:
    is_init: bool = False
    use_keystore: bool = True


class Keystore:
    keys: dict = {}


def start():
    if not os.path.exists("data/options.json") or not bool(json.load(open("data/options.json"))["is_init"]):
        first_launch()
    else:
        main_menu()


def print_header():
    os.system("cls") if os.name == "nt" else os.system("clear")
    print("===========================================================")
    print("  _____ _ _ _              _____                  _        ")
    print(" |_   _| | (_)            / ____|                | |       ")
    print("   | | | | |_  ___ ___   | |     _ __ _   _ _ __ | |_ ___  ")
    print("   | | | | | |/ __/ _ \  | |    | '__| | | | '_ \| __/ _ \ ")
    print("  _| |_| | | | (_| (_) | | |____| |  | |_| | |_) | || (_) |")
    print(" |_____|_|_|_|\___\___/   \_____|_|   \__, | .__/ \__\___/ ")
    print("                                       __/ | |             ")
    print("                                      |___/|_|             ")
    print("        Cryptez tous vos messages, en un instant !         ")
    print("    Spécialité NSI - Première année - Louis de Chorivit    ")
    print("===========================================================")
    print(" ")


def first_launch():
    print_header()
    if not os.path.exists("data"):
        os.mkdir("data")

    with open("data/options.json", "x") as json_file:
        json.dump({"is_init": True, "use_keystore": False}, json_file, indent=4, default=lambda o: o.__dict__)

    print("  Bienvenue dans la configuration de mon programme de cryptage !")
    print("Vous pouvez utiliser le Keystore pour sauvegarder automatiquement")
    print("vos clés de cryptage et ne pas avoir à les retenir.")
    use_keystore: str = input("Souhaitez-vous utiliser le keystore ? (O/N) ")

    if use_keystore == "O" or use_keystore == "o":
        with open("data/options.json", "wr+") as json_file:
            options: Options = json.load(json_file)
            print("Vous avez choisi d'utiliser le keystore." + str(options))
            options["use_keystore"] = True
            json.dump(options, json_file, indent=4, default=lambda o: o.__dict__)

        with open("data/keystore.json", "x") as json_file:
            json.dump({"test_text": "test_key"}, json_file, indent=4, default=lambda o: o.__dict__)

    print("Configuration terminée ! Les fichiers de configuration ont été sauvegardés dans le dossier ~/data.")


def main_menu():
    print_header()
    print("Que souhaitez-vous faire ?")
    print("1. Encrypter un message")
    print("2. Décrypter un message")
    print("3. Quitter")
    choice: int = int(input("Votre choix : "))

    if choice == 1:
        encrypt_menu()
    elif choice == 2:
        decrypt_menu()
    elif choice == 3:
        print("Au revoir ! Fermeture dans quelques secondes...")
        sleep(3)
        exit()


def encrypt_menu():
    print_header()
    print("Que souhaitez-vous faire ?")
    print("1. Encrypter avec code ROT13")
    print("2. Encrypter avec le code de César")
    print("3. Encrypter avec le code de Vigenère")
    print("4. Encrypter avec le carré de Polybe")
    print("5. Retour au menu principal")
    choice: int = int(input("Votre choix : "))

    if choice == 1:
        encrypt(Methods.ROT13_METHOD)
    elif choice == 2:
        encrypt(Methods.CESAR_METHOD)
    elif choice == 3:
        encrypt(Methods.VIGENERE_METHOD)
    elif choice == 4:
        encrypt(Methods.POLYBE_METHOD)
    elif choice == 5:
        main_menu()


def encrypt(method: IEncryptMethod):
    print_header()
    message: str = input("Entrez le message à crypter : ")
    encrypted_message: EncryptEntry = method.encrypt(message, input("Entrez la clé de cryptage : ")) if is_key_required(
        method) else method.encrypt_without_key(message)

    print("Voici le message crypté : " + encrypted_message.text)
    print("Voici la clé de cryptage : " + encrypted_message.key)

    with open("data/options.json", "wr+") as json_file:
        options: Options = json.load(json_file)
        if options.use_keystore:
            print("Sauvegarde de la clé de cryptage dans le keystore...")

            with open("data/keystore.json", "wr+") as keystore_json_file:
                keystore: Keystore = json.load(keystore_json_file)
                keystore.keys[encrypted_message.text] = encrypted_message.key
                json.dump(keystore, keystore_json_file, indent=4, default=lambda o: o.__dict__)

            print("Sauvegarde terminée !")

    input("Appuyez sur entrée pour continuer...")
    main_menu()


def decrypt_menu():
    print_header()
    print("Que souhaitez-vous faire ?")
    print("1. Décrypter avec code ROT13")
    print("2. Décrypter avec le code de César")
    print("3. Décrypter avec le code de Vigenère")
    print("4. Décrypter avec le carré de Polybe")
    print("5. Retour au menu principal")
    choice: int = int(input("Votre choix : "))

    if choice == 1:
        decrypt(Methods.ROT13_METHOD)
    elif choice == 2:
        decrypt(Methods.CESAR_METHOD)
    elif choice == 3:
        decrypt(Methods.VIGENERE_METHOD)
    elif choice == 4:
        decrypt(Methods.POLYBE_METHOD)
    elif choice == 5:
        main_menu()


def decrypt(method: IEncryptMethod):
    print_header()
    message: str = input("Entrez le message à décrypter : ")

    with open("data/options.json", "wr+") as json_file:
        options: Options = json.load(json_file)

        if options.use_keystore:
            with open("data/keystore.json", "wr+") as keystore_json_file:
                keystore: Keystore = json.load(keystore_json_file)
                key = keystore.keys[message] if message in keystore.keys else ""

                if key == "":
                    key = input("Impossible de charger la clé depuis le Keystore, entrez la clé de cryptage : ")
        else:
            key = input("Entrez la clé de cryptage : ")

        print("Voici le message décrypté : " + method.decrypt(EncryptEntry(key, message)))
        input("Appuyez sur entrée pour continuer...")
        main_menu()


# For PyCharm only
if __name__ == '__main__':
    start()
