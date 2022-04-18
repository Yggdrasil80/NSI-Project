from random import randint
from enum import Enum
from string import *


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

    @staticmethod
    def check_key(key: str) -> bool:
        """
        On vérifie si chaque caractère de la clé est une lettre, sinon on lève une exception.

        :param str key: La clé de cryptage du texte
        :return: True si la clé est valide, False sinon
        """
        try:
            for lettre in key:
                if not lettre.isalpha():
                    raise Exception("La clé doit être composée exclusivement de lettres.")

            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def check_text(text: str, to_skip: str) -> bool:
        """
        On vérifie si chaque caractère du texte est une lettre ou si il n'est pas à ignorer, sinon on lève une exception.

        :param str text: Le texte à crypter
        :param str to_skip: La liste des caractères à ignorer
        :return: True si le texte est valide, False sinon
        """
        try:
            for lettre in text:
                # Si la lettre est un caractère ignoré, on ne fait rien et passe au caractère suivant.
                if lettre in to_skip:
                    continue

                # Si le caractère n'est pas ignoré, mais n'est quand même pas une lettre, on lève une exception.
                if not lettre.isalpha():
                    raise EncryptionException("Le texte à chiffrer doit être composé exclusivement de lettres.")
            return True
        except Exception as e:
            print(e)
            return False


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
        if self.check_text(text, self.to_skip):
            return EncryptEntry("Empty", text.translate(get_translator(13)))

    def decrypt(self, entry: EncryptEntry) -> str:
        # Cette fonction décrypte le texte crypté passé en argument, via la fonction translate de la classe str,
        # avec un décalage inverse de 13.
        # Pour plus d'informations, voir la documentation de IEncryptMethod.
        if self.check_text(entry.text, self.to_skip):
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
        if self.check_text(text, self.to_skip):
            return EncryptEntry(key, text.translate(get_translator(int(key))))

    def decrypt(self, entry: EncryptEntry) -> str:
        # Cette fonction décrypte le texte crypté passé en argument, via la fonction translate de la classe str,
        # avec un décalage donné.
        # Pour plus d'informations, voir la documentation de IEncryptMethod.
        # Ici, on ajoute un "-" devant la clé de décryptage (correspondant au décalage dans l'alphabet)
        # afin de pouvoir retrouver l'alphabet original, à la différence du ROT13. L'alphabet étant composé de 26
        # lettres, si on décale deux fois de 13 lettres, on obtient un décalage de 26, ce qui donne l'alphabet original
        if self.check_text(entry.text, self.to_skip):
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

        if self.check_key(key) and self.check_text(text, self.to_skip):
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

        if self.check_key(entry.key) and self.check_text(entry.text, self.to_skip):
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
        if self.check_text(text, self.to_skip):
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


class Methods(Enum):
    ROT13_METHOD: IEncryptMethod = ROT13()
    CESAR_METHOD: IEncryptMethod = Cesar()
    VIGENERE_METHOD: IEncryptMethod = Vigenere()
    POLYBE_METHOD: IEncryptMethod = Polybe()


def is_key_required(method: IEncryptMethod) -> bool:
    return False if method == Methods.ROT13_METHOD or method == Methods.POLYBE_METHOD else True
