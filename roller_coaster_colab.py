# 🎢 Roller Coaster Dynamics Lab — Google Colab

## 1. Install/import packages
!pip -q install numpy pandas matplotlib plotly

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from physics_model import default_track, simulate_coaster, summary, score_ride

## 2. Generate a track
x, h = default_track()
df = simulate_coaster(x, h, mass=5000, v0=5, friction=0.008, cd=0.55, area=8)

## 3. Results
print(summary(df))
print(score_ride(df))

## 4. Track
plt.figure(figsize=(14,5))
plt.plot(df.x_m, df.height_m)
plt.xlabel("Distance (m)")
plt.ylabel("Height (m)")
plt.title("Roller Coaster Track")
plt.grid()
plt.show()

## 5. Speed
plt.figure(figsize=(14,5))
plt.plot(df.x_m, df.velocity_km_h)
plt.xlabel("Distance (m)")
plt.ylabel("Speed (km/h)")
plt.title("Velocity Profile")
plt.grid()
plt.show()

## 6. G-force
plt.figure(figsize=(14,5))
plt.plot(df.x_m, df.g_resultant)
plt.xlabel("Distance (m)")
plt.ylabel("G")
plt.title("Resultant G-force")
plt.grid()
plt.show()

## 7. Jerk
plt.figure(figsize=(14,5))
plt.plot(df.x_m, df.jerk_m_s3)
plt.xlabel("Distance (m)")
plt.ylabel("Jerk (m/s³)")
plt.title("Jerk Profile")
plt.grid()
plt.show()

## 8. Save results
df.to_csv("coaster_simulation_results.csv", index=False)
