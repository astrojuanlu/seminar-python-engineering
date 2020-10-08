import numpy as np

G_MARS = 3.72  # m / s2
FREE_FALL_ALTITUDE = 2  # m
FREE_FALL_VERTICAL_VELOCITY = 4 / 3.6  # m / s


def kinetic_energy(vertical_velocity: float):
    return vertical_velocity ** 2 / 2


def potential_energy(altitude: float):
    return G_MARS * altitude


def edm_energy(altitude: float, vertical_velocity: float) -> float:
    if altitude < 0.0:
        raise ValueError(f"Altitude {altitude:.3f} is invalid")
    return potential_energy(altitude) + kinetic_energy(vertical_velocity)


def edm_altitude(rda_range: float, pitch: float) -> float:
    if not is_consistent(rda_range, pitch):
        return np.nan
    else:
        return rda_range * np.cos(pitch)


def is_consistent(rda_range: float, pitch: float) -> bool:
    return -np.pi / 2 < pitch < np.pi / 2 and np.isfinite(rda_range)


def rcs_switch_off(
    rda_range: float,
    pitch: float,
    vertical_velocity: float,
    energy_threshold: float = edm_energy(
        FREE_FALL_ALTITUDE, FREE_FALL_VERTICAL_VELOCITY
    ),
):
    altitude = edm_altitude(rda_range, pitch)
    energy = edm_energy(altitude, vertical_velocity)
    return energy <= energy_threshold
