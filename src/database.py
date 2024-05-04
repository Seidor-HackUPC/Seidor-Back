import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def init_db():
    cred = credentials.Certificate("../FireBase-Credentials.json")
    firebase_admin.initialize_app(cred, {"dataBaseURL":"https://hack-2024-cca67-default-rtdb.europe-west1.firebasedatabase.app/"})


def get_product(docID):
    db = firestore.client()
    doc_ref = db.collection('Productos').document(docID)
    
    try: 
        doc = doc_ref.get()
        if not doc.exists:
            return "No such product!"
        else: 
            return doc.to_dict()
    except Exception as e:
        return str(e)

def add_data(doc_id,doc):

    db = firestore.client()
    doc_ref = db.collection('Productos').document(doc_id)

    doc_ref.set(doc)
    return
    

