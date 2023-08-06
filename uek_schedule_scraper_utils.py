import bs4
import requests


base_url = 'https://planzajec.uek.krakow.pl/index.php/'


def get_soup_from_url(url):
    response = requests.get(url)
    return bs4.BeautifulSoup(response.content, 'html.parser')


def to_faculty_group_name_document(group_name):
    return group_name.replace('.', '').replace('*', '').replace('/', '').lower()


def to_faculty_name_document(faculty_name):
    return faculty_name.replace(' ', '_').replace('*', '').lower()


def group_name_for(type):
    if type == 'TEACHERS':
        return 'group'
    elif type == 'PAVILIONS':
        return 'pavilion'
    else:
        return 'faculty'


def group_items_name_for(type):
    if type == 'TEACHERS':
        return 'teachers'
    elif type == 'PAVILIONS':
        return 'classrooms'
    else:
        return 'groups'
