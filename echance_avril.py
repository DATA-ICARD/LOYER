import matplotlib.pyplot as plt
from IPython.display import display, FileLink
from dotenv import load_dotenv
import os
from datetime import datetime
import locale


load_dotenv()  # Charge les variables d'environnement depuis le fichier .env
adresse_proprio = os.getenv('adresse_proprio')
adresse_location = os.getenv('adresse_location')
IBAN = os.getenv('IBAN')
BIC = os.getenv('BIC')
nom_proprio = os.getenv('nom_proprio')

# Définir la locale en français
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

# Récupérer la date actuelle
now = datetime.now()

# Extraire le mois et l'année
mois = now.strftime("%B")  # %B donne le nom complet du mois
annee = now.year

# Create a PDF document using matplotlib
fig, ax = plt.subplots(figsize=(8.5, 11))

# Désactiver les axes
ax.axis('off')

# Set font and title
ax.text(0.5, 0.9, f"Avis d'échéance de loyer pour le mois de : {mois} {annee}", fontsize=12, ha='center', va='center')

# Add content to the PDF
ax.text(0.1, 0.8, "Locataire : B&B Congiergerie", fontsize=10)
ax.text(0.1, 0.75, "Propriétaire : ICARD Yannick et CANIPAROLI Céline", fontsize=10)
ax.text(0.1, 0.7, f"Adresse du propriétaire : {adresse_proprio}", fontsize=10)
ax.text(0.1, 0.65, f"Adresse du bien loué : {adresse_location}", fontsize=10)

ax.text(0.1, 0.45, "Montant du loyer dû : 500 €", fontsize=10)
ax.text(0.1, 0.4, f"Période concernée : {mois} {annee}", fontsize=10)
ax.text(0.1, 0.35, f"Date d'échéance : 20 {mois} {annee}", fontsize=10)

ax.text(0.1, 0.3, "Méthode de paiement : Virement bancaire", fontsize=10)
ax.text(0.1, 0.25, f"IBAN : {IBAN}", fontsize=10)
ax.text(0.1, 0.2, f"BIC : {BIC}", fontsize=10)


# Save the PDF
pdf_path = f'avis_echeance_loyer_{mois}_{annee}.pdf'
plt.savefig(pdf_path)
plt.close()

pdf_path
