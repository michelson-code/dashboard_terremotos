import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.express as px
import pandas as pd
import numpy as np

# --- PREPARAÇÃO DOS DADOS ---
df = pd.read_csv('all_month.csv')

# Tratamento de Tempo
df['time'] = pd.to_datetime(df['time']).dt.tz_localize(None)
df['DataHora (Brasília)'] = df['time'] - pd.Timedelta(hours=3)
df['Hora (UTC)'] = df['time'].dt.strftime('%d/%m/%Y %H:%M:%S')
df['DataHora (Brasília)_Str'] = df['DataHora (Brasília)'].dt.strftime('%d/%m/%Y %H:%M:%S')

# Colunas Técnicas
df['Lat. (°)'] = df['latitude'].round(4)
df['Lon. (°)'] = df['longitude'].round(4)
df['Magnitude'] = df['mag']
df['Prof. (km)'] = df['depth']
df['Local'] = df['place']
df['Tipo (Escala)'] = df['magType'] # <-- CORREÇÃO: Usando magType

# Opções para o Dropdown (Tipos únicos de escala encontrados no CSV)
# Removemos valores nulos que às vezes aparecem na USGS
tipos_escala = df['magType'].dropna().unique()
tipos_disponiveis = [{'label': t.upper(), 'value': t} for t in tipos_escala]

# Colunas para a Planilha
cols_view = ['DataHora (Brasília)_Str', 'Hora (UTC)', 'Lat. (°)', 'Lon. (°)', 'Magnitude', 'Prof. (km)', 'Local', 'Tipo (Escala)']

df['size_viz'] = df['Magnitude'].apply(lambda x: (np.exp(x) * 0.2) if x > 0 else 0.2)

# --- INICIALIZAÇÃO DO DASH ---
app = dash.Dash(__name__)

# --- LAYOUT DO DASHBOARD ---
app.layout = html.Div(style={
    'fontFamily': 'Arial, sans-serif', 'backgroundColor': "#f4f7f6", 
    'minHeight': '100vh', 'display': 'flex', 'flexDirection': 'column', 'padding': '15px'
}, children=[
    
    html.H1("Monitoramento Sísmico Global", style={'textAlign': 'center', 'color': '#2c3e50', 'margin': '0 0 15px 0'}),
    
    # --- SEÇÃO DE FILTROS ---
    html.Div(style={'display': 'flex', 'backgroundColor': 'white', 'padding': '15px', 'borderRadius': '12px', 'boxShadow': '0 2px 4px #ddd', 'marginBottom': '15px', 'alignItems': 'center'}, children=[
        # Slider de Magnitude
        html.Div([
            html.Label("Magnitude Mínima:", style={'fontWeight': 'bold'}),
            dcc.Slider(
                id='mag-slider', min=0, max=8, step=0.5, value=2.5,
                marks={i: str(i) for i in range(9)}
            ),
        ], style={'flex': '1.5', 'padding': '0 20px'}),
        
        # Dropdown de Escala (magType)
        html.Div([
            html.Label("Escala de Magnitude:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='tipo-dropdown',
                options=tipos_disponiveis,
                value=[t['value'] for t in tipos_disponiveis], # Seleciona todos por padrão
                multi=True,
                placeholder="Selecione as escalas..."
            ),
        ], style={'flex': '1', 'padding': '0 20px'}),

        # Cards de Resumo
        html.Div([
            html.Div([html.Small("Total Eventos"), html.Br(), html.B(id="total-eventos", style={'color': '#2980b9', 'fontSize': '18px'})], style={'textAlign': 'center', 'margin': '0 10px'}),
            html.Div([html.Small("Mag. Máxima"), html.Br(), html.B(id="max-mag", style={'color': '#c0392b', 'fontSize': '18px'})], style={'textAlign': 'center', 'margin': '0 10px'}),
        ], style={'flex': '0.5', 'display': 'flex', 'borderLeft': '1px solid #ddd', 'paddingLeft': '20px'})
    ]),

    # CORPO PRINCIPAL: MAPA E GRÁFICOS
    html.Div(style={'display': 'flex', 'height': '60vh', 'marginBottom': '20px'}, children=[
        # Mapa
        html.Div([
            dcc.Graph(id='mapa-mundi', style={'height': '100%'})
        ], style={'flex': '3', 'backgroundColor': 'white', 'borderRadius': '12px', 'boxShadow': '0 4px 6px #ddd', 'marginRight': '15px'}),

        # Gráficos Laterais
        html.Div(style={'flex': '1', 'display': 'flex', 'flexDirection': 'column'}, children=[
            html.Div([dcc.Graph(id='hist-mag', style={'height': '100%'})], style={'flex': '1', 'backgroundColor': 'white', 'borderRadius': '12px', 'boxShadow': '0 4px 6px #ddd', 'marginBottom': '15px'}),
            html.Div([dcc.Graph(id='serie-temporal', style={'height': '100%'})], style={'flex': '1', 'backgroundColor': 'white', 'borderRadius': '12px', 'boxShadow': '0 4px 6px #ddd'})
        ])
    ]),

    # PLANILHA FINAL
    html.Div([
        html.H3("Planilha de Dados Filtrados", style={'marginTop': '0'}),
        dash_table.DataTable(
            id='tabela-dados',
            columns=[{"name": i.replace('_Str', ''), "id": i} for i in cols_view],
            page_size=10,
            sort_action="native",
            filter_action="native",
            style_table={'overflowX': 'auto'},
            style_header={'backgroundColor': '#2c3e50', 'color': 'white', 'fontWeight': 'bold'},
            style_cell={'textAlign': 'center', 'padding': '10px', 'fontSize': '12px'}
        )
    ], style={'backgroundColor': 'white', 'borderRadius': '12px', 'padding': '20px', 'boxShadow': '0 4px 6px #ddd'})
])

# --- CALLBACK ---
@app.callback(
    [Output('mapa-mundi', 'figure'),
     Output('hist-mag', 'figure'),
     Output('serie-temporal', 'figure'),
     Output('total-eventos', 'children'),
     Output('max-mag', 'children'),
     Output('tabela-dados', 'data')],
    [Input('mag-slider', 'value'),
     Input('tipo-dropdown', 'value')]
)
def atualizar_dashboard(min_mag, tipos_selecionados):
    # Proteção caso o usuário desmarque todas as opções no dropdown
    if not tipos_selecionados:
        tipos_selecionados = []

    # Filtro Dinâmico: Magnitude >= X  E  magType está na lista
    dff = df[(df['mag'] >= min_mag) & (df['magType'].isin(tipos_selecionados))].copy()
    
    total = f"{len(dff):,}"
    maxima = f"{dff['Magnitude'].max():.1f}" if not dff.empty else "0.0"
    
    # Mapa
    # 1. Mapa Global com Proporção Exponencial
    fig_map = px.scatter_geo(
        dff, lat='latitude', lon='longitude', color='Magnitude',
        size='size_viz', hover_name='Local',
        size_max=45, # <--- NOVO: Limita o raio máximo da bolha maior
        hover_data={'DataHora (Brasília)_Str': True, 'Magnitude': True, 'Prof. (km)': True, 'Tipo (Escala)': True, 'latitude': False, 'longitude': False, 'size_viz': False},
        projection="natural earth", color_continuous_scale='Reds', template='plotly_white'
    )
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    # Histograma
    fig_hist = px.histogram(dff, x='Magnitude', nbins=20, template='plotly_white', color_discrete_sequence=['#e67e22'])
    fig_hist.update_layout(margin={"r":10,"t":30,"l":10,"b":10}, title="Distribuição")
    
    # Série Temporal
    df_daily = dff.resample('D', on='time').count()['id'].reset_index()
    fig_time = px.line(df_daily, x='time', y='id', template='plotly_white', markers=True)
    fig_time.update_layout(margin={"r":10,"t":30,"l":10,"b":10}, title="Atividade")

    return fig_map, fig_hist, fig_time, total, maxima, dff.to_dict('records')

if __name__ == '__main__':
    app.run(debug=True)