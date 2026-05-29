"""
AGIS Finance Fact Table Generator
─────────────────────────────────
Generates ~5K monthly financial records across departments.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import pandas as pd
import numpy as np
from config.settings import RANDOM_SEED, DATE_START, DATE_END, RECORD_COUNTS, DEPARTMENTS


def generate_fact_finance(dim_department: pd.DataFrame,
                          dim_date: pd.DataFrame,
                          seed: int = RANDOM_SEED) -> pd.DataFrame:
    """
    Generate monthly financial records per department.
    Includes budget, actual costs, R&D spending, revenue, and investment data.
    """
    rng = np.random.default_rng(seed + 300)

    dept_ids    = dim_department['DepartmentID'].values
    dept_names  = dict(zip(dim_department['DepartmentID'], dim_department['DepartmentName']))
    dept_budget = dict(zip(dim_department['DepartmentID'], dim_department['AnnualBudget']))

    months = pd.date_range(DATE_START, DATE_END, freq='MS')  # month start

    records = []
    budget_counter = 0

    for dept_id in dept_ids:
        annual_budget = float(dept_budget.get(dept_id, 10_000_000))
        monthly_budget = annual_budget / 12
        dept_name = dept_names.get(dept_id, '')

        # Department-specific spending profiles
        is_rd = 'R&D' in dept_name
        is_ops = dept_name in ['Flight Operations', 'Manufacturing']
        is_exec = dept_name in ['Executive Office', 'Investor Relations']

        for month in months:
            budget_counter += 1
            year_idx = month.year - 2021  # 0-4

            # Growth factors
            growth = 1 + year_idx * 0.08  # 8% annual growth
            seasonal = 1.0 + 0.1 * np.sin(2 * np.pi * month.month / 12)

            # Budget (planned)
            budget_planned = monthly_budget * growth * float(rng.uniform(0.95, 1.05))

            # Actual operational cost (with overruns)
            overrun = float(rng.uniform(0.88, 1.15))
            operational_cost = budget_planned * overrun * seasonal

            # R&D Cost (mainly for R&D departments)
            if is_rd:
                rd_cost = operational_cost * float(rng.uniform(0.60, 0.85))
            elif dept_name == 'Engineering':
                rd_cost = operational_cost * float(rng.uniform(0.20, 0.40))
            else:
                rd_cost = operational_cost * float(rng.uniform(0.0, 0.08))

            # Revenue attribution
            if is_ops:
                revenue = float(rng.uniform(500_000, 3_000_000)) * growth
            elif is_exec:
                revenue = float(rng.uniform(1_000_000, 8_000_000)) * growth
            else:
                revenue = float(rng.uniform(0, 500_000)) * growth

            # Investment rounds (quarterly spikes)
            investment = 0.0
            if month.month in [1, 4, 7, 10] and is_exec:
                investment = float(rng.uniform(2_000_000, 20_000_000)) * (1 + year_idx * 0.15)

            # Headcount cost
            headcount_cost = float(rng.uniform(100_000, 800_000))

            records.append({
                'BudgetID':         f'BDG-{budget_counter:06d}',
                'DepartmentID':     dept_id,
                'Month':            month.strftime('%Y-%m-%d'),
                'Year':             month.year,
                'MonthNum':         month.month,
                'BudgetPlanned':    round(budget_planned, 2),
                'OperationalCost':  round(operational_cost, 2),
                'RDCost':           round(rd_cost, 2),
                'Revenue':          round(revenue, 2),
                'Investment':       round(investment, 2),
                'HeadcountCost':    round(headcount_cost, 2),
                'BudgetVariance':   round(operational_cost - budget_planned, 2),
                'BudgetVariancePct': round((operational_cost - budget_planned) / max(budget_planned, 1) * 100, 2),
                'DateKey':          int(month.strftime('%Y%m%d')),
            })

    df = pd.DataFrame(records)
    print(f"    ✓ {len(df):,} finance records generated")
    return df


if __name__ == '__main__':
    from python.generators.dimension_generators import generate_all_dimensions
    dims = generate_all_dimensions()
    df = generate_fact_finance(dims['DimDepartment'], dims['DimDate'])
    print(df.head())
    print(f"Shape: {df.shape}")
