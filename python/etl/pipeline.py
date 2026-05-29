"""
AGIS ETL Pipeline
─────────────────
Extract → Transform → Load pipeline for AGIS data.
Loads generated CSV data into SQLite database with schema validation.

Usage:
    python python/etl/pipeline.py                  # Full ETL
    python python/etl/pipeline.py --dry-run         # Validate only
"""
import sys, os
import argparse
import time
import sqlite3
import logging

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, PROJECT_ROOT)

import pandas as pd
import numpy as np
from config.settings import RAW_DATA_DIR, PROCESSED_DIR, DB_PATH, DATABASE_DIR

# ─── Logging ──────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(stream=open(sys.stdout.fileno(), mode='w', encoding='utf-8', closefd=False)),
        logging.FileHandler(os.path.join(PROJECT_ROOT, 'etl_pipeline.log'), encoding='utf-8')
    ]
)
logger = logging.getLogger('AGIS_ETL')


# ═══════════════════════════════════════════════════════════════
# EXTRACT
# ═══════════════════════════════════════════════════════════════
def extract(data_dir: str) -> dict:
    """Extract all CSV files from the raw data directory."""
    logger.info("📥 EXTRACT PHASE — Loading raw data files...")
    tables = {}
    csv_files = sorted([f for f in os.listdir(data_dir) if f.endswith('.csv') and not f.startswith('_')])

    for f in csv_files:
        name = f.replace('.csv', '')
        path = os.path.join(data_dir, f)
        df = pd.read_csv(path)
        tables[name] = df
        logger.info(f"  ✓ {name}: {len(df):,} rows × {len(df.columns)} columns")

    logger.info(f"  Total: {len(tables)} tables loaded")
    return tables


# ═══════════════════════════════════════════════════════════════
# TRANSFORM
# ═══════════════════════════════════════════════════════════════
def transform(tables: dict) -> dict:
    """Apply transformations, cleaning, and feature engineering."""
    logger.info("🔄 TRANSFORM PHASE — Cleaning and enriching data...")

    # --- DimDate: ensure proper types ---
    if 'DimDate' in tables:
        df = tables['DimDate']
        df['Date'] = pd.to_datetime(df['Date'])
        tables['DimDate'] = df
        logger.info(f"  ✓ DimDate: parsed dates, {len(df):,} rows")

    # --- DimAircraft: derive fleet age ---
    if 'DimAircraft' in tables:
        df = tables['DimAircraft']
        df['CommissionDate'] = pd.to_datetime(df['CommissionDate'])
        df['FleetAge_Years'] = ((pd.Timestamp('2025-12-31') - df['CommissionDate']).dt.days / 365.25).round(1)
        df['HealthCategory'] = pd.cut(df['CoreHealthIndex'],
                                      bins=[0, 0.5, 0.7, 0.85, 1.0],
                                      labels=['Critical', 'Poor', 'Good', 'Excellent'])
        tables['DimAircraft'] = df
        logger.info(f"  ✓ DimAircraft: added FleetAge_Years, HealthCategory")

    # --- FactFlightTelemetry: clean + add derived metrics ---
    if 'FactFlightTelemetry' in tables:
        df = tables['FactFlightTelemetry']
        # Remove any negative values
        df['Altitude_m'] = df['Altitude_m'].clip(lower=0)
        df['Velocity_mps'] = df['Velocity_mps'].clip(lower=0)
        df['StabilityScore'] = df['StabilityScore'].clip(0, 100)

        # Propulsion efficiency
        df['PropulsionEfficiency'] = np.where(
            df['EnergyConsumed_kW'] > 0,
            (df['LiftOutput_kN'] / df['EnergyConsumed_kW']).round(4),
            0
        )

        # Energy per km (energy / velocity, if velocity > 0)
        df['EnergyPerKm'] = np.where(
            df['Velocity_mps'] > 1,
            (df['EnergyConsumed_kW'] / df['Velocity_mps'] * 1000).round(2),
            0
        )

        # Null check
        null_count = df.isnull().sum().sum()
        if null_count > 0:
            logger.warning(f"  ⚠ FactFlightTelemetry has {null_count} null values, filling with 0")
            df = df.fillna(0)

        tables['FactFlightTelemetry'] = df
        logger.info(f"  ✓ FactFlightTelemetry: cleaned, added PropulsionEfficiency, EnergyPerKm")

    # --- FactMaintenance: derive cost categories ---
    if 'FactMaintenance' in tables:
        df = tables['FactMaintenance']
        df['CostCategory'] = pd.cut(df['RepairCost'],
                                    bins=[0, 10000, 50000, 100000, 500000, float('inf')],
                                    labels=['Low', 'Medium', 'High', 'Very High', 'Critical'])
        df['DowntimeCategory'] = pd.cut(df['DowntimeHours'],
                                        bins=[0, 24, 72, 168, 720, float('inf')],
                                        labels=['< 1 Day', '1-3 Days', '3-7 Days', '1-4 Weeks', '> 4 Weeks'])
        tables['FactMaintenance'] = df
        logger.info(f"  ✓ FactMaintenance: added CostCategory, DowntimeCategory")

    # --- FactManufacturing: quality flags ---
    if 'FactManufacturing' in tables:
        df = tables['FactManufacturing']
        df['IsHighDefect'] = (df['DefectRate'] > 0.10).astype(int)
        df['CostPerUnit'] = (df['ProductionCost'] / df['BatchSize'].clip(lower=1)).round(2)
        tables['FactManufacturing'] = df
        logger.info(f"  ✓ FactManufacturing: added IsHighDefect, CostPerUnit")

    # --- FactFinance: cumulative metrics ---
    if 'FactFinance' in tables:
        df = tables['FactFinance']
        df['IsOverBudget'] = (df['BudgetVariance'] > 0).astype(int)
        df['ROI'] = np.where(
            df['RDCost'] > 0,
            ((df['Revenue'] - df['RDCost']) / df['RDCost'] * 100).round(2),
            0
        )
        tables['FactFinance'] = df
        logger.info(f"  ✓ FactFinance: added IsOverBudget, ROI")

    return tables


# ═══════════════════════════════════════════════════════════════
# LOAD
# ═══════════════════════════════════════════════════════════════
def load(tables: dict, db_path: str, schema_path: str = None):
    """Load all tables into SQLite database."""
    logger.info(f"📤 LOAD PHASE — Writing to {db_path}...")

    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # Remove existing DB for clean load
    if os.path.exists(db_path):
        os.remove(db_path)
        logger.info(f"  🗑 Removed existing database")

    conn = sqlite3.connect(str(db_path))

    # Execute schema if provided
    if schema_path and os.path.exists(schema_path):
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        conn.executescript(schema_sql)
        logger.info(f"  ✓ Schema executed from {schema_path}")

    # Load dimension tables first, then facts
    dim_tables = {k: v for k, v in tables.items() if k.startswith('Dim')}
    fact_tables = {k: v for k, v in tables.items() if k.startswith('Fact')}

    for name, df in {**dim_tables, **fact_tables}.items():
        # Convert datetime columns to string for SQLite
        for col in df.select_dtypes(include=['datetime64']).columns:
            df[col] = df[col].astype(str)

        df.to_sql(name, conn, if_exists='replace', index=False)
        logger.info(f"  ✓ {name}: {len(df):,} rows loaded")

    # Verify row counts
    logger.info("  🔍 Verifying loaded data...")
    cursor = conn.cursor()
    for name in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {name}")
        count = cursor.fetchone()[0]
        expected = len(tables[name])
        status = "✓" if count == expected else "✗"
        logger.info(f"    {status} {name}: {count:,} rows (expected {expected:,})")

    conn.close()
    logger.info(f"  ✅ Database saved to {db_path}")

    # Save processed CSVs
    for name, df in tables.items():
        out_path = os.path.join(str(PROCESSED_DIR), f'{name}.csv')
        df.to_csv(out_path, index=False)
    logger.info(f"  ✅ Processed CSVs saved to {PROCESSED_DIR}")


# ═══════════════════════════════════════════════════════════════
# PIPELINE ORCHESTRATOR
# ═══════════════════════════════════════════════════════════════
def run_pipeline(dry_run: bool = False):
    """Execute the full ETL pipeline."""
    start = time.time()
    logger.info("=" * 60)
    logger.info("🚀 AGIS ETL Pipeline — Starting")
    logger.info("=" * 60)

    # Extract
    tables = extract(str(RAW_DATA_DIR))

    # Transform
    tables = transform(tables)

    if dry_run:
        logger.info("\n🏁 DRY RUN — Skipping load phase")
        for name, df in tables.items():
            logger.info(f"  {name}: {len(df):,} rows, {len(df.columns)} columns")
            logger.info(f"    Columns: {list(df.columns)}")
    else:
        # Load
        schema_path = os.path.join(str(DATABASE_DIR), 'schema.sql')
        load(tables, str(DB_PATH), schema_path)

    elapsed = time.time() - start
    total_rows = sum(len(df) for df in tables.values())
    logger.info("=" * 60)
    logger.info(f"✅ ETL Pipeline Complete — {total_rows:,} total rows in {elapsed:.1f}s")
    logger.info("=" * 60)
    return tables


def main():
    parser = argparse.ArgumentParser(description='AGIS ETL Pipeline')
    parser.add_argument('--dry-run', action='store_true',
                        help='Run extract and transform only, skip load')
    args = parser.parse_args()
    run_pipeline(dry_run=args.dry_run)


if __name__ == '__main__':
    main()
