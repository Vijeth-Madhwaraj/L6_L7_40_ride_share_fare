import pytest
from ride_share_fare import extra_distance_fare, seats_and_bags_ok, pickup_status

# Example test cases:
def test_within_included_distance():
    assert extra_distance_fare("sedan", 5, "city", False) == 0

def test_seats_and_bags_ok():
    assert seats_and_bags_ok(2, 1, False) is True

# Write the rest of the test cases so that the code is 90-100% covered.

# 1. EXTRA DISTANCE FARE TESTS

def test_unknown_cab_type():
    with pytest.raises(ValueError, match="unknown cab type"):
        extra_distance_fare("luxury", 10, "city", False)


def test_negative_distance():
    with pytest.raises(ValueError, match="invalid distance"):
        extra_distance_fare("mini", -5, "city", False)


def test_subscriber_non_suv():
    # Subscriber gets 3 additional included km
    # Sedan includes 8 + 3 = 11 km
    assert extra_distance_fare("sedan", 12, "city", True) == 12


def test_subscriber_suv():
    # SUV does not receive additional included km
    # SUV includes 12 km
    assert extra_distance_fare("suv", 13, "city", True) == 12


def test_extra_distance_non_city():
    # Mini includes 5 km, extra = 1 km
    # Non-city rate = 18
    assert extra_distance_fare("mini", 6, "outstation", False) == 18


def test_extra_distance_above_20_city():
    # Sedan includes 8 km, extra = 21 km
    # City rate = 12 + 8 = 20
    assert extra_distance_fare("sedan", 29, "city", False) == 420


def test_extra_distance_above_20_outstation():
    # Sedan includes 8 km, extra = 21 km
    # Outstation rate = 18 + 8 + 4 = 30
    assert extra_distance_fare("sedan", 29, "outstation", False) == 630


# 2. SEATS AND BAGS TESTS

def test_wheelchair_passenger_allowed():
    assert seats_and_bags_ok(2, 5, True) is True


def test_wheelchair_too_many_passengers():
    assert seats_and_bags_ok(3, 1, True) is False


def test_too_many_passengers():
    assert seats_and_bags_ok(5, 1, False) is False


def test_too_many_bags():
    assert seats_and_bags_ok(3, 3, False) is False


# 3. PICKUP STATUS TESTS

def test_scheduled_airport_on_time():
    assert pickup_status(20, True, True) == "on_time"


def test_unscheduled_non_airport_on_time():
    assert pickup_status(5, False, False) == "on_time"


def test_delayed_pickup():
    assert pickup_status(0, False, False) == "delayed"


def test_missed_pickup():
    assert pickup_status(-11, False, False) == "missed"


def test_scheduled_delayed_pickup():
    assert pickup_status(6, True, True) == "delayed"


def test_scheduled_missed_pickup():
    assert pickup_status(4, True, True) == "missed"
