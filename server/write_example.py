import pyarrow as pa
import pyarrow.parquet as pq

# Create a table with some example data
schema = pa.schema([
    ('name', pa.string()),
    ('age', pa.int32())
])
data = [
    pa.array(['Alice', 'Bob', 'Charlie']),
    pa.array([25, 30, 35])
]
table = pa.Table.from_arrays(data, schema=schema)

# Write the table to a Parquet file
pq.write_table(table, 'example.parquet')

print("Parquet file written successfully!")