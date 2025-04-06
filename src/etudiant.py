from certificat import Certificat
from PIL import Image
import requests
from io import BytesIO


class Etudiant:
    def __init__(self,nom:str,prenom:str, certificat:Certificat):
        self.nom=nom
        self.prenom=prenom
        self.certificat=certificat
        
    
    def demander_certificat(self, mdp: str) -> Image:
        data = {
            'email': f"{self.prenom}.{self.nom}@etu.unilim.fr",
            'intitule_certif': self.certificat.intitule,
            'mdp': mdp  # verification du mdp cote serveur ?
        }

        try:
            # First call the creation endpoint
            response = requests.post('http://localhost:8080/creation', data=data)

            if response.status_code == 200:
                print("Mot de passe valide on recupere l'image")
                return None  # car pour le moment, la requete ne retourne par l'image
            elif response.status_code == 403:
                print("Accès refusé par le serveur applicatif")
            else:
                print("Erreur lors de la création du certificat !")
        except requests.RequestException as e:
            raise Exception(f"Erreur réseau: {str(e)}")



if __name__=="__main__":
    etu=Etudiant("LATTE", "Chat", Certificat("Attestation de beauté"))