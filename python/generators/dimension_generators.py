"""
AGIS Dimension Table Generators
────────────────────────────────
Generates all 8 dimension tables for the star schema.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from config.settings import (
    RANDOM_SEED, DATE_START, DATE_END, AIRCRAFT_MODELS,
    FACTORY_LOCATIONS, COMPONENT_CATEGORIES, DEPARTMENTS,
    MISSION_TYPES, FAILURE_CATEGORIES, RECORD_COUNTS
)


def generate_dim_date() -> pd.DataFrame:
    """Generate a comprehensive date dimension table."""
    dates = pd.date_range(start=DATE_START, end=DATE_END, freq='D')
    df = pd.DataFrame({'Date': dates})
    df['DateKey']       = df['Date'].dt.strftime('%Y%m%d').astype(int)
    df['Year']          = df['Date'].dt.year
    df['Quarter']       = df['Date'].dt.quarter
    df['Month']         = df['Date'].dt.month
    df['MonthName']     = df['Date'].dt.strftime('%B')
    df['Week']          = df['Date'].dt.isocalendar().week.astype(int)
    df['DayOfWeek']     = df['Date'].dt.dayofweek
    df['DayName']       = df['Date'].dt.strftime('%A')
    df['DayOfMonth']    = df['Date'].dt.day
    df['DayOfYear']     = df['Date'].dt.dayofyear
    df['IsWeekend']     = df['DayOfWeek'].isin([5, 6]).astype(int)
    df['FiscalYear']    = df['Date'].apply(lambda d: d.year if d.month >= 7 else d.year - 1)
    df['FiscalQuarter'] = df['Date'].apply(lambda d: (d.month - 7) % 12 // 3 + 1)
    df['YearMonth']     = df['Date'].dt.strftime('%Y-%m')
    df['YearQuarter']   = df['Year'].astype(str) + '-Q' + df['Quarter'].astype(str)
    # US holidays (simplified)
    holidays = {
        (1, 1): "New Year's Day", (7, 4): "Independence Day",
        (12, 25): "Christmas Day", (11, 11): "Veterans Day",
    }
    df['IsHoliday'] = df['Date'].apply(
        lambda d: 1 if (d.month, d.day) in holidays else 0
    )
    df['HolidayName'] = df['Date'].apply(
        lambda d: holidays.get((d.month, d.day), '')
    )
    return df


def generate_dim_aircraft(rng: np.random.Generator) -> pd.DataFrame:
    """Generate aircraft dimension with 50 craft across 7 models."""
    n = RECORD_COUNTS['dim_aircraft']
    records = []
    for i in range(n):
        model_info = AIRCRAFT_MODELS[i % len(AIRCRAFT_MODELS)]
        commission_date = pd.Timestamp(DATE_START) + timedelta(days=int(rng.integers(0, 365 * 3)))
        records.append({
            'AircraftID':       f'AG-{i+1:04d}',
            'SerialNumber':     f'SN-{rng.integers(100000, 999999)}',
            'Model':            model_info['model'],
            'AircraftClass':    model_info['class'],
            'MaxAltitude':      model_info['max_alt'],
            'MaxVelocity':      model_info['max_vel'],
            'CrewCapacity':     model_info['crew'],
            'CommissionDate':   commission_date.strftime('%Y-%m-%d'),
            'FleetAssignment':  rng.choice(['Alpha Fleet', 'Bravo Fleet', 'Charlie Fleet',
                                            'Delta Fleet', 'Echo Fleet']),
            'Status':           rng.choice(['Active', 'Active', 'Active', 'Active',
                                            'Maintenance', 'Standby', 'Decommissioned'],
                                           p=[0.55, 0.15, 0.10, 0.05, 0.08, 0.04, 0.03]),
            'CoreHealthIndex':  round(float(rng.uniform(0.55, 1.0)), 3),
            'TotalFlightHours': int(rng.integers(100, 8000)),
        })
    return pd.DataFrame(records)


def generate_dim_pilot(rng: np.random.Generator) -> pd.DataFrame:
    """Generate 100 pilots with ranks and certifications."""
    n = RECORD_COUNTS['dim_pilot']
    first_names = ['James', 'Sarah', 'Marcus', 'Elena', 'David', 'Priya',
                   'Chen', 'Akira', 'Fatima', 'Olga', 'Raj', 'Maria',
                   'Thomas', 'Yuki', 'Amara', 'Liam', 'Sofia', 'Wei',
                   'Zara', 'Kai', 'Nina', 'Oscar', 'Luna', 'Viktor']
    last_names  = ['Hawkins', 'Mercer', 'Zhang', 'Patel', 'Kowalski',
                   'Nakamura', 'Okafor', 'Johansson', 'Torres', 'Kim',
                   'Mueller', 'Singh', 'Volkov', 'Tanaka', 'Rossi',
                   'Brooks', 'Ahmad', 'Chen', 'Larsson', 'Diaz']
    ranks = ['Flight Lieutenant', 'Captain', 'Major', 'Lt Colonel', 'Colonel',
             'Test Pilot I', 'Test Pilot II', 'Chief Test Pilot']
    certs = ['AG-Basic', 'AG-Advanced', 'AG-Expert', 'AG-Instructor',
             'Combat Rated', 'Cargo Rated', 'High-Alt Certified']

    records = []
    for i in range(n):
        pilot_certs = list(rng.choice(certs, size=rng.integers(1, 4), replace=False))
        records.append({
            'PilotID':          f'PLT-{i+1:04d}',
            'FirstName':        rng.choice(first_names),
            'LastName':         rng.choice(last_names),
            'Rank':             rng.choice(ranks),
            'Certifications':   ', '.join(pilot_certs),
            'FlightHours':      int(rng.integers(200, 12000)),
            'Specialization':   rng.choice(['Propulsion Testing', 'High-Altitude Ops',
                                            'Combat Systems', 'Cargo Operations',
                                            'Research Flights', 'Training']),
            'HireDate':         (pd.Timestamp(DATE_START) + timedelta(
                                    days=int(rng.integers(0, 365 * 4)))).strftime('%Y-%m-%d'),
            'Status':           rng.choice(['Active', 'Active', 'Active',
                                            'On Leave', 'Training', 'Retired'],
                                           p=[0.60, 0.15, 0.10, 0.06, 0.05, 0.04]),
        })
    return pd.DataFrame(records)


def generate_dim_mission(rng: np.random.Generator) -> pd.DataFrame:
    """Generate 500 unique missions."""
    n = RECORD_COUNTS['dim_mission']
    records = []
    for i in range(n):
        m_type = rng.choice(MISSION_TYPES)
        records.append({
            'MissionID':       f'MSN-{i+1:05d}',
            'MissionName':     f'Operation {rng.choice(["Thunderbolt", "Horizon", "Eclipse", "Vanguard", "Apex", "Sentinel", "Phoenix", "Spectre", "Nova", "Zenith"])}-{rng.integers(100,999)}',
            'MissionType':     m_type,
            'Priority':        rng.choice(['Critical', 'High', 'Medium', 'Low'],
                                          p=[0.10, 0.25, 0.45, 0.20]),
            'TargetAltitude':  int(rng.integers(5000, 35000)),
            'TargetVelocity':  int(rng.integers(200, 1500)),
            'DurationPlanned': int(rng.integers(1800, 14400)),  # seconds
            'Classification':  rng.choice(['Unclassified', 'Confidential',
                                            'Secret', 'Top Secret'],
                                          p=[0.40, 0.30, 0.20, 0.10]),
        })
    return pd.DataFrame(records)


def generate_dim_factory() -> pd.DataFrame:
    """Generate factory dimension from config."""
    records = []
    for i, fac in enumerate(FACTORY_LOCATIONS):
        records.append({
            'FactoryID':        f'FAC-{i+1:03d}',
            'FactoryName':      fac['name'],
            'City':             fac['city'],
            'Country':          fac['country'],
            'AnnualCapacity':   fac['capacity'],
            'CertificationLevel': np.random.choice(['ISO-9001', 'AS9100D', 'NADCAP']),
            'OperatingSince':   np.random.choice([2018, 2019, 2020, 2021]),
        })
    return pd.DataFrame(records)


def generate_dim_component(rng: np.random.Generator) -> pd.DataFrame:
    """Generate 200 components across 10 categories."""
    n = RECORD_COUNTS['dim_component']
    suppliers = ['GraviTech Industries', 'Quantum Dynamics Corp', 'AeroCore Systems',
                 'Nexus Manufacturing', 'Pinnacle Parts Ltd', 'FusionForge Inc',
                 'StellarWorks', 'Precision AG Solutions']
    records = []
    for i in range(n):
        cat = COMPONENT_CATEGORIES[i % len(COMPONENT_CATEGORIES)]
        records.append({
            'ComponentID':      f'CMP-{i+1:04d}',
            'ComponentName':    f'{cat} v{rng.integers(1,9)}.{rng.integers(0,9)}',
            'Category':         cat,
            'Supplier':         rng.choice(suppliers),
            'UnitCost':         round(float(rng.uniform(500, 50000)), 2),
            'CriticalityRating': rng.choice(['Critical', 'High', 'Medium', 'Low'],
                                            p=[0.15, 0.30, 0.35, 0.20]),
            'LeadTimeDays':     int(rng.integers(7, 120)),
            'LifespanHours':    int(rng.integers(2000, 20000)),
            'Weight_kg':        round(float(rng.uniform(0.5, 250)), 1),
        })
    return pd.DataFrame(records)


def generate_dim_department() -> pd.DataFrame:
    """Generate department dimension."""
    records = []
    for i, dept in enumerate(DEPARTMENTS):
        records.append({
            'DepartmentID':     f'DEPT-{i+1:03d}',
            'DepartmentName':   dept,
            'HeadCount':        np.random.randint(15, 200),
            'AnnualBudget':     round(np.random.uniform(2_000_000, 50_000_000), 0),
            'CostCenter':       f'CC-{(i+1)*100}',
        })
    return pd.DataFrame(records)


def generate_dim_failure_type(rng: np.random.Generator) -> pd.DataFrame:
    """Generate 30 failure type codes."""
    n = RECORD_COUNTS['dim_failure_type']
    failure_names = [
        'AG Core Overload', 'Stabilizer Misalignment', 'Power Cell Depletion',
        'Thermal Runaway', 'Control Software Crash', 'Structural Fatigue Crack',
        'Lift Nozzle Blockage', 'Inertial Dampener Drift', 'Quantum Processor Fault',
        'Energy Grid Surge', 'Coolant Leak', 'Hydraulic Pressure Loss',
        'Wiring Harness Short', 'Sensor Calibration Error', 'Bearing Wear',
        'Plasma Containment Breach', 'Vibration Resonance', 'Corrosion Damage',
        'Seal Degradation', 'Connector Oxidation', 'Software Memory Leak',
        'Firmware Version Conflict', 'Actuator Stall', 'Fan Blade Erosion',
        'Insulation Breakdown', 'Relay Failure', 'Circuit Board Delamination',
        'Torque Limiter Slip', 'Pressure Regulator Fault', 'EMI Interference',
    ]
    records = []
    for i in range(min(n, len(failure_names))):
        cat = FAILURE_CATEGORIES[i % len(FAILURE_CATEGORIES)]
        records.append({
            'FailureTypeID':    f'FLR-{i+1:03d}',
            'FailureCode':      f'{cat[:3].upper()}-{i+1:03d}',
            'FailureName':      failure_names[i],
            'Category':         cat,
            'AvgRepairCost':    round(float(rng.uniform(5000, 250000)), 0),
            'AvgDowntimeHours': round(float(rng.uniform(4, 720)), 0),
            'Severity':         int(rng.choice([1, 2, 3, 4, 5],
                                               p=[0.10, 0.20, 0.30, 0.25, 0.15])),
            'SafetyImpact':     rng.choice(['None', 'Low', 'Medium', 'High', 'Critical'],
                                           p=[0.05, 0.20, 0.35, 0.25, 0.15]),
        })
    return pd.DataFrame(records)


def generate_all_dimensions(seed: int = RANDOM_SEED) -> dict:
    """Generate all dimension tables and return as dict of DataFrames."""
    rng = np.random.default_rng(seed)
    print("  → Generating DimDate...")
    dims = {'DimDate': generate_dim_date()}
    print(f"    ✓ {len(dims['DimDate']):,} rows")

    print("  → Generating DimAircraft...")
    dims['DimAircraft'] = generate_dim_aircraft(rng)
    print(f"    ✓ {len(dims['DimAircraft']):,} rows")

    print("  → Generating DimPilot...")
    dims['DimPilot'] = generate_dim_pilot(rng)
    print(f"    ✓ {len(dims['DimPilot']):,} rows")

    print("  → Generating DimMission...")
    dims['DimMission'] = generate_dim_mission(rng)
    print(f"    ✓ {len(dims['DimMission']):,} rows")

    print("  → Generating DimFactory...")
    dims['DimFactory'] = generate_dim_factory()
    print(f"    ✓ {len(dims['DimFactory']):,} rows")

    print("  → Generating DimComponent...")
    dims['DimComponent'] = generate_dim_component(rng)
    print(f"    ✓ {len(dims['DimComponent']):,} rows")

    print("  → Generating DimDepartment...")
    dims['DimDepartment'] = generate_dim_department()
    print(f"    ✓ {len(dims['DimDepartment']):,} rows")

    print("  → Generating DimFailureType...")
    dims['DimFailureType'] = generate_dim_failure_type(rng)
    print(f"    ✓ {len(dims['DimFailureType']):,} rows")

    return dims


if __name__ == '__main__':
    dims = generate_all_dimensions()
    for name, df in dims.items():
        print(f"{name}: {len(df)} rows, columns: {list(df.columns)}")
