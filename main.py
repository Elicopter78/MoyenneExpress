import tkinter as tk
from tkinter import messagebox
import json
import os

# Fonction pour convertir une note sur une échelle donnée en une note sur 20
def convertir_vers_20(note, sur_max):
    try:
        return (note / sur_max) * 20
    except ZeroDivisionError:
        messagebox.showerror("Erreur", "La note maximale ne peut pas être zéro.")
        return 0

# Fonction pour calculer la moyenne pondérée des notes
def calculer_moyenne():
    try:
        nombre_de_notes = int(entrée_nombre_notes.get())
        if nombre_de_notes <= 0:
            messagebox.showerror("Erreur", "Le nombre de notes doit être supérieur à zéro.")
            return

        total_notes = 0
        total_coefficients = 0

        # Vérifie que le nombre de champs correspond au nombre de notes
        if len(entrée_notes) != nombre_de_notes or len(entrée_maximums) != nombre_de_notes or len(entrée_coefficients) != nombre_de_notes:
            messagebox.showerror("Erreur", "Le nombre de champs de saisie ne correspond pas au nombre de notes spécifié.")
            return

        # Calcule le total des notes pondérées et des coefficients
        for i in range(nombre_de_notes):
            note = float(entrée_notes[i].get())
            sur_max = float(entrée_maximums[i].get())
            coefficient = float(entrée_coefficients[i].get())

            if sur_max <= 0:
                messagebox.showerror("Erreur", f"La note maximale pour la note {i+1} ne peut pas être zéro ou négative.")
                return

            if coefficient < 0:
                messagebox.showerror("Erreur", f"Le coefficient pour la note {i+1} ne peut pas être négatif.")
                return

            note_sur_20 = convertir_vers_20(note, sur_max)
            total_notes += note_sur_20 * coefficient
            total_coefficients += coefficient

        if total_coefficients == 0:
            messagebox.showerror("Erreur", "La somme des coefficients ne peut pas être zéro.")
            return

        # Calcule et affiche la moyenne
        moyenne = total_notes / total_coefficients
        label_résultat.config(text=f"Moyenne : {moyenne:.2f}")

        # Sauvegarde les données entrées
        sauvegarder_données()

    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer des valeurs valides pour les notes, les maximums et les coefficients.")

# Fonction pour créer les champs de saisie pour les notes, maximums et coefficients
def créer_champs():
    try:
        # Réinitialise les champs existants
        for widget in cadre_interne.winfo_children():
            widget.destroy()

        global entrée_notes, entrée_maximums, entrée_coefficients, boutons_supprimer
        entrée_notes = []
        entrée_maximums = []
        entrée_coefficients = []
        boutons_supprimer = []

        # Obtenez le nombre de notes à créer
        nombre_de_notes = int(entrée_nombre_notes.get())

        # Crée les champs pour chaque note
        for i in range(nombre_de_notes):
            label_note = tk.Label(cadre_interne, text=f"Note {i+1}:", width=8)
            label_note.grid(row=i, column=0, padx=2, pady=2)
            entrée_note = tk.Entry(cadre_interne, width=8)
            entrée_note.grid(row=i, column=1, padx=2, pady=2)
            entrée_note.bind("<Right>", lambda e, idx=i: focus_next_cell(idx, 1))
            entrée_note.bind("<Left>", lambda e, idx=i: focus_prev_cell(idx, 1))
            entrée_note.bind("<Down>", lambda e, idx=i: focus_next_row(idx, 1))
            entrée_note.bind("<Up>", lambda e, idx=i: focus_prev_row(idx, 1))
            entrée_notes.append(entrée_note)

            label_max = tk.Label(cadre_interne, text=f"Max {i+1}:", width=8)
            label_max.grid(row=i, column=2, padx=2, pady=2)
            entrée_max = tk.Entry(cadre_interne, width=8)
            entrée_max.grid(row=i, column=3, padx=2, pady=2)
            entrée_max.bind("<Right>", lambda e, idx=i: focus_next_cell(idx, 3))
            entrée_max.bind("<Left>", lambda e, idx=i: focus_prev_cell(idx, 3))
            entrée_max.bind("<Down>", lambda e, idx=i: focus_next_row(idx, 3))
            entrée_max.bind("<Up>", lambda e, idx=i: focus_prev_row(idx, 3))
            entrée_maximums.append(entrée_max)

            label_coeff = tk.Label(cadre_interne, text=f"Coeff {i+1}:", width=8)
            label_coeff.grid(row=i, column=4, padx=2, pady=2)
            entrée_coeff = tk.Entry(cadre_interne, width=8)
            entrée_coeff.grid(row=i, column=5, padx=2, pady=2)
            entrée_coeff.bind("<Right>", lambda e, idx=i: focus_next_cell(idx, 5))
            entrée_coeff.bind("<Left>", lambda e, idx=i: focus_prev_cell(idx, 5))
            entrée_coeff.bind("<Down>", lambda e, idx=i: focus_next_row(idx, 5))
            entrée_coeff.bind("<Up>", lambda e, idx=i: focus_prev_row(idx, 5))
            entrée_coefficients.append(entrée_coeff)

            # Bouton "-" pour supprimer une note
            bouton_supprimer = tk.Button(cadre_interne, text="-", command=lambda idx=i: supprimer_note(idx))
            bouton_supprimer.grid(row=i, column=6, padx=2, pady=2)
            boutons_supprimer.append(bouton_supprimer)

            # Si des données sont chargées, les insérer dans les champs
            if données_chargées and i < len(données_chargées["notes"]):
                entrée_notes[i].insert(0, données_chargées["notes"][i])
                entrée_maximums[i].insert(0, données_chargées["maximums"][i])
                entrée_coefficients[i].insert(0, données_chargées["coefficients"][i])

        update_scrollregion()

    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer un nombre valide pour le nombre de notes.")

# Supprime une note spécifique et met à jour le fichier JSON
def supprimer_note(index):
    # Supprime les widgets de la ligne spécifiée
    for widget in cadre_interne.grid_slaves():
        if int(widget.grid_info()["row"]) == index:
            widget.grid_forget()
    del entrée_notes[index]
    del entrée_maximums[index]
    del entrée_coefficients[index]
    del boutons_supprimer[index]

    # Met à jour le nombre de notes
    nombre_de_notes = int(entrée_nombre_notes.get()) - 1
    entrée_nombre_notes.delete(0, tk.END)
    entrée_nombre_notes.insert(0, str(nombre_de_notes))

    # Sauvegarde les données restantes
    sauvegarder_données()

    update_scrollregion()

# Ajoute une nouvelle note tout en conservant les données existantes
def ajouter_note():
    try:
        # Sauvegarde les données actuelles
        notes_actuelles = [entrée.get() for entrée in entrée_notes]
        maximums_actuels = [entrée.get() for entrée in entrée_maximums]
        coefficients_actuels = [entrée.get() for entrée in entrée_coefficients]

        # Incrémente le nombre de notes
        nombre_de_notes = int(entrée_nombre_notes.get()) + 1
        entrée_nombre_notes.delete(0, tk.END)
        entrée_nombre_notes.insert(0, str(nombre_de_notes))

        # Crée les nouveaux champs
        créer_champs()

        # Restaure les données sauvegardées
        for i in range(len(notes_actuelles)):
            entrée_notes[i].delete(0, tk.END)  # Efface le contenu existant
            entrée_notes[i].insert(0, notes_actuelles[i])
            entrée_maximums[i].delete(0, tk.END)
            entrée_maximums[i].insert(0, maximums_actuels[i])
            entrée_coefficients[i].delete(0, tk.END)
            entrée_coefficients[i].insert(0, coefficients_actuels[i])

    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer un nombre valide pour le nombre de notes.")

# Réinitialise les notes et supprime le fichier de sauvegarde
def réinitialiser_notes():
    entrée_nombre_notes.delete(0, tk.END)
    entrée_nombre_notes.insert(0, "0")
    créer_champs()

    # Supprime le fichier moyenne_data.json s'il existe dans le répertoire personnel
    chemin_fichier = os.path.join(os.path.expanduser("~"), "moyenne_data.json")
    if os.path.exists(chemin_fichier):
        os.remove(chemin_fichier)

# Met à jour la région de défilement du canvas
def update_scrollregion():
    canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

# Lie le défilement de la souris au canvas
def bind_mousewheel(widget):
    widget.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(-1 * (event.delta // 120), "units"))
    widget.bind_all("<Shift-MouseWheel>", lambda event: canvas.xview_scroll(-1 * (event.delta // 120), "units"))

# Fonctions pour naviguer dans les champs avec les touches directionnelles
def focus_next_cell(row, col):
    if col == 1:
        entrée_maximums[row].focus_set()
    elif col == 3:
        entrée_coefficients[row].focus_set()
    elif col == 5 and row < len(entrée_notes) - 1:
        entrée_notes[row + 1].focus_set()

def focus_prev_cell(row, col):
    if col == 5:
        entrée_maximums[row].focus_set()
    elif col == 3:
        entrée_notes[row].focus_set()
    elif col == 1 and row > 0:
        entrée_coefficients[row - 1].focus_set()

def focus_next_row(row, col):
    if row < len(entrée_notes) - 1:
        if col == 1:
            entrée_notes[row + 1].focus_set()
        elif col == 3:
            entrée_maximums[row + 1].focus_set()
        elif col == 5:
            entrée_coefficients[row + 1].focus_set()

def focus_prev_row(row, col):
    if row > 0:
        if col == 1:
            entrée_notes[row - 1].focus_set()
        elif col == 3:
            entrée_maximums[row - 1].focus_set()
        elif col == 5:
            entrée_coefficients[row - 1].focus_set()

# Valide le nombre de notes et crée les champs de saisie
def valider_nombre_notes(event):
    créer_champs()

# Valide et calcule la moyenne
def valider_calcul_moyenne(event):
    calculer_moyenne()

# Sauvegarde les données dans un fichier JSON dans le répertoire personnel
def sauvegarder_données():
    try:
        données = {
            "nombre_de_notes": entrée_nombre_notes.get(),
            "notes": [entrer.get() for entrer in entrée_notes],
            "maximums": [entrer.get() for entrer in entrée_maximums],
            "coefficients": [entrer.get() for entrer in entrée_coefficients]
        }
        chemin_fichier = os.path.join(os.path.expanduser("~"), "moyenne_data.json")
        with open(chemin_fichier, "w") as f:
            json.dump(données, f)
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de sauvegarder les données : {e}")

# Charge les données depuis un fichier JSON dans le répertoire personnel
def charger_données():
    chemin_fichier = os.path.join(os.path.expanduser("~"), "moyenne_data.json")
    if os.path.exists(chemin_fichier):
        try:
            with open(chemin_fichier, "r") as f:
                return json.load(f)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger les données : {e}")
    return None

# Création de la fenêtre principale
root = tk.Tk()
root.title("MoyenneExpress")

# Cadre de défilement
cadre_scroll = tk.Frame(root)
cadre_scroll.pack(fill=tk.BOTH, expand=True, pady=10)

canvas = tk.Canvas(cadre_scroll)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

barre_défilement = tk.Scrollbar(cadre_scroll, orient=tk.VERTICAL, command=canvas.yview)
barre_défilement.pack(side=tk.RIGHT, fill=tk.Y)

canvas.config(yscrollcommand=barre_défilement.set)

cadre_interne = tk.Frame(canvas)
canvas.create_window((0, 0), window=cadre_interne, anchor="nw")

bind_mousewheel(root)

# Charger les données si elles existent
données_chargées = charger_données()

# Afficher le titre
label_titre = tk.Label(root, text="Entrez vos notes, je vais faire votre moyenne. \n ATTENTION, si vous avez une note décimale, \n utilisez un point à la place d'une virgule.", font=("Arial", 16))
label_titre.pack(pady=10)

# Bouton pour ajouter une nouvelle note
button_ajouter_note = tk.Button(root, text="+", command=ajouter_note)
button_ajouter_note.pack(pady=5)

# Cadre pour le nombre de notes
cadre_nombre_notes = tk.Frame(root)
cadre_nombre_notes.pack(pady=10)

label_nombre_notes = tk.Label(cadre_nombre_notes, text="Nombre de notes :")
label_nombre_notes.grid(row=0, column=0, padx=5)
entrée_nombre_notes = tk.Entry(cadre_nombre_notes)
entrée_nombre_notes.grid(row=0, column=1, padx=5)

# Si des données sont chargées, les afficher
if données_chargées:
    entrée_nombre_notes.insert(0, données_chargées["nombre_de_notes"])
    créer_champs()

# Lier la touche "Enter" pour valider le nombre de notes
entrée_nombre_notes.bind("<Return>", valider_nombre_notes)

# Bouton pour créer les champs de saisie
button_créer_champs = tk.Button(root, text="Entrer les notes", command=créer_champs)
button_créer_champs.pack(pady=10)

# Bouton pour réinitialiser les notes
button_réinitialiser = tk.Button(root, text="Réinitialiser les notes", command=réinitialiser_notes)
button_réinitialiser.pack(pady=10)

# Bouton pour calculer la moyenne
button_calculer = tk.Button(root, text="Calculer la Moyenne", command=calculer_moyenne)
button_calculer.pack(pady=10)
button_calculer.bind("<Return>", valider_calcul_moyenne)

# Label pour afficher la moyenne calculée
label_résultat = tk.Label(root, text="Moyenne : -", font=("Arial", 14))
label_résultat.pack(pady=10)

root.mainloop()
