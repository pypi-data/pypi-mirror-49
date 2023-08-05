"""
multi-objective optimization of supply systems for the CEA
"""

from __future__ import print_function
from __future__ import division

import os
import pandas as pd
import cea.config
import cea.globalvar
import cea.inputlocator
from cea.optimization.prices import Prices as Prices
from cea.optimization.distribution.network_optimization_features import NetworkOptimizationFeatures
from cea.optimization.master import master_main
from cea.optimization.preprocessing.preprocessing_main import preproccessing
from cea.optimization.lca_calculations import LcaCalculations
import cea.optimization.preprocessing.processheat as process_heat
from cea.optimization.preprocessing import electricity

__author__ = "Jimeno A. Fonseca"
__copyright__ = "Copyright 2016, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Thuy-an Ngugen", "Jimeno A. Fonseca", "Sreepathi Bhargava Krishna"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "thomas@arch.ethz.ch"
__status__ = "Production"


# optimization

def moo_optimization(locator, weather_file, gv, config):
    '''
    This function optimizes the conversion, storage and distribution systems of a heating distribution for the case
    study. It requires that the energy demand, technology potential and thermal networks are simulated, as follows:

        - energy demand simulation: run cea/demand/demand_main.py
        - PV potential: run cea/technologies/solar/photovoltaic.py
        - PVT potential: run cea/technologies/solar/photovoltaic_thermal.py
        - flat plate solar collector potential: run cea/technologies/solar/solar_collector.py with
          config.solar.type_scpanel = 'FP'
        - evacuated tube solar collector potential: run cea/technologies/solar/solar_collector.py with
          config.solar.type_scpanel = 'ET'
        - waste water heat recovery: run cea/resources/sewage_heat_exchanger.py
        - lake water potential: run cea/resources/lake_potential.py
        - thermal network simulation: run cea/technologies/thermal_network/thermal_network.py
          if no network is currently present in the case study, consider running network_layout/main.py first
        - decentralized building simulation: run cea/optimization/preprocessing/decentralized_building_main.py

    :param locator: path to input locator
    :param weather_file: path to weather file
    :param gv: global variables class
    :type locator: cea.inputlocator.InputLocator
    :type weather_file: string
    :type gv: class

    :returns: None
    :rtype: Nonetype
    '''

    # read total demand file and names and number of all buildings
    total_demand = pd.read_csv(locator.get_total_demand())
    building_names = total_demand.Name.values
    gv.num_tot_buildings = total_demand.Name.count()
    lca = LcaCalculations(locator, config.detailed_electricity_pricing)
    prices = Prices(locator, config)

    # pre-process information regarding resources and technologies (they are treated before the optimization)
    # optimize best systems for every individual building (they will compete against a district distribution solution)
    print("PRE-PROCESSING")
    solar_features = preproccessing(locator, total_demand, building_names, weather_file, gv, config, prices, lca)

    # optimize the distribution and linearize the results(at the moment, there is only a linearization of values in Zug)
    print("NETWORK OPTIMIZATION")
    network_features = NetworkOptimizationFeatures(config, locator)

    # optimize conversion systems
    print("CONVERSION AND STORAGE OPTIMIZATION")
    master_main.non_dominated_sorting_genetic_algorithm(locator, building_names, solar_features,
                                                        network_features, gv, config, prices, lca)

    print("GETTING EXTRA COSTS AND EMISSIONS FROM ELECTRICITY")
    extra_costs_emissions_primary_energy(building_names, config, lca, locator, prices, total_demand)


def extra_costs_emissions_primary_energy(building_names, config, lca, locator, prices, total_demand):
    # GET EXTRAS
    # estimate the extra costs, emissions and primary energy of electricity.
    print
    "electricity"
    elecCosts, elecCO2, elecPrim = electricity.calc_pareto_electricity(locator, lca, config, building_names)
    # estimate the extra costs, emissions and primary energy for process heat
    print
    "Process-heat"
    hpCosts, hpCO2, hpPrim = process_heat.calc_pareto_Qhp(locator, total_demand, prices, lca, config)

    extraCosts = elecCosts + hpCosts
    extraCO2 = elecCO2 + hpCO2
    extraPrim = elecPrim + hpPrim

    # Capex_a and Opex_fixed
    results = pd.DataFrame({"elecCosts": [elecCosts],
                            "hpCosts": [hpCosts],
                            "elecCO2": [elecCO2],
                            "hpCO2": [hpCO2],
                            "elecPrim": [elecPrim],
                            "hpPrim": [hpPrim],
                            "extraCosts": [extraCosts],
                            "extraCO2":[extraCO2],
                            "extraPrim": [extraPrim]
                            })
    results.to_csv(locator.get_preprocessing_costs(), index=False)


# ============================
# test
# ============================


def main(config):
    """
    run the whole optimization routine
    """
    gv = cea.globalvar.GlobalVariables()
    locator = cea.inputlocator.InputLocator(scenario=config.scenario)
    weather_file = config.weather

    try:
        check_input_files(config, locator)
    except ValueError as err:
        import sys
        print(err.message)
        sys.exit(1)

    print(config.optimization.initialind)
    moo_optimization(locator=locator, weather_file=weather_file, gv=gv, config=config)

    print('test_optimization_main() succeeded')


def check_input_files(config, locator):
    """
    Raise a ``ValueError`` if any of the required input files are missing.
    :param cea.config.Configuration config: The config object to use
    :param cea.config.InputLocator locator: The input locator to use
    :return: None
    """
    if not demand_files_exist(locator):
        raise ValueError("Missing demand data of the scenario. Consider running demand script first.")
    if not os.path.exists(locator.get_total_demand()):
        raise ValueError("Missing total demand of the scenario. Consider running demand script first.")
    if not os.path.exists(locator.PV_totals()):
        raise ValueError("Missing PV potential of the scenario. Consider running photovoltaic script first.")
    if config.district_heating_network:
        if not os.path.exists(locator.PVT_totals()):
            raise ValueError(
                "Missing PVT potential of the scenario. Consider running photovoltaic-thermal script first.")
    if not os.path.exists(locator.SC_totals(panel_type='FP')):
        raise ValueError(
            "Missing SC potential of panel type 'FP' of the scenario. Consider running solar-collector script first with panel_type as FP and t-in-SC as 75")
    if not os.path.exists(locator.SC_totals(panel_type='ET')):
        raise ValueError(
            "Missing SC potential of panel type 'ET' of the scenario. Consider running solar-collector script first with panel_type as ET and t-in-SC as 150")
    if not os.path.exists(locator.get_sewage_heat_potential()):
        raise ValueError(
            "Missing sewage potential of the scenario. Consider running sewage heat exchanger script first.")
    if not os.path.exists(locator.get_lake_potential()):
        raise ValueError("Missing lake potential of the scenario. Consider running lake potential script first.")
    if not os.path.exists(locator.get_thermal_network_edge_list_file(config.thermal_network.network_type, '')):
        raise ValueError(
            "Missing thermal network simulation results. Consider running thermal network simulation script first.")


def demand_files_exist(locator):
    """verify that the necessary demand files exist"""
    return all(os.path.exists(locator.get_demand_results_file(building_name)) for building_name in
               locator.get_zone_building_names())


if __name__ == '__main__':
    main(cea.config.Configuration())
