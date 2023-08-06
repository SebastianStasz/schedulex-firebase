from uek_schedule_event import to_event_place
from uek_schedule_scraper_utils import base_url, get_soup_from_url


def get_faculty_group_events(url_suffix):
    url = base_url + url_suffix
    url = url.replace('okres=1', 'okres=3')
    soup = get_soup_from_url(url)
    rows = soup.findAll('tr')
    rows.pop(0)
    
    result = []
    for row in rows:
        cells = row.find_all('td')
        if len(cells) > 5:
            event_type = cells[3].text
            if event_type != 'lektorat':
                event = {'date': cells[0].text,
                        'time': cells[1].text,
                        'name': cells[2].text,
                        'type': event_type,
                        'teacher': cells[4].text.strip(),
                        'place': to_event_place(cells[5].text)}
                result.append(event)
    return result


def get_faculty_group_data(element):
    url_suffix = element.get('href')
    facultyGroupEvents = get_faculty_group_events(url_suffix)
    return {'group': element.text, 'numberOfEvents': len(facultyGroupEvents), 'events': facultyGroupEvents}
