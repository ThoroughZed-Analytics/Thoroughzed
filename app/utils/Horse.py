from data.data_gathering_script import get_horse_data

class Horse:
    def __init__(self, horse_obj):
        self.name = horse_obj['data.horse.name'][0]
        self.horse_id = horse_obj['data.horse.nft_id'][0]
        self.img_url = horse_obj['data.horse.img_url'][0]
        self.genotype = horse_obj['data.horse.gen'][0]
        self.bloodline = horse_obj['data.horse.bloodline'][0]
        self.breed = horse_obj['data.horse.breed_type'][0]
        self.gender = horse_obj['data.horse.horse_type'][0]
        self.coat_color = horse_obj['data.horse.color'][0]
        self.is_super_cost = horse_obj['data.horse.super_coat'][0]
        self.birthday = horse_obj['data.horse.inserted_at'][0]
        self.total_races = horse_obj['data.horse.race_statistic.number_of_races'][0]
        self.first_place_finishes = horse_obj['data.horse.race_statistic.first_place_finishes'][0]
        self.second_place_finishes = horse_obj['data.horse.race_statistic.second_place_finishes'][0]
        self.third_place_finishes = horse_obj['data.horse.race_statistic.third_place_finishes'][0]
        self.win_rate = horse_obj['data.horse.race_statistic.win_rate'][0]
        self.total_free_races = horse_obj['data.horse.race_statistic.number_of_free_races'][0]
        self.total_paid_races = horse_obj['data.horse.race_statistic.number_of_paid_races'][0]
        self.free_win_rate = horse_obj['data.horse.race_statistic.free_win_rate'][0]
        self.paid_win_rate = horse_obj['data.horse.race_statistic.paid_win_rate'][0]
        self.place_rate = 0 if self.total_races == 0 else (self.first_place_finishes + self.second_place_finishes) / self.total_races * 100
        self.show_rate = 0 if self.total_races == 0 else (self.first_place_finishes + self.second_place_finishes + self.third_place_finishes) / self.total_races * 100
        self.mother = horse_obj['data.horse.parents']
        self.father = horse_obj['data.horse.parents']
        self.total_winnings = self.get_total_winnings(self.horse_id)
    
    def get_total_winnings(self, horse_id):
        query_result = get_horse_data(horse_id)
        total_winnings = query_result.total_paid[0]
        return total_winnings
