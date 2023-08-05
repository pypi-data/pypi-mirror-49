# -*- coding: utf-8 -*-
"""

storage sizing

This script sizes the storage and in a second part, it will plot the results of iteration.
Finally, the storage operation is performed with the parameters found in the storage optimization
All results are saved in the folder of "locator.get_optimization_slave_results_folder()".
- Data_with_Storage_applied.csv : Hourly Operation of Storage, especially Q_missing and E_aux is important for further usage
- Storage_Sizing_Parameters.csv : Saves the parameters found in the storage optimization
IMPORTANT : Storage is used for solar thermal energy ONLY!
It is possible to turn off the plots by setting Tempplot = 0 and Qplot = 0
"""
from __future__ import division

save_file = 1

import numpy as np
import pandas as pd
import cea.optimization.slave.seasonal_storage.design_operation as StDesOp
from cea.constants import HEAT_CAPACITY_OF_WATER_JPERKGK, DENSITY_OF_WATER_AT_60_DEGREES_KGPERM3, WH_TO_J

__author__ = "Tim Vollrath"
__copyright__ = "Copyright 2015, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Tim Vollrath", "Thuy-An Nguyen", "Jimeno A. Fonseca"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "thomas@arch.ethz.ch"
__status__ = "Production"


def storage_optimization(locator, master_to_slave_vars, lca, prices, config):
    """
    This function performs the storage optimization and stores the results in the designated folders
    :param locator: locator class
    :param master_to_slave_vars: class MastertoSlaveVars containing the value of variables to be passed to the slave optimization
    for each individual
    :param gv: global variables class
    :type locator: class
    :type master_to_slave_vars: class
    :type gv: class
    :return: The function saves all files when it's done in the location locator.get_potentials_solar_folder()
    :rtype: Nonetype
    """
    print "Storage Optimization Ready"
    MS_Var = master_to_slave_vars

    CSV_NAME = MS_Var.network_data_file_heating

    # Initiating
    costs_storage_USD = 0
    GHG_storage_tonCO2 = 0
    PEN_storage_MJoil = 0

    # SOLCOL_TYPE = MS_Var.SOLCOL_TYPE
    SOLCOL_TYPE = "NONE"
    T_storage_old = MS_Var.T_storage_zero
    Q_in_storage_old = MS_Var.Q_in_storage_zero
    Tempplot = 0
    Qplot = 0

    # start with initial size:
    T_ST_MAX = MS_Var.T_ST_MAX
    T_ST_MIN = MS_Var.T_ST_MIN

    # initial storage size
    V_storage_initial = MS_Var.STORAGE_SIZE
    V0 = V_storage_initial
    STORE_DATA = "yes"
    Q_stored_max0, Q_rejected_fin, Q_disc_seasonstart, T_st_max, T_st_min, Q_storage_content_fin, T_storage_fin, Q_loss0, mdot_DH_fin0, \
    Q_uncontrollable_fin = StDesOp.Storage_Design(CSV_NAME, SOLCOL_TYPE, T_storage_old, Q_in_storage_old, locator,
                                                  V_storage_initial, STORE_DATA, master_to_slave_vars, 1e12, config)

    # Design HP for storage uptake - limit the maximum thermal power, Criterial: 2000h operation average of a year
    # --> Oral Recommandation of Antonio (former Leibundgut Group)
    P_HP_max = np.sum(Q_uncontrollable_fin) / 2000.0
    # second Round optimization

    # Start optimizing the storage

    # first Round optimization
    V_storage_possible_needed = (Q_stored_max0 + Q_loss0) * WH_TO_J / (DENSITY_OF_WATER_AT_60_DEGREES_KGPERM3 * HEAT_CAPACITY_OF_WATER_JPERKGK * (T_ST_MAX - T_ST_MIN))
    V1 = V_storage_possible_needed
    Q_initial = min(Q_stored_max0 / 2.0, Q_storage_content_fin[-1])
    T_initial = T_ST_MIN + Q_initial * WH_TO_J / (DENSITY_OF_WATER_AT_60_DEGREES_KGPERM3 * HEAT_CAPACITY_OF_WATER_JPERKGK * V_storage_initial)

    # assume unlimited uptake to storage during first round optimisation (P_HP_max = 1e12)
    STORE_DATA = "yes"
    Optimized_Data = StDesOp.Storage_Design(CSV_NAME, SOLCOL_TYPE, T_initial, Q_initial, locator,
                                            V_storage_possible_needed, STORE_DATA, master_to_slave_vars, P_HP_max, config)
    Q_stored_max_opt, Q_rejected_fin_opt, Q_disc_seasonstart_opt, T_st_max_op, T_st_min_op, Q_storage_content_fin_op, \
    T_storage_fin_op, Q_loss1, mdot_DH_fin1, Q_uncontrollable_fin = Optimized_Data

    # Design HP for storage uptake - limit the maximum thermal power, Criterial: 2000h operation average of a year
    # --> Oral Recommandation of Antonio (former Leibundgut Group)
    P_HP_max = np.sum(Q_uncontrollable_fin) / 2000.0

    InitialStorageContent = float(Q_storage_content_fin_op[0])
    FinalStorageContent = float(Q_storage_content_fin_op[-1])
    # second Round optimization
    if InitialStorageContent == 0 or FinalStorageContent == 0:  # catch error in advance of having 0 / 0
        storageDeviation1 = 0
    else:
        storageDeviation1 = (abs(InitialStorageContent - FinalStorageContent) / FinalStorageContent)

    if storageDeviation1 > 0.0001:

        Q_stored_max_needed = np.amax(Q_storage_content_fin_op) - np.amin(Q_storage_content_fin_op)
        V_storage_possible_needed = Q_stored_max_needed * WH_TO_J / (DENSITY_OF_WATER_AT_60_DEGREES_KGPERM3 * HEAT_CAPACITY_OF_WATER_JPERKGK * (T_ST_MAX - T_ST_MIN))
        V2 = V_storage_possible_needed
        Q_initial = min(Q_disc_seasonstart_opt[0], Q_storage_content_fin_op[-1])
        T_initial = T_ST_MIN + Q_initial * WH_TO_J / (DENSITY_OF_WATER_AT_60_DEGREES_KGPERM3 * HEAT_CAPACITY_OF_WATER_JPERKGK * V_storage_possible_needed)
        Optimized_Data2 = StDesOp.Storage_Design(CSV_NAME, SOLCOL_TYPE, T_initial, Q_initial, locator,
                                                 V_storage_possible_needed, STORE_DATA, master_to_slave_vars, P_HP_max, config)
        Q_stored_max_opt2, Q_rejected_fin_opt2, Q_disc_seasonstart_opt2, T_st_max_op2, T_st_min_op2, \
        Q_storage_content_fin_op2, T_storage_fin_op2, Q_loss2, mdot_DH_fin2, \
        Q_uncontrollable_fin = Optimized_Data2

        InitialStorageContent = float(Q_storage_content_fin_op2[0])
        FinalStorageContent = float(Q_storage_content_fin_op2[-1])
        # second Round optimization
        if InitialStorageContent == 0 or FinalStorageContent == 0:  # catch error in advance of having 0 / 0
            storageDeviation2 = 0
        else:
            storageDeviation2 = (abs(InitialStorageContent - FinalStorageContent) / FinalStorageContent)

        if storageDeviation2 > 0.0001:

            # third Round optimization
            Q_stored_max_needed_3 = np.amax(Q_storage_content_fin_op2) - np.amin(Q_storage_content_fin_op2)
            V_storage_possible_needed = Q_stored_max_needed_3 * WH_TO_J / (DENSITY_OF_WATER_AT_60_DEGREES_KGPERM3 * HEAT_CAPACITY_OF_WATER_JPERKGK * (T_ST_MAX - T_ST_MIN))
            V3 = V_storage_possible_needed

            Q_initial = min(Q_disc_seasonstart_opt2[0], Q_storage_content_fin_op2[-1])

            T_initial = T_ST_MIN + Q_initial * WH_TO_J / (DENSITY_OF_WATER_AT_60_DEGREES_KGPERM3 * HEAT_CAPACITY_OF_WATER_JPERKGK * V_storage_initial)

            Optimized_Data3 = StDesOp.Storage_Design(CSV_NAME, SOLCOL_TYPE, T_initial, Q_initial, locator,
                                                     V_storage_possible_needed, STORE_DATA, master_to_slave_vars, P_HP_max, config)
            Q_stored_max_opt3, Q_rejected_fin_opt3, Q_disc_seasonstart_opt3, T_st_max_op3, T_st_min_op3, \
            Q_storage_content_fin_op3, T_storage_fin_op3, Q_loss3, mdot_DH_fin3, Q_uncontrollable_fin = Optimized_Data3

            InitialStorageContent = float(Q_storage_content_fin_op3[0])
            FinalStorageContent = float(Q_storage_content_fin_op3[-1])
            # second Round optimization
            if InitialStorageContent == 0 or FinalStorageContent == 0:  # catch error in advance of having 0 / 0
                storageDeviation3 = 0
            else:
                storageDeviation3 = (abs(InitialStorageContent - FinalStorageContent) / FinalStorageContent)

            if storageDeviation3 > 0.0001:

                # fourth Round optimization - reduce end temperature by rejecting earlier (minimize volume)
                Q_stored_max_needed_4 = Q_stored_max_needed_3 - (Q_storage_content_fin_op3[-1] - Q_storage_content_fin_op3[0])
                V_storage_possible_needed = Q_stored_max_needed_4 * WH_TO_J / (DENSITY_OF_WATER_AT_60_DEGREES_KGPERM3 * HEAT_CAPACITY_OF_WATER_JPERKGK * (T_ST_MAX - T_ST_MIN))
                V4 = V_storage_possible_needed
                Q_initial = min(Q_disc_seasonstart_opt3[0], Q_storage_content_fin_op3[-1])
                T_initial = T_ST_MIN + Q_initial * WH_TO_J / (DENSITY_OF_WATER_AT_60_DEGREES_KGPERM3 * HEAT_CAPACITY_OF_WATER_JPERKGK * V_storage_initial)

                Optimized_Data4 = StDesOp.Storage_Design(CSV_NAME, SOLCOL_TYPE, T_initial, Q_initial, locator,
                                                         V_storage_possible_needed, STORE_DATA, master_to_slave_vars, P_HP_max, config)
                Q_stored_max_opt4, Q_rejected_fin_opt4, Q_disc_seasonstart_opt4, T_st_max_op4, T_st_min_op4, \
                Q_storage_content_fin_op4, T_storage_fin_op4, Q_loss4, mdot_DH_fin4, Q_uncontrollable_fin = Optimized_Data4

                InitialStorageContent = float(Q_storage_content_fin_op4[0])
                FinalStorageContent = float(Q_storage_content_fin_op4[-1])
                # second Round optimization
                if InitialStorageContent == 0 or FinalStorageContent == 0:  # catch error in advance of having 0 / 0
                    storageDeviation4 = 0
                else:
                    storageDeviation4 = (abs(InitialStorageContent - FinalStorageContent) / FinalStorageContent)

                if storageDeviation4 > 0.0001:

                    # fifth Round optimization - minimize volume more so the temperature reaches a T_min + dT_margin

                    Q_stored_max_needed_5 = Q_stored_max_needed_4 - (Q_storage_content_fin_op4[-1] - Q_storage_content_fin_op4[0])
                    V_storage_possible_needed = Q_stored_max_needed_5 * WH_TO_J / (DENSITY_OF_WATER_AT_60_DEGREES_KGPERM3 * HEAT_CAPACITY_OF_WATER_JPERKGK * (T_ST_MAX - T_ST_MIN))
                    V5 = V_storage_possible_needed
                    Q_initial = min(Q_disc_seasonstart_opt4[0], Q_storage_content_fin_op4[-1])
                    if Q_initial != 0:
                        Q_initial_min = Q_disc_seasonstart_opt4 - min(
                            Q_storage_content_fin_op4)  # assuming the minimum at the end of the season
                        Q_buffer = DENSITY_OF_WATER_AT_60_DEGREES_KGPERM3 * HEAT_CAPACITY_OF_WATER_JPERKGK * V_storage_possible_needed * MS_Var.dT_buffer / WH_TO_J
                        Q_initial = Q_initial_min + Q_buffer
                        T_initial_real = T_ST_MIN + Q_initial_min * WH_TO_J / (DENSITY_OF_WATER_AT_60_DEGREES_KGPERM3 * HEAT_CAPACITY_OF_WATER_JPERKGK * V_storage_possible_needed)
                        T_initial = MS_Var.dT_buffer + T_initial_real
                    else:
                        T_initial = T_ST_MIN + Q_initial * WH_TO_J / (DENSITY_OF_WATER_AT_60_DEGREES_KGPERM3 * HEAT_CAPACITY_OF_WATER_JPERKGK * V_storage_initial)

                    Optimized_Data5 = StDesOp.Storage_Design(CSV_NAME, SOLCOL_TYPE, T_initial, Q_initial, locator,
                                                             V_storage_possible_needed, STORE_DATA, master_to_slave_vars, P_HP_max, config)
                    Q_stored_max_opt5, Q_rejected_fin_opt5, Q_disc_seasonstart_opt5, T_st_max_op5, T_st_min_op5, \
                    Q_storage_content_fin_op5, T_storage_fin_op5, Q_loss5, mdot_DH_fin5, Q_uncontrollable_fin = Optimized_Data5

                    # Attempt for debugging
                    #   Issue:    1 file showed miss-match of final to initial storage content of 30%, all others had deviations of 0.5 % max
                    #   Idea:     check the final to initial storage content with an allowed margin of 5%.
                    #             If this happens, a new storage optimization run will be performed (sixth round)
                    #
                    #             If the 5% margin is still not maintined after round 6, cover / fill
                    #             the storage with a conventional boiler up to it's final value. As this re-filling can happen during hours of low
                    #             consumption, no extra machinery will be required.

                    InitialStorageContent = float(Q_storage_content_fin_op5[0])
                    FinalStorageContent = float(Q_storage_content_fin_op5[-1])

                    if InitialStorageContent == 0 or FinalStorageContent == 0:  # catch error in advance of having 0 / 0
                        storageDeviation5 = 0
                    else:
                        storageDeviation5 = (abs(InitialStorageContent - FinalStorageContent) / FinalStorageContent)

                    if storageDeviation5 > 0.0001:
                        Q_initial = min(Q_disc_seasonstart_opt5[0], Q_storage_content_fin_op5[-1])

                        Q_stored_max_needed_6 = float(
                            Q_stored_max_needed_5 - (Q_storage_content_fin_op5[-1] - Q_storage_content_fin_op5[0]))
                        V_storage_possible_needed = Q_stored_max_needed_6 * WH_TO_J / (DENSITY_OF_WATER_AT_60_DEGREES_KGPERM3 * HEAT_CAPACITY_OF_WATER_JPERKGK * (T_ST_MAX - T_ST_MIN))
                        V6 = V_storage_possible_needed  # overwrite V5 on purpose as this is given back in case of a change

                        # leave initial values as we adjust the final outcome only, give back values from 5th round

                        Optimized_Data6 = StDesOp.Storage_Design(CSV_NAME, SOLCOL_TYPE, T_initial, Q_initial, locator,
                                                                 V_storage_possible_needed, STORE_DATA, master_to_slave_vars,
                                                                 P_HP_max, config)
                        Q_stored_max_opt6, Q_rejected_fin_opt6, Q_disc_seasonstart_opt6, T_st_max_op6, T_st_min_op6, Q_storage_content_fin_op6, \
                        T_storage_fin_op6, Q_loss6, mdot_DH_fin6, Q_uncontrollable_fin = Optimized_Data6

                        InitialStorageContent = float(Q_storage_content_fin_op6[0])
                        FinalStorageContent = float(Q_storage_content_fin_op6[-1])

                        if InitialStorageContent == 0 or FinalStorageContent == 0:  # catch error in advance of having 0 / 0
                            storageDeviation6 = 0
                        else:
                            storageDeviation6 = (abs(InitialStorageContent - FinalStorageContent) / FinalStorageContent)

                        if storageDeviation6 > 0.0001:
                            Q_initial = min(Q_disc_seasonstart_opt6[0], Q_storage_content_fin_op6[-1])

                            Q_stored_max_needed_7 = float(
                                Q_stored_max_needed_6 - (Q_storage_content_fin_op6[-1] - Q_storage_content_fin_op6[0]))
                            V_storage_possible_needed = Q_stored_max_needed_7 * WH_TO_J / (
                                    DENSITY_OF_WATER_AT_60_DEGREES_KGPERM3 * HEAT_CAPACITY_OF_WATER_JPERKGK * (T_ST_MAX - T_ST_MIN))
                            V7 = V_storage_possible_needed  # overwrite V5 on purpose as this is given back in case of a change

                            # leave initial values as we adjust the final outcome only, give back values from 5th round

                            Optimized_Data7 = StDesOp.Storage_Design(CSV_NAME, SOLCOL_TYPE, T_initial, Q_initial,
                                                                     locator,
                                                                     V_storage_possible_needed, STORE_DATA,
                                                                     master_to_slave_vars,
                                                                     P_HP_max, config)
                            Q_stored_max_opt7, Q_rejected_fin_opt7, Q_disc_seasonstart_opt7, T_st_max_op7, T_st_min_op7, Q_storage_content_fin_op7, \
                            T_storage_fin_op7, Q_loss7, mdot_DH_fin7, Q_uncontrollable_fin = Optimized_Data7

                            InitialStorageContent = float(Q_storage_content_fin_op7[0])
                            FinalStorageContent = float(Q_storage_content_fin_op7[-1])

                            if InitialStorageContent == 0 or FinalStorageContent == 0:  # catch error in advance of having 0 / 0
                                storageDeviation7 = 0
                            else:
                                storageDeviation7 = (
                                        abs(InitialStorageContent - FinalStorageContent) / FinalStorageContent)

                            if storageDeviation7 > 0.0001:
                                Q_initial = min(Q_disc_seasonstart_opt7[0], Q_storage_content_fin_op7[-1])

                                Q_stored_max_needed_8 = float(
                                    Q_stored_max_needed_7 - (
                                            Q_storage_content_fin_op7[-1] - Q_storage_content_fin_op7[0]))
                                V_storage_possible_needed = Q_stored_max_needed_8 * WH_TO_J / (
                                        DENSITY_OF_WATER_AT_60_DEGREES_KGPERM3 * HEAT_CAPACITY_OF_WATER_JPERKGK * (T_ST_MAX - T_ST_MIN))
                                V8 = V_storage_possible_needed  # overwrite V5 on purpose as this is given back in case of a change

                                # leave initial values as we adjust the final outcome only, give back values from 5th round

                                Optimized_Data8 = StDesOp.Storage_Design(CSV_NAME, SOLCOL_TYPE, T_initial, Q_initial,
                                                                         locator,
                                                                         V_storage_possible_needed, STORE_DATA,
                                                                         master_to_slave_vars,
                                                                         P_HP_max, config)
                                Q_stored_max_opt8, Q_rejected_fin_opt8, Q_disc_seasonstart_opt8, T_st_max_op8, T_st_min_op8, Q_storage_content_fin_op8, \
                                T_storage_fin_op8, Q_loss8, mdot_DH_fin8, Q_uncontrollable_fin = Optimized_Data8

                                InitialStorageContent = float(Q_storage_content_fin_op8[0])
                                FinalStorageContent = float(Q_storage_content_fin_op8[-1])

                                if InitialStorageContent == 0 or FinalStorageContent == 0:  # catch error in advance of having 0 / 0
                                    storageDeviation8 = 0
                                else:
                                    storageDeviation8 = (
                                            abs(InitialStorageContent - FinalStorageContent) / FinalStorageContent)

                                if storageDeviation8 > 0.0001:
                                    Q_initial = min(Q_disc_seasonstart_opt8[0], Q_storage_content_fin_op8[-1])

                                    Q_stored_max_needed_9 = float(
                                        Q_stored_max_needed_8 - (
                                                Q_storage_content_fin_op8[-1] - Q_storage_content_fin_op8[0]))
                                    V_storage_possible_needed = Q_stored_max_needed_9 * WH_TO_J / (
                                            DENSITY_OF_WATER_AT_60_DEGREES_KGPERM3 * HEAT_CAPACITY_OF_WATER_JPERKGK * (T_ST_MAX - T_ST_MIN))
                                    V9 = V_storage_possible_needed  # overwrite V5 on purpose as this is given back in case of a change

                                    # leave initial values as we adjust the final outcome only, give back values from 5th round

                                    Optimized_Data9 = StDesOp.Storage_Design(CSV_NAME, SOLCOL_TYPE, T_initial,
                                                                             Q_initial,
                                                                             locator,
                                                                             V_storage_possible_needed, STORE_DATA,
                                                                             master_to_slave_vars,
                                                                             P_HP_max, config)
                                    Q_stored_max_opt9, Q_rejected_fin_opt9, Q_disc_seasonstart_opt9, T_st_max_op9, T_st_min_op9, Q_storage_content_fin_op9, \
                                    T_storage_fin_op9, Q_loss9, mdot_DH_fin9, Q_uncontrollable_fin = Optimized_Data9

                                    InitialStorageContent = float(Q_storage_content_fin_op9[0])
                                    FinalStorageContent = float(Q_storage_content_fin_op9[-1])

                                    if InitialStorageContent == 0 or FinalStorageContent == 0:  # catch error in advance of having 0 / 0
                                        storageDeviation9 = 0
                                    else:
                                        storageDeviation9 = (
                                                abs(InitialStorageContent - FinalStorageContent) / FinalStorageContent)

                                    if storageDeviation9 > 0.0001:
                                        Q_initial = min(Q_disc_seasonstart_opt9[0], Q_storage_content_fin_op9[-1])

                                        Q_stored_max_needed_10 = float(
                                            Q_stored_max_needed_9 - (
                                                    Q_storage_content_fin_op9[-1] - Q_storage_content_fin_op9[0]))
                                        V_storage_possible_needed = Q_stored_max_needed_10 * WH_TO_J / (
                                                DENSITY_OF_WATER_AT_60_DEGREES_KGPERM3 * HEAT_CAPACITY_OF_WATER_JPERKGK * (T_ST_MAX - T_ST_MIN))
                                        V10 = V_storage_possible_needed  # overwrite V5 on purpose as this is given back in case of a change

                                        # leave initial values as we adjust the final outcome only, give back values from 5th round

                                        Optimized_Data10 = StDesOp.Storage_Design(CSV_NAME, SOLCOL_TYPE, T_initial,
                                                                                 Q_initial,
                                                                                 locator,
                                                                                 V_storage_possible_needed, STORE_DATA,
                                                                                 master_to_slave_vars,
                                                                                 P_HP_max, config)
                                        Q_stored_max_opt10, Q_rejected_fin_opt10, Q_disc_seasonstart_opt10, T_st_max_op10, T_st_min_op10, Q_storage_content_fin_op10, \
                                        T_storage_fin_op10, Q_loss10, mdot_DH_fin10, Q_uncontrollable_fin = Optimized_Data10

    storage_operation_data = pd.read_csv(locator.get_optimization_slave_storage_operation_data(MS_Var.individual_number, MS_Var.generation_number))
    E_aux_ch_W = np.array(storage_operation_data['E_aux_ch_W'])
    E_aux_dech_W = np.array(storage_operation_data['E_aux_dech_W'])
    E_thermalstorage_W = np.add(E_aux_ch_W, E_aux_dech_W)

    # costs, GHG and PEN corresponding to the operation of the heat pump associated with thermal storage
    for hour in range(len(E_thermalstorage_W)):
        costs_storage_USD = costs_storage_USD + E_thermalstorage_W[hour] * lca.ELEC_PRICE[hour]
    GHG_storage_tonCO2 = GHG_storage_tonCO2 + (np.sum(E_thermalstorage_W) * lca.EL_TO_CO2 * WH_TO_J / 1.0E6)
    PEN_storage_MJoil = PEN_storage_MJoil + (np.sum(E_thermalstorage_W) * lca.EL_TO_OIL_EQ * WH_TO_J / 1.0E6)

    Q_storage_content_W = np.array(storage_operation_data['Q_storage_content_W'])
    StorageContentEndOfYear = Q_storage_content_W[-1]
    StorageContentStartOfYear = Q_storage_content_W[0]

    if StorageContentEndOfYear < StorageContentStartOfYear:
        QToCoverByStorageBoiler = float(StorageContentEndOfYear - StorageContentStartOfYear)
        eta_fictive_Boiler = 0.8  # add rather low efficiency as a penalty
        E_gasPrim_fictiveBoiler = QToCoverByStorageBoiler / eta_fictive_Boiler

    else:
        E_gasPrim_fictiveBoiler = 0

    PEN_storage_MJoil = PEN_storage_MJoil + (E_gasPrim_fictiveBoiler * lca.NG_BOILER_TO_OIL_STD * WH_TO_J / 1.0E6)
    GHG_storage_tonCO2 = GHG_storage_tonCO2 + (E_gasPrim_fictiveBoiler * lca.NG_BOILER_TO_CO2_STD * WH_TO_J / 1.0E6)


    # Fill up storage if end-of-season energy is lower than beginning of season
    Q_Storage_SeasonEndReheat_W = Q_storage_content_W[-1] - Q_storage_content_W[0]

    if Q_Storage_SeasonEndReheat_W > 0:
        cost_Boiler_for_Storage_reHeat_at_seasonend_USD = float(Q_Storage_SeasonEndReheat_W) / 0.8 * prices.NG_PRICE  # efficiency is assumed to be 0.8
        GHG_Boiler_for_Storage_reHeat_at_seasonend_tonCO2 = (float(Q_Storage_SeasonEndReheat_W) / 0.8) * lca.NG_BOILER_TO_CO2_STD * WH_TO_J / 1.0E6
        PEN_Boiler_for_Storage_reHeat_at_seasonend_MJoil = (float(Q_Storage_SeasonEndReheat_W) / 0.8) * lca.NG_BOILER_TO_OIL_STD * WH_TO_J / 1.0E6
    else:
        cost_Boiler_for_Storage_reHeat_at_seasonend_USD = 0
        GHG_Boiler_for_Storage_reHeat_at_seasonend_tonCO2 = 0
        PEN_Boiler_for_Storage_reHeat_at_seasonend_MJoil = 0

    costs_storage_USD = costs_storage_USD + cost_Boiler_for_Storage_reHeat_at_seasonend_USD
    GHG_storage_tonCO2 = GHG_storage_tonCO2 + GHG_Boiler_for_Storage_reHeat_at_seasonend_tonCO2
    PEN_storage_MJoil = PEN_storage_MJoil + PEN_Boiler_for_Storage_reHeat_at_seasonend_MJoil


    return costs_storage_USD, GHG_storage_tonCO2, PEN_storage_MJoil