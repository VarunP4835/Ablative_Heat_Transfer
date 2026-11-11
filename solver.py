import numpy as np

from config import (
    RHO,
    C,
    K,
    T0,
    L_DOT,
    D_T,
    T_END,
    Q_TRUE,
    SENSOR_TIMES
)
from mesh import domain_length, landau_grid, physical_grid,remap_grid
from tdma import solve_tridiagonal


def solve_heat_transfer(heat_flux=Q_TRUE, dt=D_T, t_end=T_END):
    eta = landau_grid()
    N = len(eta)
    if N < 3:
            raise ValueError("At least 3 grid nodes are required.")
    
    x = physical_grid(0.0, eta)
    T = np.full(N, T0,dtype = float)
    times = [0.0]
    temperature_history = [T.copy()]
    grid_history = [x.copy()]
    n_steps = int(round(t_end / dt))

    if not np.isclose(n_steps * dt, t_end):
            raise ValueError("t_end must be divisible by dt")
    
    sample_steps = {}
    
    for t in SENSOR_TIMES:
    
        if t <= t_end:
    
            step_index = int(round(t / dt))
    
            if not np.isclose(step_index * dt, t):
                    raise ValueError(
                        "Sensor times must align with dt"
                    )
    
            sample_steps[step_index] = t
    alpha = K / (RHO * C)
    for step in range(1,n_steps + 1):
       t_old = (step-1)*dt
       t_new = step * dt

       l_old = domain_length(t_old)
       l_new = domain_length(t_new)

       x_new = remap_grid(x, l_old, l_new)

       dx = np.diff(x_new)

       velocity = (x_new - x) / dt

       q = (heat_flux(t_old)
            if callable(heat_flux) else heat_flux)
       k = np.full(N, K)
       rho_cp = RHO * C

       lower = np.zeros(N)
       upper = np.zeros(N)
       diagonal = np.zeros(N)
       rhs = np.zeros(N)

       #Left Boundary Condition
       diagonal[0] = 1.0
       upper[0] = -1.0
       rhs[0] = 0.0

       for i in range(1, N - 1):
           dx_left = dx[i-1]
           dx_right = dx[i]

           dx_cv = 0.5 * (dx_left + dx_right)
           
           D_left = alpha / (dx_left * dx_cv)
           D_right = alpha / (dx_right * dx_cv)
           
           adv_coeff = (
                           velocity[i] * dt /
                           (dx_left + dx_right)
                       )
           
           lower[i] = -dt * D_left - adv_coeff
           
           diagonal[i] = (
                           1.0
                           + dt * D_left
                           + dt * D_right
                       )
           
           upper[i] = -dt * D_right + adv_coeff
           
           rhs[i] = T[i]

       #Right Boundary Condition
       lower[N-1] = -1.0
       diagonal[N-1] = 1.0
       rhs[N - 1] = q * dx[N - 2] / K
       T_new = solve_tridiagonal(lower, diagonal, upper, rhs)
       if np.any(np.isnan(T_new)):
           raise ValueError("NaN encountered in temperature solution at step {}".format(step))
       if not np.all(np.isfinite(T_new)):
           raise ValueError("Non-finite values encountered in temperature solution at step {}".format(step))
       T = T_new
       x = x_new
       if step in sample_steps:
              times.append(sample_steps[step])
              temperature_history.append(T.copy())
              grid_history.append(x.copy())
       if step % max(1, n_steps // 10) == 0:
      
                  print(
                      f"Time: {t_new:.2f} s | "
                      f"Thickness: {l_new * 1000:.3f} mm | "
                      f"Max temperature: {np.max(T):.2f} K"
                  )

    return np.array(times), np.array(temperature_history), np.array(grid_history)


       

       

       



       


       
