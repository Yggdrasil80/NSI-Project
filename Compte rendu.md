<h1 align="center">Projet final de NSI</h1>
<h2 align="center">Projet de réalisation d'un programme de cryptage</h2>

---

## 🚀 Introduction

Ce projet est un programme de cryptage de texte, disposant de quatre méthodes de cryptage différentes, à savoir:
- Cryptage ROT13
- Code de César
- Cryptage de Vigenère
- Carré de Polybe

Dans un premier temps, nous analyserons en détail le projet, et ensuite analyserons son avancée, et ses résultats, avant de conclure dessus ainsi que sur les outils utilisés.

## 💼 Le projet

Par ce projet, j'ai voulu réaliser un programme de cryptage de texte, qui serait capable de chiffrer et de déchiffrer un texte, en utilisant quatre méthodes différentes de cryptage. Je voulais aussi l'associer à une interface graphique afin de faciliter son utilisation, et disposer d'une façon de stocker automatiquement les clés de cryptage. Je m'étais aussi fixé comme objectif (si on fait exception de Qt pour l'interface), de n'utiliser que des librairies fournies par défaut dans Python 3.+

## ⚠️ Les problèmes rencontrés

En travaillant sur le projet, j'ai pû rencontrer un problème majeur et un moins important, mais notable tout de même.
- Le premier problème, majeur :
    - En travaillant mon interface (Prototype accessible ici : https://www.figma.com/file/s13ALkaFWGt3WTJisimllD/Projet-final-NSI?node-id=0%3A1), j'ai été frappé par mon manque de talent en tant que designer d'interface (comme quoi, cela confirme la phrase "Il faudrait offrir à tous les bons développeurs des cours d'UI/UX Design" 😉).
    - En intégrant cette interface dans le code, à l'aide des outils Qt Studio, j'ai rencontré beaucoup de soucis de mauvais fonctionnement.

    J'ai donc décidé d'abandonner l'idée d'interface graphique, pour perfectionner plutôt mon code.
- Le second problème, moins important :
    J'ai pû me rendre compte qu'il y avait énormément de répétitions de code entre le cryptage et le décryptage, que je n'ai pas réussi à optimiser.

Je me suis aussi, en finalisant le projet, heurté au fait de devoir rassembler tout le code en un seul fichier python, pour correspondre aux exigences de la remise du projet, ce qui peut dégrader la lisibilité du code et fait des fichiers de plus de 500 lignes.

## ✨ Le résultat

Le programme est correctement capable de chiffrer et de déchiffrer un texte, en utilisant quatre méthodes différentes de cryptage, et d'enregistrer automatiquement les clés de cryptage. Voici quelques illustrations du programme :
- Configuration du programme, stockage des options dans un fichier json
![Config](https://raw.githubusercontent.com/Yggdrasil80/NSI-Project/master/doc/Configuration.png)
- Cryptage ROT13, ne nécessitant pas de clé de cryptage
![ROT13](https://raw.githubusercontent.com/Yggdrasil80/NSI-Project/master/doc/Cryptage%20ROT13.png)
- Ainsi que son décryptage
![ROT13](https://raw.githubusercontent.com/Yggdrasil80/NSI-Project/master/doc/ROT13%20Décrypté.png)
- Cryptage de Vigénère, nécessitant une clé de cryptage
![Vigenère](https://raw.githubusercontent.com/Yggdrasil80/NSI-Project/master/doc/Cryptage%20Vigénère.png)
- Ainsi que son décryptage (Même si on peut observer l'insertion de caractères aléatoires lors du déchiffrement 😅)
![Vigenère](https://raw.githubusercontent.com/Yggdrasil80/NSI-Project/master/doc/Vig%C3%A9n%C3%A8re%20D%C3%A9crypt%C3%A9.png)

Je suis globalement satisfait de la réalisation de ce projet, et il m'a permis d'approfondir mes connaissances en en Python, même si j'ai pû être parfois perturbé par mes habitudes de développeur Java/C++.

## 🛠️ Les outils utilisés

Pour la réalisation du projet, j'ai utilisé les outils suivants :
- [PyCharm Ultimate](https://www.jetbrains.com/pycharm/)
- [Github](https://github.com)

Je me suis aidé de :
- Github Copilot
- Stack Overflow
- La théorie des méthodes de cryptage avec Wikipedia et DCode
- La documentation officielle de Python

J'ai utilisé comme librairies :
- Random
- Time
- String
- Json
- Os