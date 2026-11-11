import numpy as np

def solve_tridiagonal(lower,diagonal,upper,rhs):
  lower = np.asarray(lower, dtype=float)
  diagonal = np.asarray(diagonal, dtype=float)
  upper = np.asarray(upper, dtype=float)
  rhs = np.asarray(rhs, dtype=float)

  n = len(diagonal)
  if not(
    len(lower) == n and len(upper) == n and len(rhs) == n): raise ValueError("All input arrays must have the same length.")
  if(n==0): raise ValueError("Input arrays must not be empty.")

  c_prime = np.zeros(n)
  d_prime = np.zeros(n)
  c_prime[0] = upper[0] / diagonal[0]
  d_prime[0] = rhs[0] / diagonal[0]
  for i in range(1, n):
    denominator = diagonal[i] - lower[i] * c_prime[i-1]
    if abs(denominator) < 1e-12:
            raise ValueError("Zero pivot encountered")

    if i < n - 1:
            c_prime[i] = upper[i] / denominator

    d_prime[i] = (
            rhs[i] -
            lower[i] * d_prime[i - 1]
        )/denominator
  x = np.zeros(n)

  x[n-1] = d_prime[n-1]

  for i in range(n - 2, -1, -1):

        x[i] = (
            d_prime[i] -
            c_prime[i] * x[i + 1]
        )

  return x