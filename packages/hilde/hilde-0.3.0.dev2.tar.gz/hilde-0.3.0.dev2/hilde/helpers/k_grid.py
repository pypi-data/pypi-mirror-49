""" Helpers for working with kpoint densites """

import numpy as np
from hilde.helpers.utils import talk


def d2k(atoms, kptdensity=3.5, even=True):
    """[ase.calculators.calculator.kptdensity2monkhorstpack] Convert k-point density to Monkhorst-Pack grid size.

    Parameters
    ----------
    atoms: Atoms object
        Contains unit cell and information about boundary conditions.
    kptdensity: float or list of floats
        Required k-point density.  Default value is 3.5 point per Ang^-1.
    even: bool
        Round up to even numbers.

    Returns
    -------
    list
        Monkhorst-Pack grid size in all directions
    """
    recipcell = atoms.get_reciprocal_cell()
    return d2k_cellinfo(recipcell, atoms.pbc, kptdensity, even)


def d2k_cellinfo(recipcell, pbc, kptdensity=3.5, even=True):
    """Convert k-point density to Monkhorst-Pack grid size.

    Parameters
    ----------
    recipcell: ASE Cell object
        The reciprocal cell
    pbc: list of Bools
        If element of pbc is True then system is periodic in that direction
    kptdensity: float or list of floats
        Required k-point density.  Default value is 3.5 point per Ang^-1.
    even: bool
        Round up to even numbers.

    Returns
    -------
    list
        Monkhorst-Pack grid size in all directions
    """
    if not isinstance(kptdensity, list) and not isinstance(kptdensity, np.ndarray):
        kptdensity = 3 * [float(kptdensity)]
    kpts = []
    for i in range(3):
        if pbc[i]:
            k = 2 * np.pi * np.sqrt((recipcell[i] ** 2).sum()) * float(kptdensity[i])
            if even:
                kpts.append(2 * int(np.ceil(k / 2)))
            else:
                kpts.append(int(np.ceil(k)))
        else:
            kpts.append(1)
    return kpts


def k2d(atoms, k_grid=[2, 2, 2]):
    """Generate the kpoint density in each direction from given k_grid.

    Parameters
    ----------
    atoms: Atoms
        Atoms object of interest.
    k_grid: list
        k_grid that was used.

    Returns
    -------
    np.ndarray
        The density of kpoints in each direction. Use result.mean() to compute average kpoint density.
    """

    recipcell = atoms.get_reciprocal_cell()
    densities = k_grid / (2 * np.pi * np.sqrt((recipcell ** 2).sum(axis=1)))
    return np.array(densities)


def update_k_grid(atoms, calc, kptdensity, even=True):
    """Update the k_grid in calc with the respective density

    Parameters
    ----------
    atoms: ase.atoms.Atoms
        structure that the calculator is attached to
    calc: ase.calculators.calulator.Calculator
        The calculator
    kptdensity: list of floats
        desired k-point density in all directions
    even: bool
        If True k-grid must be even

    Returns
    -------
    calc: ase.calculators.calulator.Calculator
        The calculator with updated kgrid
    """

    k_grid = d2k(atoms, kptdensity, even)

    if calc.name == "aims":
        talk(f"Update aims k_grid with kpt density of {kptdensity} to {k_grid}")
        calc.parameters["k_grid"] = k_grid
    return calc


def update_k_grid_calc_dict(calc_dict, recipcell, pbc, kptdensity, even=True):
    """Update the k_grid in dictionary representation of a calculator with the respective density

    Parameters
    ----------
    calc_dict: dict
        Dictionary representation of calc
    recipcell: np.ndarray
        The reciprocal lattice
    pbc: list of bool (len=3)
        True if preodic in that direction
    kptdensity: list of floats
        Desired k-point density in all directions
    even: bool
        If True k-grid must be even

    Returns
    -------
    calc_dict: dict
        The dictionary representation of the calculator with an updated kgrid
    """
    k_grid = d2k_cellinfo(recipcell, pbc, kptdensity, even)

    calc_dict["calculator_parameters"]["k_grid"] = k_grid
    return calc_dict
