from uek_schedule_event import none_if_empty, to_event_date
from uek_schedule_scraper_utils import base_url, get_soup_from_url, get_url_for_events


def get_faculty_group_events(url_suffix, is_language_class):
    url = get_url_for_events(url_suffix)
    soup = get_soup_from_url(url)
    rows = soup.findAll('tr')
    if len(rows) > 0:
        rows.pop(0)
    else:
        print(f'No rows: {url}')
        return []
    
    result = []
    for row in rows:
        cells = row.find_all('td')
        if len(cells) > 5:
            event_type = cells[3].text
            
            if not is_language_class and event_type == 'lektorat': 
                continue
            
            event_date = to_event_date(cells[0].text, cells[1].text)
            start_date = None
            end_date = None
            
            if event_date is not None:
                start_date = event_date['start_datetime']
                end_date = event_date['end_datetime']
            
            event = {'startDate': start_date,
                    'endDate': end_date,
                    'name': none_if_empty(cells[2].text),
                    'type': none_if_empty(event_type),
                    'teacher': none_if_empty(cells[4].text),
                    'place': none_if_empty(cells[5].text)}
            
            result.append(event)
    
    return result


def get_faculty_group_data(element, is_language_class):
    url_suffix = element.get('href')
    facultyGroupEvents = get_faculty_group_events(url_suffix, is_language_class)
    return {'group': element.text, 'numberOfEvents': len(facultyGroupEvents), 'events': facultyGroupEvents}
