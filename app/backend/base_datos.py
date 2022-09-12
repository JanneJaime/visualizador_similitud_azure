import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class BaseDatos():
    def __init__(self):
        self.path = "./app/analisisdocumentos-4e315-firebase-adminsdk-io7wb-c7e236ffc9.json"
        self.credentials = credentials.Certificate(self.path)
        firebase_admin.initialize_app(self.credentials)
        self.db = firestore.client()

    def get(self,params = None, collection = 'documents1'):
        if params is None:
            return self.db.collection(collection).get()
        try:            
            result = self.db.collection(collection)
            for param in params:
               result = result.where(param[0],param[1],param[2])
            return result.get()
        except Exception as e:
            print("Error %s"%e)
            return False

    def post(self,params = None, collection = 'documents1', query_id = None):
        if params is None:
            return False
        
        from uuid import uuid4
        doc = self.db.collection(collection)
        for param in params:
            if not query_id is None:
                param['query_id'] = query_id
            doc.document(str(uuid4())).set(param)
        return True