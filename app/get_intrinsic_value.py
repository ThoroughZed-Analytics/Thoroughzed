from app.meta_data_query_and_loop_script import get_summary_horse_data
import math


def get_intrinsic_value(id, horse_cost):
    # extract data from horse
    df = get_summary_horse_data(id)
    total_races = df['data.horse.race_statistic.number_of_races'][0]
    first_place_percent = df['data.horse.race_statistic.win_rate'][0]
    second_place_percent = df['data.horse.race_statistic.second_place_finishes'][0] / total_races * 100
    third_place_percent = df['data.horse.race_statistic.third_place_finishes'][0] / total_races * 100
    total_free_races = df['data.horse.race_statistic.number_of_free_races'][0]
    total_paid_races = df['data.horse.race_statistic.number_of_paid_races'][0]
    first_place_percent_free = df['data.horse.race_statistic.free_win_rate'][0]
    first_place_percent_paid = df['data.horse.race_statistic.paid_win_rate'][0]

    # Potential net earnings for each race (takes into account entry fee)
    per_race_net_win = ((6 * first_place_percent / 100) + (3 * second_place_percent / 100) + (2 * third_place_percent / 100)) - 1

    # 3-month yield (assuming 10 races per day)
    three_month_yield = (per_race_net_win * 90 * 10) / horse_cost * 100

    # Races required to pay back the initial cost of the horse
    races_needed = horse_cost / per_race_net_win

    return ["{:.2f}".format(per_race_net_win), "{:.2f}".format(three_month_yield), math.ceil(races_needed)]


if __name__ == '__main__':
    get_intrinsic_value(8919, 1000)