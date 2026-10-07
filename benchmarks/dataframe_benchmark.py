import time

import duckdb
import numpy as np
import pandas as pd
import polars as pl

ROWS = 25_000_000

print(f"Generating {ROWS:,} rows...")

rng = np.random.default_rng(42)

categories = rng.integers(0, 100, size=ROWS)
values = rng.random(ROWS)

# pandas
pdf = pd.DataFrame({
    "category": categories,
    "value": values,
})

start = time.perf_counter()
pandas_result = pdf.groupby("category")["value"].sum()
pandas_time = time.perf_counter() - start

# Polars
pldf = pl.DataFrame({
    "category": categories,
    "value": values,
})

start = time.perf_counter()
polars_result = pldf.group_by("category").agg(pl.col("value").sum())
polars_time = time.perf_counter() - start

# DuckDB
start = time.perf_counter()
duckdb_result = duckdb.sql("""
    SELECT category, SUM(value)
    FROM pdf
    GROUP BY category
""").fetchall()
duckdb_time = time.perf_counter() - start

print()
print("Results")
print("-" * 30)
print(f"pandas: {pandas_time:.4f} seconds")
print(f"Polars: {polars_time:.4f} seconds")
print(f"DuckDB: {duckdb_time:.4f} seconds")