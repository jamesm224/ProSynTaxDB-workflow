# GORG-AMZ Classifer

Hey Future Researchers who use this! Here are the code repository for the GORG-AMZ Classifier.

# Phylogenetic Tree of All Pro and Syn used in Creating this Database
![updated_genomes (2)](https://github.com/jamesm224/gorg_db_update/assets/86495895/181bba39-b338-4553-97c3-8a7f553ec7fa)

# Where are the files?
1. pro_syn_classification - scripts for classification of pro/syn
2. Database - scripts and files for running the database

# How to Install the Pipeline

Dependencies (These were the versions we used, but other verisions may work):

        1. pandas v2.0.3
        2. seqtk v1.4
        3. diamond v2.1.8
        4. kaiju v1.9.2

1. Install Conda/Mamba Environment:

       mamba create -n gorg_amz_database
   
       mamba activate gorg_amz_database

       mamba install -c bioconda diamond=2.1.8 seqtk=1.4 pandas=2.0.3 kaiju=1.9.2

2. Install [nextflow](https://www.nextflow.io/docs/latest/install.html):
   
        curl -s https://get.nextflow.io | bash

3. Clone repository: (still in progress):

       git clone https://github.com/jamesm224/gorg_db_update/

4. Annotate sequences with GORG-AMZ database and normalize data

   nextflow run updated_run.nf \
    --input_reads '/path/to/input_data/*_{1,2}_sequence.fastq' \
    --nodes /path/to/final_ncbi_pro_nodes.dmp \
    --names /path/to/final_ncbi_pro_names.dmp \
    --fmi /path/to/final_MARMICRODB2_virus.fmi \
    --outputdir /path/to/output_directory \
    --dmnd /path/to/CyCOG6.dmnd

