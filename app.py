import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from physics_model import simulate_roller_coaster

st.set_page_config(
    page_title="Roller Coaster Dynamics Lab",
    page_icon="🎢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Styling ----------
st.markdown("""
<style>
.block-container {padding-top: 1.8rem; padding-bottom: 2rem;}
.hero {
    padding: 1.8rem 2rem;
    border-radius: 18px;
    background: linear-gradient(135deg, #111827 0%, #1f2937 55%, #374151 100%);
    color: white;
    margin-bottom: 1.2rem;
}
.hero h1 {font-size: 2.55rem; margin: 0 0 .35rem 0;}
.hero p {font-size: 1.05rem; color: #d1d5db; margin: 0;}
.metric-card {
    padding: 1rem;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    background: white;
}
.small {font-size: .88rem; color: #6b7280;}
.section-note {
    padding: .9rem 1rem;
    border-left: 4px solid #4b5563;
    background: #f9fafb;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# ---------- Helpers ----------
def get_col(df, names):
    for n in names:
        if n in df.columns:
            return df[n].to_numpy()
    return None

def safe_max(x):
    return float(np.nanmax(np.abs(x))) if x is not None and len(x) else 0.0

def plot_line(x, y, xlabel, ylabel, title):
    fig, ax = plt.subplots(figsize=(10, 4.4))
    ax.plot(x, y, linewidth=2)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=.25)
    fig.tight_layout()
    return fig

# ---------- Header ----------
st.markdown("""
<div class="hero">
<h1>🎢 Roller Coaster Dynamics Lab</h1>
<p>Interactive physics-based simulation for speed, acceleration, G-force, jerk, comfort and ride dynamics.</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.title("🎛️ Coaster Design")
st.sidebar.caption("Change the parameters and run the simulation.")

height = st.sidebar.slider("Starting height (m)", 10.0, 150.0, 80.0, 1.0)
length = st.sidebar.slider("Track length (m)", 100.0, 2500.0, 900.0, 25.0)
mass = st.sidebar.slider("Train mass (kg)", 200.0, 3000.0, 900.0, 50.0)
v0 = st.sidebar.slider("Initial velocity (m/s)", 0.0, 30.0, 5.0, 0.5)
friction = st.sidebar.slider("Friction coefficient μ", 0.0, 0.08, 0.015, 0.001)
cd = st.sidebar.slider("Drag coefficient Cd", 0.0, 1.5, 0.30, 0.05)
area = st.sidebar.slider("Frontal area (m²)", 0.3, 5.0, 2.0, 0.1)

st.sidebar.divider()
st.sidebar.caption("Model assumptions")
st.sidebar.write("• Point-mass train approximation")
st.sidebar.write("• Prescribed track profile")
st.sidebar.write("• Approximate rolling friction")
st.sidebar.write("• Aerodynamic drag")
st.sidebar.write("• Preliminary comfort/safety indicators")

run = st.sidebar.button("🚀 Run Simulation", type="primary", use_container_width=True)

# Always have a simulation available
params = dict(
    initial_height=height,
    track_length=length,
    mass=mass,
    initial_velocity=v0,
    friction_coefficient=friction,
    drag_coefficient=cd,
    frontal_area=area,
)
try:
    result = simulate_roller_coaster(**params)
except TypeError:
    # Compatibility fallback for alternate versions of the supplied model
    result = simulate_roller_coaster(height, length, mass, v0, friction, cd, area)

if isinstance(result, tuple):
    df = result[0] if hasattr(result[0], "columns") else pd.DataFrame(result[0])
    summary = result[1] if len(result) > 1 and isinstance(result[1], dict) else {}
else:
    df = result if hasattr(result, "columns") else pd.DataFrame(result)
    summary = {}

# Normalize likely column names
x = get_col(df, ["x", "distance", "s", "position"])
if x is None:
    x = np.arange(len(df))

height_arr = get_col(df, ["height", "h", "y"])
speed = get_col(df, ["velocity", "speed", "v"])
acc = get_col(df, ["acceleration", "a", "tangential_acceleration"])
gforce = get_col(df, ["g_force", "G", "normal_g", "resultant_g"])
jerk = get_col(df, ["jerk", "j"])

if height_arr is None:
    height_arr = np.linspace(height, 0, len(df))
if speed is None:
    speed = np.zeros(len(df))
if acc is None:
    acc = np.gradient(speed, x)
if gforce is None:
    gforce = np.abs(acc) / 9.80665
if jerk is None:
    jerk = np.gradient(acc, x) * np.maximum(speed, 0.1)

max_speed = float(np.nanmax(speed))
max_g = float(np.nanmax(np.abs(gforce)))
max_jerk = float(np.nanmax(np.abs(jerk)))
min_height = float(np.nanmin(height_arr))

# ---------- KPI row ----------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Maximum speed", f"{max_speed:.1f} m/s")
c2.metric("Maximum G-force", f"{max_g:.2f} G")
c3.metric("Maximum jerk", f"{max_jerk:.2f} m/s³")
c4.metric("Lowest height", f"{min_height:.1f} m")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎢 Simulation", "📊 Physics", "🛡️ Safety & Comfort",
    "📋 Survey", "🔬 Research"
])

with tab1:
    st.subheader("Track profile")
    st.pyplot(plot_line(x, height_arr, "Distance (m)", "Height (m)",
                        "Roller Coaster Track Profile"), clear_figure=True)

    st.subheader("Ride profile")
    left, right = st.columns(2)
    with left:
        st.pyplot(plot_line(x, speed, "Distance (m)", "Velocity (m/s)",
                            "Velocity Along Track"), clear_figure=True)
    with right:
        st.pyplot(plot_line(x, gforce, "Distance (m)", "G",
                            "Estimated G-Force"), clear_figure=True)

with tab2:
    st.subheader("Physics outputs")
    a, b = st.columns(2)
    with a:
        st.pyplot(plot_line(x, acc, "Distance (m)", "Acceleration (m/s²)",
                            "Acceleration"), clear_figure=True)
    with b:
        st.pyplot(plot_line(x, jerk, "Distance (m)", "Jerk (m/s³)",
                            "Jerk"), clear_figure=True)

    st.markdown("### Governing equations")
    st.latex(r"E_p=mgh")
    st.latex(r"E_k=\frac{1}{2}mv^2")
    st.latex(r"F_d=\frac{1}{2}\rho C_d A v^2")
    st.latex(r"a_n=\frac{v^2}{R}")
    st.latex(r"j=\frac{da}{dt}")

    st.markdown("""
    <div class="section-note">
    <b>Interpretation:</b> As the train descends, gravitational potential energy is
    converted into kinetic energy. Friction and aerodynamic drag remove mechanical
    energy. Curvature converts speed into normal acceleration, which contributes to
    passenger-perceived G-force.
    </div>
    """, unsafe_allow_html=True)

with tab3:
    st.subheader("Preliminary comfort indicators")

    # These are intentionally labeled as research indicators, not certification limits.
    if max_g < 3.0:
        g_status = "Lower simulated G-force"
    elif max_g < 4.0:
        g_status = "Moderate simulated G-force"
    else:
        g_status = "High simulated G-force"

    if max_jerk < 10:
        j_status = "Lower simulated jerk"
    elif max_jerk < 25:
        j_status = "Moderate simulated jerk"
    else:
        j_status = "High simulated jerk"

    c1, c2 = st.columns(2)
    with c1:
        st.metric("G-force indicator", g_status)
        st.progress(min(max_g / 5.0, 1.0))
    with c2:
        st.metric("Jerk indicator", j_status)
        st.progress(min(max_jerk / 30.0, 1.0))

    st.warning(
        "These indicators are for educational/research comparison only. "
        "They are not amusement-ride certification limits or engineering approval."
    )

    st.markdown("### Design interpretation")
    st.write(
        "A strong design balances speed and curvature with controlled changes in "
        "acceleration. Large rapid changes in acceleration can increase jerk and "
        "reduce perceived smoothness."
    )

with tab4:
    st.subheader("Customer / rider survey")
    st.write(
        "Use the prepared survey questions to collect rider preferences through "
        "Google Forms, Instagram, TikTok or another social platform."
    )

    survey_path = "survey_questions.txt"
    if __import__("os").path.exists(survey_path):
        with open(survey_path, "r", encoding="utf-8") as f:
            st.text(f.read())
    else:
        st.info("Survey questions file not found.")

    st.markdown("### Recommended analysis")
    st.write(
        "Compare preferred speed, height, G-force, smoothness and excitement "
        "against the simulated ride metrics. This creates a link between "
        "engineering performance and customer perception."
    )

with tab5:
    st.subheader("Research overview")
    st.markdown("""
**Research question:**  
How can a physics-based computational model be used to evaluate and improve
roller coaster speed, acceleration, G-force, jerk, passenger comfort and
preliminary ride performance?

**Research gap:**  
High-fidelity roller-coaster analysis can involve vehicle dynamics, wheel-rail
contact, structural deformation, vibration and nonlinear effects. This project
creates a transparent educational framework that makes the main physical
relationships accessible and interactive.

**Future work**
- 3D track geometry
- Full multibody vehicle dynamics
- Wheel/rail contact modelling
- Track elasticity and irregularities
- Real IMU measurements
- Experimental validation
- AI-based track optimization
- Digital-twin integration
""")

    if __import__("os").path.exists("PROJECT_REPORT.md"):
        st.download_button(
            "📄 Download project report",
            data=open("PROJECT_REPORT.md", "rb").read(),
            file_name="Roller_Coaster_Dynamics_Project_Report.md",
            mime="text/markdown",
        )

st.divider()
st.caption(
    "Educational research simulator • Physics model is an approximation and "
    "should not be used for real-world ride certification or safety approval."
)
