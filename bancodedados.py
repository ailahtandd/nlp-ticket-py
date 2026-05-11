import sqlite3
import csv
import os


def inserir_no_banco() :
     if not os.path.exists ('chamados_classificados.csv'):
         print ("ERRO: 'chamados_classificados.csv' não encontrado. A transformação falhou.")
         return 


# Criar e conectar ao banco de dados 

conexao = sqlite3.connect('incidentes_itil.db')

#O cursor é o objeto que executa os comandos SQL dentro do banco
cursor = conexao.cursor()

# Construir a estrutura da tabela (DDL - Data Definition Language)
# Usamos IF NOT EXISTS para não dar erro se rodarmos o script duas vezes
cursor.execute('''
CREATE TABLE IF NOT EXISTS chamados (
    id_ticket TEXT PRIMARY KEY,
    data_abertura TEXT,
    descricao_usuario TEXT,
    categoria_itil TEXT
)
''')

# Limpar dados antigos para evitar duplicação durante os testes
cursor.execute('DELETE FROM chamados')

# Ler o CSV e carregar os dados (DML - Data Manipulation Language)
with open('chamados_classificados.csv', 'r', encoding='utf-8') as arquivo_csv:
    leitor = csv.DictReader(arquivo_csv)
    
    # Query de inserção parametrizada com "?"
    query_insert = '''
    INSERT INTO chamados (id_ticket, data_abertura, descricao_usuario, categoria_itil)
    VALUES (?, ?, ?, ?)
    '''
    
    # Iterar sobre o CSV e executar o INSERT linha por linha
    for linha in leitor:
        cursor.execute(query_insert, (
            linha['ID_Chamado'], 
            linha['Data'], 
            linha['Descricao_Usuario'], 
            linha['Categoria_ITIL']
        ))

# Salvar (Commit) as alterações permanentemente no arquivo .db
conexao.commit()
print("Dados importados com sucesso para o banco SQLite 'incidentes_itil.db'!\n")

#Testando o banco com uma consulta SQL 
print("Resultado da Query SQL (Filtrando apenas chamados de nivel basico")
cursor.execute("SELECT id_ticket, categoria_itil FROM chamados WHERE categoria_itil = 'Nível 1 - Triagem Manual'")

# fetchall() traz todos os resultados encontrados pela query
resultados = cursor.fetchall()
for registro in resultados:
    print(f"Ticket: {registro[0]} | Categoria: {registro[1]}")

# 5. Encerrar a conexão
conexao.close()