import pytest
from app.get_intrinsic_value import get_intrinsic_value

def test_get_intrinsic_value_positive():
    actual = get_intrinsic_value(8919, 1000)
    expected = ['0.09', '7.95', 11327]
    assert actual == expected

def test_get_intrinsic_value_negative():
    actual = get_intrinsic_value(472060, 100)
    expected = ['-0.46', '-411.27', -218]    
    assert actual == expected

def test_get_intrinsic_value_unraced():
    with pytest.raises(ValueError):
        get_intrinsic_value(0, 100)
