from uek_schedule_scraper import get_cracow_univeristy_of_economics_data
from firebase_admin import credentials, firestore
import CracowUniversityOfEconimicsDocument
import firebase_admin


def initialize_app():
    cred = credentials.Certificate("schedulex-service-account-key.json")
    firebase_admin.initialize_app(cred)


if __name__ == '__main__':
    initialize_app()
    db = firestore.client()
    uekDocument = CracowUniversityOfEconimicsDocument(db)
    data = get_cracow_univeristy_of_economics_data()
    uekDocument.set_document_data(data)
    uekDocument.check_document_size()
