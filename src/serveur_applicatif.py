from steganographie import Steganographie
from etudiant import Etudiant
from PIL import Image
from certificat import Certificat
import sys, os
import subprocess
import qrcode
import zbarlight
from time import time # TODO remove when all the tests pass, it's to test the certificate
from const import LONGUEUR_BLOC_INFORMATION, LONGUEUR_TIMESTAMP


class ServeurApplicatif:
    def __init__(self, steganographie:Steganographie, cle_privee:str):
        self.stegano= steganographie
        self.cle_privee= cle_privee

    def obtenir_timestamp(self, nom_certificat: str):
        """
        Cette fonction crée ./src/cert/certFreeTSA/timestamp.tsq
        """
        commande=subprocess.Popen(f'openssl ts -query -data {nom_certificat} -no_nonce -sha512 -cert -out ./src/cert/certFreeTSA/timestamp.tsq', shell=True,stdout=subprocess.PIPE)
        (resultat, ignorer) = commande.communicate()
        #commande=subprocess.Popen(f"curl -H 'Content-Type: application/timestamp-query' --data-binary '@./src/cert/certFreeTSA/timestamp.tsq' https://freetsa.org/tsr > ./src/cert/certFreeTSA/timestamp.tsr", shell=True,stdout=subprocess.PIPE)
        #(resultat, ignorer) = commande.communicate()


    def creation_certificat(self, etudiant: Etudiant)-> Image:
        """
        Cette fonction crée ./src/img/attestation_stegano.png
        """
        commande=subprocess.Popen(f'convert -size 1000x600 -gravity center -pointsize 66 label:"{etudiant.certificat.intitule} \n délivré(e) à {etudiant.nom} {etudiant.prenom}" -transparent white ./src/img/texte.png', shell=True,stdout=subprocess.PIPE)
        (resultat, ignorer) = commande.communicate()

        bloc=(etudiant.nom+etudiant.prenom+etudiant.certificat.intitule).zfill(64)
        self.signature(bloc)
        self.creer_qrcode("./src/cles/bloc_hash.sig") 

        commande=subprocess.Popen(f'convert ./src/img/qrcode.png -resize 100x100 ./src/img/qrcode.png', shell=True,stdout=subprocess.PIPE)
        (resultat, ignorer) = commande.communicate()

        commande=subprocess.Popen("composite -gravity center ./src/img/texte.png ./src/img/fond_attestation.png ./src/img/combinaison.png", shell=True,stdout=subprocess.PIPE)
        (resultat, ignorer) = commande.communicate()
        commande=subprocess.Popen("composite -geometry +1470+985 ./src/img/qrcode.png ./src/img/combinaison.png ./src/img/attestation.png", shell=True,stdout=subprocess.PIPE)
        (resultat, ignorer) = commande.communicate()

        self.dissimulation_par_steganographie(bloc)



    def creer_qrcode(self,chemin_signature:str):
        """
        Cette fonction crée ./src/img/qrcode.png
        """
        signature=""
        with open(chemin_signature,"r") as fichier:
            signature=fichier.readlines()

        data = signature
        nom_fichier = "./src/img/qrcode.png"
        qr = qrcode.make(data)
        qr.save("./src/img/qrcode.png", scale=1)

        img2 = Image.open("./src/img/qrcode.png")
        qrImage = img2.crop((40,40,570,570))
        qrImage.save("./src/img/qrcode.png", scale=1)
        print(qrImage.size)
   
        print(qr.size)


    def verifier_attestation(self,certificat: Certificat, cle_publique:str)->bool:
        pass

    def dissimulation_par_steganographie(self, bloc_information: str) -> bytes:
        """
        Cette fonction crée ./src/img/attestation_stegano.png
        """
        timestamp = []
        with open("./src/cert/certFreeTSA/timestamp.tsq", "rb") as f:
            content = f.readlines()[0]
            for c in content:
                timestamp.append(c)

        img = self.stegano.cacher("./src/img/attestation.png", bytes(bloc_information.encode())+bytes(timestamp))
        img.save("./src/img/attestation_stegano.png")


    def extraire_infos_steganographie(self,chemin_image:str) -> dict:
        res: dict = {}
        steganoRes = stegano.recuperer(chemin_image, LONGUEUR_BLOC_INFORMATION+LONGUEUR_TIMESTAMP)
        # TODO pourquoi c'est 65 et pas 64 ???? [zfill(64)]
        res["bloc_information"] = steganoRes[:65].decode()
        res["timestamp"] = steganoRes[65:]
        with open("./src/cert/certFreeTSA/timestampFromStegano.tsq", "wb") as f:
            f.write(res["timestamp"])
        
        print(res)
        return res
    
    def signature(self,bloc:str): #Curve25519
        """
        Cette fonction crée ./src/cles/bloc_hash.sig 
        """
        commande=subprocess.Popen(f"openssl ecparam -out ./src/cles/ecc25519_cle_privee_signature.pem -name prime256v1 -genkey", shell=True,stdout=subprocess.PIPE)
        (resultat, ignorer) = commande.communicate()
        commande=subprocess.Popen(f"openssl ec -in ./src/cles/ecc25519_cle_privee_signature.pem -pubout -out ./src/cles/ecc25519_cle_publique_signature.pem", shell=True,stdout=subprocess.PIPE)
        (resultat, ignorer) = commande.communicate()

        commande=subprocess.Popen(f"echo -n {bloc} | openssl dgst -hex -sha256 -sign ./src/cles/ecc25519_cle_privee_signature.pem -out ./src/cles/bloc_hash.sig", shell=True,stdout=subprocess.PIPE)
        (resultat, ignorer) = commande.communicate()


    def extraire_qrcode_informations(self,chemin_image:str)->str:  
        attestation = Image.open(chemin_image)
        qrImage = attestation.crop((1470,985,1470+100,985+100))
        qrImage.save("./src/img/qrcode_recupere.png", "PNG")
        qrcoderecupere="./src/img/qrcode_recupere.png"

        image = Image.open(qrcoderecupere)
        data = zbarlight.scan_codes(['qrcode'], image)
        return(data[0].decode()[2:-4])
        

if __name__ == "__main__":
    etu=Etudiant("Chat","LATTE", Certificat("Attestation de beauté ultime"))
    # Taille fichier .tsq: 91 octets
    #signature="chatouille"
    stegano: Steganographie = Steganographie()
    serveur_app=ServeurApplicatif(stegano, "Iscia")
    
    #print(serveur_app.creer_qrcode(signature))

    print(serveur_app.creation_certificat(etu))
    print(serveur_app.extraire_qrcode_informations("./src/img/attestation_stegano.png"))
    """
    print(os.getcwd())
    serveur_app.extraire_infos_steganographie("./src/img/attestation_stegano.png")
    """
    print(serveur_app.signature("bonjour"))
    """
    serveur_app.obtenir_timestamp("./src/img/attestation.png")
    #### DÉBUT: Pour la vérification du certificat (timestamp)
    commande=subprocess.Popen(f"curl -H 'Content-Type: application/timestamp-query' --data-binary '@./src/cert/certFreeTSA/timestamp.tsq' https://freetsa.org/tsr > ./src/cert/certFreeTSA/certificat.tsr", shell=True,stdout=subprocess.PIPE)
    (resultat, ignorer) = commande.communicate()
    commande=subprocess.Popen(f"openssl ts -verify -in ./src/cert/certFreeTSA/timestamp.tsr -queryfile ./src/cert/certFreeTSA/timestamp.tsq -CAfile ./src/cert/certFreeTSA/cacert.pem -untrusted ./src/cert/certFreeTSA/tsa.crt", shell=True,stdout=subprocess.PIPE)
    (resultat, ignorer) = commande.communicate()
    print(resultat.decode())
    #### FIN: De la vérification du certificat (timestamp)


    ### Test stenographie avec le .tsq
    print("#"*45)
    print("### TEST STEGANOGRAPHIE AVEC LE TIMESTAMP ###")
    print("#"*45)
    with open("./src/cert/certFreeTSA/timestamp.tsq", "rb") as f:
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
    """
    """
    commande=subprocess.Popen(f"curl -H 'Content-Type: application/timestamp-query' --data-binary '@./src/cert/certFreeTSA/timestampFromStegano.tsq' https://freetsa.org/tsr > ./src/cert/certFreeTSA/timestampFromStegano.tsr", shell=True,stdout=subprocess.PIPE)
    (resultat, ignorer) = commande.communicate()
    commande=subprocess.Popen(f"openssl ts -verify -in ./src/cert/certFreeTSA/timestampFromStegano.tsr -queryfile ./src/cert/certFreeTSA/timestampFromStegano.tsq -CAfile ./src/cert/certFreeTSA/cacert.pem -untrusted ./src/cert/certFreeTSA/tsa.crt", shell=True,stdout=subprocess.PIPE)
    (resultat, ignorer) = commande.communicate()
    print(resultat.decode())
    """