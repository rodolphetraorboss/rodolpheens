import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DB = "transit_manager.db"

conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS clients(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT,
    telephone TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS dossiers(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero TEXT,
    client TEXT,
    statut TEXT
)
""")
conn.commit()

root = tk.Tk()
root.title("TRANSIT MANAGER PRO")
root.geometry("1200x700")
root.configure(bg="#f4f6f9")

STYLE_TITLE = ("Segoe UI", 20, "bold")
STYLE_CARD = ("Segoe UI", 12, "bold")

# HEADER
header = tk.Frame(root, bg="#0d6efd", height=70)
header.pack(fill="x")

titre = tk.Label(
    header,
    text="🚚 TRANSIT MANAGER PRO",
    bg="#0d6efd",
    fg="white",
    font=("Segoe UI", 22, "bold")
)
titre.pack(side="left", padx=20, pady=15)

# CREATION DU NOTEBOOK
tabs = ttk.Notebook(root)
tabs.pack(fill="both", expand=True)

# ACCUEIL
frame_accueil = ttk.Frame(tabs)
tabs.add(frame_accueil, text="🏠 Accueil")

title = tk.Label(frame_accueil, text="GESTION D'ENTREPRISE DE TRANSIT", font=("Arial", 18, "bold"))
title.pack(pady=10)

card1 = tk.Frame(frame_accueil, bg="#198754", width=250, height=120)
card1.place(x=30, y=40)

tk.Label(card1, text="👥 CLIENTS", bg="#198754", fg="white", font=STYLE_CARD).pack(pady=10)
lbl_clients = tk.Label(card1, text="0", bg="#198754", fg="white", font=("Segoe UI", 30, "bold"))
lbl_clients.pack()

card2 = tk.Frame(frame_accueil, bg="#dc3545", width=250, height=120)
card2.place(x=320, y=40)

tk.Label(card2, text="📁 DOSSIERS", bg="#dc3545", fg="white", font=STYLE_CARD).pack(pady=10)
lbl_dossiers = tk.Label(card2, text="0", bg="#dc3545", fg="white", font=("Segoe UI", 30, "bold"))
lbl_dossiers.pack()

message = tk.Label(
    frame_accueil,
    text="""
Bienvenue dans TRANSIT MANAGER PRO

✔ Gestion des clients
✔ Gestion des dossiers de transit
✔ Suivi des opérations
✔ Gestion logistique
✔ Tableau de bord dynamique
""",
    font=("Segoe UI", 14),
    justify="left"
)
message.place(x=30, y=220)

# CLIENTS
frame_clients = ttk.Frame(tabs)
tabs.add(frame_clients, text="Clients")

tk.Label(frame_clients, text="Nom").grid(row=0, column=0, padx=5, pady=5)
nom_entry = tk.Entry(frame_clients)
nom_entry.grid(row=0, column=1)

tk.Label(frame_clients, text="Téléphone").grid(row=1, column=0, padx=5, pady=5)
tel_entry = tk.Entry(frame_clients)
tel_entry.grid(row=1, column=1)

tree_clients = ttk.Treeview(frame_clients, columns=("ID","Nom","Téléphone"), show="headings")
for c in ("ID","Nom","Téléphone"):
    tree_clients.heading(c, text=c)
tree_clients.grid(row=3, column=0, columnspan=3, sticky="nsew")

def charger_clients():
    tree_clients.delete(*tree_clients.get_children())
    for r in cur.execute("SELECT * FROM clients"):
        tree_clients.insert("", "end", values=r)

def ajouter_client():
    cur.execute("INSERT INTO clients(nom,telephone) VALUES(?,?)",
                (nom_entry.get(), tel_entry.get()))
    conn.commit()
    charger_clients()
    nom_entry.delete(0, tk.END)
    tel_entry.delete(0, tk.END)

tk.Button(frame_clients, text="Ajouter Client", command=ajouter_client).grid(row=2,column=1,pady=5)

# DOSSIERS
frame_dossiers = ttk.Frame(tabs)
tabs.add(frame_dossiers, text="Dossiers")

tk.Label(frame_dossiers, text="N° Dossier").grid(row=0,column=0,padx=5,pady=5)
num_entry = tk.Entry(frame_dossiers)
num_entry.grid(row=0,column=1)

tk.Label(frame_dossiers, text="Client").grid(row=1,column=0,padx=5,pady=5)
client_entry = tk.Entry(frame_dossiers)
client_entry.grid(row=1,column=1)

tk.Label(frame_dossiers, text="Statut").grid(row=2,column=0,padx=5,pady=5)
statut_entry = tk.Entry(frame_dossiers)
statut_entry.grid(row=2,column=1)

tree_dossiers = ttk.Treeview(frame_dossiers, columns=("ID","Numero","Client","Statut"), show="headings")
for c in ("ID","Numero","Client","Statut"):
    tree_dossiers.heading(c, text=c)
tree_dossiers.grid(row=4,column=0,columnspan=3,sticky="nsew")

def charger_dossiers():
    tree_dossiers.delete(*tree_dossiers.get_children())
    for r in cur.execute("SELECT * FROM dossiers"):
        tree_dossiers.insert("", "end", values=r)

def ajouter_dossier():
    cur.execute("INSERT INTO dossiers(numero,client,statut) VALUES(?,?,?)",
                (num_entry.get(), client_entry.get(), statut_entry.get()))
    conn.commit()
    charger_dossiers()
    num_entry.delete(0, tk.END)
    client_entry.delete(0, tk.END)
    statut_entry.delete(0, tk.END)

tk.Button(frame_dossiers, text="Ajouter Dossier", command=ajouter_dossier).grid(row=3,column=1,pady=5)

# Charger les données au démarrage
charger_clients()
charger_dossiers()

root.mainloop()
