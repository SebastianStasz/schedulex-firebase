from uek_schedule_scraper_utils import get_url_for_events
from uek_schedule_faculty_group import get_number_of_events


def get_pavilion_data(element):
    number_of_events = get_number_of_events(element, False)
    classroom_url = get_url_for_events(element.get('href'))
    
    return {'name': element.text,
            'numberOfEvents': number_of_events, 
            'eventsUrl': classroom_url}
