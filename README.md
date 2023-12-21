# GORG-AMZ Database

Hey Future Researchers who use this! Here are the code repository for the updated GORG database (or pro/syn annotation database)!

# Phylogenetic Tree of All Pro and Syn used in Creating this Database
![updated_genomes (2)](https://github.com/jamesm224/gorg_db_update/assets/86495895/181bba39-b338-4553-97c3-8a7f553ec7fa)

# Where are the files?
1. pro_syn_classification - scripts for classification of pro/syn
2. Database - scripts and files for running the database

# How to Use Database

Dependencies (These were the versions we used, but other verisions may work):

        1. pandas v2.0.3
        2. seqtk v1.4
        3. diamond v2.1.8
        4. kaiju v1.9.2

1. Install Conda/Mamba Environment:

       mamba create -n gorg_amz_database
   
       mamba activate gorg_amz_database

       mamba install -c bioconda diamond=2.1.8 seqtk=1.4 pandas=2.0.3 kaiju=1.9.2

2. Clone repository: (still in progress):

       git clone https://github.com/jamesm224/gorg_db_update/

3. Prepare scripts for running (ensure this file is executable):

       chmod +x /database/run_kaiju.sh
       (insert appropriate input files for running Kaiju output)

4. Run the script against your dataset!

        sbatch main_run.sh
   
            OR
   
        ./main_run.sh

