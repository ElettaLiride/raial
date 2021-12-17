import os
import numpy as np

from database import parameters_setting as pm
from database import ccdb_connection as cc
from scripts import run_plots
from scripts import run_reco

RICHGEOAL = os.path.basename("RICHGEOAL")

filterdir = RICHGEOAL + "/filter/"
plotdir = RICHGEOAL + "/plots/"
recodir = RICHGEOAL + "/reco/"

calibration_connection = "sqlite:///" + RICHGEOAL + "/database/ccdb_4.3.2.sqlite"
calibration_table = "/calibration/rich/misalignments"
variation = "default"
user = "Costantini"


def read_output(string):
    tiles = string.split('Layer')[1:]
    chi = float(str(string).split('Layer')[0].split('chi2=')[1].split('\\')[0])
    val = [float(tile.split('dEtaC=')[1].split('\\')[0]) for tile in tiles]
    layer = [float(tile.split()[0]) for tile in tiles]
    t = [float(tile.split()[2]) for tile in tiles]
    nice_output = np.asarray([layer, t, val])

    return nice_output, chi


def compute_score(nice_output, chi):
    return sum([abs(el) for el in nice_output]) / len(nice_output) + chi


def make_mean(file):
    f = open(file, "r")
    nline = 0
    mean = 0
    chi2 = 0
    lines = f.readlines()

    for line in lines:
        if nline==1:
            chi2 = abs(float(line.split()[-1].split('=')[-1]))

        mean = mean + abs(float(line.split()[-1].split('=')[-1]))
        nline+=1
    mean = mean/(nline-1) + chi2
    f.close()
    return mean


def make_mean1(file):
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


def pass_dict_param_to_table(par_dict, table):
    for layer, val in par_dict.items():
        module = [4, int(layer.split('_')[1]), 0]
        pars = [layer.split('_')[0], val]
        pm.changing_one_parameter(table, module, pars)

    return table


def obj_gp(space, names, RN):
    """

    :param space:
    :param names:
    :return:
    """
    global recodir, plotdir, calibration_table, calibration_connection, variation, user
    filefromplot = "RichPlots_" + RN + ".out"

    my_provider = cc.connecting_ccdb(calibration_connection, variation)

    params = {names[i]: space[i] for i in range(len(space))}

    # CHANGING PARAM ON CCDB
    old_pars_table = cc.reading_ccdb(my_provider, calibration_table, variation)
    new_table = pass_dict_param_to_table(params, old_pars_table)
    to_add = new_table.values.tolist()
    cc.adding_to_ccdb(to_add, provider, calibration_table, variation)

    # start_time = time.time()
    # RUN EVENTBUILDER
    print("-----------------------------------------------------------------------------------------------")
    print("----------------------------------- START RECO ------------------------------------------------")
    print("-----------------------------------------------------------------------------------------------")

    for file in os.listdir(filterdir):
        if os.path.isfile(filterdir + file):
            run_reco.runcommand(filterdir + file)
        else:
            run_reco.runcommand(filterdir)

    # reco_time = int(time.time() - start_time)
    # second_time = time.time()

    # RUN ANGLE ANALYSIS
    print("-----------------------------------------------------------------------------------------------")
    print("----------------------------------- START PLOTTING --------------------------------------------")
    print("-----------------------------------------------------------------------------------------------")

    _ = run_plots.runcommand(recodir, RN)
    # plot_time = int(time.time() - second_time)

    # SCORING

    obj_score = make_mean(filefromplot)

    # , reco_time, plot_time
    print("score: ", obj_score)
    return obj_score


def obj_tpe(space):
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
    print('asked at ccdb')
    old_pars_table = pass_dict_param_to_table(params, old_pars_table)
    print('converted param to table')
    toadd = old_pars_table.values.tolist()
    cc.adding_to_ccdb(toadd, provider, calibration_table, variation)
    print('added new param to ccdb')

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

    output = run_plots.runcommand(fileforplot)
    # plot_time = int(time.time() - second_time)

    # SCORING
    score = make_mean(output)
    #, reco_time, plot_time
    print("score: ", score)
    return score


if __name__=="__main__":
    filterdir = "output/filter/"
    plotdir = "output/plots/"
    recodir = "output/reco/"
    fileforreco = filterdir + "rec_clas_5424_AIskim1_-1.hipo"
    fileforplot = recodir + "rec_clas_5424_AIskim1_-1.hipo"
    filefromplot = plotdir + "RichPlots_5424.out"

    calibration_connection = "sqlite:///database/ccdb_4.3.2.sqlite"
    calibration_table = "/calibration/rich/misalignments"
    variation = "default"
    user = "Costantini"

    provider = cc.connecting_ccdb(calibration_connection, variation)

    # space_tpe = {
    #     'dx_401': 1.,
    #     'dy_401': 0.,
    #     'dz_401': 0.,
    #     'dthx_401': 0.,
    #     'dthy_401': 1.,
    #     'dthz_401': 0.,
    #     'dx_201': 0.,
    #     'dy_201': 0.,
    #     'dz_201': 1.,
    #     'dthx_201': 1.,
    #     'dthy_201': 0.,
    #     'dthz_201': 0.,
    #     'dx_202': 0.,
    #     'dy_202': 0.,
    #     'dz_202': 1.,
    #     'dthx_202': 0.,
    #     'dthy_202': 1.,
    #     'dthz_202': 0.
    # }
    # score = obj_tpe(space_tpe)

    space_gp = [0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.]
    score = obj_gp(space_gp)
    print("SCORE: ", score)