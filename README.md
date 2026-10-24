import numpy as np


# ============================================================
# PHYSICS MODEL FOR ROLLER COASTER SIMULATION
# ============================================================

G = 9.81          # gravitational acceleration (m/s^2)
RHO = 1.225       # air density (kg/m^3)


def default_track(
    n=2500,
    length=900.0,
    initial_height=80.0
):
    """
    Creates a smooth roller-coaster track profile.

    Returns:
        x : horizontal position (m)
        h : height of track (m)
    """

    x = np.linspace(0, length, n)

    # Normalized position
    u = x / length

    # Smooth coaster-style track profile
    h = (
        initial_height
        - 55.0 * np.sin(np.pi * u) ** 2
        + 18.0 * np.sin(2 * np.pi * u)
        + 8.0 * np.sin(4 * np.pi * u)
    )

    # Keep the minimum height positive
    h = h - np.min(h) + 5.0

    return x, h


def simulate_coaster(
    x,
    h,
    mass=900.0,
    v0=5.0,
    friction=0.015,
    cd=0.30,
    area=2.0
):
    """
    Simulates roller-coaster motion using conservation of energy
    with friction and aerodynamic drag.

    Parameters:
        x       : horizontal track coordinates (m)
        h       : track height (m)
        mass    : coaster mass (kg)
        v0      : initial velocity (m/s)
        friction: coefficient of rolling/frictional resistance
        cd      : aerodynamic drag coefficient
        area    : frontal area (m^2)

    Returns:
        Dictionary containing the complete simulation results.
    """

    x = np.asarray(x, dtype=float)
    h = np.asarray(h, dtype=float)

    # --------------------------------------------------------
    # Track geometry
    # --------------------------------------------------------

    dh_dx = np.gradient(h, x)

    # Track angle
    theta = np.arctan(dh_dx)

    # Arc length increments
    ds_dx = np.sqrt(1.0 + dh_dx ** 2)

    ds = np.zeros_like(x)
    ds[1:] = np.cumsum(
        0.5 * (ds_dx[1:] + ds_dx[:-1]) * np.diff(x)
    )

    # --------------------------------------------------------
    # Curvature
    # --------------------------------------------------------

    d2h_dx2 = np.gradient(dh_dx, x)

    curvature = np.abs(d2h_dx2) / (
        1.0 + dh_dx ** 2
    ) ** 1.5

    # Avoid division by zero
    radius = np.where(
        curvature > 1e-8,
        1.0 / curvature,
        1e8
    )

    # --------------------------------------------------------
    # Energy model
    # --------------------------------------------------------

    initial_height = h[0]

    potential_energy_initial = mass * G * initial_height
    kinetic_energy_initial = 0.5 * mass * v0 ** 2

    total_initial_energy = (
        potential_energy_initial
        + kinetic_energy_initial
    )

    velocity = np.zeros_like(x)
    velocity[0] = max(v0, 0.1)

    friction_energy = np.zeros_like(x)
    drag_energy = np.zeros_like(x)

    # --------------------------------------------------------
    # Step through track
    # --------------------------------------------------------

    for i in range(1, len(x)):

        delta_s = ds[i] - ds[i - 1]

        # Gravity contribution
        gravity_energy = (
            mass
            * G
            * (h[i - 1] - h[i])
        )

        # Approximate friction energy loss
        friction_force = (
            friction
            * mass
            * G
            * np.cos(theta[i - 1])
        )

        friction_loss = max(
            friction_force * delta_s,
            0.0
        )

        # Aerodynamic drag
        drag_force = (
            0.5
            * RHO
            * cd
            * area
            * velocity[i - 1] ** 2
        )

        drag_loss = max(
            drag_force * delta_s,
            0.0
        )

        friction_energy[i] = (
            friction_energy[i - 1]
            + friction_loss
        )

        drag_energy[i] = (
            drag_energy[i - 1]
            + drag_loss
        )

        # Energy available for kinetic motion
        kinetic_energy = (
            0.5 * mass * velocity[i - 1] ** 2
            + gravity_energy
            - friction_loss
            - drag_loss
        )

        kinetic_energy = max(
            kinetic_energy,
            0.0
        )

        velocity[i] = np.sqrt(
            2.0 * kinetic_energy / mass
        )

    # --------------------------------------------------------
    # Accelerations
    # --------------------------------------------------------

    # Tangential acceleration from velocity change
    tangential_acceleration = np.gradient(
        velocity,
        ds,
        edge_order=1
    ) * velocity

    # Normal / centripetal acceleration
    normal_acceleration = (
        velocity ** 2 / radius
    )

    # Approximate vertical-normal G loading
    normal_g = (
        np.cos(theta)
        + normal_acceleration / G
    )

    # Resultant acceleration
    total_acceleration = np.sqrt(
        tangential_acceleration ** 2
        + normal_acceleration ** 2
    )

    resultant_g = (
        total_acceleration / G
    )

    # --------------------------------------------------------
    # Jerk
    # --------------------------------------------------------

    time = np.zeros_like(x)

    for i in range(1, len(x)):

        average_velocity = (
            velocity[i - 1] + velocity[i]
        ) / 2.0

        if average_velocity < 0.01:
            average_velocity = 0.01

        time[i] = (
            time[i - 1]
            + (ds[i] - ds[i - 1])
            / average_velocity
        )

    jerk = np.gradient(
        total_acceleration,
        time,
        edge_order=1
    )

    # Snap
    snap = np.gradient(
        jerk,
        time,
        edge_order=1
    )

    # --------------------------------------------------------
    # Energy
    # --------------------------------------------------------

    potential_energy = (
        mass * G * h
    )

    kinetic_energy = (
        0.5 * mass * velocity ** 2
    )

    total_energy = (
        potential_energy
        + kinetic_energy
        + friction_energy
        + drag_energy
    )

    # --------------------------------------------------------
    # Convert units
    # --------------------------------------------------------

    velocity_kmh = velocity * 3.6

    # --------------------------------------------------------
    # Return results
    # --------------------------------------------------------

    return {
        "x": x,
        "height": h,
        "distance": ds,
        "time": time,

        "velocity": velocity,
        "velocity_kmh": velocity_kmh,

        "theta": theta,
        "curvature": curvature,
        "radius": radius,

        "tangential_acceleration":
            tangential_acceleration,

        "normal_acceleration":
            normal_acceleration,

        "total_acceleration":
            total_acceleration,

        "normal_g": normal_g,
        "resultant_g": resultant_g,

        "jerk": jerk,
        "snap": snap,

        "potential_energy":
            potential_energy,

        "kinetic_energy":
            kinetic_energy,

        "friction_energy":
            friction_energy,

        "drag_energy":
            drag_energy,

        "total_energy":
            total_energy,

        "mass": mass,
        "friction": friction,
        "cd": cd,
        "area": area,
    }


# ============================================================
# COMPATIBILITY FUNCTION USED BY app.py
# ============================================================

def simulate_roller_coaster(
    initial_height=80.0,
    track_length=900.0,
    mass=900.0,
    initial_velocity=5.0,
    friction_coefficient=0.015,
    drag_coefficient=0.30,
    frontal_area=2.0,
):
    """
    Main wrapper used by the Streamlit application.
    """

    x, h = default_track(
        n=2500,
        length=float(track_length),
        initial_height=float(initial_height),
    )

    return simulate_coaster(
        x,
        h,
        mass=float(mass),
        v0=float(initial_velocity),
        friction=float(friction_coefficient),
        cd=float(drag_coefficient),
        area=float(frontal_area),
    )


# ============================================================
# SUMMARY FUNCTIONS
# ============================================================

def summary(results):
    """
    Returns important ride statistics.
    """

    velocity = results["velocity"]
    velocity_kmh = results["velocity_kmh"]
    normal_g = results["normal_g"]
    resultant_g = results["resultant_g"]
    jerk = results["jerk"]
    height = results["height"]
    time = results["time"]

    return {
        "max_speed_ms":
            float(np.max(velocity)),

        "max_speed_kmh":
            float(np.max(velocity_kmh)),

        "min_speed_ms":
            float(np.min(velocity)),

        "max_height_m":
            float(np.max(height)),

        "min_height_m":
            float(np.min(height)),

        "max_normal_g":
            float(np.max(normal_g)),

        "min_normal_g":
            float(np.min(normal_g)),

        "max_resultant_g":
            float(np.max(resultant_g)),

        "max_abs_jerk":
            float(np.max(np.abs(jerk))),

        "ride_time_s":
            float(time[-1]),
    }


def score_ride(results):
    """
    Simple project-specific comfort/thrill indicator.

    This is NOT an official amusement-ride safety standard.
    """

    max_g = float(
        np.max(results["normal_g"])
    )

    max_jerk = float(
        np.max(np.abs(results["jerk"]))
    )

    max_speed = float(
        np.max(results["velocity_kmh"])
    )

    # Thrill score
    thrill = (
        0.45 * min(max_speed / 120.0, 1.0)
        + 0.55 * min(max_g / 4.0, 1.0)
    )

    # Comfort score
    comfort = 1.0 - min(
        max_jerk / 15.0,
        1.0
    )

    comfort = max(
        0.0,
        comfort
    )

    # Overall score
    overall = (
        0.55 * thrill
        + 0.45 * comfort
    )

    return {
        "thrill_score":
            float(thrill * 100.0),

        "comfort_score":
            float(comfort * 100.0),

        "overall_score":
            float(overall * 100.0),

        "max_g":
            max_g,

        "max_jerk":
            max_jerk,

        "max_speed_kmh":
            max_speed,
    }
