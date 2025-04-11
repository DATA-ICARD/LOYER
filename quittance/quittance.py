import matplotlib.pyplot as plt
import matplotlib.image as mpimg
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

# Vérifier que les variables sont bien chargées
if not all([adresse_proprio, adresse_location, IBAN, BIC, nom_proprio]):
    print("Erreur : Une ou plusieurs variables d'environnement sont manquantes.")
    adresse_proprio = adresse_proprio or "Adresse proprio non définie"
    adresse_location = adresse_location or "Adresse location non définie"

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

# Ajouter le texte
ax.text(0.5, 0.9, f"Quittance de loyer pour le mois de : {mois} {annee}", fontsize=12, ha='center', va='center', zorder=2)
ax.text(0.1, 0.8, "Locataire : B&B Congiergerie", fontsize=10, zorder=2)
ax.text(0.1, 0.75, "Propriétaire : ICARD Yannick et CANIPAROLI Céline", fontsize=10, zorder=2)
ax.text(0.1, 0.7, f"Adresse du propriétaire : {adresse_proprio}", fontsize=10, zorder=2)
ax.text(0.1, 0.65, f"Adresse du bien loué : {adresse_location}", fontsize=10, zorder=2)
ax.text(0.1, 0.6, "Montant du loyer réglé : 500 €", fontsize=10, zorder=2)
ax.text(0.1, 0.55, f"Période concernée : {mois} {annee}", fontsize=10, zorder=2)

# Ajouter une image de signature
signature_path = "C:/appartement/valbenoite/echeance/signature.png"
try:
    img = mpimg.imread(signature_path)
    # Ajuster la position et la taille de l'image (x_min, x_max, y_min, y_max)
    ax.imshow(img, extent=[0.5, 0.8, 0.3, 0.4], aspect='auto', zorder=1)
except FileNotFoundError:
    print(f"Erreur : L'image {signature_path} n'a pas été trouvée.")

# Définir les limites de la figure pour s'assurer que tout est visible
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

# Save the PDF
pdf_path = f'quittance_loyer_{mois}_{annee}.pdf'
plt.savefig(pdf_path, bbox_inches='tight')
plt.close()

pdf_path