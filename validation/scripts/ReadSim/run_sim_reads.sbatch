#!/bin/bash
#SBATCH -p newnodes   # sched_mit_chisholm
#SBATCH --job-name=readsim
#SBATCH --nodes=1        # Request one node
#SBATCH --exclusive      # Request the entire node
#SBATCH --time=12:00:00 # 5-0
#SBATCH --array=1-10%2
#SBATCH --output=data/logs/simulate_reads.%a.%j.out
#SBATCH --error=data/logs/simulate_reads.%a.%j.err

date

echo "SLURM Job ID: ${SLURM_JOB_ID}"
echo "Array index number: ${SLURM_ARRAY_TASK_ID} (out of: ${SLURM_ARRAY_TASK_MAX})"
echo "Array Job ID: ${SLURM_ARRAY_JOB_ID}"
echo "CPU Requested/Allocated for task: ${SLURM_CPUS_PER_TASK}"

eval "$(conda shell.bash hook)"
conda activate data

subset_num=${SLURM_ARRAY_JOB_ID}
genome_dir=path/to/genome/dir
outdir=path/to/output/dir
read_count=1000000  # 1 million total reads per sample

python3 simulate_reads.py ${subset_num} ${genome_dir} ${outdir} ${read_count} 

echo Done!
date