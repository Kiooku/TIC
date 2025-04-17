from PIL import Image
from io import BytesIO
import subprocess
from time import sleep

class Employeur:

    certificat_image : Image
    def __init__(self, certificat_path: str):
        self.certificat_path = certificat_path


    def verifier_certificat(self) -> bool:
        """
        Employeur envoie une requete au serveur frontal pour demander a verifier un certificat à partir
        d'une image. Le serveur renvoie une réponse en fonction de si le certificat est valide ou non
        :return: bool
        """
        # TODO change to HTTPS (Don't work with https for POST but work for GET, why???)
        # Testing with HTTP for POST so far, to setup everything for the main.py file
        # -F "image=@/home/user1/Desktop/test.jpg"
        """
        commande_curl = subprocess.Popen(
            f"curl -v -F image=@{self.certificat_path} --cacert ./src/cert/certCertifPlus/ecc.ca.cert.pem https://localhost:9000/verification",
            shell=True, stdout=subprocess.PIPE)
        (resultat, _) = commande_curl.communicate()
        print("Resultat", resultat,": Erreur", _)
        """
        print("$"*25)
        print(self.certificat_path)
        print("$"*25)

        commande_curl = subprocess.Popen(
            f"curl -v -X POST -d 'image_path={self.certificat_path}' --cacert ./src/cert/certCertifPlus/ecc.ca.cert.pem https://localhost:9000/verification",
            shell=True, stdout=subprocess.PIPE)
        (resultat, _) = commande_curl.communicate()
        print("* Resultat:", resultat)
        return resultat.decode() == "Certificat valide"