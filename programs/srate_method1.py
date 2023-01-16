# coding: utf-8

#------------------- Metodologia 1 --------------------# 
# Este programa visa a implementação da metodologia 1  #
# descrita no README.md deste repositório              #
#------------------------------------------------------#

#módulos externos:
import pyleoclim as pyleo
import xarray as xr
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import lasio

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
a = pd.DataFrame.from_dict(inpefa_log)#.to_csv(saida+bacia+input("Nome do arquivo de saída (*csv,*txt):"),columns=['DEPT','OG','1','2','3','4'],index=False)




# Uma vez que o dado é carregado, o Pyleoclim precisa que ele seja convertido em um objeto Pyleo.series. Esse objeto assume
# uma fonte para o dado de tempo (idades) e outra para a variável (proxy). Como não temos as idades, precisamos assumir como 
# tempo a profundidade do poço

serietemporal = pyleo.Series(time=a['DEPT'], value=a['4'], 
                        time_name='Depth', time_unit='m',
                        value_name='Shorter INPEFA', value_unit='GR INPEFA')

fig, ax = serietemporal.plot() #apenas para visualizarmos aqui, acho que não precisamos exibir o gráfico no Achilles.
plt.show()



# Aparentemente a saída do INPEFA já sai interpolada garantindo valores igualmente espaçados pela profundidade. O resultado
# também é bastante "sem tendência". Mas para garantir que os passos seguintes funcionem bem podemos garantir que o Pyleoclim
# interpole e remova qualquer tendência (detrend).

serietemporal_ps = serietemporal.interp().detrend(method='linear')



# Análise espectral do resultado do PyNPEFA. Aqui deveríamos ser capazes de extrair deste resultado o ciclo com maior potência
# acima de 99% que acontece perto de ~10.107 m.

serietemporal_mtm = serietemporal_ps.spectral(method='mtm').signif_test(qs=[0.90,0.95,0.99])
fig, ax = serietemporal_mtm.plot(xlabel='Period [m]', ylabel='PSD')
plt.show()



# Uma vez acessando os valores numéricos da MTM acima, precisamos usar um filtro de banda (bandpass filter) para seleciornarmos
# especificamente o ciclo de ~10.107 m. As técnicas de filtragem exigem que se trabalhe no domínio da frequência. Esse ciclo,
# então teria uma frequência de 0.09894 (1/10.107). Precisamos indicar as frequências de corte ao redor desta frequencia para
# formar uma banda simétrica.


serietemporal_filter = serietemporal_ps.filter(method='butterworth', cutoff_freq = [0.07915, 0.11873])
fig, ax = serietemporal_filter.plot()
plt.show()




# Agora é preciso elaborar uma forma para selecionar os picos ou vales da senoidal e associar a passagem deles ao tempo de 405k
