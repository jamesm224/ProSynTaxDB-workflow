# GORG-AMZ Classifer

Hey Future Researchers who use this! Here are the code repository for the GORG-AMZ Classifier.

Made by James Mullet and Nhi Vo!
![updated_genomes (2)](https://github.com/jamesm224/gorg_db_update/assets/86495895/181bba39-b338-4553-97c3-8a7f553ec7fa)
This figure depicts a Phylogenetic Tree of All Pro and Syn in this Database

# How to Install the Pipeline:

1. Clone repository:

       git clone https://github.com/jamesm224/gorg_amz_classifier/

2. Install Dependencies using Conda/Mamba:  
Install Mamba following instructions on the [official Mamba documentation](https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html).  
Then, create a new environment with snakemake:

       mamba create -c bioconda -c conda-forge -n snakemake snakemake
   
       mamba activate snakemake

# Setting Up the Pipeline:

1. Edit ```inputs/config.yaml``` file:  
    - Required edits:  
      - Change "nodes_file": to path to nodes.dmp file for Kaiju. 
      - Change "names_file": to path to names.dmp file for Kaiju. 
      - Change "fmi_file": to path to .fmi file for Kaiju. 
      - Change "diamond_file": to path to Cycog6 database file for Blast. 
      - Change "genus_list": to list of genus you would like to extract read count for. 
        - Default: ['Synechococcus', 'Prochlorococcus', 'unclassified']
        - Notes: 
          - Reads classified as other genus not listed will be summed into 1 group called "other_genus". 
          - "unclassified": include reads that are labeled "unclassified" or "cannot be assigned to a (non-viral) genus" by Kaiju. 
        - Refer to [Interpreting Output Files](#interpreting-output-files) for more information. 
      - Change "scratch directory": to path to folder for storing intermediate files. Such as: Kaiju outputs, Blast outputs. 
      - Change "results directory": to path to directory for storing final output files: "summary_read_count.tsv" and "normalized_counts.tsv"

    - Optional:  
      - Change "experiment_name": to name of your experiement. 

2. Create ```inputs/samples.tsv``` file for your samples: 
    - Required columns: 
      - "sample": unique name for sample. 
      - "forward read": path to forward read. 
      - "reverse read": path to reverse read.
    - Feel free to add any other sample metadata columns. 

3. Edit ```profile/config.yaml``` file: 
    - Required edits:
      - Change "jobs": to number of jobs you would like to run at once. 
      - Change "default-resources: time": to amount of time to allocate to all jobs in pipeline. 
      - Change "default-resources: partition": to partition name to submit jobs to. 
      - Change "default-resources: mem": to amount of memory to allocate. 
      - Change all "set-resources: cpus_per_task": to number of cores to allocate for multi-threaded jobs. 
      - Change all "set-resources: mem": to amount of memory to allocate for multi-threaded jobs. 

4. Edit ```run_classify_smk.sbatch``` file:
    - Change "--time": to amount of time to allocate to pipeline. 
    - Change "--partition": to name of partition to send main run to. 

5. Run pipeline: 
    - Submit slurm script to cluster:  
       ```
       sbatch run_classify_smk.sbatch
       ```

6. Track Progress: 
    - Snakemake log will be located in ```logs/[SLURM_JOB_ID].err```. This file will contain messages about pipeline progress. 
    - In addition, each individual snakemake rule will create its own sub-directory for rule-specific log files. 
    - Debug errors accordingly, if any. 
    - Once all steps in the pipeline have completed, the file ```logs/[SLURM_JOB_ID].err``` will end with the following:
      ```
      N of N steps (100%) done
      Complete log: .snakemake/log/YYYY-MM-DDTXXXXXX.XXXXXX.snakemake.log
      ```

# Test Run: 

The ```inputs/example``` directory includes an example Python script to make the ```samples.tsv``` file located in ```inputs/``` from the read files in ```inputs/example/raw_reads/```.  

To test run the pipeline on these files provided, follow all the steps in [Setting Up the Pipeline](#setting-up-the-pipeline) above except for Step 2. 


# Interpreting Output Files:

This pipeline outputs 2 main output files, both located in "results directory" path specified in ```inputs/config.yaml``` file. 

1. "summary_read_count.tsv": contains the total classified read counts for the genus listed in ```inputs/config.yaml``` file.   
    - Columns:  
      - taxon_name: name of genus. Values in this column are affected by genus list in config.yaml file. 
      - reads: number of reads Kaiju classified as specified genus in "taxon_name" 
      - percent: percent of this genus out of all reads in sample 
      - sample_name: name of sample; same as "sample" column in ```samples.tsv```.

2. "normalized_counts.tsv": contains normalized genome equivalent for each Prochlorococcus.  
    - Columns:  
      - sample_name: name of sample; same as "sample" column in ```samples.tsv```.
      - genus: genus classified by Kaiju ("Prochlorococcus" or "Synechococcus"). 
      - clade: clade/subclade/ecotype classified by Kaiju. 
      - alignment_length:  sum of alignment length of unique hits from Diamond Blast. 
      - genome_equivalents: normalized abundance of classified clade in sample. 
        - Refer to "Read Normalization" Step in [Pipeline Workflow](#pipeline-workflow) for more information on how this value was calculated. 

# Pipeline Workflow: 

![Workflow Overview](workflow/images/ReadClassifierWorkflow.svg "Pipeline Workflow")

1. Read Trimming: 
    - Raw reads are trimmed using bbduk with parameters: minlen=25 qtrim=rl trimq=10 ktrim=r k=23 mink=11 hdist=1
2. Kaiju Read Classification: 
    - Reads are classified using kaiju with parameters: -m 11 -s 65 -E 0.05 -x -e 5
    - Full taxon paths are added to kaiju output using ```kaiju-addTaxonNames``` command. 
    - Kaiju classification summaries are obtained using ```kaiju2table``` command. 
      - All output files are aggregated into final results table "summary_read_count.tsv" using ```workflow/scripts/classification_summary.py```
3. Read Normalization: 
    - Reads classified as "Prochlorococcus" and "Synechococcus" by Kaiju are extracted and compared against 424 CyCOGs using DIAMOND sequence aligner.  
    - Reads with hits to 424 CyCOGs are used to normalize read count of each classified clade. 
    - All normalized output files are aggregated into file results table "normalized_counts.tsv". 


# Intermediate Files Description: 

The following are descriptions of intermediate files, located in "scartch directory" path specified in ```inputs/config.yaml```, that may be useful for further analysis: 
- "classified_kaiju_read_output/*_kaiju.txt": 
  - Output from rule "kaiju_run", which runs the base Kaiju command 
  - Columns: read status, read name, taxon_id
- "classified_kaiju_read_output/*_kaiju_summary.tsv": 
  - Output from rule "kaiju_summary_taxa", which runs the Kaiju command ```kaiju2table``` to summarize counts of reads for each genus from "*_kaiju.txt" file of the same sample. 
  - Columns: file, percent reads, taxon_id, taxon_name
- "classified_kaiju_read_output/*_names.out": 
  - Output from rule "kaiju_name", which runs the Kaiju command ```kaiju-addTaxonNames``` to add full taxon path to read name
  - Columns: read status, read name, taxon_id, full taxon
