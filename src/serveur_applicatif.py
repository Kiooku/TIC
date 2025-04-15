import traceback

from steganographie import Steganographie
from etudiant import Etudiant
from PIL import Image
from certificat import Certificat
import sys, os
import subprocess
import qrcode
import zbarlight
from time import time  # TODO remove when all the tests pass, it's to test the certificate
from const import LONGUEUR_BLOC_INFORMATION, LONGUEUR_TIMESTAMP
import binascii


class ServeurApplicatif:
    def __init__(self, steganographie: Steganographie, cle_privee: str):
        self.stegano = steganographie
        self.cle_privee = cle_privee

    def obtenir_timestamp(self, nom_certificat: str):
        """
        Cette fonction crée ./src/cert/certFreeTSA/timestamp.tsq
        """
        commande = subprocess.Popen(
            f'openssl ts -query -data {nom_certificat} -no_nonce -sha512 -cert -out ./src/cert/certFreeTSA/timestamp.tsq',
            shell=True, stdout=subprocess.PIPE)
        (resultat, ignorer) = commande.communicate()
        # commande=subprocess.Popen(f"curl -H 'Content-Type: application/timestamp-query' --data-binary '@./src/cert/certFreeTSA/timestamp.tsq' https://freetsa.org/tsr > ./src/cert/certFreeTSA/timestamp.tsr", shell=True,stdout=subprocess.PIPE)
        # (resultat, ignorer) = commande.communicate()

    def creation_certificat(self, etudiant: Etudiant) -> Image:
        """
        Cette fonction crée ./src/img/attestation_stegano.png
        """
        commande = subprocess.Popen(
            f'convert -size 1000x600 -gravity center -pointsize 66 label:"{etudiant.certificat.intitule} \n délivré(e) à {etudiant.nom} {etudiant.prenom}" -transparent white ./src/img/texte.png',
            shell=True, stdout=subprocess.PIPE)
        (resultat, ignorer) = commande.communicate()

        bloc = (etudiant.nom + etudiant.prenom + etudiant.certificat.intitule).zfill(64)
        self.signature(bloc)
        self.creer_qrcode("./src/cles/bloc_hash.sig")

        commande = subprocess.Popen(f'convert ./src/img/qrcode.png -resize 100x100 ./src/img/qrcode.png', shell=True,
                                    stdout=subprocess.PIPE)
        (resultat, ignorer) = commande.communicate()

        commande = subprocess.Popen(
            "composite -gravity center ./src/img/texte.png ./src/img/fond_attestation.png ./src/img/combinaison.png",
            shell=True, stdout=subprocess.PIPE)
        (resultat, ignorer) = commande.communicate()
        commande = subprocess.Popen(
            "composite -geometry +1470+985 ./src/img/qrcode.png ./src/img/combinaison.png ./src/img/attestation.png",
            shell=True, stdout=subprocess.PIPE)
        (resultat, ignorer) = commande.communicate()

        self.obtenir_timestamp("./src/img/attestation.png")
        self.dissimulation_par_steganographie(bloc)

    def creer_qrcode(self, chemin_signature: str):
        """
        Cette fonction crée ./src/img/qrcode.png
        """
        signature = ""
        with open(chemin_signature, "r") as fichier:
            signature = fichier.readlines()

        data = signature
        print(f"Signature: {signature}")
        
        nom_fichier = "./src/img/qrcode.png"
        qr = qrcode.make(data)
        qr.save("./src/img/qrcode.png", scale=1)

        img2 = Image.open("./src/img/qrcode.png")
        qrImage = img2.crop((40, 40, 570, 570))
        qrImage.save("./src/img/qrcode.png", scale=1)
        print(qrImage.size)

        print(qr.size)

    def verifier_attestation(self, chemin_image: str,
                             cle_publique: str = "./src/cles/ecc25519_cle_publique_signature.pem") -> bool:
        """
        Permet de verifier qu'une attestation est valide:
        - Extrait les informations cachées par stegano
        - Extrait la signature du QR code
        - Vérifie la signature avec la clé publique
        - Vérifie le timestamp

        :param chemin_image: Chemin vers l'image de l'attestation à vérifier
        :param cle_publique: Chemin vers la clé publique pour vérifier la signature
        :return: True si l'attestation est valide, False sinon
        """
        try:
            infos_stegano = self.extraire_infos_steganographie(chemin_image)
            bloc_info = infos_stegano["bloc_information"]
            timestamp_data = infos_stegano["timestamp"]
            print("Bloc info:", bloc_info)
            print("Timestamp data:", timestamp_data)

            print("Bloc d'info:", bloc_info)

            signature_qrcode = self.extraire_qrcode_informations(chemin_image)
            signature_hex = signature_qrcode.split("SHA2-256(stdin)=")[1].strip()

            if len(signature_hex) % 2 == 1:
                signature_hex = '0' + signature_hex

            signature_binary = binascii.unhexlify(signature_hex)
            temp_bloc_file = "./src/cert/temp_bloc.txt"
            with open(temp_bloc_file, "w") as f:
                f.write(bloc_info)

            temp_sig_file = "./src/cert/temp_sig.bin"
            with open(temp_sig_file, "wb") as f:
                f.write(signature_binary)

            # on verifie la signature avec openssl
            cmd = subprocess.Popen(
                f"openssl dgst -hex -sha256 -verify {cle_publique} -signature {temp_sig_file} {temp_bloc_file}",
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            (resultat, erreur) = cmd.communicate()
            print("Erreur:", erreur)

            if os.path.exists(temp_bloc_file):
                os.remove(temp_bloc_file)
            if os.path.exists(temp_sig_file):
                os.remove(temp_sig_file)

            # Verification du timestamp
            with open("./src/cert/certFreeTSA/timestampFromStegano.tsq", "wb") as f:
                f.write(timestamp_data)

            cmd = subprocess.Popen(
                "curl -H 'Content-Type: application/timestamp-query' --data-binary '@./src/cert/certFreeTSA/timestampFromStegano.tsq' https://freetsa.org/tsr > ./src/cert/certFreeTSA/timestampFromStegano.tsr",
                shell=True,
                stdout=subprocess.PIPE
            )
            (_, _) = cmd.communicate()

            cmd = subprocess.Popen(
                "openssl ts -verify -in ./src/cert/certFreeTSA/timestampFromStegano.tsr -queryfile ./src/cert/certFreeTSA/timestampFromStegano.tsq -CAfile ./src/cert/certFreeTSA/cacert.pem -untrusted ./src/cert/certFreeTSA/tsa.crt",
                shell=True,
                stdout=subprocess.PIPE
            )
            (timestamp_resultat, _) = cmd.communicate()

            signature_valide = "Verified OK" in resultat.decode()
            timestamp_valide = "Verification: OK" in timestamp_resultat.decode()

            print("Signature Valide ?", signature_valide, ":", resultat.decode())
            print("Timestamp Valide ?", timestamp_valide, ":", timestamp_resultat.decode())

            return signature_valide and timestamp_valide

        except Exception as e:
            print(f"Erreur lors de la vérification de l'attestation: {str(e)}")
            return False

    def dissimulation_par_steganographie(self, bloc_information: str) -> bytes:
        """
        Cette fonction crée ./src/img/attestation_stegano.png
        """
        timestamp = []
        with open("./src/cert/certFreeTSA/timestamp.tsq", "rb") as f:
            content = f.readlines()[0]
            for c in content:
                timestamp.append(c)

        img = self.stegano.cacher("./src/img/attestation.png", bytes(bloc_information.encode()) + bytes(timestamp))
        img.save("./src/img/attestation_stegano.png")

    def extraire_infos_steganographie(self, chemin_image: str) -> dict:
        """
        Extrait les informations cachées par stéganographie dans l'image
        :return: Dictionnaire contenant le bloc d'information et le timestamp
        """
        res: dict = {}
        steganoRes = self.stegano.recuperer(chemin_image, LONGUEUR_BLOC_INFORMATION + LONGUEUR_TIMESTAMP)
        # TODO pourquoi c'est 65 et pas 64 ???? [zfill(64)]
        res["bloc_information"] = steganoRes[:LONGUEUR_BLOC_INFORMATION].decode()
        res["timestamp"] = steganoRes[LONGUEUR_BLOC_INFORMATION:]
        with open("./src/cert/certFreeTSA/timestampFromStegano.tsq", "wb") as f:
            f.write(res["timestamp"])

        print(res)
        return res

    def signature(self, bloc: str):
        """
        Cette fonction crée ./src/cles/bloc_hash.sig
        :param bloc: Le bloc d'information à signer
        :return: Le résultat de la commande
        """
        # Génération des clés si elles n'existent pas déjà
        if not os.path.exists("./src/cles/ecc25519_cle_privee_signature.pem"):
            commande = subprocess.Popen(
                f"openssl ecparam -out ./src/cles/ecc25519_cle_privee_signature.pem -name prime256v1 -genkey",
                shell=True, stdout=subprocess.PIPE)
            (resultat, ignorer) = commande.communicate()

        if not os.path.exists("./src/cles/ecc25519_cle_publique_signature.pem"):
            commande = subprocess.Popen(
                f"openssl ec -in ./src/cles/ecc25519_cle_privee_signature.pem -pubout -out ./src/cles/ecc25519_cle_publique_signature.pem",
                shell=True, stdout=subprocess.PIPE)
            (resultat, ignorer) = commande.communicate()

        # Signature du bloc
        print("Bloc:", bloc)
        commande = subprocess.Popen(
            f"echo -n {bloc} | openssl dgst -hex -sha256 -sign ./src/cles/ecc25519_cle_privee_signature.pem -out ./src/cles/bloc_hash.sig",
            shell=True, stdout=subprocess.PIPE)
        (resultat, ignorer) = commande.communicate()

        return resultat

    def extraire_qrcode_informations(self, chemin_image: str) -> str:
        try:
            attestation = Image.open(chemin_image)
            qrimage = attestation.crop((1470, 985, 1470 + 100, 985 + 100))
            qr_save_path = "./src/img/qrcode_recupere.png"
            qrimage.save(qr_save_path, "PNG")
            image = Image.open(qr_save_path)

            if image.mode != 'L':
                print(f"Converting image from {image.mode} to L (grayscale) for better QR detection")
                image = image.convert('L')

            data = zbarlight.scan_codes(['qrcode'], image)
            decoded_data = data[0].decode()
            result = decoded_data[2:-4]
            print(f"Processed QR data: {result}")
            return result

        except Exception as e:
            error_details = traceback.format_exc()
            print(f"ERROR extracting QR code: {str(e)}")
            print(f"Full traceback:\n{error_details}")
            raise


if __name__ == "__main__":
    etu = Etudiant("Chat", "LATTE", Certificat("Attestation de beauté ultime"))
    # Taille fichier .tsq: 91 octets
    # signature="chatouille"
    stegano: Steganographie = Steganographie()
    serveur_app = ServeurApplicatif(stegano, "Iscia")

    # print(serveur_app.creer_qrcode(signature))

    print(serveur_app.creation_certificat(etu))
    print(serveur_app.verifier_attestation("./src/img/attestation_stegano.png"))
    # print(serveur_app.extraire_qrcode_informations("./src/img/attestation_stegano.png"))
    """
    print(os.getcwd())
    """
    # print(serveur_app.extraire_infos_steganographie("./src/img/attestation_stegano.png"))

    # print(serveur_app.signature("bonjour"))
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