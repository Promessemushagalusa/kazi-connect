import sqlite3

lignes = sqlite3.connect("kazi.db").execute("SELECT * FROM travailleurs").fetchall()
for ligne in lignes:
    print(ligne)
print(len(lignes), "travailleur(s)")