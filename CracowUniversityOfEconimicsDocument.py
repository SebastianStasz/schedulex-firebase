from firestore_size.calculate import document_size


class CracowUniversityOfEconimicsDocument():
    def __init__(self, db):
        self.db = db


    def set_document_data(self, uek_data):
        doc_ref = self.document_reference()
        doc_ref.set(uek_data)


    def check_document_size(self):
        doc_ref = self.document_reference()
        data = doc_ref.get().to_dict()
        doc_size = document_size(data)
        print(f'cracow_university_of_economics document size is {doc_size} bytes.')


    def document_reference(self):
        return self.db.collection('schools').document('cracow_university_of_economics')
