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
etudiant: Etudiant = Etudiant("Chat-ouille", "Latte", Certificat("Certificat de beaute ultime"))

t1 = Thread(target = serveur_frontal.demarrer)
# Run on another terminal: # socat openssl-listen:9000,fork,cert=./src/cert/certCertifPlus/bundle_serveur.pem,cafile=./src/cert/certCertifPlus/ecc.ca.cert.pem,verify=0 tcp:127.0.0.1:8080

t1.start()
sleep(1)
input("Commencer ?")

certificat = etudiant.demander_certificat("TODO")
print(certificat)
certificat.save("test.png")
#print("eza", certificat.filename)
employeur: Employeur = Employeur("test.png")
print(employeur.verifier_certificat())