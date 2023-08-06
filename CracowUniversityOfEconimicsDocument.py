from firestore_size.calculate import document_size
from uek_schedule_scraper_utils import to_faculty_group_name_document, to_faculty_name_document


class CracowUniversityOfEconimicsDocument():
    def __init__(self, db):
        self.db = db


    def set_school_data(self, school_data):
        doc_ref = self.school_document_reference()
        doc_ref.set(school_data)

    
    def set_faculty_groups_data(self, faculty, faculty_groups):
        faculty_name = to_faculty_name_document(faculty)
        for group in faculty_groups:
            group_name = to_faculty_group_name_document(group['group'])
            doc_ref = self.db.collection('schools').document('cracow_university_of_economics').collection('faculties').document(faculty_name).collection('groups').document(group_name)
            doc_ref.set(group)


    def check_school_document_size(self):
        doc_ref = self.school_document_reference()
        data = doc_ref.get().to_dict()
        doc_size = document_size(data)
        print(f'cracow_university_of_economics document size is {doc_size} bytes.')


    def school_document_reference(self):
        return self.db.collection('schools').document('cracow_university_of_economics')
