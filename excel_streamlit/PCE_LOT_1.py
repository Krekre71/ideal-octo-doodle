import pandas as pd
import plotly_express as px
import streamlit as st


# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="PCE_MI",
                   page_icon=":house:",
                   layout="wide"
)

adresse = "C:\\Users\\Jean-David\\OneDrive\\Bureau\\Python\\CSV PANDAS\\CSV CW2020\\CW2020_ExportACV_Version 1-Maison individuelle_2022.xlsx"

df = pd.read_excel(adresse,
                   engine='openpyxl',
                   usecols='B:N',)

# print(df)


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
)




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


PCE_by_LOT = (
    df_selection.groupby(by=["Lot"]).sum()[[" kgeqCO2 par m²"]].sort_values(by=" kgeqCO2 par m²")
)
fig_LOT = px.bar(
    PCE_by_LOT,
    y=" kgeqCO2 par m²",
    x=PCE_by_LOT.index,
    orientation="v",
    title="<b>kgCO² par LOT</b>",
    color_discrete_sequence=["#b83500"] * len(PCE_by_LOT),
    template="plotly_white",
)
fig_LOT.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

# SALES BY PRODUCT LINE [BAR CHART]
PCE_by_DED = (
    df_selection.groupby(by=["Nature_des_données"]).sum()[[" kgeqCO2 par m²"]].sort_values(by=" kgeqCO2 par m²")
)
fig_PCE = px.bar(
    PCE_by_DED,
    x=" kgeqCO2 par m²",
    y=PCE_by_DED.index,
    orientation="h",
    title="<b>PCE en fonction par type de données</b>",
    color_discrete_sequence=["#b83500"] * len(PCE_by_DED),
    template="plotly_white",
)
fig_PCE.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_LOT, use_container_width=True)
right_column.plotly_chart(fig_PCE, use_container_width=True)


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