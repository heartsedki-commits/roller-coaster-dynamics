def simulate_roller_coaster(
    initial_height=80.0,
    track_length=900.0,
    mass=900.0,
    initial_velocity=5.0,
    friction_coefficient=0.015,
    drag_coefficient=0.30,
    frontal_area=2.0,
):
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
