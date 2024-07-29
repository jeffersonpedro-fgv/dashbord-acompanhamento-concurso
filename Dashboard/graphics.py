# graphics.py
from dash import Dash, html, dcc
import plotly.graph_objects as go
from sql_consultation import SQLConsultation


class Graphics:
    def __init__(self):
        self.sqlConsultation = SQLConsultation()
        self.fig = None

    def totalRecurso(self):
        pass

    def totalCandidato(self):
        pass

    def criarGraficoDonutChart(self):

        data = self.sqlConsultation.totalRecursosPorCargo()

        labels = data['Cargo']
        values = data['Total Recursos']

        # Use `hole` to create a donut-like pie chart
        self.fig = go.Figure(
            data=[go.Pie(
                labels=labels,
                values=values,
                hole=.3,
                textinfo='percent',
                insidetextorientation='radial'
            )])
        self.fig.update_layout(title_text="Recursos por Cargos")
        # self.fig.show()

    def totalAcessoSistema(self):
        pass

    def totalRespostaProfessor(self):
        pass