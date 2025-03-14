# HPC Resource Tips
Some commands on how to obtain resource sepcifications from your compute cluster for the workflow. 

### Partitions
- To see names of partitions and the compute nodes you have access to: 

       sinfo

- Example output: 
    ```
    PARTITION            AVAIL  TIMELIMIT  NODES  STATE NODELIST
    sched_any_quicktest*    up      15:00      4 drain* node[028-029,101,142]
    sched_any               up   12:00:00     12 drain* node[019-026,106-108,123]
    sched_mit_hill          up   12:00:00      9    mix node[073,146,156,160,235,337,369,371,376]
    newnodes                up   12:00:00     19 drain* node[274-275,277-278,280-288,317,340-341,393,426-427]
    sched_mit_chisholm      up 90-00:00:0      2    mix node[420-422]
    mit_normal              up   12:00:00      7    mix node[1600-1602,1606-1607,1624-1625]
    mit_normal_gpu          up 1-00:00:00      1  maint node1707
    mit_quicktest           up      15:00      1  alloc node1603
    ```

- Needed in: 
    - `profile/config.yaml` file: "default-resources: partition" where you need to specify which partitions to submit jobs to 
        - **Note:** `default-resources: time=[value]` should not exceed "TIMELIMIT" in the chosen partition 
    - `run_classify_smk.sbatch` file: where you need to specify which partition to submit the main Snakemake job to 
        - **Note:** the `#SBATCH --time [value]` should not exceed "TIMELIMIT" in the chosen partition 

### Compute nodes 
- To see resource specification of each node. First, pick a partition (e.g. "sched_mit_chisholm"), then pick a random node within that partition (e.g. node420). Note: the `node[420-422]` connocation means there are nodes: node420, node421, and node422 in the partition. 

       # replace node420 with name of node in your partition
       scontrol show node node420

- Example output: 
    ```
    NodeName=node420 Arch=x86_64 CoresPerSocket=10 
        CPUAlloc=12 CPUEfctv=20 CPUTot=20 CPULoad=2.18
        AvailableFeatures=node420,centos7
        ActiveFeatures=node420,centos7
        Gres=(null)
        NodeAddr=node420 NodeHostName=node420 Version=22.05.6
        OS=Linux 3.10.0-1062.el7.x86_64 #1 SMP Wed Aug 7 18:08:02 UTC 2019 
        RealMemory=257000 AllocMem=139120 FreeMem=118085 Sockets=2 Boards=1
        State=MIXED ThreadsPerCore=1 TmpDisk=0 Weight=1 Owner=N/A MCS_label=N/A
        Partitions=sched_mit_chisholm 
        BootTime=2024-10-14T15:11:00 SlurmdStartTime=2025-01-28T16:21:34
        LastBusyTime=2025-03-13T17:28:15
        CfgTRES=cpu=20,mem=257000M,billing=20
        AllocTRES=cpu=12,mem=139120M
        CapWatts=n/a
        CurrentWatts=0 AveWatts=0
        ExtSensorsJoules=n/s ExtSensorsWatts=0 ExtSensorsTemp=n/s
    ```
- Needed in: 
    - `profile/config.yaml` file: 
        - `default-resources: mem=[value]` and `set-resources: mem=[value]` should not exceed value in `RealMemory=[value]`
        - `set-resources: cpus_per_task=[value]` should not exceed `CPUTot=[value]`