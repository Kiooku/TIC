from serveur_applicatif import ServeurApplicatif
from steganographie import Steganographie
from etudiant import Etudiant
from certificat import Certificat
from bottle import route, run, template, request, response
import urllib.request
import urllib.parse
import re
import sys

class ServeurFrontal:
    def __init__(self, serveur_applicatif: ServeurApplicatif):
        self.serveur_applicatif: ServeurApplicatif = serveur_applicatif

    
    def obtenir_date(self) -> str:
        pass


    def demarrer(self):
        run(host='0.0.0.0',port=8080,debug=True)
        pass


    def contacter_sso_universite(self):
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
        data = urllib.parse.urlencode({'user':'toto','password':'secret','token':token})

        request = urllib.request.Request('https://cas.unilim.fr',bytes(data,encoding='ascii'))
        reponse = opener.open(request)
        cookies = [c for c in cookieProcessor.cookiejar if c.name=='lemonldap']
        print(cookies)


    @route('/fond')
    def récupérer_fond():
        response.set_header('Content-type', 'image/png')
        descripteur_fichier = open('./src/img/attestation.png','rb')
        contenu_fichier = descripteur_fichier.read()
        descripteur_fichier.close()
        return contenu_fichier

    
    @route('/verification', method='POST')
    def verification():
        contenu_image = request.files.get('image')
        contenu_image.save('attestation_a_verifier.png',overwrite=True)
        response.set_header('Content-type', 'text/plain')
        return "ok!"

    
    @route('/creation', method='POST')
    # def creation(self, etudiant: Etudiant, mdp: str):
    def creation():
        contenu_nom = request.forms.get('nom')
        contenu_prenom = request.forms.get('prenom')
        contenu_intitulé_certification = request.forms.get('intitule_certif')
        etudiant_actuel: Etudiant = Etudiant(contenu_nom, contenu_prenom, Certificat(contenu_intitulé_certification))
        print('nom prénom :', contenu_nom, ",", contenu_prenom, ' intitulé de la certification :', contenu_intitulé_certification)
        response.set_header('Content-type', 'text/plain')
        return "ok!"


if __name__ == "__main__":
    stegano: Steganographie = Steganographie()
    serveurApplicatif: ServeurApplicatif = ServeurApplicatif(stegano, "chatouillle")
    serveurFrontal: ServeurFrontal = ServeurFrontal(serveurApplicatif)

    serveurFrontal.demarrer()