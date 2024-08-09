from contextlib import contextmanager

import mysql.connector
import pandas as pd

class SQLConsultation:

    def __init__(self):
        self.host = 'ALH001-DEV'
        self.user = 'fgv'
        self.password = 'rY44ob7N'
        self.database = 'apresentacao2024_recursos_dis' # Banco de dados padrão

    @contextmanager
    def get_connection(self):

        print("Class SQL - Conectado ao banco de dados(get_connection):", self.database)

        # if self.database is None:
        #     database = self.database

        try:
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                charset='utf8'
            )
            yield conn
        except mysql.connector.Error as err:
            print(f"Erro ao conectar ao banco de dados: {err}")
            raise
        finally:
            if 'conn' in locals() and conn.is_connected():
                conn.close()

    def list_databases(self):

        print(f"Class SQL - Tentando listar bancos com o database: {self.database}")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SHOW DATABASES;")
            databases = cursor.fetchall()

            # Retorna uma lista de dicionários para o Dropdown filtrando apenas os bancos de dados que terminam com '_recursos_dis'
            database_list = [{'label': db[0], 'value': db[0]} for db in databases if db[0].endswith('_recursos_dis')]

            # Exibir a lista no console (para debug)
            print("Lista de Databases: ", database_list)

            return database_list

    def update_database(self, database):

        # Atualiza o banco de dados
        print(f"Class SQL - Recebendo a nova base de dados {database}")
        self.database = database
        print(f"Class SQL - Base atualizada para: {self.database}")

    def totalCandidatos(self):
        print(f"Class SQL - Tentando buscar total de candidatos com o database: {self.database}")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            comando = "SELECT COUNT(codigo) as 'Total Candidatos' FROM cadastro"
            cursor.execute(comando)
            # totalCandidatos = cursor.fetchall()
            totalCandidatos = cursor.fetchone()[0]

            print(f"Total de Candidados: {totalCandidatos}")
            return totalCandidatos

    def totalRecursos(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            comando = "SELECT COUNT(protocolo) as 'Total Recursos' FROM recursos"
            cursor.execute(comando)
            totalRecursos = cursor.fetchall()

            colunasTotalRec = [desc[0] for desc in cursor.description]
            totalRecursos = pd.DataFrame(totalRecursos, columns=colunasTotalRec)

            totalRecursos = totalRecursos.iloc[0, 0]

            print(f"Total de Recursos: {totalRecursos}")
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

            # print("Total Recursos por Cargo:")
            # print(totalRecursosCargo)
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

            # print("Total de Respostas por Cargo:")
            # print(totalRespostaCargo)
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

            # print("Total de Acessos:")
            # print(acessoSystem)
            return acessoSystem