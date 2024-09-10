# Dashboard Interativo de Seguro de Viagem

Este é um projeto de análise de dados de seguro de viagem que visa visualizar e comparar tendências de volume de buscas por regiões e períodos específicos. O projeto foi desenvolvido usando **Dash** e **Flask** e está hospedado na plataforma **PythonAnywhere**.

## Acesse o Dashboard

Você pode acessar e interagir com o dashboard clicando no link abaixo:

[**Visualizar o Dashboard**](https://davifalmeida.pythonanywhere.com/dashboard/)
![image](https://github.com/user-attachments/assets/f16b418d-6602-4132-9b6c-e51a704e601a)

## Descrição do Dashboard

Este dashboard permite que o usuário visualize duas análises principais:

1. **Comparação de Volume de Busca por Região**:
   - O gráfico permite comparar o volume de buscas relacionadas a seguros de viagem por diferentes regiões ao longo de vários anos.
   - O usuário pode selecionar um ou mais anos para comparar as regiões, e os dados são exibidos em um gráfico de barras comparativo.
   - Informações sobre os picos de busca e a popularidade de termos específicos por sub-região são visualizados facilmente.

2. **Tendência de Busca ao Longo do Tempo**:
   - Este gráfico permite que o usuário compare o volume de buscas ao longo de diferentes períodos.
   - Através de um **Range Slider**, o usuário pode selecionar dois períodos de tempo e comparar a evolução do volume de buscas ao longo das semanas.
   - O gráfico de linhas facilita a identificação de tendências de aumento ou queda no interesse por seguros de viagem durante os períodos analisados.

## Informações Relevantes que Podemos Retirar

- **Tendências Regionais**: O dashboard permite identificar quais regiões tiveram maior volume de buscas para seguros de viagem em períodos específicos, o que pode ajudar a direcionar campanhas de marketing para essas áreas.
- **Análise Temporal**: A comparação entre diferentes períodos ajuda a entender o comportamento de busca dos usuários ao longo do tempo, como a sazonalidade da procura por seguros de viagem.
- **Identificação de Picos**: Através dos gráficos, é possível identificar quando ocorrem os picos de busca por seguros de viagem, permitindo ajustar estratégias de negócios e promoções.
- **Visualização Comparativa**: Com a funcionalidade de comparação, os usuários podem visualizar múltiplos anos ou semanas em um único gráfico, facilitando a análise de variações ano a ano ou semana a semana.

## Tecnologias Utilizadas

- **Python**: Linguagem principal utilizada no desenvolvimento do backend e processamento de dados.
- **Dash**: Biblioteca Python usada para construir o frontend interativo, responsável pelos gráficos e elementos do dashboard.
- **Flask**: Framework web usado para integrar o Dash e servir a aplicação.
- **Pandas**: Biblioteca Python para manipulação de dados e análise de séries temporais.
- **Plotly**: Usado para gerar gráficos interativos no dashboard.
- **uWSGI**: Usado para servir a aplicação no PythonAnywhere.
- **PythonAnywhere**: Plataforma de hospedagem usada para disponibilizar o projeto online.

## Estrutura do Projeto

- **main.py**: Código principal contendo a lógica do dashboard e integração com Flask.
- **data**: Diretório que contém os arquivos CSV com os dados de busca por região e período.
- **requirements.txt**: Arquivo com as dependências necessárias para rodar o projeto.

## Como Executar o Projeto Localmente

Para executar o projeto localmente, siga os passos abaixo:

1. Clone o repositório:
   ```bash
   git clone https://github.com/davifalmeida/Dashboard---Seguro-Viagem.git
   cd Dashboard-Seguro-Viagem

2. Crie um ambiente virtual e ative-o:
   ```bash
    python3 -m venv venv
    source venv/bin/activate

3. Instale as dependências:
   ```bash
    pip install -r requirements.txt
   
4. Execute o aplicativo:
   ```bash
    python main.py

O servidor rodará localmente em http://127.0.0.1:8050/ e o dashboard estará disponível no navegador.

