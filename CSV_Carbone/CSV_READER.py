import pandas as pd
import numpy as np
import plotly_express as px
from io import BytesIO

adresse = "C:\\Users\\Jean-David\\OneDrive\\Documents\\GitHub\\ideal-octo-doodle\\CSV_Carbone\\CW2020_ExportACV.csv"

with open(adresse) as f:
    print(f)

df = pd.read_csv(adresse,encoding='utf-8',engine='python',sep=';')
                 #converters={' kgeqCO2 par m²':int})

#Suppression colonne inutiles
df = df.drop(['Batiment ou Zone','DE Bénéf. charges hors cycle (kgeqCO2)','DE Total (kgeqCO2)','DE Bénéf. charges hors cycle (kgeqCO2)'], axis=1)
#df[' kgeqCO2 par m²'].dtype
print(df)

#df[' kgeqCO2 par m²'] = df[' kgeqCO2 par m²'].astype(int)
#for col in df.columns:
#df[' kgeqCO2 par m²'] = pd.to_numeric(df[' kgeqCO2 par m²'], errors='ignore')

#modifie objet en num (float) et remplace , par .str.replace(',','.')


df_LOT = df.loc[df['Libellé'].isin( ['TOTAL LOT','LOT FORFAITAIRE'])]
df_LOT = df_LOT.drop(['Sous-Lot','Id Fiche','Nature des données','Quantité','Unité fonctionnelle','Durée de vie','Taux de renouvellement'], axis=1)
df_LOT[' Total kgeqCO2'] = df[' Total kgeqCO2'].str.replace(',','.').astype(float)
df_LOT[' kgeqCO2 par m²'] = df[' kgeqCO2 par m²'].str.replace(',','.').astype(float)



df['Taux de renouvellement'] = df['Taux de renouvellement'].str.replace(',','.').astype(float)
#df['DE Total (kgeqCO2)'] = df['DE Total (kgeqCO2)'].str.replace(',','.').astype(float)
#df['DE Bénéf. charges hors cycle (kgeqCO2)'] = df['DE Bénéf. charges hors cycle (kgeqCO2)'].str.replace(',','.').astype(float)
df[' Total kgeqCO2'] = df[' Total kgeqCO2'].str.replace(',','.').astype(float)
df[' kgeqCO2 par m²'] = df[' kgeqCO2 par m²'].str.replace(',','.').astype(float)


df_PCE = df[df['Id Fiche'].notna()]

#df_LOT = df.groupby(by=["Lot"]).sum()[[" kgeqCO2 par m²"]].sort_values(by="Lot")


print(df_LOT)

#Index(['Batiment ou Zone;Lot;Sous-Lot;Libellé;Id Fiche;Nature des données;Quantité;Unité fonctionnelle;
# Durée de vie;Taux de renouvellement;DE Total (kgeqCO2);DE Bénéf. charges hors cycle (kgeqCO2); Total kgeqCO2; kgeqCO2 par m²'], dtype='object')

#df_value = df.sort_values([' kgeqCO2 par m²'])

df_NB_LOT = (df_PCE.groupby(by=["Lot"]))

print(df_NB_LOT)
#df_NB_LOT = (df_PCE.groupby(by=["Lot"]).sum()[["Libellé"]].sort_values(by="Lot"))

Total_PCE = df_LOT.sum()
print(Total_PCE)

#print(PCE_by_LOT)


#fig_LOT.update_layout(
    #plot_bgcolor="rgba(0,0,0,0)",
    #xaxis=(dict(showgrid=False))
#)

writer = pd.ExcelWriter('export_dataframe.xlsx', engine='xlsxwriter')

df_PCE.to_excel(writer, sheet_name='Sheet1')
df.to_excel(writer, sheet_name='Feuill2')
df_LOT.to_excel(writer, sheet_name='PCE_LOT')



#workbook  = writer.book
#worksheet = writer.sheets['Sheet1']

# Convert it to a BytesIO stream.
#image_data = BytesIO(fig_LOT.to_image(format="png"))

# Write the image to the same sheet as the data.
#worksheet.insert_image(2, 3, 'plotly.png', {'image_data': image_data})

# Create a new worksheet and add the image to it.
#worksheet = workbook.add_worksheet()
#worksheet.insert_image(2, 3, 'plotly.png', {'image_data': image_data})


#df.to_excel (r'C:\\Users\\Jean-David\\OneDrive\\Documents\\GitHub\\ideal-octo-doodle\\CSV_Carbone\\export_dataframe.xlsx', index = False, header=True)



# Convert the dataframe to an XlsxWriter Excel object.

#workbook = writer.book


#df.to_excel(writer, sheet_name='Sheet{}'.format(i))



# Close the Pandas Excel writer and output the Excel file.
writer.save()


