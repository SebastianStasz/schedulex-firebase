from uek_schedule_scraper_utils import get_url_for_events


def get_teacher_data(element):
    full_name, degree = extract_name_and_degree(element.text)
    events_url = get_url_for_events(element.get('href'))
    
    return {'fullName': full_name,
            'degree': degree,
            'eventsUrl': events_url}


def extract_name_and_degree(text):
    name_and_degree = text.split(',')
    full_name = name_and_degree[0].strip()
    degree_data = name_and_degree[1].strip()
    degree = degree_data if len(degree_data) > 0 else None

    return full_name, degree
