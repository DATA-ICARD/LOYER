import matplotlib.pyplot as plt
from IPython.display import display, FileLink

# Create a PDF document using matplotlib
fig, ax = plt.subplots(figsize=(8.5, 11))

# Set font and title
ax.text(0.5, 0.9, "Avis d'échéance de loyer", fontsize=12, ha='center', va='center')

# Add content to the PDF
ax.text(0.1, 0.8, "Locataire : B&B Congiergerie", fontsize=10)
ax.text(0.1, 0.75, "Propriétaire : ICARD Yannick et CANIPAROLI Céline", fontsize=10)
ax.text(0.1, 0.7, "Adresse du propriétaire : 43 rue Voltaire, 83640 Saint Zacharie", fontsize=10)
ax.text(0.1, 0.65, "Adresse du bien loué : 66 bd Valbenoite, 42100 Saint Etienne", fontsize=10)

ax.text(0.1, 0.55, "Objet : Avis d'échéance de loyer pour le mois d'avril 2025", fontsize=10)

ax.text(0.1, 0.45, "Montant du loyer dû : 500 €", fontsize=10)
ax.text(0.1, 0.4, "Période concernée : Avril 2025", fontsize=10)
ax.text(0.1, 0.35, "Date d'échéance : 20 avril 2025", fontsize=10)

ax.text(0.1, 0.25, "Méthode de paiement : Virement bancaire", fontsize=10)

# Save the PDF
pdf_path = 'avis_echeance_loyer.pdf'
plt.savefig(pdf_path)
plt.close()

pdf_path