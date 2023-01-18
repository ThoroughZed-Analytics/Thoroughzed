from app.meta_data_query_and_loop_script import get_summary_horse_data
from app.Horse import Horse
import math


def get_intrinsic_value(id, horse_cost):
    horse_object = get_summary_horse_data(id)
    horse = Horse(horse_object)
    total_races = horse.total_races
    win_rate = horse.win_rate
    place_rate = horse.place_rate
    show_rate = horse.show_rate
    total_free_races = horse.total_free_races
    total_paid_races = horse.total_paid_races
    win_rate_free = horse.free_win_rate
    win_rate_paid = horse.paid_win_rate

    # Potential net earnings for each race (takes into account entry fee)
    per_race_net_win = ((6 * win_rate / 100) + (3 * place_rate / 100) + (2 * show_rate / 100)) - 1

    # 3-month yield (assuming 10 races per day)
    three_month_yield = (per_race_net_win * 90 * 10) / horse_cost * 100

    # Races required to pay back the initial cost of the horse
    races_needed = horse_cost / per_race_net_win

    return ["{:.2f}".format(per_race_net_win), "{:.2f}".format(three_month_yield), math.ceil(races_needed)]


if __name__ == '__main__':
    print(get_intrinsic_value(8919, 1000))
