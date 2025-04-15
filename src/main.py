from serveur_frontal import ServeurFrontal
from serveur_applicatif import ServeurApplicatif
from steganographie import Steganographie
from etudiant import Etudiant
from employeur import Employeur

steganographie: Steganographie = Steganographie()
serveur_applicatif: ServeurApplicatif = ServeurApplicatif(steganographie, "TODO")
serveur_frontal: ServeurFrontal = ServeurFrontal(serveur_applicatif)
etudiant: Etudiant = Etudiant("Chatouille", "Latte", "Certificat de beauté ultime")

employeur: Employeur = Employeur()