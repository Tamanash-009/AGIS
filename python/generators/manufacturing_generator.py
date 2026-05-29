"""
AGIS Manufacturing Fact Table Generator
───────────────────────────────────────
Generates ~300K manufacturing production records.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import pandas as pd
import numpy as np
from config.settings import RANDOM_SEED, DATE_START, DATE_END, RECORD_COUNTS


def generate_fact_manufacturing(dim_component: pd.DataFrame,
                                dim_factory: pd.DataFrame,
                                dim_date: pd.DataFrame,
                                target_rows: int = None,
                                seed: int = RANDOM_SEED) -> pd.DataFrame:
    """
    Generate manufacturing production records.
    Includes learning-curve effects and factory-specific quality.
    """
    rng = np.random.default_rng(seed + 200)
    target = target_rows or RECORD_COUNTS['fact_manufacturing']

    comp_ids     = dim_component['ComponentID'].values
    comp_cost    = dict(zip(dim_component['ComponentID'], dim_component['UnitCost']))
    comp_cat     = dict(zip(dim_component['ComponentID'], dim_component['Category']))
    factory_ids  = dim_factory['FactoryID'].values
    factory_cap  = dict(zip(dim_factory['FactoryID'], dim_factory['AnnualCapacity']))
    date_range   = pd.date_range(DATE_START, DATE_END, freq='D')

    # Factory quality factors (some factories are better)
    factory_quality = {fid: float(rng.uniform(0.88, 0.99)) for fid in factory_ids}

    records = []
    for i in range(target):
        comp_id = rng.choice(comp_ids)
        fac_id = rng.choice(factory_ids)
        prod_date = pd.Timestamp(rng.choice(date_range))

        base_cost = float(comp_cost.get(comp_id, 5000))
        quality = factory_quality.get(fac_id, 0.95)

        # Learning curve: costs decrease slightly over time
        year_frac = (prod_date - pd.Timestamp(DATE_START)).days / 1826
        learning_factor = 1.0 - 0.08 * year_frac  # 8% reduction over 5 years

        # Production cost with variance
        prod_cost = base_cost * learning_factor * float(rng.uniform(0.85, 1.25))

        # Assembly time (hours) — varies by component category
        cat = comp_cat.get(comp_id, 'Unknown')
        if 'Core' in cat or 'Processor' in cat:
            base_time = float(rng.uniform(40, 120))
        elif 'Shield' in cat or 'Frame' in cat:
            base_time = float(rng.uniform(20, 60))
        else:
            base_time = float(rng.uniform(8, 40))

        assembly_time = base_time * learning_factor * float(rng.uniform(0.8, 1.3))

        # Defect rate — correlated with factory quality
        defect_rate = (1 - quality) * float(rng.uniform(0.3, 2.5))
        defect_rate = min(defect_rate, 0.25)  # cap at 25%

        # Batch size
        batch_size = int(rng.choice([10, 25, 50, 100, 200],
                                     p=[0.10, 0.25, 0.30, 0.25, 0.10]))

        # Quality grade
        if defect_rate < 0.02:
            grade = 'A+'
        elif defect_rate < 0.05:
            grade = 'A'
        elif defect_rate < 0.10:
            grade = 'B'
        elif defect_rate < 0.15:
            grade = 'C'
        else:
            grade = 'D'

        records.append({
            'ProductionID':     f'PRD-{i+1:07d}',
            'ComponentID':      comp_id,
            'FactoryID':        fac_id,
            'ProductionDate':   prod_date.strftime('%Y-%m-%d'),
            'ProductionCost':   round(prod_cost, 2),
            'AssemblyTime_hrs': round(assembly_time, 1),
            'DefectRate':       round(defect_rate, 4),
            'BatchSize':        batch_size,
            'QualityGrade':     grade,
            'YieldRate':        round(1 - defect_rate, 4),
            'ShiftType':        rng.choice(['Day', 'Swing', 'Night'],
                                           p=[0.45, 0.35, 0.20]),
            'DateKey':          int(prod_date.strftime('%Y%m%d')),
        })

    df = pd.DataFrame(records)
    print(f"    ✓ {len(df):,} manufacturing records generated")
    return df


if __name__ == '__main__':
    from python.generators.dimension_generators import generate_all_dimensions
    dims = generate_all_dimensions()
    df = generate_fact_manufacturing(dims['DimComponent'], dims['DimFactory'],
                                    dims['DimDate'], target_rows=1000)
    print(df.head())
