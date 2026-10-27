"""SpaceX dashboard: python spacex_dash_app.py."""
from pathlib import Path
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA = PROJECT_ROOT / 'data/raw/spacex_launch_dash.csv'
URL = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv'
spacex_df = pd.read_csv(DATA if DATA.exists() else URL)
SITES = sorted(spacex_df['Launch Site'].unique())
app = Dash(__name__)
app.title = 'SpaceX Launch Dashboard'
app.layout = html.Div([
    html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center'}),
    html.Label('Launch site'),
    dcc.Dropdown(id='site-dropdown', options=[{'label': 'All Sites', 'value': 'ALL'}] +
                 [{'label': s, 'value': s} for s in SITES], value='ALL',
                 placeholder='Select a Launch Site here', searchable=True, clearable=False),
    dcc.Graph(id='success-pie-chart'),
    html.Label('Payload range (kg) — filters the scatter plot'),
    dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000,
                    marks={i: f'{i:,}' for i in range(0, 10001, 1000)},
                    value=[0, 10000], tooltip={'placement': 'bottom', 'always_visible': True}),
    dcc.Graph(id='success-payload-scatter-chart'),
], style={'maxWidth': '1200px', 'margin': 'auto', 'padding': '24px', 'fontFamily': 'Arial'})

@app.callback(Output('success-pie-chart', 'figure'), Input('site-dropdown', 'value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        counts = spacex_df.groupby('Launch Site', as_index=False)['class'].sum()
        fig = px.pie(counts, names='Launch Site', values='class', title='Successful launches by site')
    else:
        subset = spacex_df.loc[spacex_df['Launch Site'].eq(entered_site)]
        counts = subset['class'].value_counts().reindex([0, 1], fill_value=0)
        fig = px.pie(names=['Failure', 'Success'], values=counts.values,
                     title=f'Landing outcomes — {entered_site}', color=['Failure', 'Success'],
                     color_discrete_map={'Failure': '#d9534f', 'Success': '#238b45'})
    fig.update_traces(textinfo='label+percent')
    return fig

@app.callback(Output('success-payload-scatter-chart', 'figure'),
              Input('site-dropdown', 'value'), Input('payload-slider', 'value'))
def get_scatter_chart(entered_site, payload_range):
    low, high = payload_range or [0, 10000]
    subset = spacex_df.loc[spacex_df['Payload Mass (kg)'].between(low, high)]
    if entered_site != 'ALL':
        subset = subset.loc[subset['Launch Site'].eq(entered_site)]
    fig = px.scatter(subset, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                     hover_data=['Launch Site'], title=f'Payload and landing outcome — {entered_site}')
    fig.update_yaxes(tickvals=[0, 1], ticktext=['Failure', 'Success'], range=[-0.15, 1.15])
    if subset.empty:
        fig.add_annotation(text='No launches in this selection', x=0.5, y=0.5,
                           xref='paper', yref='paper', showarrow=False)
    return fig

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8050, debug=False)
