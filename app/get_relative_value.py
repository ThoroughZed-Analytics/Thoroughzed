from app.meta_data_query_and_loop_script import get_summary_horse_data


def get_relative_value(id):
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

    return total_races


if __name__ == '__main__':
    get_relative_value(8919)
