from database import parameters_setting as pm
from database import ccdb_connection as cc
from run_control import run_plots
from run_control import run_reco
import os

def make_mean(file):
    f = open(file, "r")
    nline = 0
    mean = 0
    while (True):
        nline += 1
        line = f.readline()
        if not line:
            break

        mean = mean + abs(float(line.split()[-1].split('=')[-1]))
    mean = mean / nline
    f.close()
    return mean


def pass_dict_param_to_table(dict, table):
    for layer, val in dict.items():
        module = [4, int(layer.split('_')[1]), 0]
        pars = [layer.split('_')[0], val]
        pm.changing_one_parameter(table, module, pars)

    return table


def objective(space):
    # COMPUTING SCORE
    params = {
        'dx_401': float(space['dx_401']),
        'dy_401': float(space['dy_401']),
        'dz_401': float(space['dz_401']),
        'dthx_401': float(space['dthx_401']),
        'dthy_401': float(space['dthy_401']),
        'dthz_401': float(space['dthz_401']),
        'dx_201': float(space['dx_201']),
        'dy_201': float(space['dy_201']),
        'dz_201': float(space['dz_201']),
        'dthx_201': float(space['dthx_201']),
        'dthy_201': float(space['dthy_201']),
        'dthz_201': float(space['dthz_201']),
        'dx_202': float(space['dx_202']),
        'dy_202': float(space['dy_202']),
        'dz_202': float(space['dz_202']),
        'dthx_202': float(space['dthx_202']),
        'dthy_202': float(space['dthy_202']),
        'dthz_202': float(space['dthz_202'])
    }

    # CHANGING PARAM ON CCDB
    old_pars_table = cc.reading_ccdb(provider, calibration_table, variation)
    old_pars_table = pass_dict_param_to_table(params, old_pars_table)
    toadd = old_pars_table.values.tolist()
    cc.adding_to_ccdb(toadd, provider, calibration_table, variation)

    # start_time = time.time()
    # RUN EVENTBUILDER
    print("-----------------------------------------------------------------------------------------------")
    print("----------------------------------- START RECO -----------------------------------------")
    print("-----------------------------------------------------------------------------------------------")
    run_reco.runcommand(fileforreco)
    # reco_time = int(time.time() - start_time)
    # second_time = time.time()


    # RUN ANGLE ANALYSIS
    print("-----------------------------------------------------------------------------------------------")
    print("----------------------------------- START PLOTTING -----------------------------------------")
    print("-----------------------------------------------------------------------------------------------")

    run_plots.runcommand(fileforplot)
    # plot_time = int(time.time() - second_time)

    # SCORING
    score = make_mean(filefromplot)
    #, reco_time, plot_time
    print("score: ", score)
    return score



if __name__=="__main__":
    maindir = os.getcwd() + "/"
    filterdir = maindir + "output/filter/"
    plotdir = maindir + "output/plots/"
    recodir = maindir + "output/reco/"
    fileforreco = filterdir + "rec_clas_5206_AIskim1_-1.hipo"
    fileforplot = recodir + "rec_clas_5206_AIskim1_-1.hipo"
    filefromplot = plotdir + "RichPlots_5206.out"

    calibration_connection = "sqlite:///../ccdb_4.3.2.sqlite"
    calibration_table = "/calibration/rich/misalignments"
    variation = "misalignments"
    user = "Costantini"

    provider = cc.connecting_ccdb(calibration_connection, variation)
    space = {
        'dx_401': 0.,
        'dy_401': 0.,
        'dz_401': 0.,
        'dthx_401': 0.,
        'dthy_401': 0.,
        'dthz_401': 0.,
        'dx_201': 0.,
        'dy_201': 0.,
        'dz_201': 0.,
        'dthx_201': 0.,
        'dthy_201': 0.,
        'dthz_201': 0.,
        'dx_202': 0.,
        'dy_202': 0.,
        'dz_202': 0.,
        'dthx_202': 0.,
        'dthy_202': 0.,
        'dthz_202': 0.
    }

    score=objective(space)
    print("SCORE: ", score)