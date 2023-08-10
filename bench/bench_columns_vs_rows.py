import pandas as pd
import pyarrow as pa
from timeit import timeit
import pyarrow.compute as pc

# Create a DataFrame with row-oriented data
n_samples = 20000
df_row = pd.DataFrame({
    'name': ['John Doe', 'Jane Doe'] * n_samples,
    'age': [30, 25] * n_samples
})

# Create a DataFrame with column-oriented data
df_column = df_row.set_index('name')

# Convert Pandas DataFrame to PyArrow Table
py_table = pa.Table.from_pandas(df_row)

# Benchmark the time it takes to find all customers with age between 18 and 25
n_iter = 10000
time_row = timeit(lambda: df_row[df_row['age'].between(18, 25)], number=n_iter)
time_column = timeit(lambda: df_column[df_column['age'].between(18, 25)], number=n_iter)
age_chunks = py_table.column('age').combine_chunks()
time_arrow = timeit(lambda: age_chunks.filter(
    pc.and_(pc.greater_equal(age_chunks, 18), pc.less_equal(age_chunks, 25))
), number=n_iter)

print('Time to find all customers with age between 18 and 25')
print('    in row-oriented data:', time_row)
print('    in column-oriented data:', time_column)
print('    using PyArrow Table:', time_arrow)