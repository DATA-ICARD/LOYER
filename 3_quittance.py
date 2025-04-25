import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from IPython.display import display, FileLink
import os
from datetime import datetime
import locale

# Essayer de charger les variables depuis un .env (utile en local)
try:
    from dotenv import load_dotenv
    load_dotenv(override=False)
except ImportError:
    print("dotenv non installé, les variables seront récupérées via l'environnement système uniquement.")

# Récupérer les variables d'environnement (qu'elles viennent du .env ou des variables système)
adresse_proprio = os.getenv('ADRESSE_PROPRIO')
adresse_location = os.getenv('ADRESSE_LOCATION')
IBAN = os.getenv('IBAN')
BIC = os.getenv('BIC')
nom_proprio = os.getenv('NOM_PROPRIO')
locataire = os.getenv('LOCATAIRE')

# Vérifier que les variables essentielles sont bien chargées
if not all([adresse_proprio, adresse_location, IBAN, BIC, nom_proprio, locataire]):
    print("⚠️ Attention : Une ou plusieurs variables d'environnement sont manquantes.")
    adresse_proprio = adresse_proprio or "Adresse proprio non définie"
    adresse_location = adresse_location or "Adresse location non définie"
    nom_proprio = nom_proprio or "Nom proprio non défini"
    locataire = locataire or "Locataire non défini"
    IBAN = IBAN or "IBAN non défini"
    BIC = BIC or "BIC non défini"

# Définir la locale en français
try:
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
except locale.Error:
    print("Locale fr_FR.UTF-8 non disponible, fallback sur locale système.")

# Récupérer la date actuelle
now = datetime.now()
mois = now.strftime("%B").lower()  # Nom complet du mois
annee = now.year

# Create a PDF document using matplotlib
fig, ax = plt.subplots(figsize=(8.5, 11))
ax.axis('off')

# Ajouter le texte
ax.text(0.5, 0.9, f"Quittance de loyer pour le mois de : {mois} {annee}", fontsize=12, ha='center', va='center', zorder=2)
ax.text(0.1, 0.8, f"Locataire : {locataire}", fontsize=10, zorder=2)
ax.text(0.1, 0.75, f"Propriétaire : {nom_proprio}", fontsize=10, zorder=2)
ax.text(0.1, 0.7, f"Adresse du propriétaire : {adresse_proprio}", fontsize=10, zorder=2)
ax.text(0.1, 0.65, f"Adresse du bien loué : {adresse_location}", fontsize=10, zorder=2)
ax.text(0.1, 0.6, "Montant du loyer réglé : 500 €", fontsize=10, zorder=2)
ax.text(0.1, 0.55, f"Période concernée : {mois} {annee}", fontsize=10, zorder=2)

# Ajouter une image de signature
signature_path = os.path.join(os.path.dirname(__file__), 'signature.png')
if os.path.exists(signature_path):
    img = mpimg.imread(signature_path)
    ax.imshow(img, extent=[0.5, 0.8, 0.3, 0.4], aspect='auto', zorder=1)
else:
    print(f"⚠️ Image {signature_path} non trouvée")

# Limites de la figure
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

# Save PDF
pdf_path = f'quittance_loyer_{mois}_{annee}.pdf'
plt.savefig(pdf_path, bbox_inches='tight')
plt.close()

# Retourner le chemin du PDF généré
print(f"✅ PDF : {pdf_path} générée")
