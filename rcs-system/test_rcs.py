import numpy as np
import pytest

from rcs import (
    rcs_switch_off,
    potential_energy,
    kinetic_energy,
    edm_energy,
    is_consistent,
    edm_altitude,
)


def test_rcs_switch_off_happens_if_energy_below_threshold():
    rda_range = pitch = vertical_velocity = 0
    energy_threshold = 1

    expected_result = True

    result = rcs_switch_off(rda_range, pitch, vertical_velocity, energy_threshold)

    assert result == expected_result


def test_rcs_switch_off_does_not_happen_if_energy_above_threshold():
    rda_range = 3.5e3
    pitch = vertical_velocity = 0
    energy_threshold = 0

    expected_result = False

    result = rcs_switch_off(rda_range, pitch, vertical_velocity, energy_threshold)

    assert result == expected_result


def test_kinetic_energy_zero_velocity_is_zero():
    expected_result = 0.0
    result = kinetic_energy(0.0)
    assert result == expected_result


@pytest.mark.parametrize(
    "vertical_velocity",
    [
        1.0,
        2.0,
        10000.0,
        0.1,
        -1.0,
        -2.0,
        -1000.0,
    ],
)
def test_kinetic_energy_for_nonzero_velocity_is_always_positive(vertical_velocity):
    result = kinetic_energy(vertical_velocity)
    assert result > 0


def test_potential_energy_has_same_sign_as_altitude():
    result = potential_energy(1.0)
    assert result > 0.0

    result = potential_energy(-1.0)
    assert result < 0.0


@pytest.mark.parametrize(
    "vertical_velocity",
    [
        1.0,
        2.0,
        10000.0,
        0.1,
        -1.0,
        -2.0,
        -1000.0,
    ],
)
@pytest.mark.parametrize("altitude", [1.0, 10.0, 100.0])
def test_energy_is_sum_of_kinetic_plus_potential(vertical_velocity, altitude):
    e_k = kinetic_energy(vertical_velocity)
    e_g = potential_energy(altitude)

    e = edm_energy(altitude, vertical_velocity)

    assert e == pytest.approx(e_k + e_g)


def test_rcs_switch_off_at_default_threshold():
    vertical_velocity = 4 / 3.6  # m / s
    rda_range = 2  # m
    pitch = 0.0

    expected_result = True

    result = rcs_switch_off(rda_range, pitch, vertical_velocity)


def test_rcs_switch_off_just_above_default_threshold_is_false():
    vertical_velocity = 4 / 3.6  # m / s
    rda_range = 2 + 0.01  # m
    pitch = 0.0

    expected_result = False

    result = rcs_switch_off(rda_range, pitch, vertical_velocity)

    assert result == expected_result
    assert result == expected_result


def test_pitch_larger_than_90_deg_make_sensor_inconsistent():
    expected_result = False
    rda_range = 0
    pitch = np.radians(100)

    result = is_consistent(rda_range, pitch)

    assert result == expected_result


def test_infinite_range_make_sensor_inconsistent():
    expected_result = False
    pitch = np.radians(0)
    rda_range = np.inf

    result = is_consistent(rda_range, pitch)

    assert result == expected_result


def test_inconsistent_sensor_makes_altitude_nan():
    rda_range = 0
    pitch = np.radians(100)

    result = edm_altitude(rda_range, pitch)

    assert np.isnan(result)


def test_inconsistent_sensor_never_switches_off_rcs():
    rda_range = 10_000
    pitch = np.radians(100)
    vertical_velocity = 0

    expected_result = False

    result = rcs_switch_off(rda_range, pitch, vertical_velocity)

    assert result == expected_result


def test_energy_with_negative_altitude_raises_error():
    altitude = -1_000_000
    vertical_velocity = 0

    with pytest.raises(ValueError, match="Altitude .* is invalid"):
        edm_energy(altitude, vertical_velocity)
