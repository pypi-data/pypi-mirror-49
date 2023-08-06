# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['hilde',
 'hilde.WIP.statistical_sampling',
 'hilde.aims',
 'hilde.cli',
 'hilde.fireworks',
 'hilde.fireworks.tasks',
 'hilde.fireworks.tasks.fw_out',
 'hilde.fireworks.workflows',
 'hilde.green_kubo',
 'hilde.harmonic_analysis',
 'hilde.helpers',
 'hilde.helpers.sobol',
 'hilde.helpers.supercell',
 'hilde.k_grid',
 'hilde.konstanten',
 'hilde.materials_fp',
 'hilde.molecular_dynamics',
 'hilde.phono3py',
 'hilde.phonon_db',
 'hilde.phonopy',
 'hilde.relaxation',
 'hilde.scripts',
 'hilde.spglib',
 'hilde.structure',
 'hilde.tasks',
 'hilde.tdep',
 'hilde.templates',
 'hilde.templates.config_files',
 'hilde.templates.lammps',
 'hilde.templates.settings',
 'hilde.trajectory']

package_data = \
{'': ['*'],
 'hilde': ['WIP/*'],
 'hilde.WIP.statistical_sampling': ['examples/statistical_sampling/*',
                                    'tests/statistical_sampling/*'],
 'hilde.fireworks': ['.scripts/*', 'cli/*'],
 'hilde.scripts': ['run/*']}

install_requires = \
['ase>=3.18.0,<4.0.0',
 'attrs>=19.1,<20.0',
 'click>=7.0,<8.0',
 'click_completion>=0.5.1,<0.6.0',
 'matplotlib>=3.1,<4.0',
 'netCDF4>=1.5,<2.0',
 'numpy>=1.16,<2.0',
 'pandas>=0.24.2,<0.25.0',
 'phonopy>=2.1,<3.0',
 'scipy>=1.2.1,<1.3.0',
 'seekpath>=1.8.4,<2.0.0',
 'son>=0.3.2,<0.4.0',
 'spglib>=1.12,<2.0',
 'xarray>=0.12.3,<0.13.0']

extras_require = \
{'fireworks': ['fireworks>=1.9,<2.0',
               'python-gssapi>=0.6.4,<0.7.0',
               'pymongo>=3.8,<4.0',
               'fabric>=2.4,<3.0',
               'paramiko>=2.4,<3.0'],
 'phono3py': ['phono3py>=1.17,<2.0'],
 'postgresql': ['psycopg2>=2.8.0,<3.0.0'],
 'tutorial': ['seaborn>=0.9.0,<0.10.0', 'jupyter>=1.0,<2.0']}

entry_points = \
{'console_scripts': ['hilde = hilde.cli:cli']}

setup_kwargs = {
    'name': 'hilde',
    'version': '0.3.0.dev2',
    'description': 'Haber Institute Lattice Dynamics Environment',
    'long_description': 'hilde\n===\n## Installation\n\nExternal dependencies:\n\n```bash\napt-get install gfortran liblapack-dev liblapacke-dev mongodb\n```\n\nMake sure `poetry` is installed:\n```\npip install poetry\n```\n\nCreate a virtual environment\n```bash\npython3 -m venv hilde_venv\nsource hilde_venv/bin/activate\n```\n\nInstall `hilde` with `poetry`\n```bash\npoetry install\n```\n\nConfigure Hilde by creating a `~/.hilderc` configuration file in the home directory. To this end, first\n\n```\nhilde template configuration\n```\n\nand edit according to system. The `aims_command` is a command or script that takes care\nof running aims. This can be either just `mpirun aims.x`, or a script loading necessary\nmodules etc. and finally calling `srun aims.x` on a cluster.\n\nThen copy to your home folder with \n```\ncp hilderc ~/.hilderc\n```\n\n**You\'re now good to go!** Just make sure your hilde virtual environment is activated.\n\n### Autocompletion\nTo activate autocompletion of `hilde` subcommands, add this to your `.bashrc`:\n```bash\neval "$(_HILDE_COMPLETE=source hilde)"\n```\nand source it.\n\nIf you use the `fishshell`, add a file `~/.config/fish/completions/hilde.fish` containing\n```bash\neval (env _HILDE_COMPLETE=source-fish hilde)\n```\n\n### Remarks for Cluster\nOn clusters with `conda` environment, it is typically best to have a minimal base\nenvironment that holds nothing but `python`, `numpy`, and `scipy` to benefit from `mkl`\nspeedup:\n```bash\nconda create -n py37 python=3.7 numpy scipy mkl\n```\nFrom within the conda environment (`conda activate py37`), a `venv` can be created that\nholds the other dependencies. To benefit from `numpy` and `mkl`, the `venv` can be\ncreated with\n```bash\npython3 -m venv hilde_venv --system-site-packages\nsource hilde_venv/bin/activate\n```\nOne should verify that the `numpy` and `scipy` packages are indeed the ones from the\nconda environment by inspecting \n```bash\nconda list | grep numpy\n```\n within conda and\n```bash\npip list | grep numpy\n```\nwith `hilde_venv`. To enforce this, the `pyproject.toml` file\ncan be adjusted.\n\nDon\'t forget to activate `hilde_venv` before starting to work!\n\n## Settings Files\n\n`hilde` uses the Python `configparser` module for parsing settings files named\n`settings.in` and the configuration file `.hilderc`. The\nparser is augmented by `JSON` so it understands any input on the right hand side that is\nvalid `JSON`. The inputs get converted to Python objects according to [this conversion\ntable](https://realpython.com/python-json/#serializing-json).\n\n**New Features**\n* Simplified Settings Files:\n  * Settings files named `settings.in` are automatically parsed when calling\n    `Settings()` within Hilde.\n  * The configuration file `hilde.cfg` gets installed to system.\n* Molecular dynamics workflow with input and output files\n  * see hilde/examples/md\n* Phonopy workflow with input and output files\n  * see hilde/examples/phonopy\n* Relaxation workflow with config file and output files\n  * see hilde/examples/relaxation\n* YAML Trajectories:\n  * save MD trajectories as YAML with tools in `hilde.trajectories`\n  * example in `hilde/examples/trajectory/trajectory.son.ipynb`\n* Emails:\n  * send notifications via email with `hilde.helpers.notifications.send_simple_mail`\n* Watchdogs:\n  * supervise e.g. an MD to estimate when the walltime will be reached.\n    Example in `examples/md/md_with_watchdog.ipynb`\n* Wrapper for `phono3py`\n  * Preprocess and re-creation of Phono3py objects from precomputed force\n  constants, see examples\n* Wrapper for `phonopy`\n  * Preprocess and (some) postprocess, see examples\n* Templates\n  * `from hilde.templates.lammps import setup_lammps_si` to provide lammps calculator\n* Brillouin zone helpers\n  * `hilde.helpers.brillouinzone` features `get_paths`, `get_bands`, and\n  `get_labels` to provide paths in the BZ that can be fed to `phonopy` via\n  `phonon.set_bandstructure(bands)`, and\n  `phonon.plot_band_structure(labels=labels)`.\n  * These functions are used by `hilde.phonopy.plot_dos_and_bandstructure` to\n  plot DOS and bandstructure in the working directory.\n* Scripts:\n  * `make_supercell`: create supercell from supercell matrix or\n  target target\n  * `geometry_info`: print geometry information for given input\n  structure\n* Symmetry Block Generation Functions\n  * `AtomsInput`: A storage class that stores relevant information about a structure\n  * `write_sym_constraints_geo`: Read any geometry.in file and use the list of `AtomInputs`\n  to create a new supercell with a user defined symmetry block added to it\n* FireWorks integration\n  * Functions that can be used with PyTask to use FireWorks as a job manager\n  * Jobs can now be submitted to the queue from a local machine and have the results processed locally\n\n\n**Setup of FireWorks on Computational Resources**\n\nSee also: `doc/README_FHI_FireWorksConnections.md`\n* Overview of Managing FireWorks Remotely\n  * FireWorks does not copy functions but only finds them in the PYTHONPATH\n  * To pass it functions give it the function_module.function_name as a str\n  * Functions that are run on the local machine\n    * All functions/files that set up FireWorks\n      * All scripts that initially call hilde.fireworks.tasks.generate_firework\n      * .cfg Files that define the steps (if used)\n      * All functions used by a Fireworks without a task that calls a function in task2queue list\n    * claunch_hilde and associated functions\n  * Function that are run on the remote machine\n    * All functions used by a Firework with a task that calls a function in task2queue\n    * qluanch_hilde and associated functions\n  * Functions that can run on both machines\n    * All FireWorks API functions\n    * All database accessors functions\n    * Spec modifying functions (hilde.fireworks.tasks.fw_action_outs)\n    * hilde.fireworks.tasks.generate_firework\n  * Machine specific settings such as the aims_command is handled dynamically\n    * It automatically changes when called on a machine\n    * Can always use local settings without an issue\n* Prerequisites for using FireWorks\n  * Fabric 2 (for remote connections)\n  * paramiko (used by Fabric 2)\n  * python-gssapi (for gss authorization)\n  * pymongo\n* Using FireWorks on the clusters\n  * Download/clone from https://github.com/materialsproject/fireworks.git and move the FireWorks directory\n  * Modify fw\\_tutorials/worker/my\\_fworker.yaml and copy it to $HOME/.fireworks\n    * Probably do not need to do any modifications if running on similar environments\n    * Useful if you want to run specific jobs on specific machines without specified reservations\n  * Modify fw\\_tutorials/worker/my\\_launchpad.yaml and copy it to $HOME/.fireworks\n    * host: Host to the DB server\n      * If connected through an ssh tunnel use localhost\n    * port: Port the DB server is listening on\n      * If connected through an ssh tunnel use the port connected the DB server via the tunnel\n    * username: username used to access the database\n    * password: password used to access the database\n    * logdir: default directory to store logs\n    * strm_lvl: How much information the launchpad prints by default\n  * Modify the correct fw\\_tutorials/queue\\_???.yaml file for your submission system and copy it to $HOME/.fireworks/my\\_qadapter.yaml\n    * Only used on clusters\n    * Set to minimal queue defaults\n      * nodes = 1\n      * ntasks_per_node = 32\n      * walltime = "00:30:00"\n      * queue = "express"\n      * logdir = /some/path/that/must/exist (make sure this exists)\n  * Find the FireWorks install directory with lpad version and modify\n    $FW_INSTALL_DIR/fireworks/fw_config.py:\n    * LAUNCHPAD_LOC: $HOME/.fireworks/my_launchpad.yaml\n    * FWORKER_LOC: $HOME/.fireworks/my_fworker.yaml\n    * QUEUEADAPTER_LOC: $HOME/.fireworks/my_qadapter.yaml\n* Setup a MongoDB database for fireworks\n  * Best to have it always accessible by all machines that need it\n  * Check with the cluster management on what solution they\'d prefer\n* Connections between computers\n  * Passwordless connections are preferred\n  * If this is not possible you can pass the password as a command line argument, (delete\n    bash history afterwards)\n* FireWorks Etiquette\n  * Name all Fireworks/WorkFlows\n  * If you are using a shared launchpad only use lpad reset if everyone is okay with that\n',
    'author': 'Florian Knoop',
    'author_email': 'knoop@fhi-berlin.mpg.de',
    'url': 'https://gitlab.com/flokno/hilde',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
