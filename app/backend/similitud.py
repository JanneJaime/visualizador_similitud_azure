from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity,cosine_distances

import numpy as np
def similitud_jaccard(objetos):
    matrizjacc = []
    for obj_1 in objetos:
        filas = []
        for obj_2 in objetos:
            a=set(obj_2)
            b=set(obj_1)
            union=a.union(b)
            inter=a.intersection(b)
                
            if len(union)==0:
                if len(inter)==0:
                    filas.append(1)
            
            #similitud 
            similitud=len(inter)/len(union)
            filas.append(similitud)
        matrizjacc.append(filas)
    return matrizjacc

def similitud_coseno(objetos):
    bolsa = np.array(dict_bolsa(objetos)).T
    matrizcoseno = np.identity(len(bolsa))
    for index in range(len(bolsa)):
        for index1 in range(index+1,len(bolsa)):
            resultado = cosine_similarity(bolsa[index].reshape(1,-1),bolsa[index1].reshape(1,-1))
            matrizcoseno[index,index1] = resultado[0][0]
            matrizcoseno[index1,index] = resultado[0][0]
    return matrizcoseno



def dict_bolsa(objetos):
    diccionario = []
    bolsa = []
    print("diccionario")
    for o in objetos:
        diccionario += o
    diccionario = list(set(diccionario))
    print("bolsa")
    for dic in diccionario:
        linea = []
        for obj in objetos:
            linea.append(obj.count(dic))
        bolsa.append(linea)
    print("return")
    return bolsa