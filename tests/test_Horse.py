from app.utils.Horse import Horse
from data.data_gathering_script import get_summary_horse_data


def test_Horse_name():
    horse_object = get_summary_horse_data(8919)
    horse = Horse(horse_object)
    actual = horse.name
    expected = "Midnightmane"
    assert actual == expected


def test_Horse_bloodline():
    horse_object = get_summary_horse_data(8919)
    horse = Horse(horse_object)
    actual = horse.bloodline
    expected = "Buterin"
    assert actual == expected


def test_Horse_breed():
    horse_object = get_summary_horse_data(8919)
    horse = Horse(horse_object)
    actual = horse.breed
    expected = "genesis"
    assert actual == expected


def test_Horse_genotype():
    horse_object = get_summary_horse_data(8919)
    horse = Horse(horse_object)
    actual = horse.genotype
    expected = "Z10"
    assert actual == expected


def test_Horse_gender():
    horse_object = get_summary_horse_data(8919)
    horse = Horse(horse_object)
    actual = horse.gender
    expected = "Stallion"
    assert actual == expected


def test_Horse_is_super_coat():
    horse_object = get_summary_horse_data(8919)
    horse = Horse(horse_object)
    actual = horse.is_super_cost
    expected = False
    assert actual == expected
