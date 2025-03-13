import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

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


def convert_date(date):
    try:
        if str(date).isdigit():  
            return pd.to_datetime(int(date), origin='1899-12-30', unit='D')
        elif '-' in str(date):  
            return pd.to_datetime(date, format='%Y-%m-%d', errors='coerce')
    except:
        return np.nan  
    return np.nan


def fix_dates(data):
    data['correct_date'] = data['Date'].apply(convert_date)
    data['year'] = data['correct_date'].dt.year
    data['decade'] = data['year'].apply(lambda x: f"{x // 10 * 10}s" if pd.notna(x) else np.nan)

    return data



data = load_data()
data = fix_dates(data)



slider_css = """
    <style>
        /* Hide default slider thumb */
        input[type="range"]::-webkit-slider-thumb {
            visibility: hidden;
        }

        input[type="range"]::-moz-range-thumb {
            visibility: hidden;
        }

        /* Positioning the custom image */
        .slider-container {
            position: relative;
            height: 50px;
        }

        .custom-slider-thumb {
            position: absolute;
            top: -15px;
            width: 40px;
            height: 40px;
            background-image: url('https://raw.githubusercontent.com/prongselk/krillguard_app/main/discovery.png'); /* Replace with your image */
            background-size: cover;
            background-position: center;
            border-radius: 50%;
            pointer-events: none;
            transform: translateX(-50%);
        }
    </style>
"""


st.markdown(slider_css, unsafe_allow_html=True)



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

if st.sidebar.button("Deselect All Species"):
    st.session_state['selected_species'] = []

if st.sidebar.button("Select All Species"):
    st.session_state['selected_species'] = valid_species

#sidebar for year selection
st.sidebar.title("Year Selection")
decades = {decade: list(years_list) for decade, years_list in data.groupby('decade')['year'].unique().items()}  

valid_years = [years for years_list in decades.values() for years in years_list] 

if "selected_years" not in st.session_state:
    st.session_state.selected_years = valid_years  

selected_years = []
for decade, years_list in decades.items():
    with st.sidebar.expander(decade, expanded=False):
        selected = st.multiselect(
            f"Select years ({decade})",
            options=years_list,  
            default=[year for year in years_list if year in st.session_state.selected_years]  
        )
        selected_years.extend(selected)

if set(selected_years) != set(st.session_state.selected_years):
    st.session_state.selected_years = selected_years 




filtered_data = data[(data['year'].isin(selected_years)) & (data['Species'].isin(selected_species))]

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
st.write("Click on the legend to filter by expedition. Open the side menu on the left to filter by species or year (double click 'Select All' and 'Deselect All' buttons for them to work). Hover over points for details. ")
st.plotly_chart(fig)




if st.sidebar.button("Deselect All Years"):
    st.session_state['selected_years'] = []

if st.sidebar.button("Select All Years"):
    st.session_state['selected_years'] = valid_years



min_year, max_year = int(data['year'].min()), int(data['year'].max())

selected_slider_year = st.slider(
    "Slide to focus on a single year:",
    min_value=min_year,
    max_value=max_year,
    value=min_year,  
    step=1
)


st.markdown(f"""
    <div class="slider-container">
        <div class="custom-slider-thumb" id="slider-thumb"></div>
    </div>
    <script>
        // JavaScript to move the custom slider thumb
        document.addEventListener('DOMContentLoaded', function () {{
            let slider = document.querySelector('input[type="range"]');
            let thumb = document.getElementById('slider-thumb');

            function updateThumbPosition() {{
                let percentage = (slider.value - {min_year}) / ({max_year} - {min_year}) * 100;
                thumb.style.left = `calc({{percentage}}% + 5px)`;
            }}

            slider.addEventListener('input', updateThumbPosition);
            updateThumbPosition();
        }});
    </script>
""", unsafe_allow_html=True)






filtered_data_slider = data[
    (data['year'] == selected_slider_year) & 
    (data['Species'].isin(selected_species))
]

fig_slider = px.scatter_geo(filtered_data_slider, lat='Lat', lon='Long',
                            hover_name='Station',
                            hover_data=['Station', 'Date', 'Gear', 'Species'],
                            color='Expedition', opacity=0.8,
                            color_discrete_sequence=px.colors.qualitative.Set2)

fig_slider.update_layout(
    geo=dict(
        showland=True,
        landcolor="white",
        showocean=True,
        oceancolor="#e4f7fb",
        bgcolor='#e4f7fb')
)


st.plotly_chart(fig_slider)



st.markdown(
    """
    <div style="display: flex; justify-content: center; margin-top: 20px;">
        <a href="https://o-william-white.github.io/" target="_blank">
            <button style="padding: 10px 20px; font-size: 16px; background-color: #7d7fe0; color: white; border: none; border-radius: 5px; cursor: pointer;">
                Back to Homepage
            </button>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)