### ANÁLISE ESTATÍSTICA DOS ROUBOS DE VEÍCULOS POR MUNICÍPIO RJ

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt


# Obtendo os dados
try:
    print('Obtendo os dados...')

    ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'

    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')
    
    #df_ocorrencias = df_ocorrencias[df_ocorrencias['regiao'] == 'Capital']
    #df_ocorrencias = df_ocorrencias[df_ocorrencias['regiao'] == 'Baixada fluminense']
    #df_ocorrencias = df_ocorrencias[df_ocorrencias['regiao'] == 'Grande Niterói']
    #df_ocorrencias = df_ocorrencias[df_ocorrencias['regiao'] == 'Interior']


    # delimitando os dados
    df_roubo_veiculo = df_ocorrencias[['munic', 'roubo_veiculo']]
    # print(df_roubo_veiculo.head(30))
    # print(df_roubo_veiculo.tail(30))


    # PREPARANDO OS DADOS
    # Totalizando os roubos por cidade (Var Qualitativa 'munic' e Variável Quantitativa 'roubo_veiculo')
    df_roubo_veiculo = df_roubo_veiculo.groupby('munic', as_index=False)['roubo_veiculo'].sum()


    maior_munic = df_roubo_veiculo.loc[df_roubo_veiculo['roubo_veiculo'].idxmax()]

    

    # Obtendo porcentual e percentual de roubos spor município
    total_roubos = df_roubo_veiculo['roubo_veiculo'].sum()


    #PERCENTUAL
    df_roubo_veiculo['percentual %'] = (
        df_roubo_veiculo['roubo_veiculo'] / total_roubos * 100
    ).round(2)

    
    
    # PERCENTUAL DO MUNICÍPIO COM MAIOR NÚMERO DE OCORRÊNCIA
    percentual_maior = df_roubo_veiculo['percentual %'].max()
    
    # PERCENTUAL DO MUNICÍPIO COM MENOR NÚMERO DE OCORRÊNCIA
    percentual_menor = df_roubo_veiculo['percentual %'].min()


    # Ordenando os dados
    df_roubo_veiculo = df_roubo_veiculo.sort_values(
        by='roubo_veiculo',
        ascending=False
    )

    print(df_roubo_veiculo.head(10))
    # print(df_roubo_veiculo.tail(10))

except Exception as e:
    print(f'Erro ao obter os dados - {e}')



try:
    print(f'\nObtendo informações a cerca dos roubos dos veículos...')
    array_roubo_veiculo = np.array(df_roubo_veiculo['roubo_veiculo'])

    media_roubo_veiculo = np.mean(array_roubo_veiculo)
    mediana_roubo_veiculo = np.median(array_roubo_veiculo)
    distancia = abs(
        (media_roubo_veiculo - mediana_roubo_veiculo) / mediana_roubo_veiculo * 100
    )

    print('\nMedidas de Tendência Central')
    print(f'Média: {media_roubo_veiculo}')
    print(f'Mediana: {mediana_roubo_veiculo}')
    print(f'Distância Média - Mediana: {distancia:.2f}%')


except Exception as e:
    print(f'Obtendo Medidas - {e}')



# Calculando os quartis
try:
    print(f'\nSeparando os quartis...')
    q1 = np.quantile(array_roubo_veiculo, 0.25)
    q2 = np.quantile(array_roubo_veiculo, 0.50)
    q3 = np.quantile(array_roubo_veiculo, 0.75)

    print('\nMedidas de Posição')
    print(f'Q1: {q1}')
    print(f'Q2: {q2}')
    print(f'Q3: {q3}')

    # CIDADES COM MENORES OCORRÊNCIAS DE ROUBO
    df_roubo_veiculo_menores = df_roubo_veiculo[
        df_roubo_veiculo['roubo_veiculo'] < q1
    ]

    # CIDADES COM MAIORES OCORRÊNCIAS DE ROUBO
    df_roubo_veiculo_maiores = df_roubo_veiculo[
        df_roubo_veiculo['roubo_veiculo'] > q3
    ]

    # Menores
    print('\nMunicípios com menores roubos')
    print(30*'-')
    print(df_roubo_veiculo_menores.sort_values(by='roubo_veiculo', ascending=True))
    #EXPORTANDO O DATAFRAME
    df_roubo_veiculo_menores.to_csv('menores.csv', index=False, sep=';', encoding='iso-8859-1')

    # Maiores
    print('\nMunicípios com maiores roubos')
    print(30*'-')
    print(df_roubo_veiculo_maiores.sort_values(by='roubo_veiculo', ascending=False))
    # EXPORTANDO O DATAFRAME 
    df_roubo_veiculo_maiores.to_csv('maiores.csv', index=False, sep=';', encoding='iso-8859-1')


except Exception as e:
    print(f'Erro ao analizar a distribuição {e}')


# Medidas de Posição e Dispersão
try:
    print('\nCalculando a Amplitude Total')
    # anplitude_total = maior - menor
    # Quanto mais próximo do 0, mais homogêneos são os dados do conjunto.
    # Quanto mais próximo do maior valor, mais heterogêneos são os dados do conjunto.
    maximo = np.max(array_roubo_veiculo)
    minimo = np.min(array_roubo_veiculo)
    amplitude = maximo - minimo

except Exception as e:
    print(f'Erro ao calcular a amplitude: {e}')


try:

    # Variância
    # É uma medida p/ observar a dispersão dos dados.
    # Observa - se em relação a média.
    # É a média dos quadrados das diferenças entre cada valor e a média
    # OBS: O resultado da variância  
    variancia = np.var(array_roubo_veiculo)

    # distância variancia media
    # < 10% - Baixa Dispersão
    # Entre 10% e 25% - Tendência de Moderada Dispersão
    # Entre 10% e 25% - Tendência de Moderada Dispersão
    # > 25% - Alta dispersão
    distancia_var_media = variancia / (media_roubo_veiculo **2) * 100


    # DESVIO PADRÃO
    # É a raiz quadrada da Variância. Observa-se em relação a média
    # É a normalização da variâcia.
    # Quanto os dados se afastam da Média.
    desvio_padrao = np.std(array_roubo_veiculo)


    # Coeficiente de Variação
    # É a magnitude do desvio padrâo em relação a média
    coef_variacao = (desvio_padrao / media_roubo_veiculo) * 100 


except Exception as e:
    print(f'Erro ao calcular a variabilidade do conjunto: - {e}') 




# VERIFICANDO ASSIMETRIA DA DISTRIBUIÇÃO
# INDICA COMO OS DADOS ESTÃO DISTRIBUÍDOS.
# PARA QUE LADO TENDE A DISTRIBUIÇÃO
try:
    
    # ASSIMETRIA
    assimetria = df_roubo_veiculo['roubo_veiculo'].skew()
    print('\nAnalisando a Distribuição')
    print(30 * '-')
    print(f'Assimetria: {assimetria}')


    # CURTOSE 
    # É UMA MEDIDA QUE VERIFICA O PESO DAS CAUDAS DE UMA DISTRIBUIÇÃO
    # INDICANDO A IMPORTÂNDO DOS PESOS DOS VALORES EXTREMOS.
    # QUANTO MAIOR A CURTOSE, MAIOR TENDE A SER A INFLUENCIA DOS EXTREMOS.
 
    curtose = df_roubo_veiculo['roubo_veiculo'].kurtosis()  
    print('\nAnalisando Curtose')
    print(30*'-')
    print(f'Curtose: {curtose}')

except Exception as e:
    print(f'Erro ao calcular a Assimetria dos Dados: {e}') 


# ACHANDO OUTLIERS
try:
    # Intervalo Interquartil (IQR)
    # É a amplitude dos dados mais centrais
    # Ignora o maior e o menor valor
    # Não sofre interferência dos Extremos
    # Quanto mais próximo do 0, mais homogêneos são os dados mais centrais
    # Quanto mais próximo do Q3, mais heterogêneos são os dados dos 50% mais centrais
    # 970.75

    iqr = q3 - q1

    # CALCULANDO LIMITES
    # SUPERIOR
    limite_superior = q3 + (1.5 * iqr)

    # INFERIOR
    limite_inferior = q1 - (1.5 * iqr)


    print(f'\nLimite Superior: {limite_superior}')
    print(f'\nLimite Inferior: {limite_inferior}')

    # FILTRANDO OUTLIERS MENORES
    df_roubo_veiculo_outliers_menores = (
        df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < limite_inferior]
    )

    # PRINTANDO OUTLIERS MENORES
    print('\nMunicípios com outliers inferiores')
    print(30*'-')
    if len(df_roubo_veiculo_outliers_menores) == 0:
        print('Não há outliers Inferiores')
    else:
        print(df_roubo_veiculo_outliers_menores)
    

    # FILTRANDO OUTLIERS MAIORES
    df_roubo_veiculo_outliers_maiores = (
        df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > limite_superior]
    )

    #PRINTANDO OUTLIERS MAIORES
    print('\nMunicípios com outliers superiores')
    print(30*'-')
    if len(df_roubo_veiculo_outliers_maiores) == 0:
        print('Não há outliers Superiores')
    else:
        print(df_roubo_veiculo_outliers_maiores)

except Exception as e:
    print(f'Erro ao calcular os outliers {e}')





   #MOSTRANDO MEDIDAS DE ESTATÍSTICAS
try:

    print('\nMostrando Medidas')
    print(30*'-')
    print(f'Mínimo: {minimo}')
    print(f'Limite Inferior: {limite_inferior}')
    print(f'Q1: {q1}')
    print(f'Q2: {q2}')
    print(f'Q3: {q3}')
    print(f'Limite Superior: {limite_superior}')
    print(f'Máximo: {maximo}')
    print(f'Total de Roubos: {total_roubos} ')
    print()
    print(f'Município que concentra o maior registro de ocorrências de roubos de veículos {maior_munic}')
    print(f'Percentual Maior: O Município maior número de ocorrêcias concentra {percentual_maior}% do total de roubos')
    print('Isso corresponde aproximadamente 404603 ocorrências.')
    print()
    print(f'Percentual Menor: O Município com menor número de ocorrências concentra {percentual_menor}% do total de roubos')
    print(f'Isso quer dizer que temos Municipios com 0 ocorrências de roubos de veiculos. Apontando principalmente para o interior do estado.')
    print()
    print(f'\nMédia: {media_roubo_veiculo}')
    print(f'Mediana: {mediana_roubo_veiculo}')
    print(f'Distancia: {distancia}')
    print(f'IQR: Dispersão dos 50% centrais dos meus dados {iqr}')
    print(f'Amplitude: {amplitude}')
    print(f'Variância: {variancia:.2f}')
    print(f'Distancia Variância Media {distancia_var_media}')
    print(f'Desvio Padrão {desvio_padrao}')
    print(f'Coeficiente de Variação: {coef_variacao}')
    print(f'Assimetria: {assimetria} ')
    print(f'Curtose: {curtose}')
  
except Exception as e:
    print(f'\nErro ao mostrar medidas {e}')



try:
    print('\nInformações de Roubos de Veículos')

    plt.figure(figsize=(16,8))

    # GRÁFICO BOXPLOT 
    plt.subplot(2, 2, 1)

    plt.boxplot(
        df_roubo_veiculo['roubo_veiculo'],
        orientation='horizontal',
        showmeans=True,
        showfliers=True
    )

    plt.title('Distribuição dos Roubos de Veículos')
    plt.xlabel('Total de roubos')


    # MEDIDAS DE ESTATÍSTICAS 
    plt.subplot(2, 2, 2)

    plt.text(0.05, 0.95, f'Mínimo: {minimo}', fontsize=10)
    plt.text(0.05, 0.87, f'Limite inferior: {limite_inferior:.2f}', fontsize=10)
    plt.text(0.05, 0.79, f'Q1: {q1:.2f}', fontsize=10)
    plt.text(0.05, 0.71, f'Q2 (Mediana): {q2:.2f}', fontsize=10)
    plt.text(0.05, 0.63, f'Q3: {q3:.2f}', fontsize=10)
    plt.text(0.05, 0.55, f'Limite superior: {limite_superior:.2f}', fontsize=10)
    plt.text(0.05, 0.47, f'Máximo: {maximo}', fontsize=10)
    plt.text(0.05, 0.39, f'Média: {media_roubo_veiculo:.2f}', fontsize=10)
    plt.text(0.05, 0.29, f'IQR: {iqr:.2f}', fontsize=10)
    plt.text(0.05, 0.21, f'Amplitude: {amplitude}', fontsize=10)
    plt.text(0.05, 0.13, f'Desvio padrão: {desvio_padrao:.2f}', fontsize=10)
    plt.text(0.05, 0.07, f'Coeficiente de variação: {coef_variacao:.2f}%', fontsize=10)
    plt.text(0.05, 0.01, f'Assimetria: {assimetria:.2f}', fontsize=10)
    plt.text(0.05, - 0.05, f'Curtose: {curtose:.2f}', fontsize=10)
    plt.text(0.05, - 0.11, f'Total de Roubos: {total_roubos}', fontsize=10)
    plt.text(0.05, -0.17, f'Percentual Maior: {percentual_maior}', fontsize=10)
    plt.text(0.05, -0.22, f'Percentual Menor: {percentual_menor}', fontsize=10)
    plt.title('Resumo Estatístico')
    plt.axis('off')


    # GRÁFICO HISTOGRAMA 
    plt.subplot(2, 2, 3)
    plt.hist(array_roubo_veiculo, bins=100, edgecolor='black')
    plt.axvline(media_roubo_veiculo, color='green', linewidth=1) #Média
    plt.axvline(mediana_roubo_veiculo, color= 'red', linewidth=1) #Mediana 

    contagens, limites = np.histogram(array_roubo_veiculo, bins=100)

    # MOSTRANDO FAIXA DE ROUBOS DO HISTOGRAMA
    print(f'\nFaixas de Roubos do Histograma')
    for i in range(len(contagens)):
        if contagens[i] >0:
            print(
                f'Faixa {i+1}: '
                f'{limites[i]:.0f} até {limites[i+1]:.0f} roubos '
                f'=> {contagens[i]} Municípios'
            )


    # GRÁFICO DE BARRAS - DEZ MUNICÍPIOS COM MAIS ROUBOS 
    plt.subplot(2, 2, 4)

    df_roubo_veiculo_10_maiores = (
        df_roubo_veiculo
        .sort_values(by='roubo_veiculo', ascending=False)
        .head(10)
        .sort_values(by='roubo_veiculo', ascending=False)
    )

    plt.bar(
        df_roubo_veiculo_10_maiores['munic'],
        df_roubo_veiculo_10_maiores['roubo_veiculo']
    )

    plt.title('10 Municípios com Mais Roubos')
    plt.xlabel('Município')
    plt.ylabel('Total de roubos')
    plt.xticks(rotation=45, ha='right')


    # TÍTULO GERAL E AJUSTES
    plt.suptitle(
        'Análise Estatística de Roubos de Veículos por Município',
        fontsize=15
    )

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

except Exception as e:
    print(f'Erro ao plotar os gráficos: {e}')

