from serveur_applicatif import ServeurApplicatif
from etudiant import Etudiant
from certificat import Certificat
from bottle import Bottle, route, run, template, request, response

class CommunicationServeurApplicatif:
    def __init__(self, serveur_applicatif: ServeurApplicatif):
        self.app = Bottle()
        self.serveur_applicatif: ServeurApplicatif = serveur_applicatif
        self.setup_routes()


    def setup_routes(self):
        self.app.route('/recuperation_fond', callback=self.recuperer_fond)
        self.app.route('/faire_verification', method='POST', callback=self.faire_verification)
        self.app.route('/faire_creation', method='POST', callback=self.faire_creation)


    def demarrer(self):
        self.app.run(host='127.0.0.1',port=1234,debug=True)

    
    def recuperer_fond(self):
        response.set_header('Content-type', 'image/png')
        
        descripteur_fichier = open('./src/img/attestation_stegano.png','rb')
        contenu_fichier = descripteur_fichier.read()
        descripteur_fichier.close()
        return contenu_fichier

    
    def faire_verification(self):
        try:
            contenu_image = request.files.get('image')
            print("*"*25)
            print("--- Contenu image:", contenu_image)
            print("*"*25)
            chemin_image = './attestation_a_verifier.png'
            contenu_image.save(chemin_image, overwrite=True)
            
            resultat = self.serveur_applicatif.verifier_attestation(chemin_image)
            print("Resultat:", resultat)
            response.set_header('Content-type', 'text/plain')
            if resultat:
                response.status = 200
                return "Certificat valide"
            else:
                response.status = 403
                return "Certificat invalide"
                
        except Exception as e:
            response.status = 500
            return f"Erreur lors de la vérification: {str(e)}"


    def faire_creation(self):
        # Récupération des informations
        contenu_email = request.forms.get('email')
        nom_etudiant: str = contenu_email.split(".")[0]
        prenom_etudiant: str = contenu_email.split(".")[1].split("@")[0]
        contenu_intitulé_certification = request.forms.get('intitule_certif')
        contenu_mot_de_passe = request.forms.get('mdp')
        etudiant_actuel: Etudiant = Etudiant(nom_etudiant, prenom_etudiant, Certificat(contenu_intitulé_certification))
        print(f"--- Nom: {etudiant_actuel.nom}; Prénom: {etudiant_actuel.prenom}; Certificat: {etudiant_actuel.certificat.intitule}")

        # Le SSO ne fonctionne plus depuis le 2FA (Top !!) - Sauf avec eduroam
        """
        # Vérification de l'étudiant avec le SSO de l'université
        cookies: list = self.contacter_sso_universite(contenu_email, contenu_mot_de_passe)
        if cookies:
            # Intéraction avec le serveur d'application
            self.serveur_applicatif.creation_certificat(etudiant_actuel)

            # Réponse
            response.set_header('Content-type', 'text/plain')
            return "ok!"
        
        return "Mot de passe ou nom de l'utilisateur incorrect"
        """
        self.serveur_applicatif.creation_certificat(etudiant_actuel)
        return "ok!"