import streamlit as st
import pandas as pd
import plotly.express as px

st.cache_data.clear()

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/prongselk/krillguard/main/KrillGUARD_public.xlsx"
    df = pd.read_excel(url, sheet_name="Raw_Data")
    df = df.truncate(before=6).dropna(how='all').dropna(subset=['Lat'])
    df['Species'] = df['Species'].fillna('Unknown')
    df['Genus'] = df['Genus'].fillna('Unknown')
    df['Species'] = df.apply(lambda row: f"{row['Genus']} sp." if row['Species'] == "Unknown" and row['Genus'] != "Unknown" else row['Species'], axis=1)
    return df

data = load_data()

#sidebar for species selection
st.sidebar.title("Species Selection")
genus_groups = {genus: list(species_list) for genus, species_list in data.groupby('Genus')['Species'].unique().items()}  

valid_species = [species for species_list in genus_groups.values() for species in species_list] 

if "selected_species" not in st.session_state:
    st.session_state.selected_species = valid_species  

selected_species = []
for genus, species_list in genus_groups.items():
    with st.sidebar.expander(genus, expanded=False):
        selected = st.multiselect(
            f"Select species ({genus})",
            options=species_list,  
            default=[species for species in species_list if species in st.session_state.selected_species]  
        )
        selected_species.extend(selected)

if set(selected_species) != set(st.session_state.selected_species):
    st.session_state.selected_species = selected_species  

filtered_data = data[data['Species'].isin(st.session_state.selected_species)]

fig = px.scatter_geo(filtered_data, lat='Lat', lon='Long',
                     hover_name='Station',
                     hover_data=['Station', 'Date', 'Gear', 'Species'],
                     color='Expedition', opacity=0.8,
                     color_discrete_sequence=px.colors.qualitative.Set2)

fig.update_layout(
    geo=dict(
        showland = True,
        landcolor = "white",
        showocean = True,
        oceancolor = "#e4f7fb",
        bgcolor='#e4f7fb'))

st.markdown("<h1 style='text-align: center; font-size: 30px;'>Krill Station Data - Discovery Expeditions</h1>", unsafe_allow_html=True)
st.write("Click on the legend to filter by expedition. Open the side menu on the left to filter by species. Hover over points for details. ")
st.plotly_chart(fig)

if st.sidebar.button("Deselect All"):
    st.session_state['selected_species'] = []

if st.sidebar.button("Select All"):
    st.session_state['selected_species'] = valid_species
