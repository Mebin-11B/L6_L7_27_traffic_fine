import pytest
from traffic_fine import speeding_fine, license_action, total_penalty

# Example test cases:
def test_no_speeding():
    assert speeding_fine(50, 60, "city") == 0

def test_clean_record():
    assert license_action(2, False, False) == "none"

# Code coverage test cases:
def test_school_high_excess():
    assert speeding_fine(110, 60, "school") == 6000

def test_highway_medium_excess():
    assert speeding_fine(90, 60, "highway") == 2000

def test_city_low_excess():
    assert speeding_fine(70, 60, "city") == 500

def test_license_revoke_commercial():
    assert license_action(15, True, False) == "revoke"

def test_license_suspend_non_commercial():
    assert license_action(12, False, False) == "suspend"

def test_license_suspend_repeat_offender():
    assert license_action(9, False, True) == "suspend"

def test_license_warning():
    assert license_action(8, False, False) == "warning"

def test_license_notice():
    assert license_action(5, False, False) == "notice"

def test_total_penalty_capped():
    assert total_penalty([6000, 5000]) == 10000

def test_total_penalty_negative():
    with pytest.raises(ValueError, match="negative fine"):
        total_penalty([-100])

