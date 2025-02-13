import os
import sys
import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd
import plotly.io as pio
import numpy as np
import dash
from dash import dcc, html, Input, Output, State, ALL

# Ensure Conda is activated and Basemap is available
def check_conda():
    conda_env = os.environ.get('CONDA_DEFAULT_ENV', None)
    if conda_env != 'myenv':
        print(f"Warning: The script is not running inside the expected Conda environment ('myenv').")
        print("Attempting to activate Conda environment...")
        os.system("source $HOME/miniconda/etc/profile.d/conda.sh && conda activate myenv")

# Check and activate Conda before importing Basemap
check_conda()

try:
    from mpl_toolkits.basemap import Basemap
except ImportError:
    print("Error: Basemap is not installed or not accessible. Ensure you are running inside the correct Conda environment ('myenv').")
    sys.exit(1)

# Load dataset
raw_url = "https://raw.githubusercontent.com/prongselk/krillguard/main/KrillGUARD_public.xlsx"
data = pd.read_excel(raw_url, sheet_name="Raw_Data")
data = data.truncate(before=6)
data = data.dropna(how='all')
data = data.dropna(subset=['Lat'])

data['Species'] = data['Species'].fillna('Unknown')
data['Genus'] = data['Genus'].fillna('Unknown')

for column in data.columns:
    if data[column].dtype == 'object':
        if all(isinstance(x, str) for x in data[column] if pd.notna(x)):
            data[column] = data[column].str.strip()
        else:
            print(f"Column '{column}' contains non-string values. Skipping .str.strip().")

fig = px.scatter_geo(data, lat='Lat', lon='Long',
                     hover_name='Station',
                     hover_data=['Station', 'Date', 'Gear', 'Species'],
                     color='Expedition', opacity=0.5,
                     color_discrete_sequence=px.colors.qualitative.Set2)

fig.update_layout(geo=dict(bgcolor='#e4f7fb'))

def fix_species(row):
    if row['Species'] == "Unknown" and row['Genus'] != "Unknown":
        return f"{row['Genus']} sp."
    return row['Species']

data['Species'] = data.apply(fix_species, axis=1)

grouped_species = {}
for genus, group in data.groupby('Genus'):
    species_list = sorted(group['Species'].unique().tolist())
    grouped_species[genus] = species_list

non_unknown_genera = sorted([g for g in grouped_species.keys() if g != "Unknown"])
if "Unknown" in grouped_species:
    non_unknown_genera.append("Unknown")

species_checklist_layout = []
for genus in non_unknown_genera:
    species_checklist_layout.append(
        html.Details([
            html.Summary(genus, style={'cursor': 'pointer', 'fontSize': '14px', 'font-family': 'Helvetica'}),
            dcc.Checklist(
                id={'type': 'species-checklist', 'index': genus},
                options=[{'label': species, 'value': species} for species in grouped_species[genus]],
                value=grouped_species[genus],
                style={'fontSize': '12px', 'lineHeight': '1.5', 'fontStyle': 'italic'},
                inputStyle={"margin-right": "5px"}
            )
        ], open=False)
    )

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(style={'display': 'flex'}, children=[
    html.Div(style={'width': '20%', 'padding': '50px', 'backgroundColor': '#f8f8f8'}, children=[
        html.H4("Toggle species:", style={'fontSize': '14px', 'font-family': 'Helvetica'}),
        html.Button(
            "Deselect All",
            id="deselect-button",
            n_clicks=0,
            style={'marginBottom': '10px', 'fontSize': '12px'}
        ),
        html.Button(
            "Select All",
            id="select-all-button",
            n_clicks=0,
            style={'marginBottom': '10px', 'fontSize': '12px'}
        ),
        html.Div(species_checklist_layout),
    ]),

    html.Div(style={'width': '80%'}, children=[
        html.H1("Discovery Expeditions: Krill Station Data from the IOS Collection",
                style={'textAlign': 'center',
                       'fontSize': '16px',
                       'font-family': 'Helvetica'}),
        html.H2("Click on legend to select expeditions, hover over points to see details",
               style={'textAlign': 'right',
                      'fontSize': '12px',
                      'font-family': 'Helvetica',
                      'fontWeight': 'normal',
                      'marginLeft': '20px',
                      'marginBottom': '5px'}),
        dcc.Graph(id='map-graph')
    ])
])

@app.callback(
    Output({'type': 'species-checklist', 'index': ALL}, 'value'),
    Input('deselect-button', 'n_clicks'),
    Input('select-all-button', 'n_clicks'),
    State({'type': 'species-checklist', 'index': ALL}, 'options')
)
def update_checklists(deselect_clicks, select_clicks, options_list):
    ctx = dash.callback_context
    if not ctx.triggered:
        return [[opt['value'] for opt in options] for options in options_list]

    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if triggered_id == 'deselect-button':
        return [[] for _ in options_list]
    elif triggered_id == 'select-all-button':
        return [[opt['value'] for opt in options] for options in options_list]

    return dash.no_update

@app.callback(
    Output('map-graph', 'figure'),
    Input({'type': 'species-checklist', 'index': ALL}, 'value')
)
def update_map(list_of_values):
    selected_species = [species for sublist in list_of_values for species in sublist]
    filtered_data = data[data['Species'].isin(selected_species)]

    fig = px.scatter_geo(
        filtered_data,
        lat='Lat',
        lon='Long',
        hover_name='Station',
        hover_data=['Station', 'Date', 'Gear', 'Species'],
        color='Expedition',
        opacity=0.8,
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig.update_layout(geo=dict(bgcolor='#e4f7fb'))
    return fig

if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=8080)
