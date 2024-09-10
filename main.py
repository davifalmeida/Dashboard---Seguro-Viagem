import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import os

# Função para carregar e combinar todos os arquivos geoMap
def carregar_geo_data(pasta):
    dfs = []
    for arquivo in os.listdir(pasta):
        if arquivo.startswith("geoMap") and arquivo.endswith(".csv"):
            try:
                ano = int(arquivo.replace('geoMap ', '').replace('.csv', ''))
            except (IndexError, ValueError):
                print(f"Erro ao processar o arquivo: {arquivo}. Ignorando...")
                continue
            
            df = pd.read_csv(os.path.join(pasta, arquivo), skiprows=1)
            df.columns = ['Regiao', 'Volume_Busca']
            df['Ano'] = ano
            dfs.append(df)
    return pd.concat(dfs)

# Função para carregar o multiTimeline
def carregar_multitimeline(caminho):
    df = pd.read_csv(caminho, skiprows=1)
    df.columns = ['Semana', 'Volume_Busca']
    df['Semana'] = pd.to_datetime(df['Semana'])
    return df

# Carregar os dados
df_geo = carregar_geo_data('./data')
df_timeline = carregar_multitimeline('./data/multiTimeline.csv')

# Inicializar o app Dash com supressão de exceções de callback
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=['./assets/style.css'])

# Layout Responsivo e Simples com descrições adicionais
app.layout = html.Div([
    # Cabeçalho
    html.Div(
        html.H1("Dashboard de Seguro de Viagem", style={'textAlign': 'center', 'padding': '20px', 'color': '#4CAF50'}),
        className='row'
    ),

    # Seção 1: Comparação de Volume por Região
    html.Div([
        html.H4("Comparação de Volume de Busca por Região", style={'color': '#4CAF50'}),
        
        # Descrição do gráfico por região
        html.P(
            "Interesse por sub-região: Veja em que local seu termo foi mais famoso durante um período específico. "
            "Os valores são calculados em uma escala de 0 a 100, em que 100 é o local com a maior popularidade "
            "como uma fração do total de pesquisas naquele local; 50 indica um local que tem metade da popularidade; "
            "e 0 indica um local em que não houve dados suficientes para o termo. "
            "Observação: um valor maior significa uma proporção maior de consultas, não uma contagem absoluta maior.",
            style={'color': '#6c757d', 'fontSize': '14px'}
        ),
        
        # Filtro para Anos
        html.Div([
            html.Label('Selecione os Anos para Comparar:', style={'color': '#6c757d'}),
            dcc.Dropdown(
                id='filtro-anos',
                options=[{'label': str(ano), 'value': ano} for ano in df_geo['Ano'].unique()],
                value=[df_geo['Ano'].min(), df_geo['Ano'].max()],
                multi=True,
                clearable=False,
                style={'width': '50%'}
            )
        ], style={'margin-bottom': '20px'}),

        # Gráfico de Volume por Região Comparativo
        dcc.Graph(id='grafico-geo-comparativo', config={'displayModeBar': False}),

        # Tabela Resumo (com rolagem)
        html.H5("Resumo por Região", style={'textAlign': 'center', 'color': '#4CAF50'}),
        html.Div(id='tabela-resumo', style={'height': '300px', 'overflowY': 'scroll'})
    ], className='container'),

    # Seção 2: Comparação de Tendência de Busca
    html.Div([
        html.H4("Comparação de Tendências de Busca ao Longo do Tempo", style={'color': '#4CAF50'}),
        
        # Descrição do gráfico ao longo do tempo
        html.P(
            "Interesse ao longo do tempo: Os números representam o interesse de pesquisa relativo ao ponto mais alto no "
            "gráfico de uma determinada região em um dado período. Um valor de 100 representa o pico de popularidade de "
            "um termo. Um valor de 50 significa que o termo teve metade da popularidade. Uma pontuação de 0 significa que "
            "não havia dados suficientes sobre o termo.",
            style={'color': '#6c757d', 'fontSize': '14px'}
        ),
        
        # Filtro de Semanas
        html.Label('Selecione os períodos para comparar:', style={'color': '#6c757d'}),
        dcc.RangeSlider(
            id='filtro-semanas-comparativo',
            min=0,
            max=len(df_timeline)-1,
            value=[0, len(df_timeline)//2, len(df_timeline)-1],
            marks={i: str(df_timeline['Semana'].iloc[i].date()) for i in range(0, len(df_timeline), len(df_timeline)//10)},
            step=1
        ),

        # Gráfico de Tendência por Semana Comparativo
        dcc.Graph(id='grafico-timeline-comparativo', config={'displayModeBar': False}),

        # Tabela Resumo de Semanas (com rolagem)
        html.H5("Resumo por Período", style={'textAlign': 'center', 'color': '#4CAF50'}),
        html.Div(id='tabela-resumo-semanas', style={'height': '300px', 'overflowY': 'scroll'})
    ], className='container')
], className='container-fluid')


# Callback para atualizar o gráfico de GeoMAP comparativo
@app.callback(
    [Output('grafico-geo-comparativo', 'figure'), Output('tabela-resumo', 'children')],
    [Input('filtro-anos', 'value')]
)
def atualizar_geo_comparativo(anos):
    df_filtrado = df_geo[df_geo['Ano'].isin(anos)]
    fig = px.bar(df_filtrado, x='Regiao', y='Volume_Busca', color='Ano', barmode='group',
                 title=f'Comparação de Volume de Busca por Região para {anos}',
                 color_discrete_sequence=px.colors.qualitative.Set1)
    
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', title_x=0.5)

    # Criar uma tabela resumo das regiões e volumes
    tabela_resumo = df_filtrado.groupby(['Regiao', 'Ano'])['Volume_Busca'].sum().reset_index()

    return fig, html.Table(html.Tbody([
        html.Tr([html.Th(col) for col in tabela_resumo.columns]) 
    ] + [
        html.Tr([html.Td(tabela_resumo.iloc[i][col]) for col in tabela_resumo.columns]) for i in range(len(tabela_resumo))
    ]), style={'width': '100%', 'text-align': 'center'})


# Callback para atualizar o gráfico do MultiTimeline comparativo
@app.callback(
    [Output('grafico-timeline-comparativo', 'figure'), Output('tabela-resumo-semanas', 'children')],
    [Input('filtro-semanas-comparativo', 'value')]
)
def atualizar_timeline_comparativo(range_semanas):
    primeiro_periodo = df_timeline.iloc[range_semanas[0]:range_semanas[1]]
    segundo_periodo = df_timeline.iloc[range_semanas[1]:range_semanas[2]]
    
    # Criar um dataframe combinado para os dois períodos
    primeiro_periodo['Periodo'] = 'Primeiro Período'
    segundo_periodo['Periodo'] = 'Segundo Período'
    df_comparativo = pd.concat([primeiro_periodo, segundo_periodo])
    
    fig = px.line(df_comparativo, x='Semana', y='Volume_Busca', color='Periodo',
                  line_shape='spline', markers=True,
                  title='Comparação de Tendência de Busca - Dois Períodos',
                  color_discrete_sequence=px.colors.qualitative.Set1)
    
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', title_x=0.5)

    # Criar uma tabela resumo das semanas e volumes
    tabela_resumo_semanas = df_comparativo.groupby(['Periodo', 'Semana'])['Volume_Busca'].sum().reset_index()

    return fig, html.Table(html.Tbody([
        html.Tr([html.Th(col) for col in tabela_resumo_semanas.columns]) 
    ] + [
        html.Tr([html.Td(tabela_resumo_semanas.iloc[i][col]) for col in tabela_resumo_semanas.columns]) for i in range(len(tabela_resumo_semanas))
    ]), style={'width': '100%', 'text-align': 'center'})

# Executar o servidor
if __name__ == '__main__':
    app.run_server(debug=True)
