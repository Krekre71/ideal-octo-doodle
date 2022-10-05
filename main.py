import pandas as pd

adresse = "C:\\Users\\admin\\PycharmProjects\\Carbone\\CW2020_ExportACV.csv"

with open(adresse) as f:
    print(f)

df = pd.read_csv(adresse,encoding='cp1252', delimiter='\\t', engine='python')

#df = df_read[df_read['Id Fiche'].notna()]

#print(df.columns)

#Index(['Batiment ou Zone;Lot;Sous-Lot;Libellé;Id Fiche;Nature des données;Quantité;Unité fonctionnelle;
# Durée de vie;Taux de renouvellement;DE Total (kgeqCO2);DE Bénéf. charges hors cycle (kgeqCO2); Total kgeqCO2; kgeqCO2 par m²'], dtype='object')

df_value = df.sort_values(['Lot'])

print(df_value)
