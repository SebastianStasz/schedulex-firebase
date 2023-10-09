import bs4
import requests


base_url = 'https://planzajec.uek.krakow.pl/index.php/'

def get_url_for_faculty_group_events(url_suffix):
    url = base_url + url_suffix
    url = url.replace('okres=1', 'okres=2')
    return url


def get_soup_from_url(url):
    response = requests.get(url)
    return bs4.BeautifulSoup(response.content, 'html.parser')


def to_faculty_group_name_document(group_name):
    return group_name.replace('.', '').replace('*', '').replace('/', '').lower()


def to_faculty_name_document(faculty_name):
    return faculty_name.replace(' ', '_').replace('*', '').replace('/', '_').lower()


def group_type_for(type, name):
    if type != "FACULTIES": return None
    
    if name == "*Centrum Językowe*" or name == "*SWFiS*":
        return 'GLOBAL'
    elif name[0] == '*':
        return 'OTHER'
    else: 
        return 'FACULTY'


def group_key_for(type):
    if type == 'TEACHERS':
        return 'group'
    elif type == 'PAVILIONS':
        return 'pavilion'
    else:
        return 'faculty'


def group_items_key_for(type):
    if type == 'TEACHERS':
        return 'teachers'
    elif type == 'PAVILIONS':
        return 'classrooms'
    else:
        return 'groups'
