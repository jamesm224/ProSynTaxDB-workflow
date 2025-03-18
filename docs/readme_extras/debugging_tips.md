# Troubleshooting Guide
Guide on debugging and troubleshooting when the pipeline runs into an error. 

**Some tips for debugging:**
- Each rule/step in the pipeline will get its own `.err` log file that often details why the job failed. When a rule/step fails, check the subfolder with that rule's name and sample. 
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