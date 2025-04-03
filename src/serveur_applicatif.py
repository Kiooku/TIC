from stegano import Steganographie
from etudiant import Etudiant
from PIL import Image
from certificat import Certificat

class ServeurApplicatif:
    def __init__(self, stegano:Steganographie, cle_privee:str):
        self.stegano= stegano
        self.cle_privee= cle_privee

    def obtenir_timestamp()-> int:
        pass

    def creation_certificat(etudiant: Etudiant)-> Image:
        pass

    def creer_qrcode(etudiant:Etudiant):
        pass

    def verifier_attestation(certificat: Certificat, cle_publique:str)->bool:
        pass

    def dissimulation_par_steganographie(etudiant:Etudiant, chemin_image:str):
        pass

    def extraire_infos_steganographie(chemin_image:str)->dict:
        pass

    def extraire_qrcode_informations(chemin_image:str)->int:
        pass
