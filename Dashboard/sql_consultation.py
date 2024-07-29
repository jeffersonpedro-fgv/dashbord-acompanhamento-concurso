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
            # print("Chamado por:")
            # traceback.print_stack()  # Imprime o rastreamento da pilha
            return totalRecursosCargo

    def totalRespostasPorCargo(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            comando = '''
                SELECT 
                    rec.sigla as Sigla, 
                    car.CARR as 'Cargo', 
                    COUNT(rec.protocolo) as 'Total Recursos',  
                    COUNT(CASE WHEN rec.respondido = 1 THEN rec.respondido END) AS 'Total Respostas' 
                FROM 
                    recursos as rec 
                INNER JOIN 
                    questao as q 
                    ON rec.questao = q.IDQUESTAO 
                INNER JOIN 
                    carreira as car 
                    ON rec.sigla = car.SIGLA 
                GROUP BY 
                    car.CARR;
            '''
            cursor.execute(comando)
            totalRespostaCargo = cursor.fetchall()

            colunasTotalAcesso = [desc[0] for desc in cursor.description]
            totalRespostaCargo = pd.DataFrame(totalRespostaCargo, columns=colunasTotalAcesso)

            print("Total de Respostas por Cargo:")
            print(totalRespostaCargo)
            return totalRespostaCargo

    def totalAcessoSistema(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            comando = '''
                SELECT 
                    DATE(dtInclusao) as Data, 
                    HOUR(dtInclusao) as Hora,
                    COUNT(*) as 'Total de Acessos'
                FROM 
                    recursos 
                GROUP BY 
                    DATE(dtInclusao), HOUR(dtInclusao)
                ORDER BY 
                    Data, Hora;
                '''
            cursor.execute(comando)
            resultado = cursor.fetchall()

            colunasTotalAcesso = [desc[0] for desc in cursor.description]
            acessoSystem = pd.DataFrame(resultado, columns=colunasTotalAcesso)

            print("Total de Acessos:")
            print(acessoSystem)
            return acessoSystem
