from serveur_applicatif import ServeurApplicatif
from steganographie import Steganographie
from etudiant import Etudiant
from certificat import Certificat
from bottle import Bottle, route, run, template, request, response
import urllib.request
import urllib.parse
import re
import sys
import datetime

class ServeurFrontal:
    def __init__(self, serveur_applicatif: ServeurApplicatif):
        self.app = Bottle()
        self.serveur_applicatif: ServeurApplicatif = serveur_applicatif
        self.setup_routes()

    def setup_routes(self):
        self.app.route('/fond', callback=self.recuperer_fond)
        self.app.route('/verification', method='POST', callback=self.verification)
        self.app.route('/creation', method='POST', callback=self.creation)

    
    def obtenir_date(self) -> str:
        t = datetime.datetime.now()
        return t.strftime('%d/%m/%Y')


    def demarrer(self):
        self.app.run(host='127.0.0.1',port=8080,debug=True)


    def contacter_sso_universite(self, email: str, mdp: str) -> list:
        re_token = re.compile(rb'name="token" value="([^"]+)"')
        request = urllib.request.Request('https://cas.unilim.fr')
        rep = urllib.request.urlopen(request)
        contenu = rep.read()
        resultat = re_token.search(contenu)
        if resultat:
            token = resultat.group(1)
            print(token)
        else:
            sys.exit(1)
        cookieProcessor = urllib.request.HTTPCookieProcessor()
        opener = urllib.request.build_opener(cookieProcessor)
        data = urllib.parse.urlencode({'user':email,'password':mdp,'token':token})

        request = urllib.request.Request('https://cas.unilim.fr',bytes(data,encoding='ascii'))
        reponse = opener.open(request)
        cookies = [c for c in cookieProcessor.cookiejar if c.name=='lemonldap']
        return cookies


    #@route('/fond')
    def recuperer_fond(self):
        response.set_header('Content-type', 'image/png')
        descripteur_fichier = open('./src/img/attestation.png','rb')
        contenu_fichier = descripteur_fichier.read()
        descripteur_fichier.close()
        return contenu_fichier

    
    @route('/verification', method='POST')
    def verification(self):
        try:
            contenu_image = request.files.get('image')
            chemin_image = './attestation_a_verifier.png'
            contenu_image.save(chemin_image, overwrite=True)
            
            resultat = self.serveur_applicatif.verifier_attestation(chemin_image)
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


    #@route('/creation', method='POST')
    def creation(self):
        # Récupération des informations
        contenu_email = request.forms.get('email')
        nom_etudiant: str = contenu_email.split(".")[0]
        prenom_etudiant: str = contenu_email.split(".")[1]
        contenu_intitulé_certification = request.forms.get('intitule_certif')
        contenu_mot_de_passe = request.forms.get('mdp')
        etudiant_actuel: Etudiant = Etudiant(nom_etudiant, prenom_etudiant, Certificat(contenu_intitulé_certification))
        
        # Vérification de l'étudiant avec le SSO de l'université
        cookies: list = self.contacter_sso_universite(contenu_email, contenu_mot_de_passe)
        if cookies:
            # Intéraction avec le serveur d'application
            # TODO signature on fait quoi??? Ce n'est pas le serveur d'application qui fait ça ?
            self.serveur_applicatif.creation_certificat(etudiant_actuel, "TODO voir quoi mettre ici")

            # Réponse
            response.set_header('Content-type', 'text/plain')
            return "ok!"
        
        return "Mot de passe ou nom de l'utilisateur incorrecte"

    def extraire_intitule_du_bloc(self, bloc_info):
        return "" #TODO voir si on dois extraire les infos et is oui i faut un separateur


if __name__ == "__main__":
    stegano: Steganographie = Steganographie()
    serveurApplicatif: ServeurApplicatif = ServeurApplicatif(stegano, "chatouillle")
    serveurFrontal: ServeurFrontal = ServeurFrontal(serveurApplicatif)
    print(serveurFrontal.obtenir_date())
    serveurFrontal.demarrer()