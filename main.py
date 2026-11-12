import numpy as np
import matplotlib.pyplot as plt
import csv
from solver import solve_heat_transfer
from config import SENSOR_POSITIONS
from interpolation import interpolate_sensor_data


times, temperatures, grids = solve_heat_transfer()

sensor_temperatures = interpolate_sensor_data(
    grids,
    temperatures,
    SENSOR_POSITIONS
)
with open("output/sensor_data.csv", "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow([
        "time",
        "position",
        "temperature"
    ])

    for j, t in enumerate(times):

        for i, position in enumerate(SENSOR_POSITIONS):

            writer.writerow([
                t,
                position,
                sensor_temperatures[j, i]
            ])


print("\nSENSOR TEMPERATURE DATA")

for j, t in enumerate(times):

    print(f"\nTime = {t:.0f} s")

    for i, position in enumerate(SENSOR_POSITIONS):

        print(
            f"Sensor at {position * 1000:.1f} mm: "
            f"{sensor_temperatures[j, i]:.2f} K"
        )

print("\nTEMPERATURE RESULTS")

for j, t in enumerate(times):

    print(f"\nTime = {t:.2f} seconds")

    print(
        "Minimum temperature:",
        temperatures[j].min()
    )

    print(
        "Maximum temperature:",
        temperatures[j].max()
    )



plt.figure(figsize=(9, 6))

for j, t in enumerate(times):

    plt.plot(
        grids[j] * 1000,
        temperatures[j],
        label=f"t = {t:.0f} s"
    )

plt.xlabel("Position (mm)")

plt.ylabel("Temperature (K)")

plt.title("Temperature Distribution During Ablation")

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.savefig("output/temperature_profiles.png")

plt.show()


plt.figure(figsize=(9, 6))

for j, t in enumerate(times):

    plt.scatter(
        grids[j] * 1000,
        np.full(len(grids[j]), t),
        s=5,
        label=f"t = {t:.0f} s"
    )

plt.xlabel("Position (mm)")

plt.ylabel("Time (s)")

plt.title("Moving Computational Grid")

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.savefig("output/moving_grid.png")

plt.show()
