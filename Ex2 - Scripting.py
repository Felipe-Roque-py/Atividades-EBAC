import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import sys

sns.set()

def plota_pivot_table(df, value, index, func, ylabel, xlabel, opcao='nada'):
    if opcao == 'nada':
        pd.pivot_table(df, values=value, index=index, aggfunc=func).plot(figsize=[15, 5])
    elif opcao == 'unstack':
        pd.pivot_table(df, values=value, index=index, aggfunc=func).unstack().plot(figsize=[15, 5])
    elif opcao == 'sort':
        pd.pivot_table(df, values=value, index=index, aggfunc=func).sort_values(value).plot(figsize=[15, 5])
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    return None



meses_entrada = sys.argv[1:]
ano = 2019

path = r"C:\Users\felip\OneDrive\Ebac\Scripting\Pratica\Support_Exercise_M14\input"
path_saida = r"C:\Users\felip\OneDrive\Ebac\Scripting\Support_Exercise2_M14\imagens"

for mes in meses_entrada:
    arquivo = f"SINASC_RO_{ano}_{mes}.csv"
    caminho = os.path.join(path, arquivo)
    if not os.path.exists(caminho):
        print(f" Arquivo {arquivo} não encontrado em {path}")
        continue

    sinasc = pd.read_csv(caminho)
    print(f" Arquivo carregado: {arquivo}")
   
    max_data = sinasc.DTNASC.max()[:7]
    pasta_mes = os.path.join(path_saida, max_data)
    os.makedirs(pasta_mes, exist_ok=True)
    print(f" Salvando gráficos em: {pasta_mes}")


    plota_pivot_table(sinasc, 'IDADEMAE', 'DTNASC', 'mean',
                      'média idade mãe por data', 'data nascimento')
    plt.savefig(os.path.join(pasta_mes, 'media idade mae por data.png'))
    plt.close()

    plota_pivot_table(sinasc, 'IDADEMAE', ['DTNASC', 'SEXO'], 'mean',
                      'media idade mae', 'data de nascimento', 'unstack')
    plt.savefig(os.path.join(pasta_mes, 'media idade mae por sexo.png'))
    plt.close()

    plota_pivot_table(sinasc, 'PESO', ['DTNASC', 'SEXO'], 'mean',
                      'media peso bebe', 'data de nascimento', 'unstack')
    plt.savefig(os.path.join(pasta_mes, 'media peso bebe por sexo.png'))
    plt.close()

    plota_pivot_table(sinasc, 'PESO', 'ESCMAE', 'median',
                      'PESO mediano', 'escolaridade mae', 'sort')
    plt.savefig(os.path.join(pasta_mes, 'PESO mediano por escolaridade mae.png'))
    plt.close()

    plota_pivot_table(sinasc, 'APGAR1', 'GESTACAO', 'mean',
                      'apgar1 medio', 'gestacao', 'sort')
    plt.savefig(os.path.join(pasta_mes, 'media apgar1 por gestacao.png'))
    plt.close()

