import csv
import re


# Dicionário de Padrões Regex 
CATEGORIES = {
    "Hardware": r"(monitor|teclado|mouse|impressora|notebook|ligar|tela|hardware)",
    "Software": r"(erro|travando|instalação|atualizacao|excel|outlook|sap|sistema)",
    "Acessos": r"(senha|login|reset|bloqueado|permissão|acesso|vpn|token)"
}





def classify_ticket(description):
    description = description.lower()
    for category, pattern in CATEGORIES.items():
        if re.search(pattern, description):
            return category
    return "Nível 1 (Triagem Manual)"


# Abrindo o arquivo de leitura e o de escrita simultaneamente
def processar_chamados(arquivo_entrada, arquivo_saida):
   
    with open(arquivo_entrada, mode='r', encoding='utf-8') as file_in, \
         open(arquivo_saida, mode='w', encoding='utf-8', newline='') as file_out:
        
        leitor = csv.DictReader(file_in)
        
        # Pegamos os nomes das colunas originais e adicionamos a nova coluna 'Categoria_ITIL'
        colunas = leitor.fieldnames + ['Categoria_ITIL']
        escritor = csv.DictWriter(file_out, fieldnames=colunas)
        
        escritor.writeheader()
        
        # Loop para processar cada linha do CSV
        for linha in leitor:
            descricao = linha['Descricao_Usuario']
            # Aplica a função de classificação
            categoria_encontrada = classify_ticket(descricao)
            
            # Adiciona o resultado na nova coluna
            linha['Categoria_ITIL'] = categoria_encontrada
            
            # Grava a linha atualizada no novo arquivo
            escritor.writerow(linha)



# Executando o script
processar_chamados('chamados_teste.csv', 'chamados_classificados.csv')