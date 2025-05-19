# ProSynTax Workflow: taxonomic classification of *Prochlorococcus* and *Synechococcus*


## Introduction
Here we present a workflow that accompanies ProSynTax - a curated protein sequence dataset aimed at enhancing the taxonomic resolution of *Prochlorococcus* and *Synechococcus* classification. ProSynTax includes proteins from 1,260 genomes of *Prochlorococcus* and *Synechococcus*, including single amplified genomes, high-quality draft genomes, and newly closed genomes. Additionally, ProSynTax incorporates proteins from 27,799 genomes of marine heterotrophic bacteria, archaea, and viruses to assess microbial and viral communities surrounding *Prochlorococcus* and *Synechococcus*. This resource enables accurate classification of picocyanobacterial clusters/clades/grades in metagenomic data – even when present at 0.60% of reads for *Prochlorococcus* or 0.09% of reads for *Synechococcus*. 

![Phylogenetic Tree](docs/images/figure1.svg "Phylogenetic Tree")


## Publication 
This workflow and the accompanying ProSynTax dataset is described in:  
         [ADD CITATION]

## Table of Contents
* Setting up the Workflow
  * [Installing the ProSynTax Workflow](#installing-the-prosyntax-workflow) 
  * [Installing ProSynTax](#installing-prosyntax)
  * [Installing Dependencies](#installing-dependencies)
  * [Edit Workflow Parameters](#edit-workflow-parameters)
* Running the Workflow
  * [Submitting Main Script](#submitting-main-script)
  * [Troubleshooting Guides](#troubleshooting-guides)
* [Pipeline Workflow](#pipeline-workflow)
* Results
  * [Raw Counts Output](#raw-counts-output)
  * [Normalized Genome Equivalent Output](#normalized-genome-equivalent-output)
* [Limit of Detection Filtering](#limit-of-detection-filtering)
* [Intermediate Files](#intermediate-files)


## Setting up the Workflow
### Installing the ProSynTax Workflow
1. Clone the ProSynTax-workflow Github repository into your working directory:  

       # (optional) create a new project directory
       mkdir my_classification_project
       cd my_classification_project  # change directory into project 

- Create a copy of the workflow into your current path:  

       git clone https://github.com/jamesm224/ProSynTax-workflow/

### Installing ProSynTax
All files associated with this workflow can be downloaded from the [Zenodo repository](https://doi.org/10.5281/zenodo.14889681) (DOI 10.5281/zenodo.14889681). 

Download the following **required** files into a directory on your machine: 
1. ProSynTax_nodes.dmp
2. ProSynTax_names.dmp
3. ProSynTax_file.fmi
4. CyCOG6.dmnd

- **Note**: The path to these files will be needed later in the `inputs/config.yaml` file in step 1 of section [Edit Workflow Parameters](#edit-workflow-parameters). 

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

### Edit Workflow Parameters
#### 1. Edit ```inputs/config.yaml```:  
This is the experimental configuration file, where you will specify ProSynTax file paths, directory paths, and more. 

- **Required** edits:  
  - `nodes_file`: path to your installation of ProSynTax_nodes.dmp file for Kaiju (completed earlier in step [Installing ProSynTax](#installing-prosyntax)). 
  - `names_file`: path to your installation of ProSynTax_names.dmp file for Kaiju. 
  - `fmi_file`: path to your installation of ProSynTax_file.fmi file for Kaiju. 
  - `diamond_file`: path to your installation of CyCOG6.dmnd dataset file for BLAST. 
  - `genus_list`: list of genus you would like to extract raw read count for. 
    - Default: ['Synechococcus', 'Prochlorococcus', 'unclassified']
    - "unclassified": include reads that are labeled "unclassified" or "cannot be assigned to a (non-viral) genus" by Kaiju. 
    - Reads classified as other genus not listed will be summed into 1 group called "other_genus". 
    - Refer to [Results](#results) for more information. 
  - `scratch directory`: path to folder for storing intermediate files. 
    - Such as: trimmed read files, Kaiju outputs, and Blast outputs. 
  - `results directory`: path to directory for storing final output files: "summary_read_count.tsv" and "normalized_counts.tsv".

#### 2. Create ```inputs/samples.tsv```: 
This file should contain metadata for your samples. We have created an example Python script that creates a samples.tsv file from raw read files located in a directory: [Example Python Script](inputs/example/make_samples_tsv.py). 

- **Required** columns: 
  - `sample`: unique name for sample. 
  - `forward read`: path to forward read file. 
  - `reverse read`: path to reverse read file.
- Optional: 
  - Feel free to add any other sample metadata columns as they will not impact the workflow. 

#### 3. Edit ```profile/config.yaml```:  
This file contains Snakemake specifications and compute resource (HPC) specifications. For tips on determining your HPC cluster resource specification for this section, visit [HPC Resource Tips](docs/readme_extras/resource_tips.md).

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
    - For example, you ran this workflow in `/home/my_username/project1/` and would like to run the workflow on another project, the "conda-prefix" path for the newer project would be: "/home/my_username/project1/.snakemake/conda"

#### 4. Edit ```run_classify_smk.sbatch```:
This file is the main Snakemake workflow submission.  

  - `--partition`: name of HPC partition to send main run to.
    - To check what partitions you have access to: `sinfo`.
  - `--time`: total amount of time to allocate to the **entire** workflow.
    - Make sure this time does not exceed the partition's maximum alloted time.
    - You should allocate more time the more samples you have.



## Running the Workflow
### Submitting Main Script
Run the pipeline by submitting `run_classify_smk.sbatch` script to the HPC cluster:   

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

### Troubleshooting Guide
We have some tips for troubleshooting and debugging for common errors located [here](docs/readme_extras/debugging_tips.md). 


## Pipeline Workflow
Below is a description of the steps in ProSynTax workflow. 

![Workflow Overview](docs/images/figure2.svg "Pipeline Workflow")

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
  - Reads are classified against the ProSynTaxSB using [Kaiju v1.10.1](https://github.com/bioinformatics-centre/kaiju) with parameters: 
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
     - Extracted FASTQ header names are used to extract FASTA sequence using [seqtk vr82](https://github.com/lh3/seqtk) for downstream BLAST 
  - Extracted FASTA sequences are compared against 424 CyCOGs using DIAMOND [Blastx v2.1.11](https://github.com/bbuchfink/diamond) sequence aligner with parameter: 
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

## Limit of Detection Filtering
To assess the accuracy of *Prochlorococcus* and *Synechococcus* cluster/clade/grade classifications, we generated mock metagenome sequence datasets and conducted simulations following the methods outlined in Coe et al. (2025) to calculate misclassification rates. To maintain misclassification rates below either 10% or 5%, we determined the minimum *Prochlorococcus*:*Synechococcus* (or vice versa) ratios, as detailed below. For broader classifications at the cluster or ecotype level, a 10% misclassification rate is sufficient.  However, for more precise subcluster/clade/grade delineations, we recommend using a 5% false positive rate threshold.

Scripts used for genome subsetting and read simulation are located in the [validation](validation) directory. 

### *Prochlorococcus* Filtering Parameters
#### 5% Misclassification Parameters  
- *Prochlorococcus* Abundance > 0.57% 
  - Counts of *Prochlorococcus* reads out of *all* classified reads 
- Ratio of *Prochlorococcus*:*Synechococcus* > 0.43
  - Ratio calculated by counts of *Prochlorococcus* divided by counts of *Synechococcus*

#### 10% Misclassification Parameters
- *Prochlorococcus* Abundance > 0.28% 
  - Counts of *Prochlorococcus* reads out of all classified reads 
- Ratio of *Prochlorococcus*:*Synechococcus* > 0.24
  - Ratio calculated by counts of *Prochlorococcus* divided by counts of *Synechococcus*

### *Synechococcus* Filtering Parameters
#### 5% Misclassification Parameters  
- *Synechococcus* Abundance > 0.09% 
  - Counts of *Synechococcus* reads out of all classified reads 
- Ratio *Synechococcus*:*Prochlorococcus* > 0.2 
  - Ratio calculated by counts of *Synechococcus* divided by counts of *Prochlorococcus*

#### 10% Misclassification Parameters
- *Synechococcus* Abundance > 0.04% 
  - Counts of *Synechococcus* reads out of *all* classified reads 
- Ratio *Synechococcus*:*Prochlorococcus* > 0.10
  - Ratio calculated by counts of *Synechococcus* divided by counts of *Prochlorococcus*


## Visualization
For visualization of clade/grade/cluster composition, we have devised a list of HEX color codes, which are located in the [taxon_colors](docs/taxon_colors) directory. 

## Intermediate Files
This workflow produces several intermediate files that may be useful for additional analysis. Descriptions of these files can be found [here](docs/readme_extras/intermediate_files.md). 
