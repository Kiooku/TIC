from certificat import Certificat
from PIL import Image
import subprocess
from io import BytesIO
from unidecode import unidecode
from time import sleep

class Etudiant:
    def __init__(self,nom:str,prenom:str, certificat:Certificat):
        self.nom=nom
        self.prenom=prenom
        self.certificat=certificat
        
    
    def demander_certificat(self, mdp: str) -> Image:
        print(self.certificat.intitule)
        data = {
            'email': f"{unidecode(self.prenom)}.{unidecode(self.nom)}@etu.unilim.fr",
            'intitule_certif': unidecode(self.certificat.intitule),
            'mdp': unidecode(mdp) 
        }

        commande_curl = subprocess.Popen(
            f"curl -v -X POST -d 'email={data['email']}' -d 'intitule_certif={data['intitule_certif']}' -d 'mdp={data['mdp']}' --cacert ./src/cert/certCertifPlus/ecc.ca.cert.pem https://localhost:9000/creation",
            shell=True, stdout=subprocess.PIPE)
        (resultat, _) = commande_curl.communicate()
        
        image = Image.open(BytesIO(resultat))
        return image



if __name__=="__main__":
    etu=Etudiant("LATTE", "Chat", Certificat("Attestation de beauté"))