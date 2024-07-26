import mysql.connector
import pandas as pd
import numpy as np


## Conexão com o banco

conexao = mysql.connector.connect(
    host= 'ALH001-DEV',
    user= 'fgv',
    password= 'rY44ob7N',
    database= 'apresentacao2024_recursos_dis',
    charset='utf8'
)

cursor = conexao.cursor()

def totalCandidatos():
    comando = "SELECT COUNT(codigo) as 'Total Candidatos' FROM cadastro"
    cursor.execute(comando)
    totalCandidatos = cursor.fetchall()

    colunasTotalCand = [desc[0] for desc in cursor.description]
    totalCandidatos = pd.DataFrame(totalCandidatos, columns=colunasTotalCand)

    print(totalCandidatos)
    return totalCandidatos

def totalRecursos():
    comando = "SELECT COUNT(protocolo) as 'Total Recursos' FROM recursos"
    cursor.execute(comando)
    totalRecursos = cursor.fetchall()

    colunasTotalRec = [desc[0] for desc in cursor.description]
    totalRecursos = pd.DataFrame(totalRecursos, columns=colunasTotalRec)

    print(totalRecursos)
    return totalRecursos

def totalRecursosPorCargo():
    comando = "SELECT CARR as Carreira FROM carreira"
    cursor.execute(comando)
    totalCarreira = cursor.fetchall()

    colunasTotalCarr = [desc[0] for desc in cursor.description]
    totalCarreira = pd.DataFrame(totalCarreira, columns=colunasTotalCarr)

    num_carreiras = totalCarreira.shape[0]  # Total de registros
    nomeCarreiras = totalCarreira['Carreira'].tolist()  # Lista com o conteudo dos registros

    print(totalCarreira)
    print(f'Total de Carreiras: {num_carreiras}')
    print(f'Nome das Carreiras: {nomeCarreiras}')
    return totalCarreira, num_carreiras, nomeCarreiras
