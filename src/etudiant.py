from certificat import Certificat
from PIL import Image

class Etudiant:
    def __init__(self,nom:str,prenom:str,certificat:Certificat):
        self.nom=nom
        self.prenom=prenom
        self.certificat=certificat
    
    def demander_certificat(self,mdp:str) -> Image :
        pass


if __name__=="__main__":
    etu=Etudiant("LATTE", "Chat", Certificat("Attestation de beauté"))