import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/prongselk/krillguard/main/KrillGUARD_public.xlsx"
    df = pd.read_excel(url, sheet_name="Raw_Data")
    df = df.truncate(before=6).dropna(how='all').dropna(subset=['Lat'])
    df['Species'] = df['Species'].fillna('Unknown')
    df['Genus'] = df['Genus'].fillna('Unknown')
    return df

data = load_data()

# Fix species names (replace "Unknown" with "Genus sp.")
data['Species'] = data.apply(lambda row: f"{row['Genus']} sp." if row['Species'] == "Unknown" and row['Genus'] != "Unknown" else row['Species'], axis=1)

# Sidebar for species selection
st.sidebar.title("Species Selection")
genus_groups = data.groupby('Genus')['Species'].unique().to_dict()

selected_species = []
for genus, species_list in genus_groups.items():
    with st.sidebar.expander(genus):
        species_selected = st.multiselect(f"Select species ({genus})", species_list, default=species_list)
        selected_species.extend(species_selected)

# Filter data based on selection
filtered_data = data[data['Species'].isin(selected_species)]

# Create interactive map
fig = px.scatter_geo(filtered_data, lat='Lat', lon='Long',
                     hover_name='Station',
                     hover_data=['Station', 'Date', 'Gear', 'Species'],
                     color='Expedition', opacity=0.8,
                     color_discrete_sequence=px.colors.qualitative.Set2)

fig.update_layout(geo=dict(bgcolor='#e4f7fb'))

# Display map
st.title("Krill Station Data - Discovery Expeditions")
st.write("Click on the legend to filter by expedition. Hover over points for details.")
st.plotly_chart(fig)

# Select/Deselect all button
if st.sidebar.button("Deselect All"):
    st.session_state['selected_species'] = []

if st.sidebar.button("Select All"):
    st.session_state['selected_species'] = [species for species_list in genus_groups.values() for species in species_list]
