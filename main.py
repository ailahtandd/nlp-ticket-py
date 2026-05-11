import classificador
import bancodedados 


print("\n[ETAPA 1] Extração e Transformação de Texto (Regex)...")

# O main chama a função do primeiro script e passa os nomes dos arquivos
classificador.processar_chamados('chamados_teste.csv', 'chamados_classificados.csv')


print("\n[ETAPA 2] Carga de Dados no Banco Relacional (SQLite)...")
# O main chama a função do segundo script
bancodedados.inserir_no_banco()

print("PIPELINE CONCLUÍDO COM SUCESSO!")
print("="*50)