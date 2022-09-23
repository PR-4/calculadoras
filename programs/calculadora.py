#---------------------------------#
#          Calculadora.py         #
#  Autor: Victor Carreira         #
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

#Funções implementadas:

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




#----------------------------------------------------------------------#
# Leitura do data frame que contém os canais da perfilagem             #
#----------------------------------------------------------------------#
#df = pd.read_csv("../inputs/1ses-0173--se-.las", sep='\s+', skiprows=38, 
#                 names=('depth(m)','cota','tvd','lat','long',
#                        'brgr.gapi','brneut.%','brdens.g/cm3','brdtp.us/ft','brcali.in'))
df = pd.read_csv(input('Endereço/nome do arquivo LAS:'), sep='\s+', skiprows=int(input('Número de linhas do cabeçalho:')), 
                 names=('Depth(m)','cota','TVD','lat','long',
                        'BRGR.gAPI','BRNEUT.%','BRDENS.g/cm3','BRDTP.us/ft','BRCALI.in'))

#análise do LAS
las = lasio.read("../inputs/1SES-0173--SE-.las")
las.sections.keys()
las.sections['Version']
for item in las.sections['Well']:
    print(f"{item.descr} ({item.mnemonic}): \t\t {item.value}")
    
    
las.sections['Well']['WELL'] = 'Brasil'

for count, curve in enumerate(las.curves):
    print(f"Curve: {curve.mnemonic}, \t Units: {curve.unit}, \t Description: {curve.descr}")
print(f"There are a total of: {count+1} curves present within this file")


#Filtra os Nan:
df=df[(df['BRGR.gAPI'] != -99999.0)]
df=df[(df['BRNEUT.%'] != -99999.0)]
df=df[(df['BRDENS.g/cm3'] != -99999.0)]

#Vetoriza as variáveis
prof=np.array(df['Depth(m)'])
tvd=np.array(df['TVD'])
GR=np.array(df['BRGR.gAPI'])
NPHI=np.array(df['BRNEUT.%'])
RHOB=np.array(df['BRDENS.g/cm3'])

#Calcula o índice de GR
IGR = igr(GR)

#Calcula e Salva em txt
fracao_areia = pd.DataFrame({'TVD':prof,'Sand Fraction':SandFraction(clavier(IGR))})
fracao_areia.to_csv('../outputs/fracao_areia.txt', sep=' ', index=False)


DAS = pd.DataFrame({'TVD':prof,'Dry density':DensidadeAparenteSeca(RHOB,NPHI)})
DAS.to_csv('../outputs/densidade_aparente_seca.txt', sep=' ', index=False) 
