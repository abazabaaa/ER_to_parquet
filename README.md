# ER_to_parquet

[[[Setting up Conda environment]]]

All environment parameters for first step are in:
	ERparq.txt (explicit lists)
OR	ERparq.yml (shorthand list)

After logging into Expanse, you need to switch to the debug node to set up a conda environment (for later steps)

$srun --partition=debug  --pty --account=was138 --nodes=1 --ntasks-per-node=4 \
    --mem=8G -t 00:30:00 --wait=0 --export=ALL /bin/bash
then

$module load cpu/0.15.4  gcc/10.2.0
$module load anaconda3/2020.11
$. $ANACONDA3HOME/etc/profile.d/conda.sh

You can then create an environment as normal (for my first step I named mine ‘Erparq’)

Use ‘pip install’ to load Pyarrow, Pandas, and RDKit

**sometimes this node will close if environment setup takes too long, you can either try again or skip the srun part and try setting things up on the initial login headnode



------------------------------------------------------------------------------------------------------

[[[Download the Enamine library]]]

Create a folder in the scratch space  /expanse/lustre/scratch/[USER]/temp_project

Modify ‘enamine_library_download_template.py’ to suite your needs

I chose to download the 32billion ChemSpace library (logins and passwords are different for each subset – Email Roman for most recent passwords)

This dataset was broken up as: /S/H* and /M/H*

[NOTES]:
line 36: you can choose to break up into multiple downloads by specifying subdirectories here (suggest copying and renaming each sub-section download *.py script differently for submission)
lines 50/51: change login info as needed
line 57: file extensions you want to download
line 60: where on Expanse you want files to go

**Some sections are quite large so at a minimum download ‘S’ and ‘M’ sections individually
**You can also use line 57 to only download files with desired logP values
** You can also move files based on MW or LogP of *.cxsmiles.bz2 file names before going to next step
** A jupyter notebook of the download script is also included if you want to test things interactively
-------------------------------------------------------------------------------------------------

[[[Convert *.cxsmiles.bz2 files to parquet files]]]

This section requires the use of 3 scripts:
er_real_csv_append_and_convert_parquet.py  #does the actual converting
er_real_csv_append_and_convert_parquet_submit_template.sb #slurm script for submitting a job
ER_parquest_job_modifier.py #modifies the slurm script for each *.cxsmiles.bz2 file and outputs an individual name for each job


[NOTES]:
- Enamine tends to chunk up data differently on a routine basis so line 21 in er_real_csv_append_and_convert_parquet.py may need to be modified to reflect the naming scheme for column headings

- line 23 needs to reflect YOUR conda enviornment name in er_real_csv_append_and_convert_parquet_submit_template.sb  #mine was ERparq (see above)

ER_parquest_job_modifier.py will need to be modified on these lines:
	line 4: where your *.cxsmiles.bz2 files are
	line 8: where er_real_csv_append_and_convert_parquet_submit_template.sb is
	line 25: where scripts and output are

*** Be sure to check that a submit*.sb file was generated for each *.cxsmiles.bz2 file 
		$ls -1 | wc -l #lists how many files are in a directory

Create a bash submit script 
		$ for i in submit_* ; do echo ‘sbatch ‘$i’’; done > parquet_batch_submit.sh

do a test submit of the first one and check that *.parquet files are generated in the output folder
***check environment*.out file for error messages

---------------------------------------------------------------------------------------------------------

[[[Confirm parquet conversion]]]

-After submitting the jobs, confirm all files from original folder have been converted to parquet files
	$ls PATH/TO/PARQUET/OUTPUT/FILES/* > parquet_files.txt
	$ls PATH/TO/INPUT/FILES/* > input_files.txt
*** use text editor to trim names to file identifier (i.e., MH18M000) for both files
-The out parquet file will have multiple entries (the *.cxsmiles.bz2 can generate multiple parquet files)
-Create a new file for only the unique output files using  unique_names.py
[NOTES]:
update lines 14 and 15 to reflect list of parquet files (parquet_files.txt) and output file (converted.txt)

-Compare list of converted files to input list:
	$grep -vxFf SECOND_FILE FIRST_FILE > OUTPUT_FILE  
	#prints files missing in second file compared to first 
	#SECOND_FILE= converted.txt
	#FIRST_FILE=input_files.txt
**If the OUTPUT_FILE is blank, delete a line from SECOND_FILE and re-run, the OUTPUT_FILE should have that name in it now. Otherwise there is a problem and take time to resolve this before moving on.

----------------------------------------------------------------------------------------------------

[[[Parquet to SMILES]]]

First, create a new conda environment ('duckdb') and install 1)pyarrow, 2) duckdb, and 3) pandas.

Before converting parquet files to SMILES, it is best to know how many molecules are contained in the parquet files. 
Update count_parquet_template.py to reflect the path to your parquet database, then submit the job using count_lines_parquet.sb
The number of files will be printed in the *.out file* specified in count_lines_parquet.sb 

Another step of pre-filtering can be done using properties_histogram_calc_template.py and properties_histogram_calc.sb on a handful of parquet files.In properties_histogram_calc_template.py, update line 6 to reflect <PATH> and line 44 to a unique output file name. This will help give an idea of the properties landscape/cutoff values you wish to use in the next step. 

Finally, convert all the parquet files to SMILE using query_dataset_create_smi.py and query_dataset_create_smi_submit_template.sb
Be careful to verify header names on parquet files match the selection criteria specified on line 28 of query_dataset_create_smi.py

Once the job is finished, ensure all files have been converted (using $ls -1 | wc -l  while inside the SMILES output directory, then multiply by 40,000 since that is the number of molecules in each chunk. The number should closely reflect the number of lines found in parquet files, determined uing count_parquet_template.py (above)    
 
