import csv
from collections import defaultdict
from pyarrow.parquet import ParquetDataset

# Load the Parquet dataset
dataset = ParquetDataset("/PATH/TO/PARQUET/DATA/", use_legacy_dataset=False)

# Initialize dictionaries to store histogram data for each property
histogram_data = {
    "Aromatics": defaultdict(int),
    "Heterocycles": defaultdict(int),
    "Carboaromatics": defaultdict(int),
    "Rotatable Bonds": defaultdict(int)
}

# Define the bins for each property (modify as needed)
aromatic_bins = range(0, 21)
heterocycles_bins = range(0, 21)
carboaromatics_bins = range(0, 21)
rotatable_bonds_bins = range(0, 101)

# Iterate through each Parquet fragment
for p in dataset.fragments:
    # Read the data from the fragment
    table = p.to_table()
    
    # Get the relevant columns (replace with the actual column names)
    aromatic_column = table.column("num_aromatic_ring")
    heterocycles_column = table.column("num_hetaromatic_ring")
    carboaromatics_column = table.column("num_carboaromatic_ring")
    rotatable_bonds_column = table.column("RotBonds")
    
    # Count occurrences in each bin for each property
    for count in aromatic_column:
        histogram_data["Aromatics"][count] += 1
    for count in heterocycles_column:
        histogram_data["Heterocycles"][count] += 1
    for count in carboaromatics_column:
        histogram_data["Carboaromatics"][count] += 1
    for count in rotatable_bonds_column:
        histogram_data["Rotatable Bonds"][count] += 1

# Write the combined histogram data to a CSV file
with open("properties_histogram.csv", "w", newline="") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["Property", "Bin", "Count"])  # Write header
    for property_name, data in histogram_data.items():
        for bin_value, count in data.items():
            csv_writer.writerow([property_name, bin_value, count])

