"""
AGIS Master Data Generator
───────────────────────────
Orchestrates generation of all dimension and fact tables.
Outputs CSV files to data/raw/ and data/synthetic/.

Usage:
    python python/generators/data_generator.py                    # Full dataset (~1M+ rows)
    python python/generators/data_generator.py --lite             # Lite dataset (~50K rows)
    python python/generators/data_generator.py --format parquet   # Parquet output
"""
import sys, os
import argparse
import time

# Ensure project root is on path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, PROJECT_ROOT)

from config.settings import RAW_DATA_DIR, SYNTHETIC_DIR, RANDOM_SEED
from python.generators.dimension_generators import generate_all_dimensions
from python.generators.flight_telemetry_generator import generate_fact_flight_telemetry
from python.generators.maintenance_generator import generate_fact_maintenance
from python.generators.manufacturing_generator import generate_fact_manufacturing
from python.generators.finance_generator import generate_fact_finance


def save_dataframe(df, name: str, output_dir, fmt: str = 'csv'):
    """Save DataFrame to disk in specified format."""
    os.makedirs(output_dir, exist_ok=True)
    if fmt == 'parquet':
        path = os.path.join(output_dir, f'{name}.parquet')
        df.to_parquet(path, index=False, engine='pyarrow')
    elif fmt == 'json':
        path = os.path.join(output_dir, f'{name}.json')
        df.to_json(path, orient='records', indent=2)
    else:
        path = os.path.join(output_dir, f'{name}.csv')
        df.to_csv(path, index=False)
    size_mb = os.path.getsize(path) / (1024 * 1024)
    print(f"    💾 Saved {name} → {path} ({size_mb:.1f} MB)")


def main():
    parser = argparse.ArgumentParser(description='AGIS Data Generator')
    parser.add_argument('--lite', action='store_true',
                        help='Generate lite dataset (~50K rows total)')
    parser.add_argument('--format', choices=['csv', 'parquet', 'json'],
                        default='csv', help='Output format')
    parser.add_argument('--seed', type=int, default=RANDOM_SEED,
                        help='Random seed for reproducibility')
    args = parser.parse_args()

    # Scale factors for lite mode
    if args.lite:
        scale = {'telemetry': 10_000, 'maintenance': 2_000,
                 'manufacturing': 5_000, 'finance': None}
        print("\n🚀 AGIS Data Generator — LITE MODE")
    else:
        scale = {'telemetry': None, 'maintenance': None,
                 'manufacturing': None, 'finance': None}
        print("\n🚀 AGIS Data Generator — FULL MODE")

    print("=" * 60)
    start = time.time()

    # ─── Dimension Tables ─────────────────────────────────────
    print("\n📐 Phase 1: Generating Dimension Tables...")
    dims = generate_all_dimensions(seed=args.seed)

    for name, df in dims.items():
        save_dataframe(df, name, str(RAW_DATA_DIR), args.format)

    # ─── Fact Tables ──────────────────────────────────────────
    print("\n📊 Phase 2: Generating Fact Tables...")

    print("\n  ⚡ FactFlightTelemetry:")
    fact_telemetry = generate_fact_flight_telemetry(
        dims['DimAircraft'], dims['DimPilot'], dims['DimMission'],
        dims['DimDate'], target_rows=scale['telemetry'], seed=args.seed
    )
    save_dataframe(fact_telemetry, 'FactFlightTelemetry', str(RAW_DATA_DIR), args.format)

    print("\n  🔧 FactMaintenance:")
    fact_maintenance = generate_fact_maintenance(
        dims['DimAircraft'], dims['DimFailureType'],
        dims['DimDate'], target_rows=scale['maintenance'], seed=args.seed
    )
    save_dataframe(fact_maintenance, 'FactMaintenance', str(RAW_DATA_DIR), args.format)

    print("\n  🏭 FactManufacturing:")
    fact_manufacturing = generate_fact_manufacturing(
        dims['DimComponent'], dims['DimFactory'],
        dims['DimDate'], target_rows=scale['manufacturing'], seed=args.seed
    )
    save_dataframe(fact_manufacturing, 'FactManufacturing', str(RAW_DATA_DIR), args.format)

    print("\n  💰 FactFinance:")
    fact_finance = generate_fact_finance(
        dims['DimDepartment'], dims['DimDate'], seed=args.seed
    )
    save_dataframe(fact_finance, 'FactFinance', str(RAW_DATA_DIR), args.format)

    # ─── Summary ──────────────────────────────────────────────
    elapsed = time.time() - start
    total_rows = sum(len(df) for df in dims.values()) + \
                 len(fact_telemetry) + len(fact_maintenance) + \
                 len(fact_manufacturing) + len(fact_finance)

    print("\n" + "=" * 60)
    print(f"✅ AGIS Data Generation Complete!")
    print(f"   Total records: {total_rows:,}")
    print(f"   Time elapsed:  {elapsed:.1f}s")
    print(f"   Output format: {args.format.upper()}")
    print(f"   Output dir:    {RAW_DATA_DIR}")
    print("=" * 60)

    # Save summary stats
    summary = {
        'Table': list(dims.keys()) + ['FactFlightTelemetry', 'FactMaintenance',
                                       'FactManufacturing', 'FactFinance'],
        'Rows': [len(df) for df in dims.values()] + [len(fact_telemetry),
                 len(fact_maintenance), len(fact_manufacturing), len(fact_finance)],
        'Type': ['Dimension'] * len(dims) + ['Fact'] * 4,
    }
    import pandas as pd
    summary_df = pd.DataFrame(summary)
    save_dataframe(summary_df, '_DataGenerationSummary', str(SYNTHETIC_DIR), 'csv')


if __name__ == '__main__':
    main()
