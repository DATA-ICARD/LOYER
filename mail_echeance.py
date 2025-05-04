import base64
import os
import locale
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

# Charger les variables d'environnement depuis les secrets GitHub
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
refresh_token = os.getenv('REFRESH_TOKEN')
nom_proprio = os.getenv('NOM_PROPRIO')
destinataire = os.getenv('DESTINATAIRE')
destinataire_cci = os.getenv('DESTINATAIRE_CCI')
expediteur = os.getenv('EXPEDITEUR')

# Vérifier les valeurs des variables d'environnement (pour le débogage)
print(f"CLIENT_ID: {client_id}")
print(f"CLIENT_SECRET: {client_secret}")
print(f"REFRESH_TOKEN: {refresh_token}")
print(f"DESTINATAIRE: {destinataire}")
print(f"DESTINATAIRE_CCI: {destinataire_cci}")
print(f"EXPEDITEUR: {expediteur}")

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
sujet = f"Avis d'échéance de loyer {mois} {annee}"
corps = f"""Bonjour,
Voici l'avis d'échéance de loyer pour le mois de : {mois} {annee},
Cordialement,
{nom_proprio}"""

# Chemin du fichier PDF
pdf_path = f'avis_echeance_loyer_{mois}_{annee}.pdf'

# Vérifier que le fichier PDF existe
if not os.path.exists(pdf_path):
    raise FileNotFoundError(f"Le fichier {pdf_path} n'existe pas. Assure-toi qu'il est dans le bon dossier.")

# Scopes nécessaires pour envoyer des emails
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# Créer les informations d'identification à partir du refresh token
creds = Credentials.from_authorized_user_info(
    info={
        'refresh_token': refresh_token,
        'client_id': client_id,
        'client_secret': client_secret,
        'token_uri': 'https://oauth2.googleapis.com/token'
    },
    scopes=SCOPES
)

# Rafraîchir le token s'il est expiré
if not creds.valid:
    if creds.expired and creds.refresh_token:
        print("Rafraîchissement du token...")
        creds.refresh(Request())
    else:
        print("Erreur : Les informations d'authentification initiales ne sont pas valides.")
        exit(1) # Arrêter le script en cas d'erreur d'authentification

# Construire le service Gmail
service = build('gmail', 'v1', credentials=creds)

# Créer un message multipart (pour le texte et la pièce jointe)
msg = MIMEMultipart()
msg['to'] = destinataire  # Adresse email du destinataire
msg['Bcc'] = destinataire_cci
msg['from'] = expediteur  # Adresse email de l'expéditeur
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
    print(f"Email envoyé avec succès ! ID du message : {message['id']}")
    os.remove(pdf_path)  # Supprime le fichier PDF après l'envoi
except HttpError as error:
    print(f"Erreur lors de l'envoi de l'email : {error}")
