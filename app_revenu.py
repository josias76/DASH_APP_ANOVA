import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# === CHARGEMENT ET PRÉTRAITEMENT DES DONNÉES ===
df = pd.read_csv('revenus_par_secteur.csv')

# Nettoyage basique
df.dropna(subset=['Revenu mensuel', 'Secteur d’emploi'], inplace=True)

# === CRÉATION DE L'APPLICATION DASH ===
app = Dash(__name__)
app.title = "Analyse des Revenus"

# === LAYOUT DE L'APPLICATION ===
app.layout = html.Div([
    html.H1("Analyse de la variance des revenus selon le secteur d’emploi", style={'textAlign': 'center'}),

    dcc.Dropdown(
        id='secteur-filter',
        options=[{'label': sec, 'value': sec} for sec in sorted(df['Secteur d’emploi'].unique())],
        value=None,
        placeholder="Filtrer par secteur (optionnel)",
        multi=True
    ),

    dcc.Graph(id='bar-graph'),

    dcc.Graph(id='box-graph'),

    html.H3("Résumé statistique par secteur"),
    html.Pre(id='summary-table', style={'fontSize': '16px'})
])

# === CALLBACK ===
@app.callback(
    Output('bar-graph', 'figure'),
    Output('box-graph', 'figure'),
    Output('summary-table', 'children'),
    Input('secteur-filter', 'value')
)
def update_graph(secteurs):
    dff = df.copy()
    if secteurs:
        dff = dff[dff['Secteur d’emploi'].isin(secteurs)]

    # TABLEAU CROISÉ DYNAMIQUE
    pivot = dff.groupby('Secteur d’emploi')['Revenu mensuel'].agg(
        Moyenne='mean', Médiane='median', Écart_Type='std', Effectif='count'
    ).round(2)

    # BAR CHART
    fig_bar = px.bar(
        pivot.reset_index(),
        x='Secteur d’emploi',
        y='Moyenne',
        title='Revenu moyen par secteur',
        labels={'Moyenne': 'Revenu moyen'},
        color='Secteur d’emploi'
    )

    # BOX PLOT
    fig_box = px.box(
        dff,
        x='Secteur d’emploi',
        y='Revenu mensuel',
        title='Distribution des revenus par secteur',
        color='Secteur d’emploi'
    )

    return fig_bar, fig_box, pivot.to_string()

# === LANCEMENT DU SERVEUR ===
if __name__ == '__main__':
    app.run(debug=True)
