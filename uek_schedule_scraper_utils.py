import bs4
import requests
from requests.adapters import HTTPAdapter, Retry



base_url = 'https://planzajec.uek.krakow.pl/index.php/'

def get_url_for_faculty_group_events(url_suffix):
    url = base_url + url_suffix
    url = url.replace('okres=1', 'okres=2')
    return url


def get_soup_from_url(url):
    max_retry = 5
    number_of_requests = 0
    response_result = None
    
    retry_strategy = Retry(total=100)
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session = requests.Session()
    session.mount('https://', adapter)

    while number_of_requests < max_retry:
        try:
            response = session.get(url)
            if response.status_code == requests.codes.ok:
                response_result = response
                break
        except requests.exceptions.RequestException as e:
            print(f'Error: {e}')
            number_of_requests += 1

    return bs4.BeautifulSoup(response_result.content, 'html.parser')


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
