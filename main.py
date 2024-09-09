import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import os

# Função para carregar e combinar todos os arquivos geoMap
def carregar_geo_data(pasta):
    # Lista para armazenar os DataFrames de cada arquivo
    dfs = []
    # Percorrer os arquivos na pasta
    for arquivo in os.listdir(pasta):
        if arquivo.startswith("geoMap") and arquivo.endswith(".csv"):
            try:
                # Extrair o ano diretamente do nome do arquivo
                ano = int(arquivo.replace('geoMap ', '').replace('.csv', ''))
            except (IndexError, ValueError):
                print(f"Erro ao processar o arquivo: {arquivo}. Ignorando...")
                continue
            
            # Carregar o arquivo
            df = pd.read_csv(os.path.join(pasta, arquivo), skiprows=1)
            df.columns = ['Regiao', 'Volume_Busca']
            df['Ano'] = ano
            dfs.append(df)
    
    # Concatenar todos os DataFrames em um único DataFrame
    return pd.concat(dfs)

# Função para carregar o multiTimeline
def carregar_multitimeline(caminho):
    df = pd.read_csv(caminho, skiprows=1)
    df.columns = ['Semana', 'Volume_Busca']
    df['Semana'] = pd.to_datetime(df['Semana'])
    return df

# Carregar os dados combinados do geoMap
df_geo = carregar_geo_data('./data')

# Carregar os dados do multiTimeline
df_timeline = carregar_multitimeline('./data/multiTimeline.csv')

# Inicializar o app Dash
app = dash.Dash(__name__)

# Layout do Dashboard
app.layout = html.Div([
    html.H1("Dashboard Interativo de Seguro de Viagem"),

    # Filtro de Ano para o GeoMAP
    dcc.Dropdown(
        id='filtro-ano',
        options=[{'label': str(ano), 'value': ano} for ano in df_geo['Ano'].unique()],
        value=df_geo['Ano'].min(),
        multi=False,
        clearable=False,
    ),
    
    # Gráfico de volume por região
    dcc.Graph(id='grafico-geo'),

    # Filtro de semanas para o MultiTimeline
    dcc.RangeSlider(
        id='filtro-semana',
        min=0,
        max=len(df_timeline)-1,
        value=[0, len(df_timeline)-1],
        marks={i: str(df_timeline['Semana'].iloc[i].date()) for i in range(0, len(df_timeline), len(df_timeline)//10)}
    ),
    
    # Gráfico de volume por semanas
    dcc.Graph(id='grafico-timeline'),
])

# Callback para atualizar o gráfico de GeoMAP
@app.callback(
    Output('grafico-geo', 'figure'),
    [Input('filtro-ano', 'value')]
)
def atualizar_geo(ano):
    df_filtrado = df_geo[df_geo['Ano'] == ano]
    fig = px.bar(df_filtrado, x='Regiao', y='Volume_Busca', title=f'Volume de Busca por Região em {ano}')
    return fig

# Callback para atualizar o gráfico do MultiTimeline
@app.callback(
    Output('grafico-timeline', 'figure'),
    [Input('filtro-semana', 'value')]
)
def atualizar_timeline(range_semanas):
    df_filtrado = df_timeline.iloc[range_semanas[0]:range_semanas[1]]
    fig = px.line(df_filtrado, x='Semana', y='Volume_Busca', title='Tendência de Busca ao Longo do Tempo')
    return fig

# Executar o servidor
if __name__ == '__main__':
    app.run_server(debug=True)
