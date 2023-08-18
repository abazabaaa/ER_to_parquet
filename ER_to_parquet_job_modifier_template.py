import os

# List of paths and file names
#CHANGE PATH!!!
paths = ['/PATH/TO/CXSMILES/FILES']
file_extension = '.cxsmiles.bz2'  # Change this to your desired file extension

# Read the template script
#UPDATE *.sb FILE WITH YOUR TEMPLATE FILE
with open('TEMPLATE_FILE.sb', 'r') as template_file:
    template_script = template_file.read()

# Loop through the list and generate numbered script files
for index, path in enumerate(paths, start=1):
    # Get a list of files with the specified extension in the new path
    file_names = [file for file in os.listdir(path) if file.endswith(file_extension)]

    if file_names:
        for file_name in file_names:
            # Construct the new path and file name
            new_path = os.path.join(path, file_name)

            # Replace placeholders in the template script
            updated_script = template_script.replace('original_path/file.txt', new_path)

            # Add updated path to the last line of the script
            #CHANGE THE OUTPUT DIRECTORY PATH!!!!
            updated_script += f'\npython /PATH/TO/er_real_csv_append_and_convert_parquet.py {new_path} /OUTPUT/DIR/PATH/\n'

            # Generate the new script file

