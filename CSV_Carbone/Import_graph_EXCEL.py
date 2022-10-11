import pandas as pd
import numpy as np
import plotly_express as px
from io import BytesIO

adresse = "C:\\Users\\Jean-David\\OneDrive\\Documents\\GitHub\\ideal-octo-doodle\\CSV_Carbone\\CW2020_ExportACV.csv"

with open(adresse) as f:
    print(f)

df = pd.read_csv(adresse,encoding='utf-8',engine='python',sep=';')
                 #converters={' kgeqCO2 par m²':int})

#df[' kgeqCO2 par m²'].dtype


#df[' kgeqCO2 par m²'] = df[' kgeqCO2 par m²'].astype(int)
#for col in df.columns:
#df[' kgeqCO2 par m²'] = pd.to_numeric(df[' kgeqCO2 par m²'], errors='ignore')

#modifie objet en num (float) et remplace , par .str.replace(',','.')



df['Taux de renouvellement'] = df['Taux de renouvellement'].str.replace(',','.').astype(float)
df['DE Total (kgeqCO2)'] = df['DE Total (kgeqCO2)'].str.replace(',','.').astype(float)
df['DE Bénéf. charges hors cycle (kgeqCO2)'] = df['DE Bénéf. charges hors cycle (kgeqCO2)'].str.replace(',','.').astype(float)
df[' Total kgeqCO2'] = df[' Total kgeqCO2'].str.replace(',','.').astype(float)
df[' kgeqCO2 par m²'] = df[' kgeqCO2 par m²'].str.replace(',','.').astype(float)


df_not = df[df['Id Fiche'].notna()]

print(df)
print(df.dtypes)
print(df_not)
#Index(['Batiment ou Zone;Lot;Sous-Lot;Libellé;Id Fiche;Nature des données;Quantité;Unité fonctionnelle;
# Durée de vie;Taux de renouvellement;DE Total (kgeqCO2);DE Bénéf. charges hors cycle (kgeqCO2); Total kgeqCO2; kgeqCO2 par m²'], dtype='object')

#df_value = df.sort_values([' kgeqCO2 par m²'])

PCE_by_LOT = (
    df.groupby(by=["Lot"]).sum()[[" kgeqCO2 par m²"]].sort_values(by="Lot")
)

Total_PCE = PCE_by_LOT.sum()


#print(PCE_by_LOT)
fig_LOT = px.bar(
    PCE_by_LOT,
    y=" kgeqCO2 par m²",
    x=PCE_by_LOT.index,
    orientation="v",
    title="<b>kgCO² par LOT</b>",
    color_discrete_sequence=["red"],
    #color_discrete_sequence=["#00818a"] * len(PCE_by_LOT),
    template="plotly_white",
    barmode='group',
)

#fig_LOT.update_layout(
    #plot_bgcolor="rgba(0,0,0,0)",
    #xaxis=(dict(showgrid=False))
#)

fig_LOT.update_xaxes(type='category')

writer = pd.ExcelWriter('export_dataframe.xlsx', engine='xlsxwriter')

df.to_excel(writer, sheet_name='Sheet1')


workbook  = writer.book
worksheet = writer.sheets['Sheet1']

# Convert it to a BytesIO stream.
image_data = BytesIO(fig_LOT.to_image(format="png"))

# Write the image to the same sheet as the data.
worksheet.insert_image(2, 3, 'plotly.png', {'image_data': image_data})

# Create a new worksheet and add the image to it.
worksheet = workbook.add_worksheet()
worksheet.insert_image(2, 3, 'plotly.png', {'image_data': image_data})


#df.to_excel (r'C:\\Users\\Jean-David\\OneDrive\\Documents\\GitHub\\ideal-octo-doodle\\CSV_Carbone\\export_dataframe.xlsx', index = False, header=True)



# Convert the dataframe to an XlsxWriter Excel object.

#workbook = writer.book


#df.to_excel(writer, sheet_name='Sheet{}'.format(i))



# Close the Pandas Excel writer and output the Excel file.
writer.save()


