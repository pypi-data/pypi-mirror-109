"""

Submodules
==========

.. autosummary::
    :toctree: _autosummary


"""

_all_ = (
    "BusInputParameters",
    "fill_xarray_from_input_parameters",
    "modify_xarray_from_custom_parameters",
    "BusModel",
    "get_standard_driving_cycle",
    "EnergyConsumptionModel",
    "get_gradients",
    "HotEmissionsModel",
    "create_fleet_composition_from_IAM_file",
    "extract_electricity_mix_from_IAM_file",
)

# library version
__version__ = (0, 0, 3)

from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"

from .bus_input_parameters import BusInputParameters
from .array import (
    fill_xarray_from_input_parameters,
    modify_xarray_from_custom_parameters,
)
from .driving_cycles import get_standard_driving_cycle
from .gradients import get_gradients
from .energy_consumption import EnergyConsumptionModel
from .model import BusModel
from .hot_emissions import HotEmissionsModel
from .inventory import InventoryCalculation
from .utils import (create_fleet_composition_from_IAM_file, extract_electricity_mix_from_IAM_file)



