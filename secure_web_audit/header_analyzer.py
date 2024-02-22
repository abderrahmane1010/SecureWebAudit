from .utils import *
import requests

class HeaderAnalyzer :

    headers_risk = {
        "Server": "Information Leak",  # Révèle des détails sur le serveur utilisé
        "X-Powered-By": "Information Leak",  # Indique le langage/framework utilisé
        "X-AspNet-Version": "Information Leak",
        "X-AspNetMvc-Version": "Information Leak",
        "Via" : "Information Leak",
        "X-Backend-Server" : "Information Leak",
        "X-Frame-Options": "High",  # Prévient le clickjacking, l'absence est risquée
        "Strict-Transport-Security": "High",  # Force l'utilisation de HTTPS, critique pour la sécurité
        "Content-Security-Policy": "High",  # Prévient les attaques XSS et le chargement de ressources externes non sécurisées
        "X-Content-Type-Options": "Medium",  # Prévient le MIME type sniffing
        "Set-Cookie": "Medium",  # L'absence des drapeaux 'HttpOnly' et 'Secure' est risquée pour les cookies
        "Access-Control-Allow-Origin": "Medium",  # Une mauvaise configuration peut entraîner des vulnérabilités CORS
        "X-XSS-Protection": "Low",  # Bien que obsolète, son absence peut indiquer un manque de précautions contre XSS
        "Referrer-Policy": "Low",  # Prévient les fuites d'URL par le header 'referer'
        "Feature-Policy": "Low",  # Contrôle les fonctionnalités que le navigateur est autorisé à utiliser
        "Public-Key-Pins": "Low",  # Obsolète, mais son utilisation peut indiquer une attention particulière à la sécurité
        "Content-Type": "Medium",  # Indique le type de contenu, son absence peut entraîner des interprétations erronées
        "Cache-Control": "Medium",  # Contrôle le comportement de mise en cache, important pour la confidentialité des données sensibles
        "Expires": "Low",  # Lié au contrôle de cache, moins critique
        "Pragma": "Low",  # Header de compatibilité pour le cache, moins utilisé
        "X-Content-Security-Policy": "Low",  # Version dépréciée de CSP, son utilisation peut indiquer des configurations obsolètes
        "X-WebKit-CSP": "Low",  # Variante de CSP pour les anciens navigateurs WebKit
        "Content-Encoding": "Low",  # Détails sur l'encodage du contenu (compression, etc.), généralement sans risque
        "Transfer-Encoding": "Low",  # Détails sur l'encodage du transfert, rarement un risque
        "ETag": "Low",  # Utilisé pour la validation des caches, peut poser des problèmes de confidentialité
        "Vary": "Low",  # Indique comment la représentation du contenu peut varier
        "Access-Control-Allow-Methods": "Medium",  # Spécifie les méthodes autorisées pour CORS
        "Access-Control-Allow-Headers": "Medium",  # Spécifie les headers autorisés pour CORS
        "Access-Control-Expose-Headers": "Low",  # Headers que les navigateurs sont autorisés à rendre accessibles au client
        "Access-Control-Max-Age": "Low",  # Indique combien de temps le résultat d'une requête préalable peut être mis en cache
        "Access-Control-Allow-Credentials": "Medium",  # Indique si les requêtes CORS peuvent inclure des informations d'identification
        "Alt-Svc": "Low",  # Indique un service alternatif pour l'accès à une ressource
        "Date": "Information Leak",  # Date et heure de la réponse, généralement sans risque
        "Expect-CT": "Medium",  # Enforce Certificate Transparency
        "Origin": "Low",  # Indique l'origine de la requête, utilisé dans le cadre de CORS
        "Timing-Allow-Origin": "Low",  # Permet de partager des temps d'accès entre différents domaines
        "X-Permitted-Cross-Domain-Policies": "Medium",  # Contrôle le traitement des fichiers Adobe products
        "Content-Location": "Low",  # Indique l'emplacement alternatif pour la ressource retournée
        "Content-Disposition": "Low",  # Indique si la ressource doit être affichée dans le navigateur ou traitée comme téléchargement
        "Link": "Low",  # Fournit un moyen pour les ressources de référencer d'autres documents
        "Allow": "Low",  # Liste les méthodes de requête supportées, utilisé dans les réponses 405
        "Retry-After": "Low",  # Indique combien de temps attendre avant de refaire une requête
        "Server-Timing": "Low",  # Transmet les métriques de performance du serveur au client
        "Tk": "Low",  # Indique le suivi de l'utilisateur
        "Upgrade": "Low",  # Indique un protocole de communication plus approprié
        "Warning": "Low",  # Transporte des avertissements sur le statut ou la transformation d'un message
        "WWW-Authenticate": "Low",  # Indique les méthodes d'authentification disponibles pour accéder à la ressource
    }

        
    def __init__(self, url):
        self.url = url 
        self.headers = requests.get(self.url).headers
        banner_headers(url)
        # print(self.list_of_headers())
        self.risk_analysis("High")
        self.risk_analysis("Medium")
        self.risk_analysis("Low")
        self.risk_analysis("Information Leak")
        self.csp_analysis()
        
    def ishere(self, header):
        return header in self.headers
    
    def get_header(self, header):
        if self.ishere(header):
            return self.headers[header]
        return None

    def list_of_headers(self):
        return list(self.headers.keys())
    
    def risk_analysis(self, risk_level):
        high = {header for header, risk in self.headers_risk.items() if risk == risk_level}
        present_fields = [element for element in high if element in list(self.headers.keys())]
        absent_fields = [element for element in high if element not in list(self.headers.keys())]
        print(colorize(f'[ {risk_level} Risk (Number : {len(present_fields)} present ; {len(absent_fields)} absent)]',risk_level))
        for field in present_fields :
            print(" +  ",field, " : ", self.headers[field])
        if risk_level != "Information Leak":
            print(f' {absent_fields}')
            # for field in absent_fields :
            #     print(" -  ",field)
        return present_fields
    
    def cookie_analysis(self):
        print(colorize(" [ Cookie analysis ]","info"))
        set_cookie = self.get_header("Set-Cookie")
        if set_cookie is None:
            print("This website seems not uses cookies")
        else :
            cookies_fields = set_cookie.split(';')
            for field in cookies_fields:
                if '=' in field :
                    key, value = field.strip().split('=')
                    print(" + ",key, " : ", value)
                else :
                    print(" + ",field)
        return set_cookie
    
    def csp_analysis(self):
        """ 
        Structure : 
         Content-Security-Policy: <policy-directive>; <policy-directive>
         <policy-directive> :  <directive> <value>
         """
        
        print(colorize(" [ CSP ]","green"))
        if self.ishere("Content-Security-Policy"):
            csp = self.get_header("Content-Security-Policy")
            list_csp = csp.split(";")
            for i in list_csp :
                csp_directive = i.split(" ")[0]
                print(colorize(csp_directive,"error"))
                csp_value = i.split(" ")[1:]
                # print(csp_value)
                print(colorize(" ".join(csp_value),"green"))
            # print(colorize(csp,"error"))
        else:
            print(colorize("  CSP is not here ","info"))
            
    def __str__(self):
        return "\n".join([f"{c}: {v}" for c, v in self.headers.items()])
 
 
 
 
#  import requests

# def guess_framework_from_cookies(url):
#     try:
#         response = requests.get(url)
#         cookies = response.cookies

#         for cookie in cookies:
#             name = cookie.name.lower()
#             if 'phpsessid' in name:
#                 print(f"Le site {url} utilise probablement PHP.")
#             elif 'asp.net_sessionid' in name:
#                 print(f"Le site {url} utilise probablement ASP.NET.")
#             elif 'connect.sid' in name:
#                 print(f"Le site {url} utilise probablement Express (Node.js).")
#             # Ajoutez d'autres frameworks en fonction de leurs cookies spécifiques ici
#             else:
#                 print(f"Nom de cookie inconnu : {cookie.name}, difficile de déterminer le framework.")
#     except requests.RequestException as e:
#         print(f"Erreur lors de la requête : {e}")

# # Testez l'URL de votre choix
# url = "https://example.com"
# guess_framework_from_cookies(url)