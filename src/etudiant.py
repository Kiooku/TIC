from certificat import Certificat
from PIL import Image

class Etudiant:
    def __init__(self, nom: str, prenom: str, certificat: Certificat):
        self.nom: str = nom
        self.prenom: str = prenom
        self.certificat: Certificat = certificat

    
    def demander_certificat(self, mdr: str) -> Image:
        pass


if __name__ == "__main__":
    pass