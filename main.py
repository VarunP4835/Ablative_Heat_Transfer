import numpy as np

from config import (
    T_END,
    SENSOR_POSITIONS,
    L0
)

from mesh import (
    domain_length,
    landau_grid,
    physical_grid,
    grid_velocity,
    remap_grid
)
eta = landau_grid()
x_initial = physical_grid(0, eta)

x_final = physical_grid(T_END, eta)

L_initial = domain_length(0)

L_final = domain_length(T_END)

print("INITIAL DOMAIN")
print("-------------------------")
print("Thickness:", L_initial, "m")
print("First grid point:", x_initial[0])
print("Last grid point:", x_initial[-1])


print("\nFINAL DOMAIN")
print("-------------------------")
print("Thickness:", L_final, "m")
print("First grid point:", x_final[0])
print("Last grid point:", x_final[-1])


# Calculate grid velocities

velocity = grid_velocity(eta)

print("\nGRID VELOCITIES")
print("-------------------------")
print("Left boundary:", velocity[0], "m/s")
print("Middle point:", velocity[len(velocity)//2], "m/s")
print("Right boundary:", velocity[-1], "m/s")


print("\nSENSOR LOCATIONS")
print("-------------------------")

for x in SENSOR_POSITIONS:
    print(x, "m")


if SENSOR_POSITIONS[-1] < L_final:
    print("\nAll sensors remain inside the material.")
else:
    print("\nWarning: A sensor is outside the material.")