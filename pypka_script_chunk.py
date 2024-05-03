# import pypka package
from pypka import Titration
import numpy as np
import pandas as pd
import sys
import glob
import os
import time


cpu_num = int(sys.argv[1])
uniprot_names_file = sys.argv[2]
pka_results_dir = sys.argv[3]

input_csv = pd.read_csv(uniprot_names_file) # read in input csv file with all interested cysteines
uniprotIDs = input_csv['Entry'].unique().tolist() # get only uniprod IDs for each and get rid of duplicates

# initialize empty dataframe
pka_matrix = np.zeros((1, 5))   # initialize empty array

# start timer
start = time.time()

# get pKa (run Poisson-Boltzmann equation + monte carlo simulations)
for name in uniprotIDs:      # aka 2nd forward
    # cys_to_keep = list(input_csv[input_csv.Entry == name].cys_num_from_Tong)
    get_file_name = "/rcfs/projects/proteometer/alphafold_db/*"+name+"*"
    files = glob.glob(get_file_name)
    if files:
        for input_file in files:
            if not os.path.isfile(input_file[:-4]+".csv"):
                # print(input_file)
                params = {
                'structure'     : input_file,      # Input structure file name
                'ncpus'         : cpu_num,              # Number of processes (-1 for maximum allowed)
                'epsin'         : 15,              # Dielectric constant of the protein
                'ionicstr'      : 0.1,             # Ionic strength of the medium (M)
                'pbc_dimensions': 0,               # PB periodic boundary conditions (0 for solvated proteins and 2 for lipidic systems)
                'sites'         : all              # Make sure all of the sites are included (this is default)
                }

                tit = Titration(params)
                print(tit)

                pH = 7.0
                for site in tit:
                    state = site.getProtState(pH)[0]
                    newrow = [name,site.res_name, site.res_number, site.pK, state]
                    pka_matrix = np.vstack([pka_matrix, newrow])
                pka_matrix = np.delete(pka_matrix, 0, 0)    # remove first row of 0's
                pka_matrix = pd.DataFrame(pka_matrix)
                pka_matrix = pka_matrix.rename(columns = {0:'uniprotID',1:'AA',2:'res_number',3:'pK',4:'state'})
                pka_df = pka_matrix 
                print(input_file[:-4])
                pka_df.to_csv(pka_results_dir + input_file.split("/")[-1][:-4] + "_out.csv")
