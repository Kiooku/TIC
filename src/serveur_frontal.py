from serveur_applicatif import ServeurApplicatif
from etudiant import Etudiant

class ServeurFrontal:
    def __init__(self, serveur_applicatif: ServeurApplicatif):
        self.serveur_applicatif: ServeurApplicatif = serveur_applicatif

    
    def obtenir_date(self) -> str:
        pass


    def demarrer(self):
        pass


    def verification(self):
        pass


    def creation(self, etudiant: Etudiant, mdp: str):
        pass


if __name__ == "__main__":
    pass