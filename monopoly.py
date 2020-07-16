import random
from collections import Counter

class Plateau:
    CASES = [
        {"name": "Départ"},
        {"name": "Boulevard de Belleville"},
        {"name": "Caisse de communaute 1"},
        {"name": "Rue Lecourbe"},
        {"name": "Impôts sur le Revenu"},
        {"name": "Gare Montparnasse"},
        {"name": "Rue de Vaugirard"},
        {"name": "Chance 1"},
        {"name": "Rue de Courcelles"},
        {"name": "Avenue de la Republique"},
        {"name": "Prison simple visite"},
        {"name": "Boulevard de la Vilette"},
        {"name": "Compagnie de distribution d'éléctricité"},
        {"name": "Avenue de Neuilly"},
        {"name": "Rue de Paradis"},
        {"name": "Gare de Lyon"},
        {"name": "Avenue Mozart"},
        {"name": "Caisse de communauté 2"},
        {"name": "Boulevard Saint-Michel"},
        {"name": "Place Pigalle"},
        {"name": "Parc Gratuit"},
        {"name": "Avenue Matignon"},
        {"name": "Chance 2"},
        {"name": "Boulevard Malesherbes"},
        {"name": "Avenue Henri-Martin"},
        {"name": "Gare du Nord"},
        {"name": "Faubourg Saint-Honoré"},
        {"name": "Place de la Bourse"},
        {"name": "Compagnie de distribution des eaux"},
        {"name": "Rue La Fayette"},
        {"name": "Allez en prison"},
        {"name": "Avenue de Breteuil"},
        {"name": "Avenue Foch"},
        {"name": "Caisse de communauté 3"},
        {"name": "Boulevard des Capucines"},
        {"name": "Gare Saint-Lazare"},
        {"name": "Chance 3"},
        {"name": "Avenue des Champs-Elysees"},
        {"name": "Taxe de Luxe"},
        {"name": "Rue de la Paix"},
    ]

    def __init__(self):
        self.chances = ["Sans déplacement"] * 6 + ["prochaine gare"] * 2 + [24, 11, 5, 0, 39, 30, "reculer de 3",
                                                                            "prochaine compagnie"]
        self.communautes = ["Sans déplacement"] * 14 + [30, 0]
        random.shuffle(self.chances)
        random.shuffle(self.communautes)

    def tirer_carte_chance(self, position):
        chance = self.chances.pop(0)
        self.chances.append(chance)
        if chance == "Sans déplacement":
            return position
        elif chance == "prochaine gare":
            if position >= 35:
                return 5
            elif position >= 25:
                return 35
            elif position >= 15:
                return 25
            elif position >= 5:
                return 15
            return 5
        elif chance == "reculer de 3":
            if position < 3:
                return 37 + position
            return position - 3
        elif chance == "prochaine compagnie":
            if position >= 12 and position < 28:
                return 28
            return 12
        return chance

    def tirer_carte_communaute(self, position):
        communaute = self.communautes.pop(0)
        self.communautes.append(communaute)
        if communaute == "Sans déplacement":
            return position
        return communaute


class Joueur:
    def __init__(self, plateau):
        self.position = 0
        self.visites = []
        self.plateau = plateau
        self.doubles = 0
        self.prison = False
        self.tentatives_sorties = 0

    def joue(self):
        if self.tentatives_sorties == 3:
            self.prison = False
            self.tentatives_sorties = 0

        de1 = random.randint(1, 6)
        de2 = random.randint(1, 6)

        if de1 == de2:
            self.prison = False
            self.tentatives_sorties = 0
            self.doubles += 1
        else:
            self.doubles = 0
        if self.doubles == 3:
            self.position = 10
            self.prison = True
            self.doubles = 0
        elif self.prison:
            self.tentatives_sorties += 1
        else:
            self.position = (self.position + de1 + de2) % 40
            if self.position in [7, 22, 36]:
                self.position = self.plateau.tirer_carte_chance(self.position)
            if self.position in [2, 17, 33]:
                self.position = self.plateau.tirer_carte_communaute(self.position)
            if self.position == 30:
                self.position = 10
                self.prison = True
        self.visites.append(self.plateau.CASES[self.position]["name"])
        
        
visites = []
for i in range(10000):
    plateau = Plateau()
    toto = Joueur(plateau)
    for i in range(100):
        toto.joue()
        visites += toto.visites
        
Counter(visites)
