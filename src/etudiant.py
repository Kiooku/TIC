from certificat import Certificat
from PIL import Image
from hashlib import sha256
import requests
from io import BytesIO
class Etudiant:
    def __init__(self,nom:str,prenom:str, mdp : str, certificat:Certificat):
        self.nom=nom
        self.prenom=prenom
        self.certificat=certificat
        self.mdp=sha256(mdp.encode()).hexdigest()


    def verifier_mdp(self, mdp : str) -> bool:
        return self.mdp == sha256(mdp.encode()).hexdigest()
    def demander_certificat(self, mdp: str) -> Image:
        if self.verifier_mdp(mdp):
            data = {
                'nom': self.nom,
                'prenom': self.prenom,
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

        else:
            raise Exception("Mot de passe invalide !")


if __name__=="__main__":
    etu=Etudiant("LATTE", "Chat", Certificat("Attestation de beauté"))