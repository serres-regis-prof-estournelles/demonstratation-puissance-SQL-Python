import sqlite3

# Connexion à la base de données
conn = sqlite3.connect('gesco.db')
cur = conn.cursor()

# Requête 1 : Sélectionner tous les clients
cur.execute('SELECT Nom_client, Prenom_client FROM Clients')
clients = cur.fetchall()
print("Clients:")
for client in clients:
    print(client)

# Requête 2 : Sélectionner tous les produits avec un prix inférieur à 50
cur.execute('SELECT * FROM Produits WHERE Prix_en_€ < 50')
produits = cur.fetchall()
print("\nProduits avec un prix inférieur à 50 € :")
for produit in produits:
    print(produit)

# Requête 3 : Sélectionner les clients et le nombre total de commandes passées par chaque client.
cur.execute("""
    SELECT
        Clients.Nom_client,
        Clients.Prenom_client,
        COUNT(Commandes.Numero_commande) AS NombreCommandes
    FROM
        Clients
    LEFT JOIN
        Commandes ON Clients.Numero_client = Commandes.Numero_client
    GROUP BY
        Clients.Numero_client
""")
commandes_par_client = cur.fetchall()
print("\nNombre de commandes par client :")
for commande in commandes_par_client:
    print(commande)

# Requête 4 : Sélectionner le total général des ventes
cur.execute("""
    SELECT
        SUM(Produits.Prix_en_€ * DetailsCommande.Quantite) AS TotalVentesGeneral
    FROM
        DetailsCommande
    LEFT JOIN
        Produits ON DetailsCommande.Numero_produit = Produits.Numero_produit
""")
total_ventes_general = cur.fetchone()

# Formater le montant total des ventes
montant_formate = "{:.2f} €".format(round(total_ventes_general[0], 2))
print("\nMontant total des ventes en € :")
print(montant_formate)

# Requête 5a : Ventes réalisées pour chaque client
cur.execute("""
    SELECT
        Clients.Nom_client,
        Clients.Prenom_client,
        ROUND(SUM(Produits.Prix_en_€ * DetailsCommande.Quantite), 2) AS VentesParClient
    FROM
        Clients
    LEFT JOIN
        Commandes ON Clients.Numero_client = Commandes.Numero_client
    LEFT JOIN
        DetailsCommande ON Commandes.Numero_commande = DetailsCommande.Numero_commande
    LEFT JOIN
        Produits ON DetailsCommande.Numero_produit = Produits.Numero_produit
    GROUP BY
        Clients.Numero_client
""")
ventes_par_client = cur.fetchall()

# Afficher les ventes par client
print("\nVentes réalisées par client :")
for vente_client in ventes_par_client:
    if vente_client[2] is not None:
        print(f"{vente_client[0]} {vente_client[1]} : {vente_client[2]:.2f} €")
    else:
        print(f"{vente_client[0]} {vente_client[1]} : Aucune vente")

# Requête 5b : Ventes réalisées pour chaque produit
cur.execute("""
    SELECT
        Produits.Nom_produit,
        ROUND(SUM(Produits.Prix_en_€ * DetailsCommande.Quantite), 2) AS VentesParProduit
    FROM
        Produits
    LEFT JOIN
        DetailsCommande ON Produits.Numero_produit = DetailsCommande.Numero_produit
    GROUP BY
        Produits.Numero_produit
""")
ventes_par_produit = cur.fetchall()

# Afficher les ventes par produit
print("\nVentes réalisées par produit :")
for vente_produit in ventes_par_produit:
    if vente_produit[1] is not None:
        print(f"{vente_produit[0]} : {vente_produit[1]:.2f} €")
    else:
        print(f"{vente_produit[0]} : Aucune vente")



# Fermer la connexion
conn.close()
