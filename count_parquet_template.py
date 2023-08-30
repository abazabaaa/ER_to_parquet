from pyarrow.parquet import ParquetDataset
dataset = ParquetDataset("/PATH/TO/PARQUET/FILES/", use_legacy_dataset=False)
nrows = sum(p.count_rows() for p in dataset.fragments)
print(nrows)
