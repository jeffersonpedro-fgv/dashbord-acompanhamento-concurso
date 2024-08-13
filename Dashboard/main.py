from datetime import datetime

from dash import Dash, html, dcc, Output, Input
from graphics import Graphics
from sql_consultation import SQLConsultation


class App:
    def __init__(self):
        self.dbManager = SQLConsultation()  # Instância única de SQLConsultation
        self.graphics = Graphics(self.dbManager)  # Passando a instância para Graphics
        self.app = Dash(__name__)
        self.totalRecursos = None
        self.totalCandidatos = None
        self.totalAcessos = None
        self.totalRecursosCargo = None
        self.totalRespostasPorCargo = None
        self.setup_layout()

    def update_data(self):
        # Atualiza os dados e gráficos
        self.totalRecursos = self.graphics.criaCardTotalRecurso()
        self.totalCandidatos = self.graphics.criaCardTotalCandidato()
        self.totalRecursosCargo = self.graphics.criarGraficoDonutChart()
        self.totalRespostasPorCargo = self.graphics.criarGraficoHorizontalBar()
        self.totalAcessos = self.graphics.criarGraficoLineChart()

        print("Class Main - Dados atualizados")
        print(self.totalCandidatos)

    def setup_layout(self):

        listaDatabases = self.dbManager.list_databases()
        listaQuestoesCargo = self.dbManager.totalRespostaPorQuestao()

        dropdown_options = [
            {'label': f"{row['Cargo']} - {row['Questão']}", 'value': row['CodQuestão']}
            for _, row in listaQuestoesCargo.iterrows()
        ]

        self.update_data()

        # Layout e Cabeçalho do aplicativo
        self.app.layout = html.Div(
            children=[
                html.Div(
                    children=[
                        html.Img(src='assets/fgv-logo.png'),
                        html.H2(children='Página de acompanhamento de concursos'),
                    ],
                    className='dash-header'
                ),

                html.Div(
                    children=[
                        html.P("Selecione um concurso"),
                        dcc.Dropdown(
                            id='database-dropdown',
                            options=listaDatabases,
                            placeholder="Nenhum Concurso selecionado",
                            value=None
                        )
                    ],
                    className='dash-dropdown'
                ),
                #Div pai dos cards
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.H3("Total de Recursos"),
                                html.P(id='total-recursos', children="Dados não carregados"),
                            ],
                            className='card'
                        ),

                        html.Div(
                            children=[
                                html.H3("Total de Candidatos"),
                                html.P(id='total-candidatos', children="Dados não carregados"),
                            ],
                            className='card'
                        ),

                        html.Div(
                            children=[
                                html.H3("Relatório"),
                                html.Button("Baixar Relatório", id='download-button', className='download-button'),
                                dcc.Download(id="download")
                            ],
                            className='card'
                        ),

                        html.Div(
                            children=[
                                html.H3("Ultima Atualização"),
                                html.P(id='update-time', children="Atualizado em: "),
                            ],
                            className='card'
                        ),
                    ],
                    className='dash-cards'
                ),
                
                #Div pai dos gráficos
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                dcc.Graph(
                                    id='horizontal-barchart',
                                    figure={},
                                    className='side-by-side-graph'
                                ),

                                dcc.Graph(
                                    id='donut-chart',
                                    figure={},
                                    className='side-by-side-graph'
                                )
                            ],
                            className='two-graphs-container'
                        ),

                        html.Div(
                                children=[
                                    dcc.Dropdown(
                                        id='questao-dropdown',
                                        options=dropdown_options,
                                        placeholder="Selecione uma questão",
                                        value=dropdown_options[0]['value'] if dropdown_options else None
                                    ),
                                    dcc.Graph(
                                        id='vertical-bar-chart',
                                        figure={},
                                        className='full-width-graph'
                                    )                      
                                ],
                                className='barchart-container'
                            ),

                        html.Div(
                            children=[
                                dcc.Graph(
                                    id='line-chart',
                                    figure={},
                                    className='full-width-graph'
                                )
                            ],
                            className='full-width-container'
                        )
                    ],
                    className='dash-content'
                ),

                #Div pai do rodapé
                html.Div(
                    children=[
                        html.P(children='Copyright© 2024 Fundação Getulio Vargas. Todos direitos reservados')
                    ],
                    className='dash-baseboard'
                ),

                dcc.Interval(
                    id='interval-component',
                    interval=1 * 60 * 1000,
                    n_intervals=0
                )
            ],
            className='dash-container'
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
        
        #Callback para atualizar o grafico de barras verticais
        @self.app.callback(
            Output('vertical-bar-chart', 'figure'),
            Input('questao-dropdown', 'value')
        )
        def update_vertical_chart(selected_questao):
            if selected_questao is None:
                return {}
            
            fig = self.graphics.criarGaficoVerticalBar(selected_questao)
            return fig
        
        # Callback para atualizar grafivis e cards
        @self.app.callback([
            Output('total-recursos', 'children'),
            Output('total-candidatos', 'children'),
            Output('horizontal-barchart', 'figure'),
            Output('donut-chart', 'figure'),
            Output('line-chart', 'figure')
            ],
            Input('database-dropdown', 'value')
        )
        def update_chart(selected_database):

            if selected_database is None:
                return (
                    "Concurso não selecionado",
                    "Concurso não selecionado",
                    {},{},{}
                    )

            print(f"Class Main - Base Selecionada: {selected_database}")
            self.dbManager.update_database(selected_database)
            self.update_data()  # Recarrega os dados com a nova base

            print('------ Class Main: Metodo Register CallBacks  -----')
            print(self.totalRecursos)

            # Retorna os novos valores para os componentes
            return (
                self.totalRecursos,
                self.totalCandidatos,
                self.totalRespostasPorCargo,
                self.totalRecursosCargo,
                self.totalAcessos
            )


# Instância da classe App para iniciar o aplicativo
if __name__ == '__main__':
    app_instance = App()
    app_instance.app.run(debug=True)
