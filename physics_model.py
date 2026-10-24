import numpy as np
import pandas as pd

G = 9.81

def simulate_coaster(
    x,
    height,
    mass=5000.0,
    v0=5.0,
    friction=0.008,
    rho=1.225,
    cd=0.55,
    area=8.0,
    efficiency=1.0,
):
    """
    Simplified physics-based roller-coaster simulation.

    The model treats the train as a point mass moving along a smooth
    2D track. Energy losses are represented by rolling friction and
    aerodynamic drag. It is intended for educational/preliminary
    design analysis, not ride certification.
    """
    x = np.asarray(x, dtype=float)
    h = np.asarray(height, dtype=float)

    if len(x) != len(h) or len(x) < 10:
        raise ValueError("x and height must have at least 10 matching points.")
    if np.any(np.diff(x) <= 0):
        raise ValueError("x must be strictly increasing.")
    if mass <= 0 or v0 < 0 or friction < 0 or rho < 0 or cd < 0 or area < 0:
        raise ValueError("Physical parameters must be non-negative and mass > 0.")

    slope = np.gradient(h, x)
    curvature = np.abs(np.gradient(slope, x)) / np.maximum((1 + slope**2)**1.5, 1e-12)
    radius = np.where(curvature > 1e-8, 1.0 / curvature, np.inf)
    theta = np.arctan(slope)

    # Integrate speed along distance using work-energy balance.
    ds = np.sqrt(1 + slope**2) * np.gradient(x)
    v2 = np.zeros_like(x)
    v2[0] = v0**2

    for i in range(1, len(x)):
        v_prev = max(np.sqrt(max(v2[i-1], 0.0)), 0.1)
        v2[i] = v2[i-1]
        dh = h[i] - h[i-1]
        # Work per unit mass:
        # -g*dh - friction*g*ds - 0.5*rho*Cd*A/m * v^2 * ds
        loss_drag = 0.5 * rho * cd * area / mass * v_prev**2 * ds[i]
        dv2 = 2.0 * (-G * dh - friction * G * ds[i] - loss_drag) * efficiency
        v2[i] = max(v2[i-1] + dv2, 0.0)

    v = np.sqrt(v2)
    dt = ds / np.maximum(v, 0.5)
    time = np.cumsum(dt)
    time -= time[0]

    # Tangential acceleration from numerical derivative of velocity.
    a_t = np.gradient(v, time)
    a_n = np.divide(v**2, radius, out=np.zeros_like(v), where=np.isfinite(radius))
    g_normal_approx = np.cos(theta) + a_n / G

    # Approximate resultant acceleration.
    a_resultant = np.sqrt(a_t**2 + a_n**2)
    g_resultant = a_resultant / G

    jerk = np.gradient(a_t, time)
    snap = np.gradient(jerk, time)

    drag_force = 0.5 * rho * cd * area * v**2
    friction_force = friction * mass * G

    df = pd.DataFrame({
        "x_m": x,
        "height_m": h,
        "track_angle_deg": np.degrees(theta),
        "curvature_1_m": curvature,
        "radius_m": radius,
        "time_s": time,
        "velocity_m_s": v,
        "velocity_km_h": v * 3.6,
        "tangential_acceleration_m_s2": a_t,
        "normal_acceleration_m_s2": a_n,
        "resultant_acceleration_m_s2": a_resultant,
        "g_normal_approx": g_normal_approx,
        "g_resultant": g_resultant,
        "jerk_m_s3": jerk,
        "snap_m_s4": snap,
        "drag_force_N": drag_force,
        "friction_force_N": friction_force,
    })
    return df

def default_track(n=2500, length=500.0, initial_height=80.0):
    x = np.linspace(0, length, n)
    # Smooth, illustrative track with a large first drop and later hills.
    h = (
        initial_height
        - 0.135*x
        + 18*np.exp(-((x-120)/55)**2)
        + 12*np.exp(-((x-245)/45)**2)
        + 8*np.exp(-((x-350)/38)**2)
        + 3*np.sin(x/28)
    )
    h -= h.min()
    h += 2.0
    h[0] = initial_height
    return x, h

def summary(df):
    return {
        "max_speed_m_s": float(df.velocity_m_s.max()),
        "max_speed_km_h": float(df.velocity_km_h.max()),
        "max_resultant_g": float(df.g_resultant.max()),
        "min_normal_g": float(df.g_normal_approx.min()),
        "max_abs_jerk_m_s3": float(np.abs(df.jerk_m_s3).max()),
        "max_abs_snap_m_s4": float(np.abs(df.snap_m_s4).max()),
        "ride_time_s": float(df.time_s.iloc[-1]),
        "max_height_m": float(df.height_m.max()),
        "min_height_m": float(df.height_m.min()),
    }

def score_ride(df):
    s = summary(df)
    # These are project-specific indicators, NOT regulatory limits.
    thrill = np.clip(
        40 + 18*(s["max_speed_km_h"]/100)
        + 12*np.clip(s["max_resultant_g"], 0, 5)
        + 10*np.clip((s["max_height_m"]-s["min_height_m"])/80, 0, 2),
        0, 100
    )
    jerk_penalty = np.clip(s["max_abs_jerk_m_s3"]/20*35, 0, 45)
    g_penalty = np.clip(max(0, s["max_resultant_g"]-3.5)*18, 0, 45)
    negative_g_penalty = np.clip(max(0, -s["min_normal_g"])*25, 0, 30)
    comfort = np.clip(100 - jerk_penalty - g_penalty - negative_g_penalty, 0, 100)
    overall = 0.55*comfort + 0.45*thrill
    return {"thrill_score": float(thrill), "comfort_score": float(comfort),
            "overall_score": float(overall)}
def simulate_roller_coaster(*args, **kwargs):
    return simulate_coaster(*args, **kwargs)
