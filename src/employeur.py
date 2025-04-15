import requests
from PIL import Image
from io import BytesIO


class Employeur:

    certificat_image : Image
    def __init__(self, certificat : Image):
        self.certificat_image = certificat
        pass

    def verification(self) -> bool:
        """
        Employeur envoie une requete au sevreur frontal pour demander a verifier un certificat à partir
        d'une image. Le serveur renvgoie une réoinse en fonction de si le certificat est valide ou non
        :return: bool
        """

        img_byte_arr = BytesIO()
        self.certificat_image.save(img_byte_arr, format='PNG')
        img_bytes = img_byte_arr.getvalue()

        files = {
            'image': ('certificat.png', img_bytes, 'image/png')
        }

        response = requests.post('https://localhost:8080/verification', files=files)
        try:
            if response.status_code == 200:
                print("Certifié !")
                return True
            elif response.status_code == 403:
                print("Attestation erronée !")
                return False
            else:
                print("Autre code (Accés refusé")
                return False
        except requests.RequestException as e:
            raise Exception(f"Erreur réseau: {str(e)}")