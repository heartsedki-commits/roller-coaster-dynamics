# Physics-Based Simulation and Optimization of Roller Coaster Dynamics

## Abstract
This project develops a Python-based preliminary roller-coaster simulation that predicts track height, velocity, acceleration, curvature, G-force and jerk. The model treats the train as a point mass moving along a smooth track and includes gravitational potential energy, kinetic energy, rolling/friction losses and aerodynamic drag. A Streamlit dashboard provides interactive parameter control and graphical output. A social-media survey is proposed to measure rider preferences concerning speed, G-force, smoothness, thrill and perceived safety. The research objective is to investigate whether a simplified physics model can provide a useful preliminary assessment of ride dynamics and whether its physical indicators correspond to rider preferences.

The model is intentionally not a certification tool. Professional roller-coaster design requires structural analysis, detailed multibody dynamics, vehicle-track contact modeling, track irregularities, safety standards, testing and engineering review.

## 1. Introduction
Roller coasters are complex dynamic systems in which a vehicle follows a spatial track while passengers experience changing accelerations. Modern engineering practice uses dynamic simulation to assess force levels and transitions. Vekoma, for example, describes using dynamic multibody environments during layout and vehicle engineering. The research literature similarly ranges from simplified point-mass models to multibody vehicle and passenger models.

## 2. Problem Statement
Detailed roller-coaster models can require specialized software and significant computational effort. There is therefore value in a transparent educational/preliminary model that connects track geometry to velocity, acceleration, G-force and jerk and presents the results interactively.

## 3. Objectives
1. Develop a physics-based roller-coaster model in Python.
2. Calculate velocity from changes in gravitational potential energy and losses.
3. Estimate acceleration and centripetal acceleration from track geometry.
4. Calculate G-force and jerk.
5. Build a professional Streamlit interface.
6. Collect rider preferences through an anonymous survey.
7. Compare physical indicators with user preferences.
8. Identify limitations and propose an advanced model.

## 4. Literature Review (2016–2026)
### 4.1 Vehicle and passenger dynamics
Ambrosio et al. (2017) describe roller-coaster dynamics as a combination of track geometry, vehicle-track interaction and suspension, and develop multibody and biomechanical models. This establishes why the present project begins with a simpler point-mass approximation and identifies the detailed vehicle/passenger model as future work.

### 4.2 Structural loading
Golenkin (2019) describes a workflow in which trajectory analysis provides train velocity and G-forces, which are then used to generate track loads for structural time-history analysis. This supports the separation between a preliminary dynamics model and later structural verification.

### 4.3 Acceleration, jerk, snap and vibration
Pendrill and Eager (2020) emphasize that acceleration, jerk, snap and vibration affect the human body during roller-coaster rides. Their discussion shows that maximum acceleration alone does not fully describe rider experience.

### 4.4 Ride and play comfort
Liu et al. (2021) investigate roller-coaster simulation as an environment for studying both physical ride comfort and mental experience. Their work connects physics quantities such as potential energy, momentum and force with perceived excitement and comfort.

### 4.5 Optimization
Schuttert (2022) formulates roller-coaster element design as a reinforcement-learning problem. Track elements are represented parametrically and rewards can combine mechanical stability, thrill and passenger safety. The work also reports difficulties caused by simplified assumptions, showing why spatial awareness and physical feasibility are important future improvements.

### 4.6 Procedural generation
The 2023 IEEE Conference on Games paper on procedural rollercoaster generation investigates Markov chains, machine learning and reinforcement learning for automatically generating coaster layouts. This supports the proposed future AI-optimization extension.

### 4.7 Modern vibration modeling
Zamora Agustí, Schilder and Kecskeméthy (2026) present advanced models incorporating 3D trajectories, nonlinear wheel-rail contact, rail irregularities, friction and elastic tracks. Their results show that vibration behavior can be strongly influenced by nonlinear contact and track elasticity. These effects are beyond the first version of the present project but provide a clear advanced-development path.

## 5. Mathematical Model
### 5.1 Potential energy
Ep = mgh

### 5.2 Kinetic energy
Ek = 1/2 mv²

### 5.3 Energy balance
For an idealized system:
mgh0 + 1/2 mv0² = mgh + 1/2 mv²

The present model adds rolling friction and aerodynamic drag as energy losses.

### 5.4 Track angle
For h=f(x):
theta = atan(dh/dx)

### 5.5 Curvature
kappa = |h''|/[1+(h')²]^(3/2)

Radius:
R = 1/kappa

### 5.6 Centripetal acceleration
an = v²/R

### 5.7 G-force
A simplified normal-load indicator is:
Gnormal ≈ cos(theta) + an/g

A resultant acceleration indicator is also calculated numerically from tangential and normal components.

### 5.8 Jerk
j = da/dt

### 5.9 Aerodynamic drag
Fd = 1/2 rho Cd A v²

### 5.10 Friction
Ff ≈ mu mg

## 6. Computational Method
1. Define a smooth track as a sampled height function.
2. Calculate slope and curvature numerically.
3. Integrate speed along the track using an energy/work balance.
4. Calculate time from ds/v.
5. Calculate acceleration from numerical derivatives.
6. Calculate centripetal acceleration from curvature.
7. Calculate G-force and jerk.
8. Export the complete trajectory as CSV.
9. Present the results in Streamlit.

## 7. Survey Method
The survey contains questions about coaster frequency, preferred features, smoothness, acceleration, G-force, perceived safety, thrill and willingness to use a simulation application. The survey should be anonymous and distributed through social media or a school-approved channel. No personally identifying information should be collected unless required by an approved research protocol.

## 8. Data Analysis
For numerical rating questions, calculate mean, median, standard deviation and response distributions. For categorical questions, calculate frequencies and percentages. Use bar charts and histograms. If enough responses are obtained, compare groups by experience level. The main exploratory comparison is between physical indicators from the simulation and preferences reported by respondents.

## 9. Limitations
The model is a simplified point-mass representation. It does not explicitly model suspension, individual wheels, nonlinear wheel-rail contact, 3D banking, structural flexibility, passenger biomechanics, track irregularity, wind variation or regulatory certification criteria. The comfort/thrill score is a project-specific research indicator and must not be presented as an official safety threshold.

## 10. Future Work
### 10.1 3D track
Represent the centerline as r(s)=[x(s),y(s),z(s)] and include banking and torsion.

### 10.2 Multibody vehicle
Model cars, bogies, wheels, suspension and rotational degrees of freedom.

### 10.3 Nonlinear wheel-rail contact
Add preload, contact stiffness, damping, creepage and friction.

### 10.4 Track elasticity and irregularity
Model the rail as an elastic beam and add measured or stochastic irregularities.

### 10.5 Sensor validation
Use smartphone/watch IMU data to compare predicted and measured acceleration.

### 10.6 AI optimization
Use genetic algorithms, particle swarm optimization or reinforcement learning to search for track layouts that maximize thrill while penalizing excessive acceleration, jerk and other constraints.

### 10.7 Digital twin
Combine real-time sensor data with the simulation to monitor a real ride and detect changes in vibration or dynamic behavior.

## 11. Conclusion
The proposed system provides a transparent bridge between introductory mechanics and modern computational roller-coaster engineering. Its strength is not that it replaces professional design software, but that it makes the relationship between geometry, energy, motion and rider experience visible and interactive. The most valuable next step is validation against measured ride data and progression toward 3D multibody and nonlinear contact modeling.

## References
1. Ambrosio, J., Viegas, M., Antunes, P., & Magalhães, H. (2017). Dynamics of a roller coaster vehicle. In *The Dynamics of Vehicles on Roads and Tracks*.
2. Golenkin, A. (2019). Dynamic time-history analysis of a structure subjected to moving loads with variable velocity, magnitude, and direction—Roller coaster design. *Structures Congress 2019*. https://doi.org/10.1061/9780784482230.024
3. Pendrill, A.-M., & Eager, D. (2020). Velocity, acceleration, jerk, snap and vibration: Forces in our bodies during a roller coaster ride. *Physics Education, 55*(6), 065012. https://doi.org/10.1088/1361-6552/aba732
4. Liu, C.-H., et al. (2021). Bridging ride and play comfort. *Information, 12*(3), 119. https://doi.org/10.3390/info12030119
5. Schuttert, W. J. (2022). *Design and Optimisation of Roller Coaster Elements using Reinforcement Learning*. University of Twente.
6. *Procedural generation of rollercoasters*. (2023). *IEEE Conference on Games*. https://doi.org/10.1109/CoG57401.2023.10333156
7. Zamora Agustí, M. G., Schilder, J., & Kecskeméthy, A. (2026). Vibrations in roller coaster systems. Part I: friction-induced self-excited oscillations. *Multibody System Dynamics, 66*, 647–687. https://doi.org/10.1007/s11044-025-10084-y
8. Zamora Agustí, M. G., Kecskeméthy, A., & Schilder, J. (2026). Vibrations in roller coaster systems. Part II: irregularity-induced oscillations and effects of track elasticity. *Multibody System Dynamics, 66*, 689–720. https://doi.org/10.1007/s11044-025-10083-z
9. Vekoma Rides Manufacturing B.V. (accessed 2026). Design and dynamic analysis information.
10. For broader motion-comfort context: studies of acceleration and jerk show that perceived comfort depends on acceleration magnitude, direction, pulse duration and jerk; these findings are useful as supporting context rather than roller-coaster-specific safety limits.
