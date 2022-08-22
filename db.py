# connect firebase database
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from pprint import pprint

cred = credentials.Certificate("static/bookstore-app-8598a-firebase-adminsdk-yexvi-c659009bb6.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# # get items
# def get_items():
#     # get id
#     doc_ref = db.collection(u'book_items').stream()
#     for doc in doc_ref:
#         print(u'{} => {}'.format(doc.id, doc.to_dict()))
    

# get_items()
