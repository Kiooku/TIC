from serveur_frontal import ServeurFrontal
from serveur_applicatif import ServeurApplicatif
from steganographie import Steganographie
from etudiant import Etudiant
from certificat import Certificat
from employeur import Employeur
from threading import Thread
import subprocess
from PIL import Image
import io
from time import sleep

steganographie: Steganographie = Steganographie()
serveur_applicatif: ServeurApplicatif = ServeurApplicatif(steganographie, "TODO supprimer ?")
serveur_frontal: ServeurFrontal = ServeurFrontal(serveur_applicatif)
etudiant: Etudiant = Etudiant("boisbaumann", "gaetan", Certificat("Certificat de beaute ultime"))

# employeur: Employeur = Employeur()

# socat openssl-listen:9000,fork,cert=./src/cert/certCertifPlus/bundle_serveur.pem,cafile=./src/cert/certCertifPlus/ecc.ca.cert.pem,verify=0 tcp:127.0.0.1:8080
# curl -v -X GET --cacert ./src/cert/certCertifPlus/ecc.ca.cert.pem https://localhost:9000/fond

t1 = Thread(target = serveur_frontal.demarrer)
"""
commande_socat = subprocess.Popen(
            f'socat openssl-listen:9000,fork,cert=./src/cert/certCertifPlus/bundle_serveur.pem,cafile=./src/cert/certCertifPlus/ecc.ca.cert.pem,verify=0 tcp:127.0.0.1:8080',
            shell=True, stdout=subprocess.PIPE)

t2 = Thread(target = commande_socat.communicate)
commande_curl = subprocess.Popen(
            f'curl -v -X GET --cacert ./src/cert/certCertifPlus/ecc.ca.cert.pem https://localhost:9000/fond',
            shell=True, stdout=subprocess.PIPE)

t3 = Thread(target = commande_curl.communicate)


sleep(2)
# t2.start()
sleep(2)
# t3.start()
print("a")
"""
t1.start()
sleep(1)
input("Commencer ?")
"""
commande_curl = subprocess.Popen(
            f'curl -v -X GET --cacert ./src/cert/certCertifPlus/ecc.ca.cert.pem https://localhost:9000/fond',
            shell=True, stdout=subprocess.PIPE)
(resultat, _) = commande_curl.communicate()
image = Image.open(io.BytesIO(resultat))
#image.show()
print(image)
image.save("test.png")
"""
certificat = etudiant.demander_certificat("TODO")
print(certificat)
certificat.save("test.png")