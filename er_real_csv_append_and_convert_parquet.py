import pandas
import pyarrow as pa
import pyarrow.csv as csv
import pyarrow.parquet as pq
from rdkit.Chem import PandasTools
from rdkit.Chem import rdMolDescriptors
import pathlib
import os
import sys

csv_file_path = sys.argv[1]
output_dir = sys.argv[2]


#output_dir = "/Users/tgraham/Temple/enamine_library/test_er_output2"
#csv_file_path = "/Users/tgraham/Temple/enamine_library/Enamine_REAL_HAC_27_967M_Part_2_CXSMILES.cxsmiles.bz2"

def open_csv_stream(csv_file):

    chunksize = 1048576*100
    include_columns = ['smiles', 'id', 'MW', 'HAC', 'sLogP', 'HBA', 'HBD', 'RotBonds', 'FSP3', 'TPSA']
    read_options = csv.ReadOptions(block_size=chunksize)
    parse_options = csv.ParseOptions(delimiter='\t')
    convert_options = csv.ConvertOptions(include_columns=include_columns)

    csv_stream = csv.open_csv(csv_file,
        read_options=read_options,
        parse_options=parse_options,
        convert_options=convert_options)
    return csv_stream

def chunk_to_df_add_descriptors(chunk):

    df = chunk.to_pandas()

    PandasTools.AddMoleculeColumnToFrame(df,smilesCol='smiles',
        molCol='ROMol',
        includeFingerprints=False)

    df['num_aromatic_ring'] = df['ROMol'].map(rdMolDescriptors.CalcNumAromaticRings)
    df['num_hetaromatic_ring'] = df['ROMol'].map(rdMolDescriptors.CalcNumAromaticHeterocycles)
    df['num_carboaromatic_ring'] = df['ROMol'].map(rdMolDescriptors.CalcNumAromaticCarbocycles)

    df = df.drop('ROMol', axis=1)

    # print(df.head(10))

    return df

def get_arrowtable_from_df(df):

    table = pa.Table.from_pandas(df, preserve_index=False)

    return table
def write_table_out(table, count, output_dir, csv_file_path):

    file_path = pathlib.Path(csv_file_path)

    outfile_stem_name = pathlib.Path(file_path.stem).stem

    out_path = os.path.join(output_dir, f'{outfile_stem_name}_{count}.parquet')

    pq.write_table(table, out_path)

def clean_compound_names(name):

    try:
        name2 = name.split(" ")
        name3 = name2[0]
        return name3
    except:
        pass
        return name
csv_stream = open_csv_stream(csv_file_path)

chunk = csv_stream.read_next_batch()
df = chunk_to_df_add_descriptors(chunk)
df["smiles"] = df["smiles"].apply(lambda x : clean_compound_names(x))
table = get_arrowtable_from_df(df)
count = 1
write_table_out(table, count, output_dir, csv_file_path)
print(count)

while len(chunk) > 0:
    try:
        count += 1
        chunk = csv_stream.read_next_batch()
        df = chunk_to_df_add_descriptors(chunk)
        df["smiles"] = df["smiles"].apply(lambda x : clean_compound_names(x))
        table = get_arrowtable_from_df(df)
        print(count)
        write_table_out(table, count, output_dir, csv_file_path)
    except StopIteration:
        break
