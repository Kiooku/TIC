# TIC
Projet TIC


main.py ::: (Gaétan)

Etudiant: ::: (Gaétan)
- nom: str
- prénom: str
- certificat: Certificat
- [ ] demander_certificat(mdp: str) -> Image [Le serveur renvoit le certificat sous forme d'image ou un message d'erreur si le mdp est incorrect] ::: (Noah)


Certificat: ::: (Iscia)
- intitulé: str
- date: None


Employeur: ::: (Noah)
- [ ] verifier_certificat() ::: (Noah)


ServeurFrontal: ::: (Gaétan)
- serveurApp: ServeurApplicatif
- [ ] obtenir_date() -> Date
- [ ] demarrer() [Lancer le serveur avec openssl (TP4 - Ex8) utilisant un certificat ajouté dans le navigateur préalablement] ::: (Gaétan)
- [ ] verification() [Fait appel à la fonction verifier_attestation du ServeurApplicatif] ::: (Noah)
- [ ] creation(etudiant: Etudiant, mdp: str) [Fait appel à la fonction creation_certificat du ServeurApplicatif. Cependant, il faut préalablement vérifier le mdp de l'étudiant avec le SSO Unilim] ::: (Gaétan/Noah - Projet page 7)
# TODO penser au bonus avec la sécurisation du serveur frontal (reverse_proxy, load_balancer, protection DoS, protection brute force)


ServeurApplicatif: ::: (Iscia)
- stegano: Steganographie
- cle_privee: str
- [X] obtenir_timestamp() -> int ::: (Gaétan - Projet page 1)
- [ ] signature_document() ::: (Iscia/Gaétan - TP 2)
- [ ] creation_certificat(etudiant: Etudiant) -> Image ::: (Iscia - TP3 exo 2)
- [X] creer_qrcode(etudiant: Etudiant) ::: (Iscia - Projet page 4)
- [ ] verifier_attestation(certificat: Certificat, cle_publique: str) -> bool ::: (Iscia/Gaétan - TP3 exo 2)
- [ ] dissimulation_par_steganographie(etudiant: Etudiant, chemin_image: str) ::: (Noah)
- [ ] extraire_infos_steganographie(chemin_image: str) -> dict ::: (Gaétan)
- [ ] extraire_qrcode_informations(chemin_image: str) -> int (signature dans le QRCode) ::: (Noah - Projet page 4)


Steganographie: ::: (Gaétan - Projet page 5)
- [X] vers_8bits(c)
- [X] modifier_pixel(pixel, bit)
- [X] recuperer_bit_pfaible(pixel)
- [X] cacher(image, message)
- [X] recuperer(image, taille)


# TODO: Faire des tests si on a le temps

