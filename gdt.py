"""
Projet Interface Graphique de Gestion de Tâches - 25 octobre 2023
Participants :
- Jonathan Rocha
- Stéphanne Koch-Gallion
- Boris Prince
"""
import tkinter as tk
from tkinter import messagebox
import json

class TaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion avancée de tâches")
        self.liste_taches = []  # Liste pour stocker les tâches
        self.listes_enregistrees = []  # liste pour stocker les noms des listes enregistrées
        self.create_gui()  # Créer l'interface graphique



    def create_gui(self):
        # Partie gauche de l'interface
        self.left_frame = tk.Frame(self.root)
        self.left_frame.grid(row=0, column=0, padx=10, pady=10)

        # éléments d'entrée des données
        self.description_label = tk.Label(self.left_frame, text="Description de la tâche:")
        self.description_label.grid(row=0, column=0, padx=10, pady=5)
        self.description_entry = tk.Entry(self.left_frame)
        self.description_entry.grid(row=0, column=1, padx=10, pady=5)

        self.date_echeance_label = tk.Label(self.left_frame, text="Date d'échéance (jj/mm/aaaa):")
        self.date_echeance_label.grid(row=1, column=0, padx=10, pady=5)
        self.date_echeance_entry = tk.Entry(self.left_frame)
        self.date_echeance_entry.grid(row=1, column=1, padx=10, pady=5)

        # Bouton pour ajouter une tâche
        self.ajouter_bouton = tk.Button(self.left_frame, text="Ajouter", command=self.ajouter_tache)
        self.ajouter_bouton.grid(row=2, column=0, columnspan=2, pady=10)

        # Liste des tâches
        self.liste_tachesbox = tk.Listbox(self.left_frame, selectmode=tk.SINGLE, width=40, height=10)
        self.liste_tachesbox.grid(row=3, column=0, columnspan=2, padx=10, pady=5)


        # Bouton pour marquer/annuler comme terminée
        self.marquer_terminee_bouton = tk.Button(self.left_frame, text="Marquer/Annuler comme terminée", command=self.marquer_comme_terminee)
        self.marquer_terminee_bouton.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

        # Bouton pour supprimer une tâche
        self.supprimer_bouton = tk.Button(self.left_frame, text="Supprimer", command=self.supprimer_tache)
        self.supprimer_bouton.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

        # Bouton pour trier les tâches par date d'échéance
        self.tri_bouton = tk.Button(self.left_frame, text="Trier les tâches par date d'échéance", command=self.trier_par_date_echeance)
        self.tri_bouton.grid(row=6, column=0, columnspan=2, pady=10)




        # Partie droite de l'interface
        self.right_frame = tk.Frame(self.root)
        self.right_frame.grid(row=0, column=1, padx=10, pady=10)

        # élément d'entrée pour le nom du fichier
        self.enregistrer_label = tk.Label(self.right_frame, text="Nom du fichier pour enregistrement:")
        self.enregistrer_label.grid(row=0, column=0, padx=10, pady=5)
        self.nom_fichier_entry = tk.Entry(self.right_frame)
        self.nom_fichier_entry.grid(row=0, column=1, padx=10, pady=5)

        # Bouton pour enregistrer la liste de tâches
        self.enregistrer_bouton = tk.Button(self.right_frame, text="Enregistrer la liste", command=self.enregistrer_liste)
        self.enregistrer_bouton.grid(row=1, column=0, columnspan=2, pady=10)

        # Liste des listes enregistrées
        self.listes_enregistreesbox = tk.Listbox(self.right_frame, width=30, height=10)
        self.listes_enregistreesbox.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        # Bouton pour charger une liste enregistrée
        self.charger_bouton = tk.Button(self.right_frame, text="Charger la liste", command=self.charger_liste)
        self.charger_bouton.grid(row=3, column=0, columnspan=2, pady=10)

        # Bouton pour supprimer une liste enregistrée
        self.supprimer_liste_bouton = tk.Button(self.right_frame, text="Supprimer la liste", command=self.supprimer_liste)
        self.supprimer_liste_bouton.grid(row=4, column=0, columnspan=2, pady=10)

        self.charger_listes_enregistrees()# Charger les listes enregistrées depuis le fichier

    def ajouter_tache(self):
        # Récupérer la description et la date d'échéance depuis les champs d'entrée
        description = self.description_entry.get()
        date_echeance = self.date_echeance_entry.get()

        if description and date_echeance:
            # Créer un dictionnaire représentant une tâche et l'ajouter à la liste de tâches
            tache = {"description": description, "date_echeance": date_echeance, "terminee": False}
            self.liste_taches.append(tache)
            self.mise_a_jour_liste_taches()  # Mise à jour de l'affichage des tâches
            self.description_entry.delete(0, tk.END)  # Effacer le champ de description
            self.date_echeance_entry.delete(0, tk.END)  # Effacer le champ de date d'échéance
        else:
            messagebox.showwarning("Erreur", "Veuillez remplir tous les champs.")

    def marquer_comme_terminee(self):
        # Récupérer la tâche sélectionnée dans la liste
        selection = self.liste_tachesbox.curselection()
        if selection:
            index = selection[0]
            if 0 <= index < len(self.liste_taches):
                
                self.liste_taches[index]["terminee"] = not self.liste_taches[index]["terminee"] # Inverser l'état "terminee" de la tâche
                self.mise_a_jour_liste_taches()  # Mettre à jour l'affichage des tâches

    def supprimer_tache(self):
        selection = self.liste_tachesbox.curselection() # Récupérer la tâche sélectionnée dans la liste
        if selection:
            index = selection[0] # Obtenir l'indice de la tâche sélectionnée
            if 0 <= index < len(self.liste_taches): # Vérifier si l'indice est valide, dans la plage des indices de la liste
                del self.liste_taches[index] # Supprimer la tâche de la liste
                self.mise_a_jour_liste_taches() # Mettre à jour l'affichage des tâches

    def trier_par_date_echeance(self):
        # Trier la liste de tâches par date d'échéance
        self.liste_taches.sort(key=lambda x: x["date_echeance"])
        self.mise_a_jour_liste_taches()  # Mettre à jour l'affichage des tâches

    def enregistrer_liste(self):
        nom_fichier = self.nom_fichier_entry.get()
        if nom_fichier:
            # Enregistrer la liste de tâches dans un fichier JSON avec le nom donné
            with open(f"{nom_fichier}.json", "w") as fichier:
                json.dump(self.liste_taches, fichier)
            self.listes_enregistrees.append(nom_fichier)  # Ajouter le nom de la liste aux listes enregistrées
            self.sauvegarder_listes_enregistrees()  # Sauvegarder la liste des listes enregistrées
            self.nom_fichier_entry.delete(0, tk.END)  # Effacer le champ du nom de fichier
            self.mise_a_jour_listes_enregistrees()  # Mettre à jour l'affichage des listes enregistrées
        else:
            messagebox.showwarning("Erreur", "Veuillez entrer un nom de fichier.")

    def charger_liste(self):
        selection = self.listes_enregistreesbox.curselection()
        if selection:
            index = selection[0]
            nom_fichier = self.listes_enregistrees[index]
            with open(f"{nom_fichier}.json", "r") as fichier:
                self.liste_taches = json.load(fichier)  #Charger la liste de tâches depuis le fichier
            self.mise_a_jour_liste_taches()  # Permet de mettre à jour l'affichage des tâches

    def supprimer_liste(self):
        selection = self.listes_enregistreesbox.curselection()
        if selection:
            index = selection[0]
            nom_fichier = self.listes_enregistrees[index]
            self.listes_enregistrees.remove(nom_fichier)  #Supprimer le nom de la liste des listes enregistrées
            self.sauvegarder_listes_enregistrees()  #Sauvegarder la liste des listes enregistrées

            #Supprimer le fichier de la liste de tâches enregistrées
            import os
            os.remove(f"{nom_fichier}.json")

        self.mise_a_jour_listes_enregistrees()  #Mettre à jour l'affichage des listes enregistrées

    def sauvegarder_listes_enregistrees(self):
        with open("listes_enregistrees.json", "w") as fichier:
            json.dump(self.listes_enregistrees, fichier)

    def charger_listes_enregistrees(self):
        try:
            with open("listes_enregistrees.json", "r") as fichier:
                self.listes_enregistrees = json.load(fichier)  #Charger la liste des listes enregistrées
        except FileNotFoundError:
            self.listes_enregistrees = []  #Si le fichier n'existe pas, initialiser une liste vide

    def mise_a_jour_liste_taches(self):
        self.liste_tachesbox.delete(0, tk.END)  #Effacer l'affichage actuel des tâches
        for i, tache in enumerate(self.liste_taches):
            description = tache["description"]
            date_echeance = tache["date_echeance"]
            terminee = tache["terminee"]
            couleur = "green" if terminee else "black"  #Déterminer la couleur du texte en fonction de l'état "terminee"
            self.liste_tachesbox.insert(tk.END, f"{i + 1}. {description} (Date d'échéance: {date_echeance}")
            self.liste_tachesbox.itemconfig(i, {'fg': couleur})  #Mise à jour de la couleur du texte
        self.mise_a_jour_listes_enregistrees()  #Mettre à jour l'affichage des listes enregistrées

    def mise_a_jour_listes_enregistrees(self):
        self.listes_enregistreesbox.delete(0, tk.END)  #effacer l'affichage actuel des listes enregistrées
        for nom_fichier in self.listes_enregistrees:
            self.listes_enregistreesbox.insert(tk.END, nom_fichier)

def main():
    root = tk.Tk()
    app = TaskManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()
