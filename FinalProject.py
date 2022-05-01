from random import randint
from time import sleep
from string import *
import json
import os


class Options(object):
    """
    Cette class représente les options du programme.
    """

    def __init__(self, json_file):
        """
        Constructeur de la classe Options.
        :param json_file: Le contenu du fichier JSON contenant les options, afin de le désérialiser et le convertir
        en objet Python.
        """
        self.__dict__ = json.loads(json_file)

    is_init: bool
    use_keystore: bool


class Keystore(object):
    """
    Cette class représente le stockage des clés de chiffrement.
    """

    def __init__(self, json_file):
        """
        Constructeur de la classe Keystore.
        :param json_file: Le contenu du fichier JSON contenant les clés, afin de le désérialiser et le convertir
        en objet Python.
        """
        self.__dict__ = json.loads(json_file)

    keys: dict


class EncryptEntry:
    """
    Cette classe est un objet qui contient les informations d'un texte crypté.
    On peut trouver dans ces informations son contenu et sa clé de décryptage.
    """

    def __init__(self, key: str, text: str):
        """
        Constructeur de la classe EncryptEntry.

        :argument str key: La clé de décryptage du texte.
        :argument str text: Le contenu du texte crypté.
        """
        self.key = key
        self.text = text


class IEncryptMethod:
    """
    Cette interface permet de définir les fonctions qui seront utilisées et communes à toutes les méthodes
    de cryptage (ROT13, Code de César, etc)
    """

    # On définit une variable de tous les caractères à ignorer (les espaces, les caractères spéciaux, etc.)
    to_skip = whitespace + punctuation

    def encrypt_without_key(self, text: str) -> EncryptEntry:
        """
        Cette fonction crypte le texte passé en argument.

        :param str text: Le texte à crypter
        :return: Une EncryptEntry avec les informations du cryptage
        """
        pass

    def encrypt(self, key: str, text: str) -> EncryptEntry:
        """
        Cette fonction crypte le texte passé en argument.

        :param str key: La clé de cryptage du texte
        :param str text: Le texte à crypter
        :return: Une EncryptEntry avec les informations du cryptage
        """
        pass

    def decrypt(self, entry: EncryptEntry) -> str:
        """
        Cette fonction décrypte le texte crypté passé en argument.

        :param EncryptEntry entry: Une EncryptEntry avec les informations du cryptage
        :return: Le texte décrypté
        """
        pass


class EncryptionException(Exception):
    """
    Cette erreur est levée lorsque le programme ne parvient pas à crypter ou décrypter quelque chose.
    """
    pass


def get_translator(gap: int) -> dict[int, int]:
    """
    Ces chaines de caractères servent à utiliser une nouvelle fonctionnalité de Python 3.0.
    Cette fonctionnalité permet d'associer à un caractère un autre caractère.
    Par exemple ici, dans la variable upper_translator avec un décalage de 13, le caractère 'A'
    sera associé au 'N', ce qui correspond à un décalage de 13 positions dans l'alphabet, et
    ainsi de suite pour toutes les lettres de l'alphabet, en majuscules et en minuscules.
    Les string.ascii_uppercase et string.ascii_lowercase sont des variables contenant les lettres
    de l'alphabet en majuscules et minuscules, fournies par Python par défaut.
    Les [gap:] et [:gap] permettent de décaler les lettres de l'alphabet, avec un écart donné.

    On obtient donc par exemple pour un décalage de 13:
    translator = {'A': 'N', 'B': 'O', 'C': 'P', ..., 'Z': 'M', 'a': 'n', 'b': 'o', ..., 'z': 'm'}

    :param int gap: Le décalage à appliquer à l'alphabet
    :return Le dictionnaire servant à la traduction
    """
    return str.maketrans(ascii_uppercase + ascii_lowercase,
                         ascii_uppercase[gap:] + ascii_uppercase[:gap]
                         + ascii_lowercase[gap:] + ascii_lowercase[:gap])


class ROT13(IEncryptMethod):
    def encrypt_without_key(self, text: str) -> EncryptEntry:
        # Cette fonction crypte le texte passé en argument, via la fonction translate de la classe str,
        # avec un décalage de 13, comme l'indique la méthode de cryptage ROT13.
        # Pour plus d'informations, voir la documentation de IEncryptMethod.
        return self.encrypt(str(13), text)

    def encrypt(self, key: str, text: str) -> EncryptEntry:
        # Cette fonction crypte le texte passé en argument, via la fonction translate de la classe str,
        # avec un décalage de 13, comme l'indique la méthode de cryptage ROT13.
        # Pour plus d'informations, voir la documentation de IEncryptMethod.
        return EncryptEntry("Empty", text.translate(get_translator(13)))

    def decrypt(self, entry: EncryptEntry) -> str:
        # Cette fonction décrypte le texte crypté passé en argument, via la fonction translate de la classe str,
        # avec un décalage inverse de 13.
        # Pour plus d'informations, voir la documentation de IEncryptMethod.
        return entry.text.translate(get_translator(13))


class Cesar(IEncryptMethod):
    def encrypt_without_key(self, text: str) -> EncryptEntry:
        # Cette fonction crypte le texte passé en argument, via la fonction translate de la classe str,
        # avec un décalage aléatoire entre 1 et 25.
        # Pour plus d'informations, voir la documentation de IEncryptMethod.
        return self.encrypt(str(randint(1, 25)), text)

    def encrypt(self, key: str, text: str) -> EncryptEntry:
        # Cette fonction crypte le texte passé en argument, via la fonction translate de la classe str,
        # avec un décalage donné.
        # Pour plus d'informations, voir la documentation de IEncryptMethod.
        return EncryptEntry(key, text.translate(get_translator(int(key))))

    def decrypt(self, entry: EncryptEntry) -> str:
        # Cette fonction décrypte le texte crypté passé en argument, via la fonction translate de la classe str,
        # avec un décalage donné.
        # Pour plus d'informations, voir la documentation de IEncryptMethod.
        # Ici, on ajoute un "-" devant la clé de décryptage (correspondant au décalage dans l'alphabet)
        # afin de pouvoir retrouver l'alphabet original, à la différence du ROT13. L'alphabet étant composé de 26
        # lettres, si on décale deux fois de 13 lettres, on obtient un décalage de 26, ce qui donne l'alphabet original.
        return entry.text.translate(get_translator(- int(entry.key)))


class Vigenere(IEncryptMethod):
    def encrypt_without_key(self, text: str) -> EncryptEntry:
        return self.encrypt("I love NSI", text)

    def encrypt(self, key: str, text: str) -> EncryptEntry:
        # On retire tous les espaces de la clé, et on la met en majuscule, pour avoir une clé valide.
        key = key.replace(" ", "").upper()
        # On met le texte à déchiffrer en majuscule, pour éviter les décalages et erreurs dues à la casse. En effet,
        # le code ASCII des lettres est différent en majuscule et en minuscule.
        text = text.upper()

        for indice, lettre in enumerate(text):
            # On décale la lettre de la clé, en fonction de l'indice de la lettre dans la clé.
            # Si la lettre décalée est supérieure à la lettre de la clé, on prend la lettre de la clé correspondante.
            # La fonction ord() de la classe string permet de retourner le code ASCII d'une lettre.
            # La fonction chr() de la classe string permet de retourner la lettre correspondant au code ASCII.
            # On doit ajouter ord('A') soit 65 pour obtenir le code ASCII du debut de l'alphabet.
            # Explications :
            # 1 - Le text[:indice] permet de récupérer le texte jusqu'à l'indice courant.
            # 2 - On utilise ord(lettre) pour obtenir le code ASCII de la lettre courante.
            # 3 - On ajoute à cette valeur le code ASCII de la lettre de la clé.
            # 4 - On ajoute ord('A') pour obtenir le code ASCII de la lettre de départ de l'alphabet.
            # 5 - On récupère le code ASCII correspondant à toute cette addition avec la fonction chr()
            # 6 - On ajoute enfin text[indice + 1:] pour obtenir le texte après l'indice courant.
            text = text[:indice] + chr(((ord(lettre) + ord(key[indice % len(key)])) % 26) + ord('A')) + text[
                                                                                                        indice + 1:]
        return EncryptEntry(key, text)

    def decrypt(self, entry: EncryptEntry) -> str:
        # On retire tous les espaces de la clé, et on la met en majuscule, pour avoir une clé valide.
        entry.key = entry.key.replace(" ", "").upper()
        # On met le texte à déchiffrer en majuscule, pour éviter les décalages et erreurs dues à la casse. En effet,
        # le code ASCII des lettres est différent en majuscule et en minuscule.
        entry.text = entry.text.upper()

        for indice, lettre in enumerate(entry.text):
            # On réalise la même opération que pour le chiffrement, mais on inverse l'étape 3 pour retrouver
            # la lettre originale.
            # Pour comprendre cette opération, il faut regarder les explications de la fonction encrypt() ci-dessus.
            entry.text = entry.text[:indice] + chr(
                ((ord(lettre) - ord(entry.key[indice % len(entry.key)])) % 26) + ord('A')) + entry.text[indice + 1:]
        return entry.text


class Polybe(IEncryptMethod):
    # Un carré de Polybe est une grille de 5x5 sous ce format:
    # 0 1 2 3 4 5
    # 1 A B C D E
    # 2 F G H I J
    # 3 K L M N O
    # 4 P Q R S T
    # 5 U V W X Y
    # Il consiste à donner à chaque lettre ses coordonnées dans la grille. Le Z n'est pas crypté
    translator: dict[str, str] = {'A': '11', 'B': '12', 'C': '13', 'D': '14', 'E': '15', 'F': '21', 'G': '22',
                                  'H': '23', 'I': '24', 'J': '25', 'K': '31', 'L': '32', 'M': '33', 'N': '34',
                                  'O': '35', 'P': '41', 'Q': '42', 'R': '43', 'S': '44', 'T': '45', 'U': '51',
                                  'V': '52', 'W': '53', 'X': '54', 'Y': '55', 'Z': 'Z'}
    untranslator: dict[str, str] = {'11': 'A', '12': 'B', '13': 'C', '14': 'D', '15': 'E', '21': 'F', '22': 'G',
                                    '23': 'H', '24': 'I', '25': 'J', '31': 'K', '32': 'L', '33': 'M', '34': 'N',
                                    '35': 'O', '41': 'P', '42': 'Q', '43': 'R', '44': 'S', '45': 'T', '51': 'U',
                                    '52': 'V', '53': 'W', '54': 'X', '55': 'Y', 'Z': 'Z'}

    def encrypt_without_key(self, text: str) -> EncryptEntry:
        return self.encrypt("I love NSI", text)

    def encrypt(self, key: str, text: str) -> EncryptEntry:
        text = text.upper()
        # On crée une chaîne de caractères correspondant au résultat
        result: str = ""

        for indice, lettre in enumerate(text):
            # Si le caractère est à ignorer, on l'ajoute simplement au résultat sans le crypter
            if lettre in self.to_skip:
                result += lettre
                continue

            # On récupère les coordonnées de la lettre dans la grille, et on les ajoute au résultat
            result += self.translator[lettre]

        return EncryptEntry("Empty", result)

    def decrypt(self, entry: EncryptEntry) -> str:
        entry.text = entry.text.upper()
        # On utilise un boolean qui sert à indiquer si le texte a été décalé ou non
        skipped: bool = False
        # On crée une chaîne de caractères correspondant au résultat
        result: str = ""

        # On ne peut pas utiliser exactement la même méthode pour le décryptage que pour le chiffrement,
        # car les coordonnées sont par groupes de 2 caractères.
        for indice in range(0, len(entry.text) - 1):
            # Si le caractère est à ignorer, on l'ajoute simplement au résultat sans le décrypter
            # On inverse aussi le boolean pour indiquer que le texte a été décalé, puis on passe à l'élément suivant de la boucle
            if entry.text[indice] in whitespace + punctuation:
                result += entry.text[indice]
                skipped = not skipped
                continue

            # On vérifie si l'indice est divisible par 2 en fonction du boolean skipped
            # Si le boolean est à True, donc que le texte a été décalé, l'indice ne doit pas être divisible par 2
            # Si le boolean est sur False, l'indice doit être divisible par 2
            if indice % 2 == (0 if not skipped else 1):
                # On décode simplement le caractère de l'indice, et son suivant et on les ajoute au résultat
                result += self.untranslator[entry.text[indice:indice + 2]]

        return result


def is_key_required(method: IEncryptMethod) -> bool:
    """
    Vérifie si une clé est nécessaire pour le chiffrement d'un texte, en fonction de la méthode de chiffrement.
    Si la méthode de chiffrement est ROT13 ou Polybius, on n'a pas besoin de clé
    :param method: La méthode de chiffrement à vérifier.
    :return: True si une clé est nécessaire, False sinon.
    """
    return False if (isinstance(method, ROT13) or isinstance(method, Polybe)) else True


def start():
    """
    Cette fonction démarre le programme.
    Si le fichier des options n'existe pas, ou que dans ce fichier il n'est pas indiqué que le programme
    est initialisé, on lance la procédure d'initialisation
    Sinon, on affiche le menu principal classique
    """
    if not os.path.exists("data/options.json") or not bool(json.load(open("data/options.json"))["is_init"]):
        first_launch()
    else:
        main_menu()


def print_header():
    """
    Cette fonction affiche le message d'entête du programme
    """
    os.system("cls") if os.name == "nt" else os.system("clear")
    # On commence par effacer la console. Si le système d'exploitation est Windows (nommé "nt"),
    # on utilise la commande cls, sinon la commande clear
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
    """
    Cette fonction est appelée lors de la première exécution du programme.
    """
    print_header()
    # Si le dossier data contenant les fichiers du programme n'existe pas, on le crée
    if not os.path.exists("data"):
        os.mkdir("data")

    # On crée le fichier options.json, qui contiendra les options du programme
    with open("data/options.json", "x") as json_file:
        # On initialise les options du programme
        options: Options = Options("{}")
        # On marque le programme comme initialisé
        options.is_init = True
        # On écrit les options dans le fichier
        # Le paramètre indent=4 permet d'ajouter des espaces pour que le JSON soit lisible
        # Le paramètre default=vars permet de transformer chaque attribut de l'objet en une valeur
        json.dump(options, json_file, indent=4, default=vars)

    # On affiche le message de bienvenue
    print("  Bienvenue dans la configuration de mon programme de cryptage !")
    print("Vous pouvez utiliser le Keystore pour sauvegarder automatiquement")
    print("vos clés de cryptage et ne pas avoir à les retenir.")
    # On demande à l'utilisateur s'il veut utiliser le Keystore, pour sauvegarder ses clés de cryptage
    use_keystore: str = input("Souhaitez-vous utiliser le keystore ? (O/N) ")

    # Si l'utilisateur a choisi de l'utiliser, donc qu'il a répondu "O", on lance la procédure de création du Keystore
    if use_keystore == "O" or use_keystore == "o":
        # On ouvre le fichier des options
        with open("data/options.json", "r+") as json_file:
            # On désérialise les options en tant qu'objet, avec le contenu du fichier JSON
            options: Options = Options(json_file.read())
            # On indique que le Keystore est utilisé
            options.use_keystore = True
            # On se place au début du fichier, afin de le réécrire
            json_file.seek(0)
            # On réécrit les options dans le fichier
            json.dump(options, json_file, indent=4, default=vars)

        # On créé le fichier Keystore
        with open("data/keystore.json", "x") as json_file:
            # On initialise le Keystore, avec un json contenant aucune clé
            keystore: Keystore = Keystore("{\"keys\":{}}")
            # On écrit le Keystore dans le fichier
            json.dump(keystore, json_file, indent=4, default=vars)

    # On attend que l'utilisateur appuie sur une touche pour afficher le menu principal
    print("Configuration terminée ! Les fichiers de configuration ont été sauvegardés dans le dossier ~/data.")
    print("Appuyez sur entrée pour continuer.")
    input()
    main_menu()


def main_menu():
    """
    Cette fonction affiche le menu principal du programme.
    """
    print_header()
    # On propose à l'utilisateur de choisir une action via les chiffres 1, 2 et 3
    print("Que souhaitez-vous faire ?")
    print("1. Encrypter un message")
    print("2. Décrypter un message")
    print("3. Quitter")
    choice: int = int(input("Votre choix : "))

    if choice == 1:
        # Si l'utilisateur a choisi d'encrypter un message, on affiche le menu d'encryption
        encrypt_menu()
    elif choice == 2:
        # Si l'utilisateur a choisi de décrypter un message, on affiche le menu de décryptage
        decrypt_menu()
    elif choice == 3:
        # Si l'utilisateur a choisi de quitter, on quitte le programme au bout de trois secondes
        print("Au revoir ! Fermeture dans quelques secondes...")
        sleep(3)
        exit()


def encrypt_menu():
    """
    Cette fonction affiche le menu d'encryption.
    """
    print_header()
    print("Que souhaitez-vous faire ?")
    print("1. Encrypter avec code ROT13")
    print("2. Encrypter avec le code de César")
    print("3. Encrypter avec le code de Vigenère")
    print("4. Encrypter avec le carré de Polybe")
    print("5. Retour au menu principal")
    choice: int = int(input("Votre choix : "))

    if choice == 1:
        encrypt(ROT13())
    elif choice == 2:
        encrypt(Cesar())
    elif choice == 3:
        encrypt(Vigenere())
    elif choice == 4:
        encrypt(Polybe())
    elif choice == 5:
        main_menu()


def encrypt(method: IEncryptMethod):
    """
    Cette fonction permet d'encrypter un message avec un algorithme de chiffrement.
    :param method: L'algorithme de chiffrement à utiliser
    """
    print_header()
    # On demande à l'utilisateur de saisir un message à encrypter
    message: str = input("Entrez le message à crypter : ")

    # On encrypte le message, en demandant la clé de chiffrement à l'utilisateur si elle est requise
    encrypted_message: EncryptEntry = method.encrypt_without_key(message) if not is_key_required(method) \
        else method.encrypt(input("Entrez la clé de cryptage : "), message)

    # On affiche le message encrypté
    print("Voici le message crypté : " + encrypted_message.text)

    # Si une clé de chiffrement était nécessaire, on l'affiche
    if is_key_required(method):
        print("Voici la clé de cryptage : " + encrypted_message.key)

    # On ouvre le fichier des options
    with open("data/options.json", "r+") as json_file:
        options: Options = Options(json_file.read())
        # Si l'utilisateur a choisi d'utiliser le KeyStore, on l'ajoute la clé dedans
        if options.use_keystore and is_key_required(method):
            print("Sauvegarde de la clé de cryptage dans le keystore...")

            # Pour pouvoir l'ajouter, on ouvre le fichier keystore
            with open("data/keystore.json", "r+") as keystore_json_file:
                keystore: Keystore = Keystore(keystore_json_file.read())
                # On ajoute la clé, dans le format "message encrypté : clé"
                keystore.keys[encrypted_message.text] = encrypted_message.key
                # On se replace au début du fichier
                keystore_json_file.seek(0)
                # On sauvegarde le KeyStore dans le fichier
                json.dump(keystore, keystore_json_file, indent=4, default=vars)

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
        decrypt(ROT13())
    elif choice == 2:
        decrypt(Cesar())
    elif choice == 3:
        decrypt(Vigenere())
    elif choice == 4:
        decrypt(Polybe())
    elif choice == 5:
        main_menu()


def decrypt(method: IEncryptMethod):
    """
    Cette fonction permet de décrypter un message avec un algorithme de chiffrement donné.
    :param method: L'algorithme de chiffrement à utiliser
    """
    print_header()
    message: str = input("Entrez le message à décrypter : ")

    # On ouvre le fichier des options
    with open("data/options.json", "r+") as json_file:
        options: Options = Options(json_file.read())
        # On initialise la variable qui contient la clé de chiffrement
        key: str = "Empty"

        # Si une clé de chiffrement est requise pour cette méthode, on essaie de la récupérer
        if is_key_required(method):
            # Si l'utilisateur a choisi d'utiliser le KeyStore, on essaie de la récupérer
            if options.use_keystore:
                # On ouvre le fichier du keystore
                with open("data/keystore.json", "r+") as keystore_json_file:
                    keystore: Keystore = Keystore(keystore_json_file.read())
                    # On récupère la clé de chiffrement, si elle existe. Sinon elle sera égale à "Empty"
                    key = keystore.keys.get(message, "Empty")

                    # Si la clé n'a pas pû être récupérée, on demande à l'utilisateur de la saisir
                    if key == "Empty":
                        key = input("Impossible de charger la clé depuis le Keystore, entrez la clé de cryptage : ")
                    # Sinon on la charge dans la variable key
                    else:
                        print("Clé de cryptage trouvée dans le keystore ! (Clé : " + key + ")")
            # Si l'utilisateur n'a pas choisi d'utiliser le KeyStore, on demande à l'utilisateur de la saisir
            else:
                key = input("Entrez la clé de cryptage : ")

        # On décrypte le message et on l'affiche
        print("Voici le message décrypté : " + method.decrypt(EncryptEntry(key, message)))
        input("Appuyez sur entrée pour continuer...")
        main_menu()


# For PyCharm only
if __name__ == '__main__':
    start()
