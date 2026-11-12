import numpy as np 

def quadratic_interpolation(x,y,x_target):
  x = np.asarray(x, dtype=float)
  y = np.asarray(y, dtype=float)

  n = len(x)
  if n < 3:
    raise ValueError("At least 3 data points are required for quadratic interpolation.")
  if x_target < x[0] or x_target > x[-1]:
    raise ValueError("x_target is outside the range of x values.")

  i = np.searchsorted(x, x_target) - 1
  if i <= 1:
    indices = [0, 1, 2]
  elif i >= n - 2:
    indices = [n - 3, n - 2, n - 1]
  else:
    indices = [i - 1, i, i + 1]

  x1, x2, x3 = x[indices]
  y1, y2, y3 = y[indices]

  L1 = ((x_target - x2) * (x_target - x3)) / ((x1 - x2) * (x1 - x3))
  L2 = ((x_target - x1) * (x_target - x3)) / ((x2 - x1) * (x2 - x3))
  L3 = ((x_target - x1) * (x_target - x2)) / ((x3 - x1) * (x3 - x2))

  return L1 * y1 + L2 * y2 + L3 * y3

def interpolate_sensor_data(
    grids,
    temperatures,
    sensor_positions
):
    sensor_positions = np.asarray(sensor_positions, dtype=float)

    sensor_data = np.zeros(
        (len(temperatures), len(sensor_positions))
    )

    for j in range(len(temperatures)):

        x = grids[j]
        T = temperatures[j]

        for i, sensor_position in enumerate(sensor_positions):

            sensor_data[j, i] = quadratic_interpolation(
                x,
                T,
                sensor_position
            )

    return sensor_data


