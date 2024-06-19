# import pypka package
from pypka import Titration
import numpy as np
import pandas as pd
import sys
import os
from pathlib import Path


cpu_num = int(sys.argv[1])
pdb_path_file = sys.argv[2]
pka_results_dir = sys.argv[3]

pdb_paths = pd.read_csv(pdb_path_file)  # read in input csv file with all interested cysteines
pdb_paths_list = pdb_paths['pdb_path'].tolist()

# get pKa (run Poisson-Boltzmann equation + monte carlo simulations)
for pdb_path in pdb_paths_list:
    pdb_file_name = Path(pdb_path).stem
    output_file = os.path.join(pka_results_dir, pdb_file_name + '.csv')
    if not os.path.isfile(output_file):
        # initialize empty dataframe
        pka_matrix = np.zeros((1, 5))   # initialize empty array
        # print(input_file)
        params = {
            'structure': pdb_path,      # Input structure file name
            'ncpus': cpu_num,              # Number of processes (-1 for maximum allowed)
            'epsin': 15,              # Dielectric constant of the protein
            'ionicstr': 0.1,             # Ionic strength of the medium (M)
            'pbc_dimensions': 0,               # PB periodic boundary conditions (0 for solvated proteins and 2 for lipidic systems)
            'sites': all              # Make sure all of the sites are included (this is default)
        }

        tit = Titration(params)
        print(tit)

        pH = 7.0
        uniprot_id = pdb_file_name.split("-")[1]
        for site in tit:
            state = site.getProtState(pH)[0]
            newrow = [uniprot_id, site.res_name, site.res_number, site.pK, state]
            pka_matrix = np.vstack([pka_matrix, newrow])
        pka_matrix = np.delete(pka_matrix, 0, 0)    # remove first row of 0's
        pka_df = pd.DataFrame(pka_matrix, columns=['UniProt', 'AA', 'Pos', 'pKa', 'State'])
        pka_df.to_csv(output_file)
