import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def save_uek_data(uek_data):
    initialize_app()
    db = firestore.client()
    doc_ref = uek_data_document_reference(db)
    doc_ref.set(uek_data)


def initialize_app():
    cred = credentials.Certificate("schedulex-service-account-key.json")
    firebase_admin.initialize_app(cred)


def uek_data_document_reference(db):
    collection_reference = db.collection('schools')
    document_reference = collection_reference.document('cracow_university_of_economics')
    return document_reference
