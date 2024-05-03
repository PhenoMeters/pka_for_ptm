# ptm_pka
Code for finding pKa for post translational modification sites

## Requirements
**Installing on Mac:** </br>
Use the docker container to run this code:
```
# pull the ptm_pypka docker image
docker pull docker pull lifeworks/pypka

#run the docker image as a shell and mount files that you'd like to run the code on & the cloned repository
docker run -it -v "{path to files}":/input_files -v "{path to pka_for_ptm}":/pka_for_ptm lifeworks/pypka:v1 bash
```

**Installing on Linux/Windows:** </br>
Use the conda environment to run this code:
```
# the conda environment is located in /envs/requirements.txt in the cloned repository
conda create -n pka_for_ptm_env {path to requirements.txt}

# activate the conda environment
conda activate pka_for_ptm_env
```

