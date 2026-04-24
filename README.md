Excelente escolha. Trocar o nome para main.py é o padrão da indústria para o arquivo de entrada de um projeto, o que facilita muito a leitura do seu repositório por outros desenvolvedores e recrutadores.

Fiz os ajustes no README.md para refletir essa mudança e alterei a descrição técnica para evitar o termo "Mapa de Calor" (Heatmap), substituindo-o por Mapeamento Geoespacial por Intensidade, que descreve com precisão a escala de cores e o tamanho das bolhas que você usou.

Aqui está o conteúdo atualizado para você copiar no seu GitHub:

🌍 Monitoramento Sísmico Global: Observatório de Dados USGS
Este projeto consiste em um Dashboard Interativo de alta performance desenvolvido para visualização e análise de eventos sísmicos globais em tempo real. O sistema processa dados complexos da USGS para oferecer uma interface de exploração rápida e técnica.

📊 O Projeto
O dashboard utiliza a stack Python + Dash + Plotly para gerenciar milhares de registros simultâneos, apresentando:

Mapeamento Geoespacial por Intensidade: Localização precisa de epicentros com escala de cores (barra de magnitude) e tamanho proporcional à energia liberada.

Análise de Frequência Diária: Identificação de picos de atividade sísmica no tempo.

Distribuição Estatística: Histograma de magnitudes para análise da frequência de eventos.

KPIs Dinâmicos: Resumo instantâneo de eventos totais, magnitude máxima e média capturada no período.

💾 Fonte e Integridade dos Dados
Os dados são extraídos do programa oficial da USGS (United States Geological Survey).

Fonte: USGS Earthquake Catalog

Conjunto de Dados: All Earthquakes (Past 30 Days)

Período de Análise: De 25 de Março de 2026 a 24 de Abril de 2026.

Volumetria: +11.600 eventos registrados.

Nota de Integridade: A utilização de fontes auditadas como a USGS reforça o compromisso deste projeto com a precisão científica e a transparência da informação.

🛠️ Tecnologias Utilizadas
Linguagem: Python 3.12

Manipulação de Dados: Pandas

Framework de Dashboard: Plotly Dash

Visualização: Plotly Express (Geo-scatter e Histogramas)

Estilização: CSS Flexbox para layout responsivo (100% viewport height).

🚀 Como Executar
Clone o repositório:

Bash
git clone https://github.com/michelson-code/dashboard_terremotos.git
Instale as dependências:

Bash
pip install dash pandas plotly
Execute a aplicação:

Bash
python main.py
Acesse no seu navegador: http://127.0.0.1:8050/

🧠 Visão Técnica
Desenvolvido sob o pilar do rigor analítico, o projeto foca na experiência do usuário ao lidar com grandes volumes de dados. O layout foi otimizado para preencher a tela (100vh), garantindo que o mapa principal tenha destaque máximo sem comprometer a leitura dos indicadores secundários.
