import bs4
import requests
import json


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


def is_teacher(type):
    return True if type == 'TEACHERS' else False



base_url = 'https://planzajec.uek.krakow.pl/index.php/'


def get_soup_from_url(url):
    response = requests.get(url)
    return bs4.BeautifulSoup(response.content, 'html.parser')


def get_name_and_url_from(url_suffix, is_teacher):
    url = base_url + url_suffix
    soup = get_soup_from_url(url)
    elements = soup.find(class_='kolumny').findAll('a')
    result = []
    for element in elements:
        if is_teacher:
            name_and_degree = element.text.split(',')
            degree_data = name_and_degree[1].strip()
            degree = degree_data if degree_data != '' else None
            result.append({'name': name_and_degree[0],
                           'degree': degree,
                           'url_suffix': element.get('href')})
        else:
            result.append({'name': element.text, 'url_suffix': element.get('href')})
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
        items = get_name_and_url_from(group['url_suffix'], is_teacher(type))
        item = {group_name_for(type): group['group'], group_items_name_for(type): items}
        result.append(item)
    return result


if __name__ == '__main__':
    soup = get_soup_from_url(base_url)
    sections = soup.findAll(class_='kategorie')

    teacher_groups = get_data_from_section(sections[0], 'TEACHERS')
    pavilions = get_data_from_section(sections[2], 'PAVILIONS')
    faculties = get_data_from_section(sections[1], 'FACULTIES')

    data = {'teacher_groups': teacher_groups,
            'pavilions': pavilions,
            'faculties': faculties}

    with open('json_data.json', 'w') as outfile:
        json.dump(data, outfile)
