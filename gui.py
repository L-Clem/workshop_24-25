import tkinter as tk

def afficher_alert_popup():
    root = tk.Tk()
    root.withdraw()  # Cacher la fenêtre principale
    tk.messagebox.showwarning("Alerte", "Niveau de négativité critique atteint !\nUne intervention peut être nécessaire.")