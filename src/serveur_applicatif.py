from steganographie import Steganographie
from etudiant import Etudiant
from PIL import Image
from certificat import Certificat
import sys, os
import subprocess
import qrcode
from time import time # TODO remove when all the tests pass, it's to test the certificate

class ServeurApplicatif:
    def __init__(self, steganographie:Steganographie, cle_privee:str):
        self.stegano= steganographie
        self.cle_privee= cle_privee

    def obtenir_timestamp(self, nom_certificat: str):
        commande=subprocess.Popen(f'openssl ts -query -data {nom_certificat} -no_nonce -sha512 -cert -out ./src/cert/certFreeTSA/certificat.tsq', shell=True,stdout=subprocess.PIPE)
        (resultat, ignorer) = commande.communicate()
        #commande=subprocess.Popen(f"curl -H 'Content-Type: application/timestamp-query' --data-binary '@./src/cert/certFreeTSA/certificat.tsq' https://freetsa.org/tsr > ./src/cert/certFreeTSA/certificat.tsr", shell=True,stdout=subprocess.PIPE)
        #(resultat, ignorer) = commande.communicate()


    def creation_certificat(self, etudiant: Etudiant,signature:str)-> Image:
        commande=subprocess.Popen(f'convert -size 1000x600 -gravity center -pointsize 66 label:"{etudiant.certificat.intitule} \n délivré(e) à {etudiant.nom} {etudiant.prenom}" -transparent white img/texte.png', shell=True,stdout=subprocess.PIPE)
        (resultat, ignorer) = commande.communicate()
        self.creer_qrcode(signature) 
        commande=subprocess.Popen("composite -gravity center ./src/img/texte.png ./src/img/fond_attestation.png ./src/img/combinaison.png", shell=True,stdout=subprocess.PIPE)
        (resultat, ignorer) = commande.communicate()
        commande=subprocess.Popen("composite -geometry +1470+985 ./src/img/qrcode.png ./src/img/combinaison.png ./src/img/attestation.png", shell=True,stdout=subprocess.PIPE)
        (resultat, ignorer) = commande.communicate()
        bloc=(etudiant.nom+etudiant.prenom+etudiant.certificat.intitule).zfill(64)
        #TODO steganographie et signature


    def creer_qrcode(self,signature:str):
        nom_fichier = "./src/img/qrcode.png"
        qr=qrcode.QRCode(box_size=5,border=0)
        qr.make(signature)
        qr=qr.make_image()
        qr.save(nom_fichier, scale=2, quiet_zone=0,)


    def verifier_attestation(self,certificat: Certificat, cle_publique:str)->bool:
        pass

    def dissimulation_par_steganographie(self,etudiant:Etudiant, chemin_image:str):
        pass

    def extraire_infos_steganographie(self,chemin_image:str)->dict:
        pass

    def extraire_qrcode_informations(self,chemin_image:str)->int:
        pass

if __name__ == "__main__":
    etu=Etudiant("Chat","LATTE", Certificat("Attestation de beauté ultime"))
    # Taille fichier .tsq: 91 octets
    signature="chatouille"
    stegano: Steganographie = Steganographie()
    serveur_app=ServeurApplicatif(stegano, "Iscia")
    print(serveur_app.creer_qrcode(signature))
    print(serveur_app.creation_certificat(etu,signature))
    print(os.getcwd())
    serveur_app.obtenir_timestamp("./src/img/attestation.png")
    #### DÉBUT: Pour la vérification du certificat
    commande=subprocess.Popen(f"curl -H 'Content-Type: application/timestamp-query' --data-binary '@./src/cert/certFreeTSA/certificat.tsq' https://freetsa.org/tsr > ./src/cert/certFreeTSA/certificat.tsr", shell=True,stdout=subprocess.PIPE)
    (resultat, ignorer) = commande.communicate()
    commande=subprocess.Popen(f"openssl ts -verify -in ./src/cert/certFreeTSA/certificat.tsr -queryfile ./src/cert/certFreeTSA/certificat.tsq -CAfile ./src/cert/certFreeTSA/cacert.pem -untrusted ./src/cert/certFreeTSA/tsa.crt", shell=True,stdout=subprocess.PIPE)
    (resultat, ignorer) = commande.communicate()
    print(resultat.decode())
    #### FIN: De la vérification du certificat


    ### Test stenographie avec le .tsq
    print("#"*45)
    print("### TEST STEGANOGRAPHIE AVEC LE TIMESTAMP ###")
    print("#"*45)
    with open("./src/cert/certFreeTSA/certificat.tsq", "rb") as f:
        content = f.readlines()[0]
        i = 0
        res = []
        for c in content:
            res.append(c)
            i+=1
        print("i:",i)
        print(bytes(res), bytes(res) == content)
        # Parfois la taille change et est égale à 48, 49 (Pour l'instant on va juste regénérer si c'est le cas)
        #print([bin(c)[2:].zfill(8) for c in content], len([bin(c)[2:].zfill(8) for c in content]))
        img = stegano.cacher("./src/img/attestation.png", bytes(res))
        img.save("./tests/stegano_attestation_test.png")
        steganoRes = stegano.recuperer("./tests/stegano_attestation_test.png", len(res))
        print("Stegano Res:", steganoRes, steganoRes == content, len(steganoRes))
        with open("./src/cert/certFreeTSA/certificatFromStegano.tsq", "wb") as f:
            f.write(steganoRes)
        
        commande=subprocess.Popen(f"curl -H 'Content-Type: application/timestamp-query' --data-binary '@./src/cert/certFreeTSA/certificatFromStegano.tsq' https://freetsa.org/tsr > ./src/cert/certFreeTSA/certificatFromStegano.tsr", shell=True,stdout=subprocess.PIPE)
        (resultat, ignorer) = commande.communicate()
        commande=subprocess.Popen(f"openssl ts -verify -in ./src/cert/certFreeTSA/certificatFromStegano.tsr -queryfile ./src/cert/certFreeTSA/certificatFromStegano.tsq -CAfile ./src/cert/certFreeTSA/cacert.pem -untrusted ./src/cert/certFreeTSA/tsa.crt", shell=True,stdout=subprocess.PIPE)
        (resultat, ignorer) = commande.communicate()
        print(resultat.decode())
        
    #stegano.cacher("./src/img/attestation.png", "")