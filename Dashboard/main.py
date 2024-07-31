from datetime import datetime

from dash import Dash, html, dcc, Output, Input
from graphics import Graphics
from sql_consultation import SQLConsultation

class App:
    def __init__(self):
        self.graphics = Graphics()
        self.dbManager = SQLConsultation()
        self.app = Dash(__name__)  #external_stylesheets=['assets/style.css'])  # Carrega o arquivo CSS
        self.setup_layout()

    def setup_layout(self):

        listaDatabases = self.dbManager.list_databases()
        print("Lista no Setup:" ,listaDatabases)  # Verifique a saída aqui
        options = [{'label': db, 'value': db} for db in listaDatabases]
        print("Options" , options)

        totalAcessos = self.graphics.criarGraficoLineChart()
        totalRecursosCargo = self.graphics.criarGraficoDonutChart()
        totalRespostasPorCargo = self.graphics.criarGraficoHorizontalBar()

        totalRecursos = self.graphics.criaCardTotalRecurso()
        totalCandidatos = self.graphics.criaCardTotalCandidato()



        # Layout do aplicativo
        self.app.layout = html.Div(
            children=[
                # Div para o Cabeçalho
                html.Div(
                    children=[
                        html.Img(src='assets/fgv-logo.png'),
                        html.H2(children='Página de acompanhamento de concursos'),
                    ],
                    className='dash-header'  # Classe CSS para o cabeçalho
                ),

                html.Div(
                    children=[
                        html.P("Selecione a Base de Dados"),
                        dcc.Dropdown(
                            id='database-dropdown',
                            options=options,
                            placeholder="Selecione uma base de dados",
                        )
                    ],
                    className='dash-dropdown'  # Classe CSS para o dropdown
                ),

                # Div para os Cards
                html.Div(
                    children=[
                        # Card Total de Recursos
                        html.Div(
                            children=[
                                html.H3("Total de Recursos"),
                                html.P(f"{totalRecursos}"),
                            ],
                            className='card'
                        ),

                        # Card Total de Candidatos
                        html.Div(
                            children=[
                                html.H3("Total de Candidatos"),
                                html.P(f"{totalCandidatos}"),
                            ],
                            className='card'
                        ),

                        # Card de Relatório
                        html.Div(
                            children=[
                                html.H3("Relatório"),
                                html.Button("Baixar Relatório", id='download-button', className='download-button'),
                                dcc.Download(id="download")
                            ],
                            className='card'
                        ),

                        # Card de Atualização
                        html.Div(
                            children=[
                                html.H3("Ultima Atualização"),
                                html.P(id='update-time', children="Atualizado em: "),
                            ],
                            className='card'
                        ),
                    ],
                    className='dash-cards'  # Classe CSS para a área de cards
                ),

                # Div com os dois gráficos lado a lado
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                # Gráfico de Barras Horizontais
                                dcc.Graph(
                                    id='horizontal-barchart',
                                    figure=totalRespostasPorCargo,
                                    className='side-by-side-graph'
                                ),

                                # Gráfico de Pizza
                                dcc.Graph(
                                    id='donut-chart',
                                    figure=totalRecursosCargo,
                                    className='side-by-side-graph'
                                )
                            ],
                            className='two-graphs-container'  # Classe CSS para a área dos gráficos lado a lado
                        ),

                        # Div com o gráfico de linha
                        html.Div(
                            children=[
                                dcc.Graph(
                                    id='exponent-format',
                                    figure=totalAcessos,
                                    className='full-width-graph'
                                )
                            ],
                            className='full-width-container'  # Classe CSS para a área do gráfico de linha
                        )
                    ],
                    className='dash-content'  # Classe CSS para a área de gráficos
                ),


                # Div para o Rodapé
                html.Div(
                    children=[
                        html.P(children='Copyright© 2024 Fundação Getulio Vargas. Todos direitos reservados')
                    ],
                    className='dash-baseboard'  # Classe CSS para o cabeçalho
                ),

                # Componente Intervalo para atualizações em tempo real
                dcc.Interval(
                    id='interval-component',
                    interval=1 * 60 * 1000,  # Atualiza a cada 1 minuto (em milissegundos)
                    n_intervals=0
                )
            ],
            className='dash-container'  # Classe CSS para o contêiner principal
        )

        # Callback para atualizar o tempo de atualização
        @self.app.callback(
            Output('update-time', 'children'),
            Input('interval-component', 'n_intervals')
        )
        def update_time(n):
            now = datetime.now()
            current_time = now.strftime("%d/%m/%Y - %H:%M:%S")
            return f"Atualizado em: {current_time}"

# Instância da classe App para iniciar o aplicativo
if __name__ == '__main__':
    app_instance = App()
    app_instance.app.run(debug=True)
