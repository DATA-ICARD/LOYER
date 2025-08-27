import base64
import os
import locale
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
from datetime import datetime
from google.auth.transport.requests import Request


# Charger les variables d'environnement depuis le fichier .env
load_dotenv()
nom_proprio = os.getenv('NOM_PROPRIO')
destinataire = os.getenv('DESTINATAIRE_CCI')
# destinataire_cci = os.getenv('DESTINATAIRE_CCI')
expediteur = os.getenv('EXPEDITEUR')
# Définir la locale en français (adapter selon ton système)
try:
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
except locale.Error:
    locale.setlocale(locale.LC_TIME, 'fr_FR')

# Récupérer la date actuelle
now = datetime.now()
mois = now.strftime("%B")  # Nom complet du mois (ex. "avril")
annee = now.year

# Sujet et corps du message
sujet = f"Contrat de sous location "
corps = f"""Bonjour,
Voici le contrat de sous location pour le mois de : {mois} {annee}. 
Cordialement,
{nom_proprio}"""

# Chemin du fichier PDF
pdf_path = f'contrat_sous_location_{mois}_{annee}.pdf'

# Vérifier que le fichier PDF existe
if not os.path.exists(pdf_path):
    raise FileNotFoundError(f"Le fichier {pdf_path} n'existe pas. Assure-toi qu'il est dans le bon dossier.")

# Scopes nécessaires pour envoyer des emails
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# Chemin pour sauvegarder les jetons
TOKEN_FILE = 'token.json'

# Charger les jetons existants ou en obtenir de nouveaux
creds = None
if os.path.exists(TOKEN_FILE):
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

# Si aucun jeton valide n'existe, demander une nouvelle autorisation
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0, prompt='consent')
    # Sauvegarder les jetons pour une utilisation future
    with open(TOKEN_FILE, 'w') as token:
        token.write(creds.to_json())

# Construire le service Gmail
service = build('gmail', 'v1', credentials=creds)

# Créer un message multipart (pour le texte et la pièce jointe)
msg = MIMEMultipart()
msg['to'] = os.getenv('DESTINATAIRE')
msg['Bcc'] = os.getenv('DESTINATAIRE_CCI')
msg['from'] =  os.getenv('EXPEDITEUR') # Adresse email de l'expéditeur
msg['subject'] = sujet

# Ajouter le corps du message
msg.attach(MIMEText(corps, 'plain'))

# Ajouter le fichier PDF en pièce jointe
part = MIMEBase('application', 'octet-stream')
with open(pdf_path, 'rb') as file:
    part.set_payload(file.read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(pdf_path)}')
msg.attach(part)

# Encoder le message pour l'API Gmail
raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
body = {'raw': raw}

# Envoyer l'email
try:
    message = service.users().messages().send(userId="me", body=body).execute()
    print("Email envoyé avec succès !")
    os.remove(pdf_path)  # Supprime le fichier PDF après l'envoi
except Exception as e:
    print(f"Erreur : {e}")
