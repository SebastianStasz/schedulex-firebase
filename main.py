from uek_schedule_scraper import get_cracow_univeristy_of_economics_data
from schedulex_firebase import save_uek_data


if __name__ == '__main__':
    data = get_cracow_univeristy_of_economics_data()
    save_uek_data(data)
