import matplotlib.pyplot as plt
from IPython.display import display, FileLink
import os
from datetime import datetime
import locale

# Essayer de charger les variables depuis un .env (utile en local)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("dotenv non installé, les variables seront récupérées via l'environnement système uniquement.")

# Récupérer les variables d'environnement
adresse_proprio = os.getenv('ADRESSE_PROPRIO')
adresse_location = os.getenv('ADRESSE_LOCATION')
IBAN = os.getenv('IBAN')
BIC = os.getenv('BIC')
nom_proprio = os.getenv('NOM_PROPRIO')  # ici tu avais une typo MON_PROPRIOgit add

# Vérifier que les variables essentielles sont bien chargées
if not all([adresse_proprio, adresse_location, IBAN, BIC, nom_proprio]):
    print("⚠️ Attention : Une ou plusieurs variables d'environnement sont manquantes.")
    adresse_proprio = adresse_proprio or "Adresse proprio non définie"
    adresse_location = adresse_location or "Adresse location non définie"
    nom_proprio = nom_proprio or "Nom proprio non défini"
    IBAN = IBAN or "IBAN non défini"
    BIC = BIC or "BIC non défini"

# Définir la locale en français
try:
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
except locale.Error:
    print("Locale fr_FR.UTF-8 non disponible, fallback sur locale système.")

# Récupérer la date actuelle
now = datetime.now()
mois_avec_accent = datetime.now().strftime("%B")  # Nom complet du mois avec accent
annee = datetime.now().year

# Dictionnaire personnalisé des mois sans accent
mois_sans_accent = {
    1: "janvier", 2: "fevrier", 3: "mars", 4: "avril",
    5: "mai", 6: "juin", 7: "juillet", 8: "aout",
    9: "septembre", 10: "octobre", 11: "novembre", 12: "decembre"
}

mois = mois_sans_accent[datetime.now().month]  # unicodedata

# Create a PDF document using matplotlib
fig, ax = plt.subplots(figsize=(8.5, 11))
ax.axis('off')

# Set title
ax.text(0.5, 0.9, f"Avis d'échéance de loyer pour le mois de : {mois} {annee}", fontsize=12, ha='center', va='center')

# Add content to the PDF
ax.text(0.1, 0.8, "Locataire : B&B Conciergerie", fontsize=10)
ax.text(0.1, 0.75, f"Propriétaire : {nom_proprio}", fontsize=10)
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
plt.savefig(pdf_path, bbox_inches='tight')
plt.close()

# Retourner le chemin du PDF généré
print(f"✅ PDF : {pdf_path} généré")
