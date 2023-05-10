from data.data_gathering_script import get_summary_horse_data


def test_get_summary_horse_data_name():
    query_result = get_summary_horse_data(8919)
    actual = query_result["data.horse.name"][0]
    expected = "Midnightmane"
    assert actual == expected


def test_get_summary_horse_data_win_rate():
    query_result = get_summary_horse_data(153242)
    actual = query_result["data.horse.race_statistic.win_rate"][0]
    expected = 10.24
    assert actual == expected


def test_get_summary_horse_data_genotype():
    query_result = get_summary_horse_data(8919)
    actual = query_result["data.horse.gen"][0]
    expected = "Z10"
    assert actual == expected


def test_get_summary_horse_data_breed():
    query_result = get_summary_horse_data(8919)
    actual = query_result["data.horse.breed_type"][0]
    expected = "genesis"
    assert actual == expected


def test_get_summary_horse_data_bloodline():
    query_result = get_summary_horse_data(8919)
    actual = query_result["data.horse.bloodline"][0]
    expected = "Buterin"
    assert actual == expected
