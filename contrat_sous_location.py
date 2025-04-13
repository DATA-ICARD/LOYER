import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os
from datetime import datetime
import locale

# Charger les variables d'environnement
load_dotenv()
adresse_proprio = os.getenv('adresse_proprio')
adresse_location = os.getenv('adresse_location')  # Valeur par défaut
IBAN = os.getenv('IBAN')
BIC = os.getenv('BIC')
nom_proprio = os.getenv('nom_proprio')

# Définir la locale en français
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

# Récupérer la date actuelle
now = datetime.now()

# Formater la date pour le contrat
date_contrat = now.strftime("%d %B %Y")  # Ex. : 13 avril 2025
mois = now.strftime("%B")  # Nom complet du mois
annee = now.year

# Créer un document PDF avec matplotlib
fig, ax = plt.subplots(figsize=(8.5, 11))
ax.axis('off')  # Désactiver les axes

# Ajouter le contenu du contrat
ax.text(0.1, 0.8, f"""
Le contrat de bail de sous-location est conclu entre les soussignés :\n
B&B conciergerie, désigné ci-après « le locataire principal » d’une part, et (ICARD Yannick),\n
désigné ci-après « le bailleur » d’autre part.\n
Il est rappelé que le propriétaire du logement situé au {adresse_location}\n
autorise la sous-location de son bien par une lettre adressée au locataire principal, et dont\n
une copie est annexée au présent contrat.\n
""", fontsize=10)

# ax.text(0.1, 0.65, f"""
# I. Objet du bail de sous-location\n
# Le locataire principal s’engage à sous-louer l’ensemble/une partie du bien situé au {adresse_location}.\n\n
# II. Durée du contrat\n
# Le présent contrat de sous-location est conclu pour une durée de 1 mois.\n
# Cette durée ne peut excéder celle indiquée dans le bail de location initial.\n
# Le locataire principal comme le sous-locataire se réservent le droit de mettre fin au contrat de sous-location avant son terme.\n\n
# III. Loyer mensuel\n
# Le locataire principal s’engage à verser au bailleur principal un loyer mensuel de cinq cents euros.\n
# Les charges, taxes et impôts sont à la charge du bailleur.\n\n
# Fait à Saint Etienne,\n
# le {date_contrat},\n
# En autant d’exemplaires que de parties,\n
# Signature du bailleur précédée de la mention « lu et approuvé »
# """, fontsize=10)

# Sauvegarder le PDF
pdf_path = f'contrat_sous_location_{mois}_{annee}.pdf'
plt.savefig(pdf_path, format='pdf', bbox_inches='tight')
plt.close()

print(f"PDF généré : {pdf_path}")