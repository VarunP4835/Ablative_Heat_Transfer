
import numpy as np

from tdma import solve_tridiagonal


# Lower diagonal
lower = np.array([0, -1, -1, -1])

# Main diagonal
diagonal = np.array([4, 4, 4, 4])

# Upper diagonal
upper = np.array([-1, -1, -1, 0])

# Right-hand side
rhs = np.array([1, 2, 3, 4])


# Solve using TDMA

x = solve_tridiagonal(
    lower,
    diagonal,
    upper,
    rhs
)

print("TDMA solution:")
print(x)


# Verify using NumPy's general solver

A = np.diag(diagonal)

A += np.diag(upper[:-1], 1)
A += np.diag(lower[1:], -1)

x_numpy = np.linalg.solve(A, rhs)

print("\nNumPy solution:")
print(x_numpy)


# Check whether both solutions match

print("\nSolutions match:",
      np.allclose(x, x_numpy))
