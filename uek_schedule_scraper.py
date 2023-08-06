from uek_schedule_scraper_utils import base_url, get_soup_from_url, group_items_name_for, group_name_for, to_faculty_name_document
from uek_schedule_faculty_group import get_faculty_group_data
from uek_schedule_teacher import getTeacherData
    

faculties = {}


def save_faculty_group(faculty_name, faculty_group):
    existing_faculty_groups = faculties.get(faculty_name)
    if existing_faculty_groups is not None:
        existing_faculty_groups.append(faculty_group)
    else:
        existing_faculty_groups = [faculty_group]
    faculties[faculty_name] = existing_faculty_groups


def get_name_and_url_from(url_suffix, group_name, type):
    url = base_url + url_suffix
    soup = get_soup_from_url(url)
    elements = soup.find(class_='kolumny').findAll('a')
    result = []
    for element in elements:
        if type == 'TEACHERS':
            result.append(getTeacherData(element))
        elif type == 'PAVILIONS':
            result.append({'name': element.text, 'url_suffix': element.get('href')})
        elif type == 'FACULTIES':
            faculty_group_data = get_faculty_group_data(element)
            save_faculty_group(group_name, faculty_group_data)
            result.append({'name': faculty_group_data['group'], 
                           'numberOfEvents': faculty_group_data['numberOfEvents'], 
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
        if group_name == '*Centrum Językowe*':
            continue
        items = get_name_and_url_from(group['url_suffix'], group_name, type)
        item = {group_name_for(type): group_name, group_items_name_for(type): items}
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
