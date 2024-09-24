# GORG-AMZ Classifer

Hey Future Researchers who use this! Here are the code repository for the GORG-AMZ Classifier.

Made by James Mullet and Nhi Vo!

# Phylogenetic Tree of All Pro and Syn in this Database
![updated_genomes (2)](https://github.com/jamesm224/gorg_db_update/assets/86495895/181bba39-b338-4553-97c3-8a7f553ec7fa)

# How to Install the Pipeline:

1. Install Conda/Mamba Environment:

       mamba create -c bioconda -c conda-forge -n snakemake snakemake
   
       mamba activate snakemake

2. Clone repository: (still in progress):

       git clone https://github.com/jamesm224/gorg_amz_classifier/

# Usage:

1. Annotate sequences with GORG-AMZ database and normalize data. Configure the config files located in the ```config/``` and the ```input/``` directories. Additionally, create a samples.tsv file. An example is located in the ```input/``` directory.

2. Run Snakemake Script - we have included a test example, which should run once the config and input directories are properly set up. Please try running the following command on the test data to ensure the pipeline was installed correctly.
   
   ```sbatch run_classify_smk.sbatch```

# Interpreting Output Files:

Files Located in ```results/``` directory

1. summary_read_count.tsv - contains the overall read counts for Prochlorococcus, Synechococcus, and Unclassified reads detected by the classifier
2. 

     

