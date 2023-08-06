from ase.io import read as ase_read
from hilde.structure.io import inform
from hilde.spglib.wrapper import get_symmetry_dataset


def get_info_str(atoms, spacegroup=False):
    """encode atoms.info as string

    Parameters
    ----------
    atoms: ase.atoms.Atoms
        The Atoms object to get the info string for
    spacegroup: bool
        If True add space group information

    Returns
    -------
    info_strings: str
        Teh info string
    """

    info_strings = [f"Number of atoms:     {len(atoms)}"]

    if spacegroup:
        spacegroup = get_symmetry_dataset(atoms).number
        info_strings += [f"Spacegroup:          {spacegroup}"]

    for key, val in atoms.info.items():
        info_strings.append(f"{key + ':':20s} {val}")

    return info_strings


def read(fname, format="aims"):
    """wrap ase.io.read

    Parameters
    ----------
    fname: str
        The input geometry file
    format: str
        The format of the geometry file

    Returns
    -------
    atoms: ase.atoms.Atoms
        The ASE representation of the structure in fname
    """

    atoms = ase_read(fname, format=format)

    return atoms


def write(atoms, fname, format="aims", spacegroup=False, **kwargs):
    """wrap ase.io.write

    Parameters
    ----------
    atoms: ase.atoms.Atoms
        The structure to write to the file
    fname: str
        The input geometry file
    format: str
        The format of the geometry file
    spacegroup: bool
        If True add space group information

    Returns
    -------
    bool
        True if completed
    """

    if format == "aims":
        atoms.write(
            fname, info_str=get_info_str(atoms, spacegroup), format=format, **kwargs
        )

    return True
