"""
Pre-processing algorithm

"""

from __future__ import division

import os
import cea.config
import cea.globalvar
import cea.inputlocator
import pandas as pd
import numpy as np

from cea.optimization.master import summarize_network
from cea.technologies import substation

from cea.resources.geothermal import calc_ground_temperature
from cea.optimization.constants import Z0
from cea.utilities import epwreader
import cea.optimization.preprocessing.processheat as process_heat
from cea.optimization.preprocessing import electricity

__author__ = "Jimeno A. Fonseca"
__copyright__ = "Copyright 2017, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Jimeno A. Fonseca", "Thuy-An Nguyen", "Tim Vollrath", "Sreepathi Bhargava Krishna"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "thomas@arch.ethz.ch"
__status__ = "Production"


def preproccessing(locator, total_demand, weather_file, config):
    """
    This function aims at preprocessing all data for the optimization.

    :param locator: path to locator function
    :param total_demand: dataframe with total demand and names of all building in the area
    :param building_names: dataframe with names of all buildings in the area
    :param weather_file: path to wather file
    :param gv: path to global variables class
    :type locator: class
    :type total_demand: list
    :type building_names: list
    :type weather_file: string
    :type gv: class
    :return:
        - extraCosts: extra pareto optimal costs due to electricity and process heat (
            these are treated separately and not considered inside the optimization)
        - extraCO2: extra pareto optimal emissions due to electricity and process heat (
            these are treated separately and not considered inside the optimization)
        - extraPrim: extra pareto optimal primary energy due to electricity and process heat (
            these are treated separately and not considered inside the optimization)
        - solar_features: extraction of solar features form the results of the solar technologies
            calculation.

    :rtype: float, float, float, float

    """

    # local variables
    network_depth_m = Z0
    district_heating_network = config.optimization.district_heating_network
    district_cooling_network = config.optimization.district_cooling_network

    print("PRE-PROCESSING 1/2: weather properties")
    T_ambient = epwreader.epw_reader(weather_file)['drybulb_C']
    ground_temp = calc_ground_temperature(locator, config, T_ambient, depth_m=network_depth_m)

    print("PRE-PROCESSING 2/2: thermal networks")  # at first estimate a distribution with all the buildings connected
    if district_heating_network:
        buildings_names_connected = get_building_names_with_load(total_demand, load_name='QH_sys_MWhyr')
        if len(buildings_names_connected) <= 1:
            raise Exception(
                "There is just one or zero buildings with heating load, a district heating network will not work,"
                "CEA can not continue")
        num_tot_buildings = len(buildings_names_connected)

        substation.substation_main_heating(locator, total_demand, buildings_names_connected,
                                           DHN_barcode = "all")

        summarize_network.network_main(locator, buildings_names_connected,
                                       ground_temp, num_tot_buildings, "DH",
                                       "all", "all")  # "_all" key for all buildings
    if district_cooling_network:
        buildings_names_connected = get_building_names_with_load(total_demand, load_name='QC_sys_MWhyr')
        if len(buildings_names_connected) <= 1:
            raise Exception(
                "There is just one or zero buildings with a cooling load, a district coooling network will not work,"
                "CEA can not continue")

        num_tot_buildings = len(buildings_names_connected)
        substation.substation_main_cooling(locator, total_demand, buildings_names_connected,
                                           DCN_barcode = "all")

        summarize_network.network_main(locator, buildings_names_connected,
                                       ground_temp, num_tot_buildings, "DC", "all", "all")  # "_all" key for all buildings


    return


def get_building_names_with_load(total_demand, load_name):
    building_names = total_demand.Name.values
    buildings_names_connected = []
    for building in building_names:
        demand = total_demand[total_demand['Name'] == building].loc[:, load_name].values[0]
        if demand > 0.0:
            buildings_names_connected.append(building)
    return buildings_names_connected




# ============================
# test
# ============================


def main(config):
    """
    run the whole preprocessing routine
    """
    gv = cea.globalvar.GlobalVariables()
    locator = cea.inputlocator.InputLocator(scenario=config.scenario)
    total_demand = pd.read_csv(locator.get_total_demand())
    building_names = locator.get_building_names()
    weather_file = config.weather
    preproccessing(locator, total_demand, building_names, weather_file, gv, config)

    print 'test_preprocessing_main() succeeded'


if __name__ == '__main__':
    main(cea.config.Configuration())
