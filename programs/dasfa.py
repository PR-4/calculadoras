#---------------------------------#
#   Calculadora da DAS e da FA    #
#     Autor: Victor Carreira      #
# Objetivo: retorna dois arquivos # 
#de saída a partir de um LAS.     #
#Densidade aparente seca e fração #
#de areira para utilizar como     #
#entrada do AchillesBR.           #
#---------------------------------#



#módulos necessários:
import matplotlib.pyplot as plt
import lasio
import numpy as np
import pandas as pd

#Funções implementadas e testadas:

def igr(GR):
    GRmin=min(GR)
    GRmax=max(GR)
    IGR = np.zeros(np.size(GR))
    IGR = (GR-GRmin)/(GRmax-GRmin)
    return IGR

def clavier(IGR):
    VSH = np.zeros(np.size(IGR))
    VSH = 1.7 - np.sqrt(3.38-(IGR+0.7)**2.0)
    return VSH

def SandFraction(VSH):
    SF= (1-VSH) * 100
    return SF

def DensidadeAparenteSeca(RHOB,NPHI):
    NPHI= NPHI / 100 # Fator de conversão
    DAS=RHOB-NPHI
    return DAS


#Diretórios:
entrada = '..'+'/'+'inputs'+'/'
saida = '..'+'/'+'outputs'+'/'


#entra o LAS
las = lasio.read(entrada+input("Nome do arquivo de entrada (*.las):"))

#transforma lasio em um pandas dataframe e reseta os índices
well = las.df().reset_index()


# ordenar em ordem decrescente as variáveis por seus valores ausentes
print('Valores nulos (%):')
print((well.isnull().sum()/well.shape[0]).sort_values(ascending=False)*100)

# retira os Nans
Nan = input('Você deseja retirar todos os valores nulos do seu poço?(sim ou não)->')
if Nan == 'sim':
    well = well.dropna(how='any')
    print(well.head())
else:
        well = well

#Seleção de alvos desejados:
alvo=input('Você deseja selecionar algum alvo específico?(sim ou não)->')
if alvo =='sim':
    topo=float(input('Profundidade de topo(m)='))
    base=float(input('Profundidade de base(m)='))
    well = well[(well['DEPT']>=topo) & (well['DEPT']<=base)]
else:
    well = well


#Vetoriza as variáveis
prof=np.array(well['DEPT'])
GR=np.array(well['BRGR'])
NPHI=np.array(well['BRNEUT'])
RHOB=np.array(well['BRDENS'])

#Calcula o índice de GR
IGR = igr(GR)

#Calcula o Sand Fraciton:
FA = SandFraction(clavier(IGR))

#Calcula Densidade aparente seca:
DAS = DensidadeAparenteSeca(RHOB,NPHI)


#Calcula e Salva em txt
fracao_areia = pd.DataFrame({'Profundidade [m]':prof,'Fração Areia [%]':FA})
fracao_areia.to_csv(saida+input("Nome do arquivo de saída da fração areia (*csv,*txt):"), sep='\t', index=False)


DAS = pd.DataFrame({'Profundidade [m]':prof,'Densidade Aparente Seca [g/cm³]':DAS})
DAS.to_csv(saida+input("Nome do arquivo de saída da densidade aparente seca (*csv,*txt):"), sep='\t', index=False) 

#Fim
print('Arquivos de Densidade Aparente Seca e Fração Areia prontos!')
