# import packages
import numpy as np
import pandas as pd
import sys
import os
from pathlib import Path
import glob
import subprocess
import re

import warnings
warnings.filterwarnings('ignore')

# read in directories and variables
input_dir = sys.argv[1] # location of pka csv's to clean # /rcfs/projects/proteometer/test_pka
working_dir = sys.argv[2] # where to output cleaned csv's # /rcfs/projects/proteometer/out_pka
pdb_dir = sys.argv[3] # location of the pdb files that coorespond to the csv's # /rcfs/projects/proteometer/alphafold_db/ 



all_csvs = glob.glob(input_dir+"/*.csv")
#print("processing " + str(len(all_csvs)) + " files")
for file in all_csvs:
    #print(file)
    pka_dataframe = pd.DataFrame(pd.read_csv(file))
    del pka_dataframe[pka_dataframe.columns[0]]

    name_of_file = file.split("/")[-1] 
    uniprot_id = name_of_file.split("-")[1] #get the correct uniprotID from the filename
    n_terminal = "NTR"

    # isolate to only correct protein sequence
    list_of_starts = list(pka_dataframe[pka_dataframe['AA'].str.contains('NTR')].index) #get all starts of new protein seq
    if list_of_starts: # check if list_of_starts is empty first
        last_NTR = list_of_starts[-1] # get last value, which is the index of the last protein seq (works even if there's only 1 value)
        new_pka_dataframe = pka_dataframe.iloc[last_NTR:len(pka_dataframe)]

        # correct the AA sequence
        #print(pdb_dir + str(name_of_file.split("_")[0]) + "_" + str(name_of_file.split("_")[1]) + ".pdb")
        pdb_file = pdb_dir + str(name_of_file.split("_")[0]) + "_" + str(name_of_file.split("_")[1]) + ".pdb"
        line_with_info = subprocess.check_output("grep DBREF " + str(pdb_file), shell=True) # probably not the most efficient/best but it works
        #print(line_with_info)
        line_with_info = str(line_with_info)
        split_list = line_with_info.split()
        first_res = int(split_list[-3]) - 1
        #last_res = split[-2] - 1

        #new_pka_dataframe['position'] = new_pka_dataframe.loc[1:,'res_number'] + first_res
        new_pka_dataframe['position'] = new_pka_dataframe["res_number"] + first_res
        new_pka_dataframe["position"] = new_pka_dataframe["position"].astype("int")
        new_pka_dataframe.iloc[0, 5] = new_pka_dataframe.iloc[0, 2] #fix NTR
        new_pka_dataframe.iloc[-1, 5] = new_pka_dataframe.iloc[-1, 2] #fix CTR
        

        #save fixed csv to output directory
        new_pka_dataframe.to_csv(working_dir + "/pKa_" + str(name_of_file.split("_")[0]) + "_" + str(name_of_file.split("_")[1]) + ".csv")





    


