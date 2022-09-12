from . import nlp as nlp
from api.routes import _api_get_
import json
import numpy as np
from backend.base_datos import BaseDatos
from . import similitud
from . import archivos
from . import grafos
db = BaseDatos()
palabras_permitidas =  nlp._steaming_words_permit(archivos.words()) 

def _main_(query):
    query_bd = ' '.join(nlp._function_nlp_([query], stopword=False)[0])
    bandera = False
    for palabra in palabras_permitidas:
        if query_bd in palabra:
            bandera = True
            query_bd = palabra
            break    
    if not bandera:
        return {'msg': 'No se ha encontrado resultados 1'}
    
    documents,querys = search_bd(query_bd)
    if not documents:
        return {'msg': 'No se ha encontrado resultados 2'}
    # if not documents:
    #     if not search_api(query_bd):
    #         return {'msg': 'No se ha encontrado resultados 2'}
    #     else:
    #         documents,querys = search_bd(query_bd)
    #         if not documents:
    #             return {'msg': 'No se ha encontrado resultados 3'}
    # matriz_consulta = np.loadtxt(archivos.path+querys.get("similitud"))
    # print(matriz_consulta)
    ms = grafos.matrizsubyacente([{'id':i['id'],'title':i['info']['title']} for i in documents], query)#
    return {'documents':documents, 'query':querys,'grafos':ms}

def _process(documents, file_name):    
    try:
        title, abstract, keywords = _extract_fields(documents)
        title = nlp._function_nlp_(title)
        abstract = nlp._function_nlp_(abstract)
        keywords = nlp._function_nlp_(keywords)
        print("NLP ACABADO")
        title_similitud = np.array(similitud.similitud_jaccard(title))
        print("title similitud acabado")
        keywords_similitud = np.array(similitud.similitud_jaccard(keywords))
        print("keywords similitud acabado")
        abstract_similitud = similitud.similitud_coseno(abstract)
        print("abstract similitud acabado")
        print("SIMILITUD ACABADO")
        title_similitud = title_similitud * 0.1
        keywords_similitud = keywords_similitud * 0.3
        abstract_similitud = abstract_similitud * 0.6

        matriz_similitud = title_similitud + keywords_similitud + abstract_similitud
        
        np.savetxt(archivos.path+file_name,matriz_similitud)
    except Exception as e:
        return False
    return True

def search_bd(query):
    bd_querys = db.get([('name','==',query)],'query')
    if not bd_querys:
        return False,False

    documents = []
    for q in bd_querys:
        documents = db.get([('query_id','==',q.get('id'))])
        # break
        # Version consulta cuando este presente la query de usuario en query de bd 
        # if query.lower() in q.get('name'):            
        #     documents = db.get([("query_id","==",q.get('id'))])
        #     break

    if not documents or len(documents) == 0:
        return False,False
    return [document.to_dict() for document in documents ],q.to_dict()

def search_api(query):
    documents = _api_get_(query)[0].json
    if documents.get('msg'):
        print("Error %s"%documents)    
        return False
    
    if len(documents.get('documents'))==0:
        return False

    from uuid import uuid4
    query_id = str(uuid4()) 
    #,'similitud':str(query_id+'.txt') if _process(documents,str(query_id+'.txt')) else ''
    db.post(params=[{'id':query_id,'name':query.lower()}],collection='query')
    db.post(params = documents.get('documents'), query_id=query_id)
    return True



def _extract_fields(dic):
    title = []
    abstract = []
    keywords = []
    for i in dic.get('documents'):
        line = i.get('info')
        title.append(line['title'])                                                                                                                 
        abstract.append(line['resumen'])                                                                                                                 
        keywords.append(line['keywords'])                                                                                                                         
    return title,abstract,keywords

def listar_palabras_cantidad():
    listado = ''
    for palabra in palabras_permitidas:
        documents,query = search_bd(palabra)
        listado += '%s, %s \n' % (palabra, str(len(documents)) if documents else '0')
    f = open ('listado_palabras_cantidad.txt','w')
    f.write(listado)
    f.close()

def backup():
    a = []
    bd_documents = db.get([])
    for d in bd_documents:
        a.append(d.to_dict())
    b = {'documentos_totales': a}
    with open('todos_documentos.json', 'w') as file:
        json.dump(b, file, indent=4)
    pass
    pass
    #resp = {'documents':[d.to_dict() for d in bd_documents]}
    #with open('todos_documentos2.json','w') as file: json.dump(resp,file, indent=4)
    
