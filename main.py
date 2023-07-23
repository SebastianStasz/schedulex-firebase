import bs4
import requests
import json


def get_soup_from_url(url):
    response = requests.get(url)
    return bs4.BeautifulSoup(response.content, 'html.parser')


def get_groups_from_section(section):
    groups = section.find_all('a')
    result = []

    for group in groups:
        name = group.text
        url_suffix = group.get('href')
        result.append({'group': name, 'url_suffix': url_suffix})

    return result


def get_name_and_link_from(url_suffix):
    url = 'https://planzajec.uek.krakow.pl/index.php/' + url_suffix
    soup = get_soup_from_url(url)
    elements = soup.find(class_='kolumny').findAll('a')
    result = []
    for element in elements:
        result.append({'name': element.text, 'url_suffix': element.get('href')})
    return result


def get_data_from_section(section, group_name, group_elements_name):
    groups = get_groups_from_section(section)
    result = []
    for group in groups:
        elements = get_name_and_link_from(group['url_suffix'])
        result.append({group_name: group['group'], group_elements_name: elements})
    return result


if __name__ == '__main__':
    base_url = 'https://planzajec.uek.krakow.pl/index.php/'
    resp = requests.get(base_url)
    soup = bs4.BeautifulSoup(resp.content, 'html.parser')
    sections = soup.findAll(class_='kategorie')

    teacher_groups = get_data_from_section(sections[0], 'group', 'teachers')
    pavilions = get_data_from_section(sections[2], 'pavilion', 'classrooms')
    faculties = get_data_from_section(sections[1], 'faculty', 'groups')

    data = {'teacher_groups': teacher_groups,
            'pavilions': pavilions,
            'faculties': faculties}

    with open('json_data.json', 'w') as outfile:
        json.dump(data, outfile)
