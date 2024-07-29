# graphics.py
from dash import Dash, html, dcc
import plotly.graph_objects as go
from sql_consultation import SQLConsultation

class Graphics:
    def __init__(self):
        self.sqlConsultation = SQLConsultation()


    def criaCardTotalRecurso(self):
        data = self.sqlConsultation.totalRecursos()
        return data

    def criaCardTotalCandidato(self):
        data = self.sqlConsultation.totalCandidatos()
        return data

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
        return self.fig

    def criarGraficoExponentFormat(self):
        data = self.sqlConsultation.totalAcessoSistema()

        # Obtem listas de dias únicos e as horas associadas
        dias = data['Data'].unique()
        totalAcessoDia = data.groupby('Data')['Total de Acessos'].sum().reindex(dias)

        # Prepara dados para os horários mais acessados
        #horarios = data.groupby('Hora')['Total de Acessos'].sum()

        # Encontra a hora mais acessada por dia
        horarioPorDia = data.loc[data.groupby('Data')['Total de Acessos'].idxmax()][['Data', 'Hora']]
        horariosMaisAcessados = horarioPorDia['Hora'].values

        # Criar o gráfico com dois eixos Y
        fig = go.Figure()

        # Linha para o total de acessos por dia
        fig.add_trace(go.Scatter(
            x=dias,
            y=totalAcessoDia,
            mode='lines+markers',
            name='Total de Acessos',
            yaxis='y1'
        ))

        # Linha para o horário mais acessado
        fig.add_trace(go.Scatter(
            x=dias,
            y=horariosMaisAcessados,
            mode='lines+markers',
            name='Hora mais acessada',
            yaxis='y2'
        ))

        # Atualizar o layout do gráfico
        fig.update_layout(
            title='Acessos ao Sistema por Dia',
            xaxis=dict(title='Dias'),
            yaxis=dict(
                title='Total de Acessos',
                showexponent='all',
                exponentformat='e'
            ),
            yaxis2=dict(
                title='Hora mais Acessada',
                overlaying='y',
                side='right',
                tickmode='array',
                tickvals=list(range(24)),
                ticktext=[f'{h:02d}:00' for h in range(24)]
            ),
            legend=dict(
                x=0.01,
                y=0.99,
                bgcolor='rgba(0,0,0,0)',
                bordercolor='rgba(0,0,0,0)'
            )
        )
        return fig

    def criarGraficoHorizontalBar(self):
        data = self.sqlConsultation.totalRespostasPorCargo()

        data['Porcentual Corrigido'] = (data['Total Respostas'] / data['Total Recursos']) * 100

        # Criar o gráfico de barras horizontal
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=data['Cargo'],
            x=data['Porcentual Corrigido'],
            orientation='h',
            text=data['Porcentual Corrigido'].apply(lambda x: f'{x:.2f}%'),
            textposition='inside', # Mostra o texto dentro das barras
            # marker=dict(
            #     color='rgba(55, 83, 109, 0.6)',
            #     line=dict(color='rgba(55, 83, 109, 1.0)', width=2)
            # )
        ))

        # Atualizar o layout do gráfico
        fig.update_layout(
            title='Porcentagem de Recursos Corrigidos Por Cargo',
            xaxis=dict(
                title='Percentual Corrigido (%)',
                range=[0,100], # Define o intervalo do eixo X
                tickvals=[0,20,40,60,80,100]
            ),
            yaxis=dict(
                title='Cargo'
            ),
            bargap=0.2, # Espaço entre as barras
            plot_bgcolor='rgba(245, 246, 249, 1)'
        )
        return fig