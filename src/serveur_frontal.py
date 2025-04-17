from bottle import Bottle, route, run, template, request, response
import urllib.request
import urllib.parse
import re
import sys
import datetime
import subprocess

class ServeurFrontal:
    def __init__(self):
        self.app = Bottle()
        self.setup_routes()

    def setup_routes(self):
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


    def verification(self):
        contenu_image_path = request.forms.get('image_path')

        commande_curl = subprocess.Popen(
            f"curl -v -F image=@{contenu_image_path} --cacert ./src/cert/certCertifPlus/ecc.ca.cert.pem http://localhost:1234/faire_verification",
            shell=True, stdout=subprocess.PIPE)
        (resultat, _) = commande_curl.communicate()
        print("Resultat", resultat,": Erreur", _)
        return resultat


    def creation(self):
        # Récupération des informations
        contenu_email = request.forms.get('email')
        contenu_intitulé_certification = request.forms.get('intitule_certif')
        contenu_mot_de_passe = request.forms.get('mdp')

        commande_curl = subprocess.Popen(
            f"curl -v -X POST -d 'email={contenu_email}' -d 'intitule_certif={contenu_intitulé_certification}' -d 'mdp={contenu_mot_de_passe}' --cacert ./src/cert/certCertifPlus/ecc.ca.cert.pem http://localhost:1234/faire_creation",
            shell=True, stdout=subprocess.PIPE)
        (resultat, _) = commande_curl.communicate()
        
        if resultat.decode() == "Mot de passe ou nom de l'utilisateur incorrect":
            return None
        
        commande_curl = subprocess.Popen(
            f'curl -v -X GET --cacert ./src/cert/certCertifPlus/ecc.ca.cert.pem http://localhost:1234/recuperation_fond',
            shell=True, stdout=subprocess.PIPE)
        (resultat, _) = commande_curl.communicate()

        return resultat


if __name__ == "__main__":
    serveurFrontal: ServeurFrontal = ServeurFrontal()
    print(serveurFrontal.obtenir_date())
    serveurFrontal.demarrer()

    # socat openssl-listen:9000,fork,cert=./src/cert/certCertifPlus/bundle_serveur.pem,cafile=./src/cert/certCertifPlus/ecc.ca.cert.pem,verify=0 tcp:127.0.0.1:8080
    # curl -v -X GET --cacert ./src/cert/certCertifPlus/ecc.ca.cert.pem https://localhost:9000/fond