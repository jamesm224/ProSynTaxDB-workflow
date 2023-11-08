# Pro/Syn Core Gene Alignment Pipeline (DRAFT)
Hey Future Researchers who use this! Here are the scripts used to generate/annotate Marine Prochlorococcus and Synechococcus phylogenetic trees like the figure below from the core genes of these elements! This should hopefully be an easy to replicate usage.

Dependencies (These were the versions we used, but other verisions may work):

    a. blast v2.14.0
    b. seqtk v1.4
    c. clustalo v1.2.4
    d. biopython v1.81
    e. fasttree v2.1.11

1. Install Conda/Mamba Environment:

       mamba create -n gorg_database_temp_name
   
       mamba activate gorg_database_temp_name

       mamba install -c conda-forge biopython=1.81

       mamba install -c bioconda blast=2.14.0 seqtk=1.4 clustalo=1.2.4 fasttree=2.1.11

2. Clone repository: (still in progress)

       git clone https://github.com/jamesm224/gorg_db_update/
   
3. Ensure that the following files are present in a script directory:
    
        1. 01_blastp.slurm
            - The number of files you want to run should likely be adjusted for your own jobs
            - #SBATCH --array=1-1%1
        2. 01_blastp_extended_genomes.slurm (OPTIONAL)
            - Optional scripts for any jobs with more than 500 genomes
            - Copy of 01_blastp.slurm (if used must add additional 0#_completion_flag.txts to pipeline)
        3. 02_clustalo.slurm
        4. 03_renamed_alignments.slurm (OPTIONAL)
        5. 04_fasttree.slurm
        6. fasta_to_phyliprelaxed.py
        7. main_run.sh
  
5. Prepare scripts for running (ensure this file is executable):

       chmod +x main_run.sh

6. Update the main_run.sh and make sure all appropriate files are present 
(Please include the full path of each variable)
    
        1. WORKDIR - working directory
        2. CYCOGBLASTDIR - directory with cycogs
        3. NAMESFILE - list file containing names of every genome in phylogeny
        4. INPUTDIR - input directory containing each individual protein faa
            - Files should be labeled (genome_NODE_1, genome_NODE_2....)
            - Numbers indicate number of each protein in genome
        5. BLASTDIR - name of directory for blast outputs (whatever you would like to call it)
        6. FULLPROTEIN - file containing every protein fasta
        7. ALIGNMENTDIR - name of directory for alignments outputs (whatever you would like to call it)
        8. CYCOGANNOTATIONS - CyCOG annotations as a txt file (should be present in info directory)
            -OPTIONAL - copy CyCOG faa and make logs directory for outputs

7. Run the script first (a optional renaming script can be run 03_renamed_alignments.slurm to fix naming errors)

        sbatch main_run.sh
   
            OR
   
        ./main_run.sh

8. Then download the output alignments_directory, and use MEGA (concatanate sequence alignments function) to generate a fasta sequence of all genomes
9. Process this newly generate .fas file into 04_fasttree.slurm to create your phylogeny!
    1. The Fasttree settings are easily changeable too!

            sbatch 04_fasttree.slurm

10. Hopefully this a fairly easy and streamline pipeline but reach out to Paul or James for any questions!


Good luck!



