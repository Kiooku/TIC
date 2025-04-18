from serveur_frontal import ServeurFrontal
from serveur_applicatif import ServeurApplicatif
from communication_serveur_applicatif import CommunicationServeurApplicatif
from steganographie import Steganographie
from etudiant import Etudiant
from certificat import Certificat
from employeur import Employeur
from threading import Thread
import subprocess
from PIL import Image
from time import sleep

steganographie: Steganographie = Steganographie()
serveur_applicatif: ServeurApplicatif = ServeurApplicatif(steganographie)
communication_serveur_applicatif: CommunicationServeurApplicatif = CommunicationServeurApplicatif(serveur_applicatif)
serveur_frontal: ServeurFrontal = ServeurFrontal()
etudiant: Etudiant = Etudiant("Chat-ouille", "Latte", Certificat("Certificat de beauté ultime"))

t1 = Thread(target = serveur_frontal.demarrer)
t2 = Thread(target = communication_serveur_applicatif.demarrer)
# Run on another terminal: # socat openssl-listen:9000,fork,cert=./src/cert/certCertifPlus/bundle_serveur.pem,cafile=./src/cert/certCertifPlus/ecc.ca.cert.pem,verify=0 tcp:127.0.0.1:8080

t1.start()
sleep(1)
t2.start()
sleep(1)
input("Commencer ?")

certificat = etudiant.demander_certificat("MonSuperMdp")
print(certificat)
certificat.save("test.png")

print("="*25)
print("="*25)
print("="*25)

#print("eza", certificat.filename)
employeur: Employeur = Employeur("test.png")
print("Certificat valide:", employeur.verifier_certificat())