
### ANÁLISE ESTATÍSTICA DE CVLI POR AISP RJ

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# OBTENDO DADOS 

try:
    print('Obtendo os dados ...')

    ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'

    df_ocorrencias = pd.read_csv(ENDERECO_DADOS,sep=';', encoding='iso-8859-1')

    # SELECIONANDO MINHAS SÉRIES
    df_cvli = df_ocorrencias[['aisp','munic', 'cvli']]

    # AGRUPANDO OS DADOS POR AISP E SOMANDO AS OCORRÊNCIAS
    df_cvli = df_cvli.groupby(['aisp', 'munic'],as_index=False)['cvli'].sum()

    
    maior_aisp = df_cvli.loc[df_cvli['cvli'].idxmax()]
    
    
    # TOTAL DE CVLI
    total_cvli = df_cvli['cvli'].sum()

    # PERCENTUAL DE CVLI POR AISP
    percentual_aisp = df_cvli['percentual %'] = (
        df_cvli['cvli'] / total_cvli * 100
    ).round(2)

    
    # PERCENTUAL DA AISP COM MAIOR NUMERO DE OCORRÊNCIAS
    percentual_maior = df_cvli['percentual %'].max()

    # PERCENTUAL DA AISP COM MENOR NUMERO DE OCORRÊNCIAS
    percentual_menor = df_cvli['percentual %'].min()

    
    # ORDENANDO OS DADOS PELO TOTAL DE CVLI, DO MAIOR PARA O MENOR
    df_cvli = df_cvli.sort_values(by='cvli',ascending=False)


    # EXIBINDO AS 5  AISP COM MAIORES TOTAIS
    print('\nCinco AISP com maiores índices de CVLI:')
    print(df_cvli.head())


    # EXIBINDO AS 5  AISP COM MENORES TOTAIS
    print('\nCinco AISP com menores índices de CVLI:')
    print(df_cvli.tail())

except Exception as e:
    print(f'Erro ao obter os dados - {e}')


    # OBTENDO MÉDIA E MEDIANA
try:
    print('\nObtendo informações sobre Crimes Violentos Letais Intencionais (CVLI)')
    array_cvli = np.array(df_cvli['cvli'])

    mediana_cvli = np.median(array_cvli)
    media_cvli = np.mean(array_cvli)
    distancia = (
    abs(media_cvli - mediana_cvli) / mediana_cvli * 100
   
)


    print('\nMedidas de Tendência Central')
    print(f'Média: {media_cvli}')
    print(f'Mediana: {mediana_cvli}')
    print(f'Distancia: Média - Mediana {distancia}')


except Exception as e:
    print(f'Erro ao obter os dados - {e}') 



    # QUARTIS       
try:
    print('\nSeparando Quartis ..')
    q1 = np.quantile(array_cvli, 0.25)
    q2 = np.quantile(array_cvli, 0.50)
    q3 = np.quantile(array_cvli, 0.75)


    print('\nMedidas de posição')
    print(f'Q1: {q1}')
    print(f'Q2: {q2}')
    print(f'Q3: {q3}')

    # ÁREAS INTEGRADAS DE SEGURANÇA PÚBLICA COM MENOS OCORRÊNCIAS.
    df_cvli_menores = df_cvli[
        df_cvli['cvli'] < q1
    ]


    # ÁREAS INTEGRADAS DE SEGURANÇA PÚBLICA COM MAIS OCORRÊNCIAS.
    df_cvli_maiores = df_cvli[
        df_cvli['cvli'] > q3
    ]


    # MENORES
    print('\nÁreas Integradas de Segurança Pública com menores ocorrências.')
    print(30 * '=')

    print(
        df_cvli_menores
        .sort_values(by='cvli', ascending=True)
        .to_string(index=False)
    )

    df_cvli_menores.to_csv(
        'menores.csv',
        index=False,
        sep=';',
        encoding='iso-8859-1'
    )

    # MAIORES
    print('\nÁreas Integradas de Segurança Pública com maiores ocorrências.')
    print(30 * '=')

    print(
        df_cvli_maiores
        .sort_values(by='cvli', ascending=False)
        .to_string(index=False)
    )

    df_cvli_maiores.to_csv(
        'maiores.csv',
        index=False,
        sep=';',
        encoding='iso-8859-1'
    )


except Exception as e:
    print(f'Erro ao obter os dados - {e}')



# MEDIDAS DE POSIÇÃO E DISPERSÃO
try:


    print('\nCalculando a Amplitude Total')    
    maximo = np.max(array_cvli)
    minimo = np.min(array_cvli)
    amplitude = maximo - minimo

except Exception as e:
    print(f'Erro ao obter os dados - {e}')


# MEDIDAS DE DISPERSÃO
try:

    # VARIÂNCIA
    variancia = np.var(array_cvli)

    # DISTÂNCIA VARIÂNCIA MÉDIA
    distancia_var_media = variancia / (media_cvli**2) * 100


    # DESVIO PADRÃO
    desvio_padrao = np.std(array_cvli)


    # COEFICIENTE DE VARIAÇÃO
    coef_variacao = (desvio_padrao / media_cvli) * 100

except Exception as e:
    print(f'Erro ao calcular medidas de dipersão - {e}')




# ANALISANDO A DISTRIBUIÇÃO
try:
    assimetria = df_cvli['cvli'].skew()
    curtose = df_cvli['cvli'].kurtosis()

    print('\nAnalisando a Distribuição')
    print(30 * '-')
    print(f'Assimetria: {assimetria:.2f}')

    print('\nAnalisando Curtose')
    print(30 * '-')
    print(f'Curtose: {curtose:.2f}')

except Exception as e:
    print(f'Erro ao calcular assimetria e curtose: {e}')




# ACHANDO OUTLIERS
try:
    iqr = q3 - q1

    # LIMITE SUPERIOR
    limite_superior = q3 + (1.5 * iqr)
    
    # LIMITE INFERIOR
    limite_inferior = q1 - (1.5 * iqr)
    
    print(f'\nLimite Superior: {limite_superior}')
    print(f'\nLimite Inferior: {limite_inferior}')


     # FILTRANDO OS OUTLIERS MENORES
    df_cvli_outliers_menores = (
        df_cvli[df_cvli['cvli'] < limite_inferior]
    )

    # FILTRANDO OS OUTLIERS MAIORES
    df_cvli_outliers_maiores = (
            df_cvli[df_cvli['cvli'] > limite_superior]
        )


     # PRINTANDO OUTLIERS MENORES
    print('\nÁreas Integradas de Segurança Pública com outliers inferiores')
    print(30*'-')
    if len(df_cvli_outliers_menores) <= 0:
        print('Não há outliers Inferiores')
    else:
        print(df_cvli_outliers_menores)


    # PRINTANDO OS OUTLIERS MAIORES
    print('\nÁreas Integradas de Segurança Pública com outliers superiores')
    print(30*'-')
    if len(df_cvli_outliers_maiores) <= 0:
        print('Não há outliers Inferiores')
    else:
        print(df_cvli_outliers_maiores)    

except Exception as e:
    print(f'Erro ao obter os dados - {e}')

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
    print(f'AISP com maior ocorrência de CVLI {maior_aisp}')
    print(f'Total de Crimes Violentos Letais Intencionais (CVLI) {total_cvli} ')
    print(f'Percentual de cada AISP {percentual_aisp}')
    print()
    print(f'A AISP com maior número de ocorrêcias concentra {percentual_maior}% do Total de CVLI')
    print('A AISP com maior participação registrou aproximadamente 9.166 ocorrências.')
    print()
    print(f'A AISP com menor número de ocorrências concentra {percentual_menor}% do total de CVLI')
    print(f" Isso responde que possuem AISPS com 0 ocorrências de CVLI")
    print()

    print(f'\nMédia: {media_cvli}')
    print(f'Mediana: {mediana_cvli}')
    print(f'Distância: {distancia}')
    print(f'IQR: {iqr}')
    print(f'Amplitude: {amplitude}') 
    print(f'Variância: {variancia:.2f}')    
    print(f'Distância Variância e Média: {distancia_var_media:.2f}')    
    print(f'Desvio Padrão: {desvio_padrao:.2f}')    
    print(f'Coeficiente de Variação: {coef_variacao:.2f}')
    print(f'Assimetria: {assimetria} considerada positiva alta. ')
    print(f'Curtose: {curtose}') # Curtose Leptocúrtica, picos mais altos e caudas longas


     # MEDIDAS ESTATÍSTICAS ================================================== 
    plt.subplot(2, 2, 1)
    
    plt.text(0.05, 0.95, f'Mínimo: {minimo}', fontsize=10)
    plt.text(0.05, 0.87, f'Limite inferior: {limite_inferior:.2f}', fontsize=10)
    plt.text(0.05, 0.79, f'Q1: {q1:.2f}', fontsize=10)
    plt.text(0.05, 0.71, f'Q2 (Mediana): {q2:.2f}', fontsize=10)
    plt.text(0.05, 0.63, f'Q3: {q3:.2f}', fontsize=10)
    plt.text(0.05, 0.55, f'Limite superior: {limite_superior:.2f}', fontsize=10)
    plt.text(0.05, 0.47, f'Máximo: {maximo}', fontsize=10)
    plt.text(0.05, 0.37, f'Média: {media_cvli:.2f}', fontsize=10)
    plt.text(0.05, 0.29, f'IQR: {iqr:.2f}', fontsize=10)
    plt.text(0.05, 0.21, f'Amplitude: {amplitude}', fontsize=10)
    plt.text(0.05, 0.13, f'Desvio padrão: {desvio_padrao:.2f}', fontsize=10)
    plt.text(0.05, 0.07, f'Coeficiente de variação: {coef_variacao:.2f}%', fontsize=10)
    plt.text(0.05, 0.01, f'Assimetria: {assimetria:.2f}', fontsize=10)
    plt.text(0.05, - 0.05, f'Curtose: {curtose:.2f}', fontsize=10)
    plt.text(0.05, - 0.11, f'Total de Crimes Violentos Letais Intencionais: {total_cvli}', fontsize=10)
    plt.text(0.05, -0.17,f'Percentual geral da maior AISP: {percentual_maior}%',fontsize=10)
    plt.text(0.05, -0.22,f'Percentual geral da menor AISP: {percentual_menor}%',fontsize=10)

    plt.title('Resumo Estatístico')
    plt.axis('off')
    
    # HISTOGRAMA  =====================================================
    plt.subplot(2, 2, 2)
    plt.title('Distribuição de Crimes Violentos Letais Intencionais (CVLI)')
    plt.xlabel('Quantidade de ocorrências por AISP')
    plt.ylabel('Frequência de AISP')
    plt.hist(array_cvli, bins=15, edgecolor='black')
    plt.axvline(media_cvli, color='green', linewidth=1) #Média
    plt.axvline(mediana_cvli, color= 'red', linewidth=1) #Mediana 
    
    contagens, limites = np.histogram(array_cvli, bins=100)
    
    print("\nFaixas de CVLI'S do Histograma")
    for i in range(len(contagens)):
        if contagens[i] >0:
            print(
                f'Faixa {i+1}: '
                f'{limites[i]:.0f} até {limites[i+1]:.0f} CVLIS '
                f'=> {contagens[i]} AISPS'
            )
    
    # BOXPLOT ====================================================================
    plt.subplot(2, 2, 3)
    plt.boxplot(
        df_cvli['cvli'],
        orientation='horizontal',
        showmeans=True,
        showfliers=True
    )
   
    plt.title('Distribuição dos Crimes Vilentos Letais Intencionais')
    plt.xlabel('Total de CVLI')
   
    # GRÁFICO DE BARRAS ==============================================================
    # DEZ MAIORES TOTAIS DE CVLI POR AISP E MUNICÍPIO
    plt.subplot(2, 2, 4)
    
    # SELECIONANDO OS 10 MAIORES TOTAIS
    df_cvli_10maiores = (
        df_cvli
        .sort_values(by='cvli', ascending=False)
        .head(10)
        .copy()
    )

    
    df_cvli_10maiores['aisp_munic'] = (
        df_cvli_10maiores['aisp'].astype(str)
        + ' - '
        + df_cvli_10maiores['munic'].astype(str)
    )

    # Ordenando para exibir a maior barra no topo
    df_cvli_10maiores = df_cvli_10maiores.sort_values(
        by='cvli',
        ascending=True
    )

    
    plt.barh(
    df_cvli_10maiores['aisp_munic'],
    df_cvli_10maiores['cvli'],
    color='steelblue',
    edgecolor='black'
)

    plt.xlabel('Total de CVLI')
    plt.ylabel('AISP - Município')
    plt.title('10 maiores totais de CVLI por AISP e município')
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

except Exception as e:
    print(f'\nErro ao mostrar medidas {e}')

