from certificat import Certificat
from PIL import Image
import requests
import subprocess
from io import BytesIO
from time import sleep

class Etudiant:
    def __init__(self,nom:str,prenom:str, certificat:Certificat):
        self.nom=nom
        self.prenom=prenom
        self.certificat=certificat
        
    
    def demander_certificat(self, mdp: str) -> Image:
        print(self.certificat.intitule)
        data = {
            'email': f"{self.prenom}.{self.nom}@etu.unilim.fr",
            'intitule_certif': self.certificat.intitule,
            'mdp': mdp 
        }

        commande_curl = subprocess.Popen(
            f"curl -v -X POST -d 'email={data['email']}' -d 'intitule_certif={data['intitule_certif']}' -d 'mdp={data['mdp']}' --cacert ./src/cert/certCertifPlus/ecc.ca.cert.pem http://localhost:8080/creation",
            shell=True, stdout=subprocess.PIPE)
        (resultat, _) = commande_curl.communicate()
        print(data, resultat.decode())
        if resultat.decode() == "Mot de passe ou nom de l'utilisateur incorrecte":
            return None
        
        print("Resultat:", resultat)
        sleep(2)
        
        commande_curl = subprocess.Popen(
            f'curl -v -X GET --cacert ./src/cert/certCertifPlus/ecc.ca.cert.pem https://localhost:9000/fond',
            shell=True, stdout=subprocess.PIPE)
        (resultat, _) = commande_curl.communicate()
        image = Image.open(BytesIO(resultat))
        return image



if __name__=="__main__":
    etu=Etudiant("LATTE", "Chat", Certificat("Attestation de beauté"))