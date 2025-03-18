# Intermediate Files
Intermediate files are files that are produced by the pipeline but are not final results tables located in the "results directory". Below are descriptions of intermediate files, located in "scratch directory" path specified in ```inputs/config.yaml```, that may be useful for further analysis:  

**classified_kaiju_read_output/*_kaiju.txt**  
Output from Snakemake rule "kaiju_run", which runs the base Kaiju command. 
- These files are useful when you want to run additional custom Kaiju commands
  - e.g. `kaiju2krona` command which creates interactive Krona plots 
  - e.g. `kaiju2table` to summarize read count on another taxonomic level that is not the default genus. 
- Columns: [read status, read name, taxon_id]

**classified_kaiju_read_output/*_kaiju_summary.tsv**  
Output from Snakemake rule "kaiju_summary_taxa", which runs the Kaiju command ```kaiju2table``` to summarize counts of reads for each genus from "*_kaiju.txt" file of the same sample. 
- These files are useful when you want to perform additional custom raw read count parsing 
- Note: These intermediate files are further aggregated/summarized to create the final output table: `summary_read_count.tsv`
- Columns: [file, percent reads, taxon_id, taxon_name]

**classified_kaiju_read_output/*_names.out**  
Output from Snakemake rule "kaiju_name", which runs the Kaiju command ```kaiju-addTaxonNames``` to add full taxon path to each read in the sample.  
- Columns: [read status, read name, taxon_id, full taxon]