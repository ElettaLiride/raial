import os
import sys

from run_control import tools as t
#for filter
#swif
#add-job
#-workflow AL_test
#-ram 1500mb
#-project clas12
#-time 6h
#-track debug
#-phase 0
#-name test_2
#-shell /bin/bash
#-input run_filter.py file:$PWD/run_control/run_filter.py
#-input filterHipo file:$PWD/scoring/RichAI_FilterC/filterHipo
#-input rec_clas_005032.evio.00085-00089.hipo file:/cache/clas12/rg-a/production/recon/fall2018/torus-1/pass1/v0/dst/recon/005032/rec_clas_005032.evio.00085-00089.hipo
#-input runfilteronfarm.sh file:$PWD/runfilteronfarm.sh
#-input setup1.sh file:$PWD/setup1.sh
#-input environment.bash file:$PWD/../ccdb/environment.bash
#-input ccdb_4.3.2.sqlite file:$PWD/database/ccdb_4.3.2.sqlite
#-input test.txt file:$PWD/output/test.txt -stderr file:$PWD/err.txt
#./runfilteronfarm.sh /work/clas12/users/costantini/RICH_alignment/output/test.txt 27 -1

##for reco
#swif add-job -workflow reco_test -ram 1500mb -project clas12 -time 6h -track debug -phase 0 -name test_reco -shell /bin/bash -input run_reco.py file:$PWD/run_control/run_reco.py -input recon_util file:/work/clas12/users/devita/rich/oldVersionWithNewGeo/clas12-offline-software/coatjava/bin/recon-util -input rec_clas_27_AIskim1_-1.hipo file:$PWD/output/filter/rec_clas_27_AIskim1_-1.hipo -input runrecoonfarm.sh file:$PWD/runrecoonfarm.sh -input setup1.sh file:$PWD/setup1.sh -input environment.bash file:$PWD/../ccdb/environment.bash -input ccdb_4.3.2.sqlite file:$PWD/database/ccdb_4.3.2.sqlite -input test.txt file:$PWD/output/test.txt -stderr file:$PWD/err.txt ./runrecoonfarm.sh rec_clas_27_AIskim1_-1.hipo

## for plot
#swif add-job
#-workflow AL_test
#-ram 1500mb
#-project clas12
#-time 6h
#-track debug
#-phase 0
#-name test_plot
#-shell /bin/bash

#-input run_plot.py file:$PWD/run_control/run_plots.py
#-input richPlots file:/work/clas12/users/costantini/RICH_alignment/scoring/RichAI_Plots/richPlots
#-input rec_clas_27_AIskim1_-1.hipo file:$PWD/output/reco/rec_clas_27_AIskim1_-1.hipo
#-input runplotonfarm.sh file:$PWD/runplotonfarm.sh
#-input setup1.sh file:$PWD/setup1.sh
#-input environment.bash file:$PWD/../ccdb/environment.bash
#-input ccdb_4.3.2.sqlite file:$PWD/database/ccdb_4.3.2.sqlite
#-stderr file:$PWD/err_plot.txt
#./runplotonfarm.sh /work/clas12/users/costantini/RICH_alignment/output/reco/rec_clas_27_AIskim1_-1.hipo
#swif add-job -workflow AL_test -ram 1500mb -project clas12 -time 6h -track debug -phase 0 -name test_plot -shell /bin/bash -input run_plots.py file:$PWD/run_control/run_plots.py -input richPlots file:/work/clas12/users/costantini/RICH_alignment/scoring/RichAI_Plots/richPlots -input rec_clas_27_AIskim1_-1.hipo file:$PWD/output/reco/rec_clas_27_AIskim1_-1.hipo -input runplotonfarm.sh file:$PWD/runplotonfarm.sh -input setup1.sh file:$PWD/setup1.sh -input environment.bash file:$PWD/../ccdb/environment.bash -input ccdb_4.3.2.sqlite file:$PWD/database/ccdb_4.3.2.sqlite -stderr file:$PWD/err_plot.txt ./runplotonfarm.sh /work/clas12/users/costantini/RICH_alignment/output/reco/rec_clas_27_AIskim1_-1.hipo
##QUELLA FINALE:
#swif
#add-job
#-workflow AL_test
#-ram 1500mb
#-project clas12
#-time 6h
#-track debug
#-phase 0
#-name test_2
#-shell /bin/bash

#-input rec_clas_27_AIskim1_-1.hipo file:$PWD/output/filter/rec_clas_27_AIskim1_-1.hipo
#-input setup1.sh file:$PWD/setup1.sh -input environment.bash file:$PWD/../ccdb/environment.bash
#-input ccdb_4.3.2.sqlite file:$PWD/database/ccdb_4.3.2.sqlite
#-input run_reco.py file:$PWD/run_control/run_reco.py
#-input run_plot.py file:$PWD/run_control/run_plots.py
#-input recon_util file:/work/clas12/users/devita/rich/oldVersionWithNewGeo/clas12-offline-software/coatjava/bin/recon-util
#-input richPlots file:/work/clas12/users/costantini/RICH_alignment/scoring/RichAI_Plots/richPlots
#-input runplotonfarm.sh file:$PWD/runplotonfarm.sh
#-input Aerogel_ccdb.dat file:$PWD/Aerogel_ccdb.dat
#-stderr file:$PWD/err_plot.txt
#./runplotonfarm.sh /work/clas12/users/costantini/RICH_alignment/output/reco/rec_clas_27_AIskim1_-1.hipo


#swif add-job -workflow AL_test -ram 1500mb -project clas12 -time 6h -track debug -phase 0 -name test_all -shell /bin/bash -input opt_firstlayer.py file:$PWD/optimization/opt_firstlayer.py -input recon_util file:/work/clas12/users/devita/rich/oldVersionWithNewGeo/clas12-offline-software/coatjava/bin/recon-util -input rec_clas_27_AIskim1_-1.hipo file:$PWD/output/filter/rec_clas_27_AIskim1_-1.hipo -input richPlots file:$PWD/scoring/RichAI_Plots/richPlots -input runallprocedure.sh file:$PWD/runallprocedure.sh -input setup1.sh file:$PWD/setup1.sh -input environment.bash file:$PWD/../ccdb/environment.bash -input ccdb_4.3.2.sqlite file:$PWD/database/ccdb_4.3.2.sqlite -stderr file:$PWD/err_all.txt ./runallprocedure.sh
time = ""
ram = ""
disk = ""
name = ""
phase = ""

aerogel_dat = ""
ccdb_file = ""
set_file = ""
python_reco = ""
recon_util = ""
python_plot = ""
rich_plot = ""

def add_job(WF, filelist, RN, yaml):
    cmq = "swif add-job "
    cmd = "- input " + " file:" + aerogel_dat
    cmd = "- input " + " file:" + ccdb_file
    cmd = "- input " + " file:" + set_file
    cmd = "- input " + " file:" + python_reco
    cmd = "- input " + " file:" + recon_util
    cmd = "- input " + " file:" + python_plot
    cmd = "- input " + " file:" + rich_plot



def run_workflow(WF):
    _ = t.runcommand('swif run ' + WF)

def create_workflow(WF):
    _ = t.runcommand('swif create ' + WF)