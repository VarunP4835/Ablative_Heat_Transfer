import numpy as np

from config import (
    RHO,
    C,
    K,
    T0,
    L0,
    L_DOT,
    D_T,
    T_END,
    Q_TRUE,
    SENSOR_TIMES
)
from mesh import domain_length, landau_grid, physical_grid
from tdma import solve_tridiagonal


def solve_heat_transfer(heat_flux=Q_TRUE, dt=D_T, t_end=T_END):
    eta = landau_grid()
    N = len(eta)
    x = physical_grid(0, eta)
    T = np.full(N, T0)
    