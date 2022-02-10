"""
    this script scan with constant step on a single or a couple of parameter the objective src/python/objective.
    It choose the right objective function looking at the name of the yaml file. If "ca" or "pb"
    is in the name it takes those funcs, otherwise it chooses the carbon one.
    It looks for checkpoints given the name and if there are not it creates one. Otherwise
    it overwrites the file.

    It takes as input
    1) the name of the yaml file for the hyperparameter space
    2) the number of calls for the search

"""
import os.path
import sys
import time

import yaml

from config import globalpath
from src.python.tools import init_opt

globalpath.VARIATION = f"scan_variation_{sys.argv[3]}"
data_dir = sys.argv[1]
yaml_space_file = sys.argv[2]
number_of_calls = int(sys.argv[3])

init_opt(data_dir, os.path.basename(yaml_space_file).split('.')[0], 1)

from src.python.objective import obj_cluster_chi_square, obj_chi_and_diff, fake_obj
from src.python.objective import change_parameter_given_dir
from src.python.ccdb_connection import init_ccdb, reading_ccdb, connecting_ccdb


def build_list_from_space(dict, call):
    list = []
    for c in range(call+1):
        list.append(dict['low'] + c*2*dict['high']/call)
    return dict['name'], list



if __name__ == "__main__":

    init_ccdb()


    file = open(yaml_space_file)
    code = yaml.load(file, Loader=yaml.FullLoader)

    if len(code) == 2:
        par1, list1 = build_list_from_space(code[0]['Real'], number_of_calls)
        par2, list2 = build_list_from_space(code[1]['Real'], number_of_calls)
        for p1 in list1:
            for p2 in list2:
                d = {par1: p1, par2: p2}
                time.sleep(2)
                fake_obj(**d)
                #obj_chi_and_diff(**d)
    else:
        par1, list1 = build_list_from_space(code[0]['Real'], number_of_calls)
        for p1 in list1:
            d = {par1: p1}
            print(d)
            time.sleep(2)
            #fake_obj(**d)
            obj_cluster_chi_square(**d)
