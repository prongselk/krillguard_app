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
    return df

data = load_data()

#fix unknown species names 
data['Species'] = data.apply(lambda row: f"{row['Genus']} sp." if row['Species'] == "Unknown" and row['Genus'] != "Unknown" else row['Species'], axis=1)

#sidebar for species selection
st.sidebar.title("Species Selection")
genus_groups = data.groupby('Genus')['Species'].unique().to_dict()

# Initialize session state if not set
if "selected_species" not in st.session_state:
    st.session_state.selected_species = sum(genus_groups.values(), [])

# Multi-select widget for species filtering
selected_species = []
for genus, species_list in genus_groups.items():
    with st.sidebar.expander(genus, expanded=False):
        selected = st.multiselect(f"Select species ({genus})", species_list, default=st.session_state.selected_species)
        selected_species.extend(selected)


# Update session state with the selected species
st.session_state.selected_species = [species for species_list in genus_groups.values() for species in species_list]  

# Filter data based on selected species
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
    st.session_state['selected_species'] = [species for species_list in genus_groups.values() for species in species_list]
