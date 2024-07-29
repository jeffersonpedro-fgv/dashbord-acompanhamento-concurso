import traceback
from contextlib import contextmanager

import mysql.connector
import pandas as pd
import numpy as np


class SQLConsultation:
    @contextmanager
    def get_connection(self):
        conn = mysql.connector.connect(
            host='ALH001-DEV',
            user='fgv',
            password='rY44ob7N',
            database='apresentacao2024_recursos_dis',
            charset='utf8'
        )
        try:
            yield conn
        finally:
            conn.close()
    def totalCandidatos(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            comando = "SELECT COUNT(codigo) as 'Total Candidatos' FROM cadastro"
            cursor.execute(comando)
            totalCandidatos = cursor.fetchall()

            colunasTotalCand = [desc[0] for desc in cursor.description]
            totalCandidatos = pd.DataFrame(totalCandidatos, columns=colunasTotalCand)

            print(totalCandidatos)
            return totalCandidatos

    def totalRecursos(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            comando = "SELECT COUNT(protocolo) as 'Total Recursos' FROM recursos"
            cursor.execute(comando)
            totalRecursos = cursor.fetchall()

            colunasTotalRec = [desc[0] for desc in cursor.description]
            totalRecursos = pd.DataFrame(totalRecursos, columns=colunasTotalRec)

            print(totalRecursos)
            return totalRecursos

    def totalRecursosPorCargo(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            comando = '''
                SELECT 
                    car.CARR as 'Cargo', 
                    COUNT(rec.protocolo) as 'Total Recursos' 
                FROM
                    recursos as rec 
                INNER JOIN questao as q 
                    ON rec.questao = q.IDQUESTAO 
                INNER JOIN carreira as car 
                    ON rec.sigla = car.SIGLA 
                GROUP BY 
                    car.CARR;
            '''
            cursor.execute(comando)
            totalRecursosCargo = cursor.fetchall()

            colunasTotalRec = [desc[0] for desc in cursor.description]
            totalRecursosCargo = pd.DataFrame(totalRecursosCargo, columns=colunasTotalRec)

            print("Total Recursos por Cargo:")
            print(totalRecursosCargo)
            print("Chamado por:")
            traceback.print_stack()  # Imprime o rastreamento da pilha
            return totalRecursosCargo

    # def totalRecursosPorCargo(self):
    #     def totalCargo():
    #         comando = "SELECT CARR as Carreira FROM carreira"
    #         self.cursor.execute(comando)
    #         totalCarreira = self.cursor.fetchall()
    #
    #         colunasTotalCarr = [desc[0] for desc in self.cursor.description]
    #         totalCarreira = pd.DataFrame(totalCarreira, columns=colunasTotalCarr)
    #
    #         num_carreiras = totalCarreira.shape[0]  # Total de registros
    #         nomeCarreiras = totalCarreira['Carreira'].tolist()  # Lista com o conteudo dos registros
    #
    #         print(totalCarreira)
    #         print(f'Total de Carreiras: {num_carreiras}')
    #         print(f'Nome das Carreiras: {nomeCarreiras}')
    #         return totalCarreira, num_carreiras, nomeCarreiras
    #
    #     def totalRecusoCargoEDisciplina():
    #         comando = (
    #             "SELECT "
    #             "rec.questao as Questão, "
    #             "rec.sigla as Sigla, "
    #             "car.CARR as 'Cargo', "
    #             "q.QUESTAO_NOME as 'Questão', "
    #             "COUNT(rec.protocolo) as 'Total Recursos' "
    #             "FROM "
    #             "recursos as rec "
    #             "INNER JOIN questao as q "
    #             "ON rec.questao = q.IDQUESTAO "
    #             "INNER JOIN carreira as car "
    #             "ON rec.sigla = car.SIGLA "
    #             "GROUP BY "
    #             "rec.questao;"
    #         )
    #         self.cursor.execute(comando)
    #         totalRecusosCargo = self.cursor.fetchall()
    #
    #         colunasTotalRecCargo = [desc[0] for desc in self.cursor.description]
    #         totalRecusosCargo = pd.DataFrame(totalRecusosCargo, columns=colunasTotalRecCargo)
    #
    #         somaRecCarr = pd.DataFrame(
    #             totalRecusosCargo.groupby('Cargo')['Total Recursos'].sum().reset_index())  # Soma de recurso por cargo
    #
    #         print(totalRecusosCargo)
    #         print(somaRecCarr)
    #         return totalRecusosCargo, somaRecCarr
    #
    #     # Chamar as funções internas e retornar seus resultados
    #     totalCarreira, num_carreiras, nomeCarreiras = totalCargo()
    #     totalRecusosCargo, somaRecCarr = totalRecusoCargoEDisciplina()
    #
    #     return totalCarreira, num_carreiras, nomeCarreiras, totalRecusosCargo, somaRecCarr
    #
    #     # Chamar a função principal
    #     totalCarreira, num_carreiras, nomeCarreiras, totalRecusosCargo, somaRecCarr = totalRecursosPorCargo()
    #
    #     # Fechar a conexão com o banco de dados
    #     self.cursor.close()
    #     self.conn.close()
