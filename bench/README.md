# Benches

## Columns vs Rows

> code bench_columns_vs_rows.py

The aim of this experiment was to compare the execution times of operations on different data structures: a Pandas DataFrame with row-oriented data, a Pandas DataFrame with column-oriented data, and a PyArrow Table - all containing the same data. 

We measured the time taken to perform the same operation on all three - finding all customers with ages between 18 and 25. 

Below is the table summarizing the execution times in seconds for the operation on different data structures:

| Data Structure                           | Time Taken (seconds) |
|------------------------------------------|----------------------|
| Pandas DataFrame (Row-oriented)          | 4.249267             |
| Pandas DataFrame (Column-oriented)       | 2.912263             |
| PyArrow Table                            | 0.692972             |

Our experiment shows that the operation on the PyArrow Table was significantly faster than the similar operations on the Pandas DataFrames. The operation on the row-oriented DataFrame was the slowest, while the operation on the column-oriented DataFrame was faster. 

These results highlight the advantage of utilizing columnar storage (like in PyArrow) for data analytic operations. It's clear that using more efficient data structures can result in significant performance improvements, which can especially be beneficial in dealing with large-scale data.