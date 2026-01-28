import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
from datetime import datetime

# Charger les variables d'environnement depuis le fichier .env
load_dotenv(override=False)
nom_proprio = os.getenv('NOM_PROPRIO')

# Récupérer directement le numéro du mois pour éviter les problèmes de locale
mois_numero = datetime.now().month
# Mapper directement par numéro de mois pour éviter les problèmes d'encodage
mois_noms = [
    'janvier', 'fevrier', 'mars', 'avril', 'mai', 'juin',
    'juillet', 'aout', 'septembre', 'octobre', 'novembre', 'decembre'
]
mois = mois_noms[mois_numero - 1]  # -1 car les listes commencent à 0
annee = datetime.now().year

# Sujet et corps du message
sujet = f"Quittance de loyer"
corps = f"""Bonjour,
Voici votre quittance de loyer pour le mois de : {mois} {annee}, 
Cordialement,
{nom_proprio}"""

# Chemin du fichier PDF
#pdf_path = f'quittance_loyer_{mois}_{annee}.pdf'

# Vérifier que le fichier PDF existe
#if not os.path.exists(pdf_path):
 #   raise FileNotFoundError(f"Le fichier {pdf_path} n'existe pas. Assure-toi qu'il est dans le bon dossier.")

# Récupérer les identifiants depuis les variables d'environnement
expediteur = os.getenv('EXPEDITEUR')
destinataire = os.getenv('DESTINATAIRE')
destinataire_cci = os.getenv('DESTINATAIRE_CCI')
mot_de_passe = os.getenv('GMAIL_APP_PASSWORD')  # Le mot de passe d'application

# Créer un message multipart (pour le texte et la pièce jointe)
msg = MIMEMultipart()
msg['From'] = expediteur
msg['To'] = destinataire
if destinataire_cci:
    msg['Bcc'] = destinataire_cci
msg['Subject'] = sujet

# Ajouter le corps du message
msg.attach(MIMEText(corps, 'plain'))

# Ajouter le fichier PDF en pièce jointe
##part = MIMEBase('application', 'octet-stream')
##with open(pdf_path, 'rb') as file:
#    part.set_payload(file.read())
#encoders.encode_base64(part)
#part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(pdf_path)}')
#msg.attach(part)

# Envoyer l'email via SMTP Gmail
try:
    # Connexion au serveur SMTP de Gmail
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()  # Sécuriser la connexion
        server.login(expediteur, mot_de_passe)
        server.send_message(msg)
    
    print("Email envoyé avec succès !")
   ## os.remove(pdf_path)  # Supprime le fichier PDF après l'envoi
except Exception as e:
    print(f"Erreur lors de l'envoi : {e}")

