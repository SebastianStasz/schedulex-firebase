from uek_schedule_scraper_utils import base_url, get_soup_from_url, group_items_key_for, group_key_for, to_faculty_name_document, group_type_for, get_url_for_events
from uek_schedule_faculty_group import get_faculty_group_data
from uek_schedule_teacher import get_teacher_data

def get_name_and_url_from(url_suffix, group_name, type):
    url = base_url + url_suffix
    soup = get_soup_from_url(url)
    elements = soup.find(class_='kolumny').findAll('a')
    result = []
    for element in elements:
        if type == 'TEACHERS':
            result.append(get_teacher_data(element))
        elif type == 'PAVILIONS':
            classroom_group_data = get_faculty_group_data(element, False)
            classroom_url = get_url_for_events(element.get('href'))
            result.append({'name': element.text,
                           'numberOfEvents': classroom_group_data['numberOfEvents'], 
                           'eventsUrl': classroom_url})
        elif type == 'FACULTIES':
            is_language_class = group_name == '*Centrum Językowe*'
            faculty_group_data = get_faculty_group_data(element, is_language_class)
            faculty_url = get_url_for_events(element.get('href'))
            result.append({'name': faculty_group_data['group'], 
                           'numberOfEvents': faculty_group_data['numberOfEvents'], 
                           'facultyUrl': faculty_url,
                           'facultyDocument': to_faculty_name_document(group_name)})
            
    return result


def get_groups_from_section(section):
    groups = section.find_all('a')
    result = []

    for group in groups:
        name = group.text
        url_suffix = group.get('href')
        result.append({'group': name, 'url_suffix': url_suffix})

    return result


def get_data_from_section(section, type: str):
    result = []
    for group in get_groups_from_section(section):
        group_name = group['group']
        print(f'Scraping: {group_name}')
        items = get_name_and_url_from(group['url_suffix'], group_name, type)
        item = {group_key_for(type): group_name.replace('*', '').strip(), 
                group_items_key_for(type): items}
        group_type = group_type_for(type, group_name)
        if group_type != None:
            item['type'] = group_type
        result.append(item)
    return result


def get_cracow_univeristy_of_economics_data():
    soup = get_soup_from_url(base_url)
    sections = soup.findAll(class_='kategorie')

    teacher_groups = get_data_from_section(sections[0], 'TEACHERS')
    pavilions = get_data_from_section(sections[2], 'PAVILIONS')
    faculties = get_data_from_section(sections[1], 'FACULTIES')

    for i in range(10):
        faculties.append(faculties.pop(0))

    data = {'name': 'Cracow University of Economics',
            'city': 'Cracow',
            'teacherGroups': teacher_groups,
            'pavilions': pavilions,
            'faculties': faculties}

    return data
