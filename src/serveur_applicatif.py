from steganographie import Steganographie
from etudiant import Etudiant
from PIL import Image
from certificat import Certificat

import subprocess
import qrcode

class ServeurApplicatif:
    def __init__(self, steganographie:Steganographie, cle_privee:str):
        self.stegano= steganographie
        self.cle_privee= cle_privee

    def obtenir_timestamp(self)-> int:
        pass

    def creation_certificat(self, etudiant: Etudiant,signature:str)-> Image:
        commande=subprocess.Popen(f'convert -size 1000x600 -gravity center -pointsize 66 label:"{etudiant.certificat.intitule} \n délivré(e) à {etudiant.nom} {etudiant.prenom}" -transparent white img/texte.png', shell=True,stdout=subprocess.PIPE)
        (resultat, ignorer) = commande.communicate()
        self.creer_qrcode(signature) 
        commande=subprocess.Popen("composite -gravity center img/texte.png img/fond_attestation.png img/combinaison.png", shell=True,stdout=subprocess.PIPE)
        (resultat, ignorer) = commande.communicate()
        commande=subprocess.Popen("composite -geometry +1470+985 img/qrcode.png img/combinaison.png img/attestation.png", shell=True,stdout=subprocess.PIPE)
        (resultat, ignorer) = commande.communicate()
        bloc=(etudiant.nom+etudiant.prenom+etudiant.certificat.intitule).zfill(64)
        #TODO steganographie et signature


    def creer_qrcode(self,signature:str):
        nom_fichier = "img/qrcode.png"
        qr=qrcode.QRCode(box_size=5,border=0)
        qr.make(signature)
        qr=qr.make_image()
        qr.save(nom_fichier, scale=2,quiet_zone=0)



    def verifier_attestation(self,certificat: Certificat, cle_publique:str)->bool:
        pass

    def dissimulation_par_steganographie(self,etudiant:Etudiant, chemin_image:str):
        pass

    def extraire_infos_steganographie(self,chemin_image:str)->dict:
        pass

    def extraire_qrcode_informations(self,chemin_image:str)->int:
        pass

if __name__ == "__main__":
    etu=Etudiant("Chat","LATTE", Certificat("Attestation de beauté"))
    signature="chatouille"
    serveur_app=ServeurApplicatif(Steganographie(), "Iscia")
    print(serveur_app.creer_qrcode(signature))
    print(serveur_app.creation_certificat(etu,signature))