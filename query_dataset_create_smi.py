import pyarrow as pa
import pyarrow.dataset as ds
import duckdb
import pyarrow.parquet as pq
import pandas as pd
from pyarrow import csv

parquet_database = "/expanse/lustre/scratch/tjagraham/temp_project/enamine_real_5B/er_real_pq_database"

parquet_database_q_out = "/expanse/lustre/scratch/tjagraham/temp_project/enamine_real_5B/rna_bp_library"

smiles_dataset = ds.dataset(parquet_database, format="parquet")

#print(type(smiles_dataset))

#dataset_scanner = ds.Scanner.from_dataset(smiles_dataset, batch_size=1)

#print(type(dataset_scanner))

con = duckdb.connect()

num = 3



con.execute('PRAGMA threads=8')
query = con.execute(
        f"SELECT smiles, idnumber FROM smiles_dataset WHERE num_aromatic_ring >= '{num}' AND HBD > 0 AND HBA > 0 AND MW <= 400 AND MW >= 275 AND sLogP <= 4 and HAC >= 14 and HAC <= 30"
    )
record_batch_reader = query.fetch_record_batch()

#print(type(record_batch_reader))


counter = 1

while True:
    try:
            # Process a single chunk here
            # pyarrow.lib.RecordBatch
        chunk = record_batch_reader.read_next_batch()
        #print(type(chunk))
        table = pa.Table.from_batches([chunk])
        record_batches = table.to_batches(max_chunksize=40000)
        for recbatchcount, record_batch in enumerate(record_batches):
            df = record_batch.to_pandas()
            #table = pa.Table.from_batches([chunk])
            #pq.write_table(table, f"{parquet_database_q_out}/er_query_out_{counter}.parquet")
            df.to_csv(f"{parquet_database_q_out}/er_query_out_{counter}_{recbatchcount}.smi", sep='\t', index=False, escapechar='n')
        print(counter)
        counter += 1
    except StopIteration:
        break
