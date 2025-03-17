# ProSynTaxDB Workflow: taxonomic classification of *Prochlorococcus* and *Synechococcus*

## Introduction

Here we present ProSynTaxDB, a curated protein sequence database and accompanying workflow aimed at enhancing the taxonomic resolution of Prochlorococcus and Synechococcus classification. ProSynTaxDB includes proteins from 1,260 genomes of Prochlorococcus and Synechococcus, including single amplified genomes, high-quality draft genomes, and newly closed genomes. Additionally, ProSynTaxDB incorporates proteins from 27,799 genomes of marine heterotrophic bacteria, archaea, and viruses to assess microbial and viral communities surrounding Prochlorococcus and Synechococcus. This resource enables accurate classification of picocyanobacterial clusters/clades/grades in metagenomic data – even when present at 0.60% of reads for Prochlorococcus or 0.09% of reads for Synechococcus. 

![updated_genomes (2)](https://github.com/jamesm224/gorg_db_update/assets/86495895/181bba39-b338-4553-97c3-8a7f553ec7fa)


## Publication 
[ADD CITATION]

## Table of Contents
* Setting up the Workflow
  * [Installing the ProSynTaxDB Workflow](#installing-the-prosyntaxdb-workflow) 
  * [Installing ProSynTaxDB](#installing-prosyntaxdb)
  * [Installing Dependencies](#installing-dependencies)
  * [Edit Workflow Specifications](#edit-workflow-specifications)
* Running the Workflow
  * [Submitting Main Script](#submitting-main-script)
  * [Troubleshooting Guides](#troubleshooting-guides)
* [Pipeline Workflow](#pipeline-workflow)
* Results
  * [Raw Counts Output](#raw-counts-output)
  * [Normalized Genome Equivalent Output](#normalized-genome-equivalent-output)
  * [Limit of Detection](#limit-of-detection)
* [Intermediate Files](#intermediate-files)



## Setting up the Workflow
### Installing the ProSynTaxDB Workflow
1. Clone the ProSynTaxDB-workflow Github repository into your working directory:  

       # (optional) create a new project directory
       mkdir my_classification_project
       cd my_classification_project  # change directory into project 

- Create a copy of the workflow into your current path:  

       git clone https://github.com/jamesm224/ProSynTaxDB-workflow/

### Installing ProSynTaxDB
All files associated with this workflow can be downloaded from the [Zenodo repository](https://zenodo.org/records/14889681?preview=1&token=eyJhbGciOiJIUzUxMiJ9.eyJpZCI6IjEwM2VjMmJlLTU2NzEtNDEyNC1hZTQwLWY0NDFkNzUwMTU4OSIsImRhdGEiOnt9LCJyYW5kb20iOiI4NjkwMTllMGQ4MWYyYTU1MzBkMDYzYWU3MmYwOTNhNSJ9.9Nedfc8bI5MZ4Mio_TaWmq26RYLHCf2mSdXpupnHUFoDb9CuAKTdL7cb88SeiSA1bW0Ft-XYe1YlmkVtijWQbg) (DOI 10.5281/zenodo.14889681). 

Download the following **required** files into a directory on your machine: 
1. ProSynTaxDB_nodes.dmp
2. ProSynTaxDB_names.dmp
3. ProSynTaxDB_file.fmi
4. CyCOG6.dmnd

- **Note**: The path to these files will be needed later in the `inputs/config.yaml` file in step 1 of section [Edit Workflow Specifications](#edit-workflow-specifications). 

### Installing Dependencies
1. Install Mamba following instructions on the [official Mamba documentation](https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html). Or follow the steps below for installation into Linux system: 

- Download miniforge (contains mamba) from Github (for Linux):  

       wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh

- Run the installer and set up mamba on your computer. :  

       # when prompted, press ENTER or enter YES
       bash Miniforge3-Linux-x86_64.sh 

- Once installation is complete, open a new terminal window  

       # check that installation worked
       mamba -V  # prints version 

- (Optional) This makes it so the base conda environment won’t automatically activate whenever you open a new terminal:  

       conda config --set auto_activate_base false 

- (Optional) Delete the installer  

       rm Miniforge3-Linux-x86_64.sh

2. Then, install [Snakemake v7.32.4](https://snakemake.readthedocs.io/en/stable/) into a new mamba environment: 

       # create a new mamba environment named snakemake and install snakemake v7.32.4
       mamba create -c bioconda -c conda-forge -n snakemake snakemake=7.32.4
   
- (Optional) test that your installation worked: 

       mamba activate snakemake  # activate the environment 
       snakemake --version  # print snakemake version 
       mamba deactivate  # deactivate snakemake environment 

### Edit Workflow Specifications
#### 1. Edit experimental configuration file ```inputs/config.yaml```:  
- **Required** edits:  
  - `nodes_file`: path to your installation of ProSynTaxDB_nodes.dmp file for Kaiju (completed earlier in step [Installing ProSynTaxDB](#installing-prosyntaxdb)). 
  - `names_file`: path to your installation of ProSynTaxDB_names.dmp file for Kaiju. 
  - `fmi_file`: path to your installation of ProSynTaxDB_file.fmi file for Kaiju. 
  - `diamond_file`: path to your installation of CyCOG6.dmnd database file for BLAST. 
  - `genus_list`: list of genus you would like to extract raw read count for. 
    - Default: ['Synechococcus', 'Prochlorococcus', 'unclassified']
    - "unclassified": include reads that are labeled "unclassified" or "cannot be assigned to a (non-viral) genus" by Kaiju. 
    - Reads classified as other genus not listed will be summed into 1 group called "other_genus". 
    - Refer to [Interpreting Output Files](#interpreting-output-files) for more information. 
  - `scratch directory`: path to folder for storing intermediate files. 
    - Such as: trimmed read files, Kaiju outputs, and Blast outputs. 
  - `results directory`: path to directory for storing final output files: "summary_read_count.tsv" and "normalized_counts.tsv"

#### 2. Create ```inputs/samples.tsv``` file containing metadata for your samples: 
We have created an example Python script that creates a samples.tsv file from raw read files located in a directory: [Example Python Script](inputs/example/make_samples_tsv.py). 

- **Required** columns: 
  - `sample`: unique name for sample. 
  - `forward read`: path to forward read file. 
  - `reverse read`: path to reverse read file.
- Optional: 
  - Feel free to add any other sample metadata columns as they will not impact the workflow. 

#### 3. Edit Snakemake specifications and resource specifications in ```profile/config.yaml``` file:  
For tips on figuring out your cluster resource specification for this section, visit [HPC Resource Tips](docs/readme_extras/resource_tips.md).

- **Required** edits:
  - `jobs`: number of jobs you would like to run at once on the compute cluster. 
  - `default-resources: partition`: partition name to submit jobs to. 
  - `default-resources: time`: amount of time to allocate to all jobs in pipeline. 
  - `default-resources: mem`: amount of memory to allocate to "default" rules (those not listed in `set-resources` section). 
  - `set-resources: cpus_per_task`: number of cores to allocate for multi-threaded jobs. 
  - `set-resources: mem`: amount of memory to allocate for multi-threaded jobs. 
- Optional edits:
  - `conda-prefix`: path to previous conda installation, located in the hidden `./snakemake` directory.
    - If you have run this pipeline before, you can save time on newer runs by referencing previous conda installations.  
    - For example, you ran this workflow in `/home/my_username/project1/` and would like to run the workflow on another project, the "conda-prefix" path for the newer project would be: ./home/"my_username/project1/snakemake/conda"

#### 4. Edit the main Snakemake workflow submission ```run_classify_smk.sbatch``` file:
  - `--partition`: name of HPC partition to send main run to.
    - To check what partitions you have access to: `sinfo`
  - `--time`: total amount of time to allocate to the entire workflow. 
    - Make sure this time does not exceed the partition's maximum alloted time



## Running the Workflow
### Submitting Main Script
Run the pipeline by submitting `run_classify_smk.sbatch` script to cluster:   

    sbatch run_classify_smk.sbatch  


Track Workflow Progress: 
- Snakemake tracks each step of the workflow (called rule) and logs progress in: `logs/[SLURM_JOB_ID].err`. 
- In addition, each individual snakemake rule/step will create its own sub-directory to store rule-specific log files for each instance of that rule/step. 
  - For example `logs/run_trim_PE/sample_1.err` logs the read trimming step of sample_1
- Once all steps in the pipeline have completed, the file ```logs/[SLURM_JOB_ID].err``` will end with the following:
  ```
  N of N steps (100%) done
  Complete log: .snakemake/log/YYYY-MM-DDTXXXXXX.XXXXXX.snakemake.log
  ```

### Troubleshooting Guides
**Some tips for debugging:**
- Each rule/step in the pipeline will get its own .err log file. When a rule/step fails, check the subfolder with the rule's name and sample where it failed. 
- If you get "OOM" ("Out of memory") errors, increase memory requests in `profile/config.yaml` file. 
  - This will often be logged in rule-specific log file, instead of the main Snakemake log file. 

**Locked directory error**:  
If you get the error message "Error: Directory cannot be locked":
- Make sure that all jobs from your previous run of the pipeline have completed/cancelled
  - To cancel all jobs submitted by your account to a particular partition: 
    ```
    scancel -u <your_username> -p <partition_name>
    ```
- In `profile/config.yaml` file: uncomment line "unlock: True" (remove the "#")
- Activate your Snakemake conda environment in the command line terminal: 
  ```
  mamba activate snakemake
  ```
- Run Snakemake to unlock the workflow: 
  ```
  snakemake --profile profile
  ```
- In `profile/config.yaml` file: comment line "unlock: True" (add the "#")
- Re-run the pipeline following: [Submitting Main Script](#submitting-main-script). The lock should now be removed. 



## Pipeline Workflow
Below is a description of the steps in ProSynTaxDB workflow. 

![Workflow Overview](docs/images/figure_2.svg "Pipeline Workflow")

**1. Quality Control:**  
  - Low-quality regions and adapter sequences are removed from raw Illumina paired-end reads using [BBDuk v37.62](https://archive.jgi.doe.gov/data-and-tools/software-tools/bbtools/bb-tools-user-guide/bbduk-guide/) from BBTools suite with parameters: 
    - `minlen=25`: discard reads shorter than 25bp after trimming to Q10 
    - `qtrim=rl`: quality-trimming of both left and ride side
    - `trimq=10`: quality-trim to Q10 using the Phred algorithm
    - `ktrim=r`: kmer-trim; once a reference kmer is matched in a read, that kmer and all the bases to the right will be trimmed, leaving only the bases to the left
    - `k=23`: Kmer length used for finding contaminants.  Contaminants shorter than k will not be found. 
    - `mink=11`: Reads need at least this many matching kmers to be considered as matching the reference.
    - `hdist=1`: Maximum Hamming distance for ref kmers

**2. Taxonomic Classification:**  
  - Reads are classified against the ProSynTaxSB using Kaiju v1.10.1 with parameters: 
    - `-m 11`: Minimum match length
    - `-s 65`: Minimum match score in Greedy mode
    - `-E 0.05`: Minimum E-value in Greedy mode
    - `-x`: Enable SEG low complexity filter
    - `-e 5`: Number of mismatches allowed in Greedy mode

**3. Raw Read Count Summary:** 
  - Kaiju classification summaries are obtained using `kaiju2table` command. 
    - All output files are aggregated into final results table "summary_read_count.tsv" using `workflow/scripts/classification_summary.py`.   

**4. Clade Normalization:**  
  - Full taxon paths are added to Kaiju output in Step 2 using `kaiju-addTaxonNames` command with the parameters: 
    - `-p`: print the full taxon path instead of just the taxon name.
    - `-u`: omit unclassified reads (saves disk space compared to output of all reads).
  - FASTQ header name and full taxonomic classification of reads classified as "*Prochlorococcus*" and "*Synechococcus*" by Kaiju are extracted using the Bash command `grep`
     - Extracted FASTQ header names are used to extract FASTA sequence using seqtk vr82 for downstream BLAST 
  - Extracted FASTA sequences are compared against 424 CyCOGs using DIAMOND Blastx v2.1.11 sequence aligner with parameter: 
    - `max-target-seqs 1`: maximum number of target sequences per query to report alignments for. 
  - Using the custom Python script `normalize_all_cycog.py`, reads are normalized by clade following these steps: 
    - Filter for reads with hits to the 424 CyCOGs protein database 
    - Obtain sum of alignment length 
    - Divide alignment length of read mapped to CyCOG by the sum of 424 CyCOG mean length, which is 59404.6391
  - All normalized output files are aggregated into file results table `normalized_counts.tsv`. 



## Results
This pipeline outputs 2 main output files (listed below), both located in "results directory" path specified in ```inputs/config.yaml``` file. 

### 1. Raw Counts Output
The output file `summary_read_count.tsv` contains the total classified raw read counts for the genus listed in ```inputs/config.yaml``` file.   
- Column Description:  
  - `sample_name`: name of sample
    - Same as the "sample" column in ```samples.tsv```.
  - `taxon_name`: name of genus 
    - Taxons in this column are defined by the genus list specified in `inputs/config.yaml` file. 
  - `reads`: number of reads Kaiju classified as specified genus in "taxon_name" 
  - `percent`: percent of this genus relative to all reads in the sample 

### 2. Normalized Genome Equivalent Output
The output file `normalized_counts.tsv` contains normalized genome equivalent for each *Prochlorococcus* and *Synechococcus* clade/subclade/ecotype in the sample.  
- Column Description:  
  - `sample_name`: name of sample; same as the "sample" column in ```samples.tsv```.
  - `genus`: genus classified by Kaiju ("*Prochlorococcus*" or "*Synechococcus*")
  - `clade`: ecotype/cluster/clade/grade classified by Kaiju 
  - `alignment_length`:  sum of alignment length of unique hits from Diamond Blast 
  - `genome_equivalents`: normalized abundance of classified ecotype/cluster/clade/grade in sample 
    - Refer to "Read Normalization" Step in [Pipeline Workflow](#pipeline-workflow) for more information on how this value was calculated 

### Limit of Detection Filtering
In order to determine the minimal abundance of *Prochlorococcus* and *Synechococcus*, we performed simulations described in publication listed in the [Publication](#publication) section. 

We recommend the 5% false positive rate threshold for accurate cluster/clade/grade delineations.

**5% Misclassification Parameters** (Cluster/Grade/Clade Level  Identification):  
- *Prochlorococcus* Abundance > 0.57% 
  - Counts of *Prochlorococcus* reads out of all classified reads 
- *Prochlorococcus*:*Synechococcus* ratio > 0.43
  - Ratio calculated by counts of *Prochlorococcus* divided by counts of *Synechococcus*
- *Synechococcus* Abundance > 0.09% 
  - Counts of *Synechococcus* reads out of all classified reads 
- *Synechococcus*:*Prochlorococcus* ratio > 0.2 
  - Ratio calculated by counts of *Synechococcus* divided by counts of *Prochlorococcus*

**10% Misclassification Parameters** (Higher Level Taxonomic Identification):  
- *Prochlorococcus* Abundance > 0.28% 
  - Counts of *Prochlorococcus* reads out of all classified reads 
- *Prochlorococcus*:*Synechococcus* ratio > 0.24
  - Ratio calculated by counts of *Prochlorococcus* divided by counts of *Synechococcus*
- *Synechococcus* Abundance > 0.04% 
  - Counts of *Synechococcus* reads out of all classified reads 
- *Synechococcus*:*Prochlorococcus* ratio > 0.10
  - Ratio calculated by counts of *Synechococcus* divided by counts of *Prochlorococcus*

## Intermediate Files
The following are descriptions of intermediate files, located in "scratch directory" path specified in ```inputs/config.yaml```, that may be useful for further analysis:  

- "classified_kaiju_read_output/*_kaiju.txt": 
  - Output from rule "kaiju_run", which runs the base Kaiju command 
  - Columns: read status, read name, taxon_id

- "classified_kaiju_read_output/*_kaiju_summary.tsv": 
  - Output from rule "kaiju_summary_taxa", which runs the Kaiju command ```kaiju2table``` to summarize counts of reads for each genus from "*_kaiju.txt" file of the same sample. 
  - These intermediate files are inputs for final output table: `summary_read_count.tsv`
  - Columns: file, percent reads, taxon_id, taxon_name

- "classified_kaiju_read_output/*_names.out": 
  - Output from rule "kaiju_name", which runs the Kaiju command ```kaiju-addTaxonNames``` to add full taxon path to read name
  - Columns: read status, read name, taxon_id, full taxon
