from uek_schedule_scraper import get_cracow_univeristy_of_economics_data
from firebase_admin import credentials, firestore
from CracowUniversityOfEconimicsDocument import CracowUniversityOfEconimicsDocument
import firebase_admin
import time


def initialize_app():
    cred = credentials.Certificate("schedulex-service-account-key.json")
    firebase_admin.initialize_app(cred)


if __name__ == '__main__':
    initialize_app()
    db = firestore.client()
    uek_document = CracowUniversityOfEconimicsDocument(db)
    data = get_cracow_univeristy_of_economics_data()
    uek_document.set_school_data(data)
    # uek_document.check_document_size()
