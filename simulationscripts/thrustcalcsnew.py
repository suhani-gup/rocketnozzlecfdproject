import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Read data with raw string for file path
df = pd.read_excel(r"C:\Users\suhan\OneDrive\Desktop\penngineer!\fun projects\nozzles\nozzle_data.xlsx")

# Calculate thrust for each row and add a new column
def calc_thrust(row):
    mdot = row['Mdot (kg/s)']
    Ve = row['Ve (m/s)']
    Pe = row['Pe (Pa)']
    Pa = row['Ambient Pressure (Pa)']
    Ae = row['Exit Area']  # Numeric value directly
    return mdot * Ve + (Pa - Pe) * Ae

df['Thrust (N)'] = df.apply(calc_thrust, axis=1)

# ---- Desired nozzle order ----
nozzle_types = ['Conical', 'CD', 'Rao']
x_pos = np.arange(len(nozzle_types))

# ---- Plot 1: Geometry vs Thrust at 0 km ----
df_0km = df[df['Altitude (km)'] == 0]

y_thrust_0km = []
for nt in nozzle_types:
    val = df_0km[df_0km['Nozzle Type'] == nt]['Thrust (N)'].values
    y_thrust_0km.append(val[0] if len(val) > 0 else np.nan)

plt.figure(figsize=(8, 5))
plt.scatter(x_pos, y_thrust_0km, color='blue', s=100)
plt.xticks(x_pos, nozzle_types)
plt.title('Geometry vs Thrust at Sea Level (0 km)')
plt.xlabel('Nozzle Geometry')
plt.ylabel('Thrust (N)')
plt.grid(True)
plt.show()

# ---- Plot 2: Geometry vs Thrust at 0, 10, 20 km ----
plt.figure(figsize=(10, 6))

altitudes = [0, 10, 20]
colors = ['blue', 'green', 'red']

for alt, color in zip(altitudes, colors):
    df_alt = df[df['Altitude (km)'] == alt]
    y_thrust = []
    for nt in nozzle_types:
        val = df_alt[df_alt['Nozzle Type'] == nt]['Thrust (N)'].values
        y_thrust.append(val[0] if len(val) > 0 else np.nan)
    plt.scatter(x_pos, y_thrust, label=f'{alt} km', color=color, s=80)
    plt.plot(x_pos, y_thrust, color=color, linestyle='--', alpha=0.7)

plt.xticks(x_pos, nozzle_types)
plt.title('Geometry vs Thrust at Different Altitudes')
plt.xlabel('Nozzle Geometry')
plt.ylabel('Thrust (N)')
plt.legend()
plt.grid(True)
plt.show()

# ---- Export summary CSV ----
target_folder = r"C:\Users\suhan\OneDrive\Desktop\penngineer!\fun projects\nozzles"
file_name = 'nozzle_thrust_comparison.csv'
full_path = os.path.join(target_folder, file_name)

summary = df.groupby(['Altitude (km)', 'Nozzle Type'])['Thrust (N)'].mean().reset_index()
pivot_summary = summary.pivot(index='Altitude (km)', columns='Nozzle Type', values='Thrust (N)')
pivot_summary = pivot_summary[nozzle_types]  # Ensure columns follow desired order
pivot_summary.to_csv(full_path)

print(f"Summary CSV saved at: {full_path}")