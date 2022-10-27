#---------------------------------#
#  Calculadora de ciclicidade para#
#alvos específicos                #
#  Autor: Victor Carreira         #
# Objetivo: retorna análise INPEFA# 
#de saída a partir de um LAS.     #          
#---------------------------------#



#módulos externos:
import matplotlib.pyplot as plt
import lasio
import numpy as np
import pandas as pd

# modulos internos
import sys
sys.path.insert(0,'../modules')
from PyNPEFA import PyNPEFA

#Diretórios:
entrada = '..'+'/'+'inputs'+'/'
saida = '..'+'/'+'outputs'+'/'
imagens = '..'+'/'+'images'+'/'


#análise do LAS
las = lasio.read(entrada+input("Nome do arquivo de entrada (*.las):"))


#transforma lasio em um pandas dataframe, reseta os índices e retira os Nans
well = las.df().reset_index().dropna(how='any') # A Análise INPEFA não permite Infs e Nans



#Seleção de alvos desejados:
alvo=input('Você deseja selecionar algum alvo específico?(sim ou não)->')
if alvo =='sim':
    topo=float(input('Profundidade de topo(m)='))
    base=float(input('Profundidade de base(m)='))
    well = well[(well['DEPT']>=topo) & (well['DEPT']<=base)]
else:
    well = well


#Análise INPEFA:
y = well.BRGR  #este nome pode variar de acordo com o dado las de entrada
x = well.DEPT

#Cálculo do INPEFA:
inpefa_log = PyNPEFA(y,x)


#Salva o arquivo de saída:
inpefa_log['DEPT'] = x
a = pd.DataFrame.from_dict(inpefa_log).to_csv(saida+input("Nome do arquivo de saída (*csv,*txt):"),columns=['DEPT','OG','1','2','3','4'],index=False)


#Fim
print('Análise INPEFA pronta!')
