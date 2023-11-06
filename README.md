# gorg_db_update

Hey Future Researchers who use this!

This should hopefully be an easy to replicate usage.

1. Create a conda/mamba environment with the following packages:
(These were the versions we used others may work)
    a. blast v2.14.0
    b. seqtk v1.4
    c. clustalo v1.2.4
    d. biopython v1.81
    e. fasttree v2.1.11

2. Ensure that the following files are present in a script directory:
    a. 01_blastp.slurm
    b. 01_blastp_extended_genomes.slurm (OPTIONAL)
        - Optional scripts for any jobs with more than 500 genomes
        - Copy of 01_blastp.slurm (if used must add additional 0#_completion_flag.txts to pipeline)
    c. 02_clustalo.slurm
        - The number of files you want to run should likely be adjusted for your own jobs
        - #SBATCH --array=1-1%1
    d. 03_renamed_alignments.slurm (OPTIONAL)
    e. 04_fasttree.slurm
    f. fasta_to_phyliprelaxed.py
    g. motherboard_script.sh

3. Update the motherboard_script.sh and make sure all appropriate files are present 
(Please include the full path of each variable)
    a. WORKDIR - working directory
    b. CYCOGBLASTDIR - directory with cycogs
    c. NAMESFILE - list file containing names of every genome in phylogeny
    d. INPUTDIR - input directory containing each individual protein faa
        - Files should be labeled (genome_NODE_1, genome_NODE_2....)
        - Numbers indicate number of each protein in genome
    e. BLASTDIR - name of directory for blast outputs (whatever you would like to call it)
    f. FULLPROTEIN - file containing every protein fasta
    g. ALIGNMENTDIR - name of directory for alignments outputs (whatever you would like to call it)
    h. CYCOGANNOTATIONS - CyCOG annotations as a txt file (should be present in info directory)
        -OPTIONAL - copy CyCOG faa and make logs directory for outputs

4. Run the motherboard_script.sh script first then use MEGA (concatanate sequence alignments function) to generate a fasta sequence of all genomes

5. Process this newly generate .fas file into 04_fasttree.slurm to create your phylogeny!
    a. The Fasttree settings are easily changeable too!

6. Hopefully this a fairly easy and streamline pipeline but reach out to Paul or James for any questions!

Good luck!
