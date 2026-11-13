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

# Branch coverage & edge case test cases:
def test_speeding_at_exact_limit():
    assert speeding_fine(60, 60, "school") == 0

def test_speeding_school_medium_and_low_excess():
    assert speeding_fine(85, 60, "school") == 4000
    assert speeding_fine(70, 60, "school") == 2000

def test_speeding_highway_high_and_low_excess():
    assert speeding_fine(110, 60, "highway") == 3000
    assert speeding_fine(80, 60, "highway") == 1000

def test_speeding_city_high_and_medium_excess():
    assert speeding_fine(110, 60, "city") == 1500
    assert speeding_fine(85, 60, "city") == 1000

def test_speeding_boundary_excess():
    assert speeding_fine(100, 60, "city") == 1000  # excess == 40 -> > 20 branch
    assert speeding_fine(101, 60, "city") == 1500  # excess == 41 -> > 40 branch
    assert speeding_fine(80, 60, "city") == 500    # excess == 20 -> <= 20 branch
    assert speeding_fine(81, 60, "city") == 1000   # excess == 21 -> > 20 branch

def test_license_action_boundaries():
    assert license_action(4, False, False) == "notice"
    assert license_action(3, True, True) == "none"
    assert license_action(8, True, True) == "suspend"
    assert license_action(11, False, False) == "warning"

def test_total_penalty_under_cap_and_empty():
    assert total_penalty([]) == 0
    assert total_penalty([0, 500, 1500]) == 2000
    assert total_penalty([5000, 5000]) == 10000

