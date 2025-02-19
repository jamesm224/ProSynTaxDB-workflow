"""
"""
import yaml
import os
import argparse
import subprocess
import pandas as pd
from pathlib import Path
from multiprocessing import Pool, cpu_count

# COMMAND LINE ARGUMENTS:
parser = argparse.ArgumentParser()
parser.add_argument("subset_num", help="Subset ID.")
parser.add_argument("genome_dir", help="Path to concat group (pro/syn) genomes.")
parser.add_argument("outdir", help="Path to simulation output directory.")
parser.add_argument("read_count", nargs="?", default=1000000, help="Total reads per simulated sample. [default: 1000000]")

args = parser.parse_args()

SUBSET_ID = int(args.subset_num)
TOTAL_READ_COUNT = int(args.read_count)
GENOME_DIR = Path(args.genome_dir)
OUTDIR = Path(args.outdir)


def load_yaml(yaml_path):
    """
    Returns dictionary of given yaml file.
    """
    with open(yaml_path, 'r') as file:
        yaml_content = yaml.safe_load(file)

    return yaml_content



def create_command_list(sample_composition_dict, subset_dir, main_outdir):
    """
    Returns a list of command used as input for mason.

    params:
    sample_composition_dict: dict with composition for each sample 
        - structure: {'sample_name': {'group1': percent, 'group2': percent}}
    subset_dir: directory to different genome subsets
        - structure: ${subset_dir}/subset_{subset_num}/GroupedGroupFasta
    """
    outdir = f"{main_outdir}/1.simulated"
    Path(outdir).mkdir(parents=True, exist_ok=True)

    command_list = []  # list of mason commands 

    # loop through each subset
    for subset_num in [SUBSET_ID]:  
        # loop through each sample in composition dict 
        for sample_name, composition_dict in sample_composition_dict.items():
            # create a command for each group within a sample (e.g. Pro, Syn)
            for group, group_pcnt in composition_dict.items():
                # obtain number of reads for group based on group percent in sample
                group_read_count = int((group_pcnt / 100) * TOTAL_READ_COUNT)

                # create command 
                command = (
                    "../../mason2/bin/mason_simulator "
                    f"-ir {subset_dir}/subset_{subset_num}/GroupedGroupFasta/{group}.fna "
                    f"-n {group_read_count} "
                    "--illumina-read-length 150 "
                    f"--read-name-prefix simulated_{group} "
                    f"-o {outdir}/subset_{subset_num}_{sample_name}_{group}_1.fq "
                    f"-or {outdir}/subset_{subset_num}_{sample_name}_{group}_2.fq "
                )

                command_list.append(command)  # add command to list 

    return command_list

def run_mason(mason_command):
    """
    Run mason read simulation. 
    """
    command_list = mason_command.split()  # split string of command into list for subprocesses
    out_fwd_path = command_list[-3]
    out_rev_path = command_list[-1]

    out_fwd_fname = out_fwd_path.split('/')[-1]
    out_rev_fname = out_rev_path.split('/')[-1]

    # run command if:
        # rev and fwd files don't exist OR 
        # rev and fwd files exist, but they're empty 
    if not (os.path.exists(out_fwd_path) and os.path.exists(out_rev_path)) or \
        ((os.path.exists(out_fwd_path) and os.path.getsize(out_fwd_path) == 0) and \
        (os.path.exists(out_rev_path) and os.path.getsize(out_rev_path) == 0)):
        # run mason command 
        try:
            subprocess.run(command_list, check=True)
            print(f'Executed simulation of {out_fwd_fname} and {out_rev_fname} successfully.')
            return None

        except subprocess.CalledProcessError as e:
            print(f'Error executing command: {e}')
            print(f'Could not successfully simulate {out_fwd_fname} and {out_rev_fname}.')
            # return command if process fails - so that can be saved into a file 
            return mason_command  

    else: 
        print(f'Files {out_fwd_fname} and {out_rev_fname} already exist. Skipping simulation.')

def parallel_run_mason(command_list):
    """
    Run mason in parallel. 
    Returns command if mason fails and saves into a file. 
    """
    with Pool() as pool:
        failed_commands = pool.map(run_mason, command_list)

    # filter out None in failed_commands
    failed_commands = [command for command in failed_commands if command is not None]
    with open(f'data/logs/failed_commands_{SUBSET_ID}.txt', 'w') as outfile:
        for command in failed_commands:
            outfile.write(f'{command}\n')



def edit_headers(edit_header_inputs):
    """
    Edit all headers (string after ">") within a file. 
    """
    input_fpath, fixed_header_outdir = edit_header_inputs
    
    fname = input_fpath.name
    
    output_fq = f'{fixed_header_outdir}/{fname}'
    with open(input_fpath, 'r') as infile, open(output_fq, 'w') as outfile:
        for line in infile:
            # remove '/' from headers 
            if line.startswith('@simulated'):
                # remove '/' and everything after 
                header, rest_of_line = line.split("/", 1)
                outfile.write(f"{header}\n")
            else:
                outfile.write(line)   

def parallel_edit_headers(main_outdir):
    """
    Change read headers of simulated samples. 
        - e.g. '@Heterotroph.1/1' will be renamed to '@Heterotroph.1'
        - Reason: kaiju name removes '/1' from read name  
    """
    # output path 
    fixed_header_outdir = Path(f'{main_outdir}/2.fixed_headers')
    fixed_header_outdir.mkdir(parents=True, exist_ok=True)

    # input path: simulated files separated 
    separated_outdir = Path(f'{main_outdir}/1.simulated')

    # obtain list of fpaths to process 
    edit_header_inputs = [(fpath, fixed_header_outdir) for fpath in separated_outdir.glob('*')]

    with Pool() as pool:
        pool.map(edit_headers, edit_header_inputs)  

    print('Header edit complete!')


def combine_files(combine_files_inputs):
    """
    Combines files in provided list using cat. 
    """
    file_list, output_path = combine_files_inputs
    command = ['cat'] + file_list

    # cat into file 
    with open(output_path, 'w') as outfile:
        # run cat command & redicrect output to output file 
        subprocess.run(command, stdout=outfile)


def parallel_combine_mason_output(main_outdir):
    """
    Combine files of 1 sample. 
    Note: Forward and reverse reads MUST be in the same order - hence the sorting.
    """
    # output path 
    concat_outdir = Path(f'{main_outdir}/3.concat_simulated')
    Path(concat_outdir).mkdir(parents=True, exist_ok=True)

    # input path 
    fixed_header_outdir = Path(f'{main_outdir}/2.fixed_headers')
    all_simulated_samples = [file.stem for file in fixed_header_outdir.glob('*') if file.is_file()]

    # turn paths into df to obtain sample name and total read 
    df = pd.DataFrame(all_simulated_samples, columns=['fname'])

    # obtain sample name, e.g. subset_{subset_num}_{sample_name} instead of the full name 
    # individual sample name (full): subset_{subset_num}_{sample_name}_{group}_1.fq
    df['sample_name'] = df['fname'].str.split('_').apply(lambda x: '_'.join(x[:-2]))
    df['read_type'] = df['fname'].str[-1]  # obtain fwd (1) or reverse (2) read type 

    sample_groups = df.groupby(['sample_name', 'read_type'])

    combine_files_inputs = []

    for index, sdf in sample_groups:
        sample_name = index[0]
        read_type = index[1]

        # to make sure the reads are concat in order in the final file 
        sdf = sdf.sort_values(by=['fname'])  

        fnames = sdf['fname'].values.tolist()
        fpaths = [f'{fixed_header_outdir}/{fname}.fq' for fname in fnames]
        concat_out_fpath = f'{concat_outdir}/{sample_name}_{read_type}.fq'

        combine_files_inputs.append([fpaths, concat_out_fpath])

    with Pool() as pool:
        pool.map(combine_files, combine_files_inputs)  

    print('All files combined!')
        
def create_sample_metadata(command_list):
    """
    Read count for each file (each file = a clade in the larger sample).
    """
    sample_metadata = {
        'sample': [], 
        'group': [], 
        'count': [], 
    }

    for command in command_list:
        command = command.split()  # split mason command into parts 

        read_count = command[4]  # count of reads of this group in sample 

        # individual file name: subset_{subset_num}_{sample_name}_{group}_2.fq
        file_name = command[-1].split('/')[-1]  # rev file name with .fq extension
        sample_name = '_'.join(file_name.split('_')[:-2])  # obtain sample name 
        clade = file_name.split('_')[-2]  # group in simulated file  

        sample_metadata['sample'].append(sample_name)
        sample_metadata['group'].append(clade)
        sample_metadata['count'].append(read_count)

    df = pd.DataFrame(sample_metadata)
    return df

def main():
    """
    """
    ### 1. Prep + Paths ### 
    # path to composition 
    sample_composition_dict = load_yaml("data/composition_config.yaml")
    
    # make output directory
    main_outdir.mkdir(parents=True, exist_ok=True)

    ### 2. Create mason read simulation commands to execute ### 
    command_list = create_command_list(sample_composition_dict, GENOME_DIR, main_outdir)

    # print resources before running parallel steps 
    num_processes = cpu_count()
    print("Number of worker processes:", num_processes)

    ## 3. Run mason read sim commands in parallel ### 
    parallel_run_mason(command_list)

    ## 4. Edit headers of simulated samples in parallel ### 
    parallel_edit_headers(main_outdir)

    ## 5. Combine files of each sample after simulation ### 
    parallel_combine_mason_output(main_outdir)

    ### 6. Create a table of files and their metadata ### 
    df = create_sample_metadata(command_list)
    df.to_csv('data/sample_metadata.tsv', sep='\t', index=False)


if __name__ == "__main__":
    main()