import numpy as np

from config import L0, L_DOT, N_NODES

def domain_length(t):
    """
    Calculate the length of the domain at time t.

    Parameters:
    t (float): Time in seconds.

    Returns:
    float: Length of the domain in meters.
    """
    L = L0 + L_DOT * t

    if L < 0:
        raise ValueError("Domain length cannot be negative. Check the time and recession rate.")

    return L


def landau_grid():
    """
    Generate a Landau grid for the simulation.

    Returns:
    np.ndarray: Array of node positions in meters.
    """
    # Create a normalized coordinate from the fixed face to the receding face.
    eta = np.linspace(0.0, 1.0, N_NODES)
    return eta


def physical_grid(t,eta):
    L = domain_length(t)
    x = eta * L
    return x


def grid_velocity(eta):
    """
    Calculate the velocity of the grid nodes at time t.

    Parameters:
    t (float): Time in seconds.
    eta (np.ndarray): Array of node positions in the Landau grid.

    Returns:
    np.ndarray: Array of velocities for each node in m/s.
    """
    v = L_DOT * eta
    return v

def remap_grid(x_old, L_old, L_new):
    """
    Remap the grid nodes based on the current time and Landau grid.

    Parameters:
    t (float): Time in seconds.
    eta (np.ndarray): Array of node positions in the Landau grid.

    Returns:
    np.ndarray: Array of remapped node positions in meters.
    """
    eta = x_old/L_old
    x_new = eta * L_new
    return x_new

    