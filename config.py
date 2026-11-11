# Physical Properties

RHO = 2250.0 # Density of the material in kg/m^3
C = 707.7 # Specific heat capacity in J/(kg*K)
K = 24.0 # Thermal conductivity in W/(m*K)

L0 = 0.05 # Initial length of the material in meters
T0 = 300.0 # Initial temperature in Kelvin

Q_TRUE = 1e6 # heat flux (W/m^2)

L_DOT = -7.5545e-5 # surface recession rate (m/s)

T_END = 100.0 # End time for the simulation in seconds

D_T = 0.25 # Time step for the simulation in seconds

N_NODES = 101

SENSOR_POSITIONS = [0.000, 0.005, 0.010, 0.015, 0.020, 0.025, 0.030, 0.035, 0.040] # Positions of sensors in meters

SENSOR_TIMES = [0, 20, 40, 60, 80, 100] # Times at which sensors record data