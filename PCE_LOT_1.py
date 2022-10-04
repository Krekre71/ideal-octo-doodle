import pandas as pd
import plotly_express as px
import streamlit as st


# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="PCE_MI",
                   page_icon=":house:",
                   layout="wide"
)

adresse = "https:/github.com/Krekre71/ideal-octo-doodle/CW2020_ExportACV_Version 1-Maison individuelle_2022.xlsx"

df_read = pd.read_excel(adresse,
                   engine='openpyxl',
                   usecols='B:N',)

df = df_read[df_read['Id Fiche'].notna()]

print(df)


#---------- SIDE BAR --------------
st.sidebar.header("Choix des filtres:")
Lot = st.sidebar.multiselect(
    "N° de Lot :",
    options=df["Lot"].unique(),
    default=df["Lot"].unique()
)

Nature_des_données = st.sidebar.multiselect(
    "Choix Nature des données :",
    options=df["Nature_des_données"].unique(),
    default=df["Nature_des_données"].unique()
)

df_selection = df.query(
    'Lot == @Lot & Nature_des_données == @Nature_des_données'
    #'Nature_des_données == Nature_des_données'
)

#df_selection = df.query(
    #'Lot == @Lot & Nature_des_données == @Nature_des_données'
#)


 #kgeqCO2_par_m² = int()

# ---- MAINPAGE ----
st.title(":house: PCE Maison Individuelle")
st.markdown("##")


# TOP KPI's
total_CO2 = int(df_selection[" kgeqCO2 par m²"].sum())
print(total_CO2)
#average_sale_by_transaction = round(df_selection[" kgeqCO2 par m²"].mean(), 2)

column, = st.columns(1)
with column:
    st.subheader(" Total PCE")
    st.subheader(f"PCE = {total_CO2:,} kgCO2/m² ")


#st.markdown("""---""")

# PCE BY LOT [BAR CHART]

#Afficher total kg.CO2/LOT
PCE_by_LOT = (
    df_selection.groupby(by=["Lot"]).sum()[[" kgeqCO2 par m²"]].sort_values(by="Lot")
)

Total_PCE = PCE_by_LOT.sum()

print(Total_PCE)
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

# SALES BY PRODUCT LINE [BAR CHART]
#PCE_by_DED = (
 #   df_selection.groupby(by=["Nature_des_données"]).sum()[[" kgeqCO2 par m²"]].sort_values(by=" kgeqCO2 par m²")
#)

PCE =     df_selection #.groupby(by=["Nature_des_données"]).sum() #[[" kgeqCO2 par m²"]] #.sort_values(by=" kgeqCO2 par m²")

fig_DED = px.pie(
    PCE,
    values=" kgeqCO2 par m²",
    names="Nature_des_données",
    title='PCE en fonction type de données',
    width=150,
)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_LOT, use_container_width=True)
right_column.plotly_chart(fig_DED, use_container_width=True)


VALU_PCE = df_selection.sort_values(by=" kgeqCO2 par m²", ascending=False, na_position='first').head(n=15)
#[" kgeqCO2 par m²"]]
#print(df_selection)

#PCE = (df_selection.head(n=20))
#print(PCE)

#print(VALU_PCE)
#PCE = VALU_PCE
#rint(PCE)

fig_LOT = px.bar(
    VALU_PCE,
    x=" kgeqCO2 par m²",
    y="Libellé",
    orientation="h",
    title="<b>Les 20 produits les plus émissifs en CO2</b>",
    color_discrete_sequence=["#00818a"],
    #template="plotly_white",
)

fig_LOT.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis={'categoryorder':'total ascending'}
)

#fig_LOT.update_xaxes(categoryorder='category ascending')


#fig_LOT.update_traces(textposition='inside', textinfo='percent+label')

st.plotly_chart(fig_LOT,use_container_width=True,sharing="streamlit",)




st.dataframe(df_selection)


# ---- HIDE STREAMLIT STYLE ----
#hide_st_style = """
            #<style>
            #MainMenu {visibility: hidden;}
            #footer {visibility: hidden;}
            #header {visibility: hidden;}
            #</style>
            #"""
#st.markdown(hide_st_style, unsafe_allow_html=True)
