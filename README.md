# Calculadoras Pr4
Repositório com as calculadoras em desenvolvimento. 
Os arquivos contidos na pasta programs tratam o dado LAS para servirem de entrada para o AchillesBR.
Até o presente momento existem 2 calculadoras que produzem 3 saídas (entradas do achillesBR) a saber: o
*dasfa.py*, que calcula a densidade aparente seca e a fração areia, e o *pynpefa.py* que retorna a análise
de ciclicidade baseada em [daely](https://github.com/daeIy/PyNPEFA).   

## Dependências
* [Anaconda](https://www.anaconda.com/) >= 3
* cvxopt >= 1.2.0
* scipy >= 1.4.0
* spectrum >= 0.7.3
* lasio >= 0.24.0

## Conteúdo do repositório
* programs: contém os programas principais
* inputs: arquivos de entrada e teste
* outputs: resultado do processamento
* modules: dependência pynpefa

### Como instalar a biblioteca cvxopt
A biblioteca cvxplot implementa a otimização numérica cônica utilizada na análise PyNPEFA.

Abra o powershell dentro do anaconda (windows) ou o terminal (linux) e digite o seguinte comando no seu terminal para a instalação via conda


> conda install -c conda-forge cvxopt

ou 


> pip install cvxopt


para instalação via pip. 

### Como instalar a biblioteca spectrum
A biblioteca spectrum implementa a análise espectral de uma função de onda e também é uma dependência da análise INPEFA.

Abra o powershell dentro do anaconda (windows) ou o terminal (linux) e digite o seguinte comando no seu terminal para a instalação via conda


> conda config --append channels conda-forge
> conda install spectrum

ou 


> pip install spectrum


para instalação via pip. 


### Como instalar a biblioteca lasio
A biblioteca lasio é uma dependência deste programa e não é uma biblioteca padrão do interna do Anaconda. Ela é responsável pelo pré-tratamento dos arquivos de poços em formato .las

Abra o powershell dentro do anaconda (windows) ou o terminal (linux) e digite o seguinte comando no seu terminal para a instalação via conda


> conda install lasio


ou 


> pip install lasio


para instalação via pip. 

## Como Executar o programa dasfa.py
* Abra o terminal (Linux) ou o powershell do anaconda (windows)
* Clone o repositório calculadoras ou faça o download se preferir
* Entre na pasta programs
* Digite o comando a seguir 
> python dasfa.py 
* Durante a execução digite as informações do nome do poço de teste
* Veja o print na tela com a porcentagem de valores nulos e decida com um sim ou não se deseja fazer a limpeza
* Decida digitando com um sim ou não se deseja selecionar um horizonte específico.
* Digite o nome do arquivo de saída da densidade aparente seca
* Digite o nome do arquivo de saída da fração areia.
 
## Como Executar o programa pynpefa.py
* Abra o terminal (Linux) ou o powershell do anaconda (windows)
* Clone o repositório calculadoras ou faça o download se preferir
* Entre na pasta programs
* Digite o comando a seguir 
> python pynpefa.py 
* Durante a execução digite as informações do nome do poço de teste
* Decida digitando com um sim ou não se deseja selecionar um horizonte específico.
* Digite o nome do arquivo de saída da análise INPEFA.
