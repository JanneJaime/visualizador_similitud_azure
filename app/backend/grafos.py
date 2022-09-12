import numpy as np
from numpy import float64, genfromtxt
from relativeNeighborhoodGraph import returnRNG
import os
import pandas as pd
import seaborn as sns
import heapq

matriz = np.loadtxt(os.path.dirname(__file__)+'/data/matriz_total.txt')

def matrizsubyacente(submatriz, query_bd):#
    ms = np.identity(len(submatriz))
    temp = []
    for x in range(len(submatriz)):
        for y in range(x+1,len(submatriz)):
            item = matriz.item((submatriz[x]['id'],submatriz[y]['id']))
            ms[x][y] = item
            ms[y][x] = item
            temp.append(item)#
    
    ids = [i['id'] for i in submatriz]#
    ms1 = pd.DataFrame(
        ms, columns= ids, index=ids
    )#
    function_exprimental(ms1,len(submatriz),query_bd,np.array(temp))#
    
    ms = returnRNG.returnRNG(ms)
    resp = {'nodos': submatriz, 'enlaces':[]}
    
    for x1 in range(len(submatriz)):
        for x2 in range(len(submatriz)):
            if ms[x1][x2] > 0:
                resp['enlaces'].append({'source':submatriz[x1]['id'],'target':submatriz[x2]['id']})
    return resp

def function_exprimental(ms,cantidad, query_bd, temp):
    print(temp)
    max_value =  temp.max()
    # min_value =  temp.min()
    t1 = np.array(list(set(temp)))
    min_value = heapq.nsmallest(2,t1)[-1]
    t2 = np.array([min_value, max_value])
    mean_value =  t2.mean()
    # desviation_value = t2.std()
    desviation_value = temp.std()
    # graph = sns.heatmap(ms,linewidths=0.3, cmap = "Blues")
    # fig = graph.get_figure()
    # fig.savefig('calor.png')
    with open('listado.txt', 'a') as f:
        f.write(f'{query_bd} & ${cantidad}$ & ${min_value}$ & ${max_value}$ & ${mean_value}$ & ${desviation_value}$ \\ \n')
    