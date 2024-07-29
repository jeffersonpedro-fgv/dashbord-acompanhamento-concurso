import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc
from graphics import Graphics

class App:
    def __init__(self):
        self.graphics = Graphics()
        self.app = Dash(__name__)  #external_stylesheets=['assets/style.css'])  # Carrega o arquivo CSS
        self.setup_layout()

    def setup_layout(self):

        totalAcessos = self.graphics.criarGraficoExponentFormat()
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
                        html.H2(children='Seu Dashboard de acompanhamento de concursos'),
                    ],
                    className='dash-header'  # Classe CSS para o cabeçalho
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
                    ],
                    className='dash-cards'  # Classe CSS para a área de cards
                ),

                # Div para os Gráficos(Barra, Pizza e Linha)
                html.Div(
                    children=[
                        dcc.Graph(
                            id='horizontal-barchart',
                            figure=totalRespostasPorCargo
                        ),
                        dcc.Graph(
                            id='donut-chart',
                            figure=totalRecursosCargo
                        ),
                        dcc.Graph(
                            id='exponent-format',
                            figure=totalAcessos
                        )
                    ],
                    className='dash-content'  # Classe CSS para a área de conteúdo
                )
            ],
            className='dash-container'  # Classe CSS para o contêiner principal
        )

# Instância da classe App para iniciar o aplicativo
if __name__ == '__main__':
    app_instance = App()
    app_instance.app.run(debug=True)
