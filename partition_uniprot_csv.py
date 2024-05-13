## Create partitioned uniprot names
import numpy as np
import pandas as pd
import os
import sys

# input1 = where to put the directories (/people/imal967/ppi/sandbox)
# input2 =  input directory of pdbs to split up (/rcfs/projects/proteometer/alphafold_db)
# input3 = how many files and directories to partition into 
# input4 = OPTIONAL check if the output already exists
# example usage:
# python partition_uniprot_csv.py /people/imal967/ppi/sandbox /qfs/projects/proteometer/pypka_scripts/test_input.csv 3

working_dir = sys.argv[1]
all_data_dir = sys.argv[2] 
amnt_of_partitions = int(sys.argv[3])
already_made = sys.argv[4]

print(working_dir)
print(all_data_dir)
print(amnt_of_partitions)

already_made_data = pd.read_csv(already_made)
already_made_data = np.array(already_made_data.iloc[:,0])
already_made_array = []
for i in already_made_data:
    to_add = np.array(i.split("-"))[1] + '-' + np.array(i.split("-"))[2]
    already_made_array.append(to_add)
all_data = np.array(os.listdir(all_data_dir))
to_run = []
for i in all_data:
    to_add = np.array(i.split("-"))[1] + '-' + np.array(i.split("-"))[2]
    to_run.append(to_add)
to_run = pd.DataFrame({"to_run":to_run})
already_made_array = pd.DataFrame({"already_made_array":already_made_array})
not_run_yet = to_run[~to_run.to_run.isin(already_made_array.already_made_array)]
not_run_yet = np.array(not_run_yet.to_run)
print(not_run_yet)
split_list_uniprots = np.array_split(not_run_yet,amnt_of_partitions) # split into x amount of arrays
print(split_list_uniprots)
counter_variable = 0
for single_list in split_list_uniprots:
    single_dataframe = pd.DataFrame(single_list)
    single_dataframe.columns = ["Entry"]
    os.system("mkdir {}/uniprot4pka_{}".format(working_dir,counter_variable))
    output_split_file = "{}/uniprot4pka_{}/uniprot4pka_{}.csv".format(working_dir,counter_variable,counter_variable)
    single_dataframe.to_csv(output_split_file)
    counter_variable = counter_variable + 1 


    


