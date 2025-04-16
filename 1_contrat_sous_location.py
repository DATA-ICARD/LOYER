import matplotlib.pyplot as plt
import matplotlib.image as mpimg
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
ax.text(0.5, 0.95, f"""\n\nContrat de sous-location\n\n""", fontweight='bold', ha='center', fontsize=12)
ax.text(0.1, 0.90, f"""Le contrat de bail de sous-location est conclu entre les soussignés :\n\n""", fontsize=9)
ax.text(0.1, 0.88, f"""B&B conciergerie, désigné ci-après « le locataire principal » d’une part, et {nom_proprio},\n""", fontsize=9)
ax.text(0.1, 0.85, f"""désigné ci-après « le bailleur » d’autre part.\n""", fontsize=9)
ax.text(0.1, 0.82, f"""Il est rappelé que le propriétaire du logement situé au {adresse_location}\n""", fontsize=9)
ax.text(0.1, 0.79, f"""autorise la sous-location de son bien par une lettre adressée au locataire principal, et dont\n""", fontsize=9)
ax.text(0.1, 0.74, f"""une copie est annexée au présent contrat.\n\n""", fontsize=9)

ax.text(0.1, 0.70, f""" I. Objet du bail de sous-location\n""", fontweight='bold', fontsize=10)
ax.text(0.1, 0.65, f""" Le locataire principal s’engage à sous-louer l’ensemble/une partie du bien situé au {adresse_location}.\n\n""", fontsize=9)
ax.text(0.1, 0.60, f""" II. Durée du contrat\n""",fontweight='bold', fontsize=10)
ax.text(0.1, 0.55, f""" Le présent contrat de sous-location est conclu pour une durée de 1 mois.\n""", fontsize=9)
ax.text(0.1, 0.52, f""" Cette durée ne peut excéder celle indiquée dans le bail de location initial.\n""", fontsize=9)
ax.text(0.1, 0.47, f""" Le locataire principal comme le sous-locataire se réservent le droit de mettre fin au contrat de sous-location avant son terme.\n\n""", fontsize=9)
ax.text(0.1, 0.44, f""" III. Loyer mensuel\n""",fontweight='bold', fontsize=10)
ax.text(0.1, 0.39, f"""  Le locataire principal s’engage à verser au bailleur principal un loyer mensuel de cinq cents euros.\n""", fontsize=9)
ax.text(0.1, 0.34, f"""  Les charges, taxes et impôts sont à la charge du bailleur.\n\n""", fontsize=9)
ax.text(0.1, 0.30, f"""  Fait à Saint Etienne,\n""", fontsize=9)
ax.text(0.1, 0.25, f"""  le {date_contrat},\n""", fontsize=9)
ax.text(0.1, 0.22, f"""  En autant d’exemplaires que de parties,\n""", fontsize=9)
ax.text(0.1, 0.18, f"""  Signature du bailleur précédée de la mention « lu et approuvé »\n""", fontsize=9)
ax.text(0.1, 0.14, f"""                         Lu et Approuvé""", fontsize=9)
ax.text(0.1, 0.05, f"""  Signature du locataire précédée de la mention « lu et approuvé »\n""", fontsize=9)
ax.text(0.1, 0.02, f"""                         Lu et Approuvé""", fontsize=9)

# Ajouter une image de signature
signature_path = "C:/appartement/valbenoite/echeance/signature.png"
try:
    img = mpimg.imread(signature_path)
    # Ajuster la position et la taille de l'image (x_min, x_max, y_min, y_max)
    ax.imshow(img, extent=[0.5, 0.8, 0.02, 0.20], aspect='auto', zorder=1)
except FileNotFoundError:
    print(f"Erreur : L'image {signature_path} n'a pas été trouvée.")

# Définir les limites de la figure pour s'assurer que tout est visible
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

# Sauvegarder le PDF
pdf_path = f'contrat_sous_location_{mois}_{annee}.pdf'
plt.savefig(pdf_path, format='pdf', bbox_inches='tight')
plt.close()

print(f"PDF généré : {pdf_path}")