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

        # Truncar os rótulos dos cargos usando a função truncate_label
        data['Cargo'] = data['Cargo'].apply(self.truncate_label)

        labels = data['Cargo']
        values = data['Total Recursos']

        # Configurações do gráfico
        self.fig = go.Figure(
            data=[go.Pie(
                labels=labels,
                values=values,
                hole=.3,
                textinfo='percent',
                insidetextorientation='radial'
            )])

        # Atualiza o layout do gráfico
        self.fig.update_layout(
            title_text="Recursos por Cargos",
            title_x=0.5,
            title_font_size=18,
            margin=dict(t=50, b=50, l=50, r=50)
        )

        return self.fig

    def criarGraficoLineChart(self):
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
            title={
               'text': 'Acessos ao Sistema por Dia',
                'x': 0.5,
                'xanchor' : 'center',
                'yanchor': 'top',
                'font': {'size':18}
            },
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

        # Truncar os rótulos dos cargos usando a função truncate_label
        data['Cargo'] = data['Cargo'].apply(self.truncate_label)

        # Criar o gráfico de barras horizontal
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=data['Cargo'],
            x=data['Porcentual Corrigido'],
            orientation='h',
            text=data['Porcentual Corrigido'].apply(lambda x: f'{x:.2f}%'),
            textposition='inside', # Mostra o texto dentro das barras

        ))

        # Atualizar o layout do gráfico
        fig.update_layout(
            title={
                'text':'Porcentagem de Recursos Corrigidos Por Cargo',
                'x':0.5,
                'xanchor':'center',
                'yanchor': 'top'
            },
            title_font_size=18,
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

    # Função para truncar legendas
    def truncate_label(self, label, max_length=41):
        if len(label) > max_length:
            return label[:max_length] + '...'
        else:
            return label