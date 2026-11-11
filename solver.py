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
from mesh import domain_length, landau_grid, physical_grid,remap_grid
from tdma import solve_tridiagonal


def solve_heat_transfer(heat_flux=Q_TRUE, dt=D_T, t_end=T_END):
    eta = landau_grid()
    N = len(eta)
    x = physical_grid(0, eta)
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

           dx_cv = 0.5*(dx_left + dx_right)

           D = dx_left*0.5 + dx_cv + dx_right*0.5

           R_right = (
               dx_cv / (2.0*k[i])
               + dx_right / (2.0*k[i+1])
           )
           R_left = (
               dx_cv / (2.0*k[i])
               + dx_left / (2.0*k[i-1])
           )
           C_right = dt/(rho_cp * R_right)
           C_left = dt/(rho_cp * R_left)

           S = velocity[i]*dt/ D

           lower[i] = S-C_left
           diagonal[i] = 1.0 + C_left + C_right
           upper[i] = -S-C_right
           rhs[i] = T[i]

    #Right Boundary Condition
       lower[N-1] = -1.0
       diagonal[N-1] = 1.0
       rhs[N-1] = (q*dx[N-1]/k[N-2])
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


       

       

       



       


       
