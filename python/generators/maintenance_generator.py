"""
AGIS Maintenance Fact Table Generator
─────────────────────────────────────
Generates ~50K maintenance records with Weibull-based failure timing.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import pandas as pd
import numpy as np
from datetime import timedelta
from config.settings import RANDOM_SEED, DATE_START, DATE_END, RECORD_COUNTS


def generate_fact_maintenance(dim_aircraft: pd.DataFrame,
                              dim_failure_type: pd.DataFrame,
                              dim_date: pd.DataFrame,
                              target_rows: int = None,
                              seed: int = RANDOM_SEED) -> pd.DataFrame:
    """
    Generate maintenance fact table.
    Failures correlate with aircraft health and flight hours.
    """
    rng = np.random.default_rng(seed + 100)  # offset seed for variety
    target = target_rows or RECORD_COUNTS['fact_maintenance']

    aircraft_ids   = dim_aircraft['AircraftID'].values
    health_map     = dict(zip(dim_aircraft['AircraftID'], dim_aircraft['CoreHealthIndex']))
    hours_map      = dict(zip(dim_aircraft['AircraftID'], dim_aircraft['TotalFlightHours']))
    failure_ids    = dim_failure_type['FailureTypeID'].values
    severity_map   = dict(zip(dim_failure_type['FailureTypeID'], dim_failure_type['Severity']))
    cost_map       = dict(zip(dim_failure_type['FailureTypeID'], dim_failure_type['AvgRepairCost']))
    downtime_map   = dict(zip(dim_failure_type['FailureTypeID'], dim_failure_type['AvgDowntimeHours']))
    date_range     = pd.date_range(DATE_START, DATE_END, freq='D')

    records = []
    for i in range(target):
        ac_id = rng.choice(aircraft_ids)
        health = health_map.get(ac_id, 0.8)
        hours = hours_map.get(ac_id, 2000)

        # Higher failure rate for unhealthy, high-hour aircraft
        failure_weight = (1.0 - health) * 0.6 + (hours / 10000) * 0.4

        # Select failure type (weighted toward severity for unhealthy craft)
        fail_id = rng.choice(failure_ids)
        severity = int(severity_map.get(fail_id, 3))
        base_cost = float(cost_map.get(fail_id, 30000))
        base_downtime = float(downtime_map.get(fail_id, 48))

        # Add variance
        repair_cost = base_cost * float(rng.uniform(0.6, 1.8))
        downtime_hours = base_downtime * float(rng.uniform(0.5, 2.0))

        # Seasonal pattern: more failures in summer (thermal stress)
        maint_date = pd.Timestamp(rng.choice(date_range))
        month = maint_date.month
        if month in [6, 7, 8]:
            # 30% more likely — but we just bias cost up slightly
            repair_cost *= 1.15

        # Maintenance type
        maint_type = rng.choice(
            ['Corrective', 'Preventive', 'Predictive', 'Emergency'],
            p=[0.40, 0.30, 0.20, 0.10]
        )

        # Resolution
        resolution = rng.choice(
            ['Repaired', 'Replaced', 'Calibrated', 'Software Update', 'Pending'],
            p=[0.35, 0.25, 0.20, 0.15, 0.05]
        )

        records.append({
            'MaintenanceID':    f'MNT-{i+1:06d}',
            'AircraftID':       ac_id,
            'FailureTypeID':    fail_id,
            'MaintenanceDate':  maint_date.strftime('%Y-%m-%d'),
            'MaintenanceType':  maint_type,
            'FailureSeverity':  severity,
            'RepairCost':       round(repair_cost, 2),
            'DowntimeHours':    round(downtime_hours, 1),
            'Resolution':       resolution,
            'PartsReplaced':    int(rng.integers(0, 8)),
            'TechnicianCount':  int(rng.integers(1, 6)),
            'DateKey':          int(maint_date.strftime('%Y%m%d')),
        })

    df = pd.DataFrame(records)
    print(f"    ✓ {len(df):,} maintenance records generated")
    return df


if __name__ == '__main__':
    from python.generators.dimension_generators import generate_all_dimensions
    dims = generate_all_dimensions()
    df = generate_fact_maintenance(dims['DimAircraft'], dims['DimFailureType'],
                                  dims['DimDate'], target_rows=1000)
    print(df.head())
