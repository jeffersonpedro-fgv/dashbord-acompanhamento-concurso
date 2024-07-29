# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash import Dash, html, dcc
from graphics import Graphics

class App:
    def __init__(self):
        self.graphics = Graphics()
        self.app = Dash(__name__)
        self.setup_layout()

    def setup_layout(self):

        donut_chart = self.graphics.criarGraficoDonutChart()

        # Layout do aplicativo
        self.app.layout = html.Div(children=[
            html.H1(children='FGV Conhecimento'),
            html.H2(children='Seu Dashboard de acompanhamento de concursos'),
            html.Img(src='/resources/fgv-logo.png', style={'width': '150px', 'height': 'auto', 'display': 'block', 'margin': 'auto'}),

            dcc.Graph(
                id='donut-chart',
                figure=donut_chart
            )
        ])

#instância da classe App para iniciar o aplicativo
if __name__ == '__main__':
    app_instance = App()
    app_instance.app.run(debug=True)