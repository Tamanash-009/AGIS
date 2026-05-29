# AGIS Deployment Guide

## Prerequisites

- **Python 3.10+** — [Download](https://python.org/downloads/)
- **Power BI Desktop** — [Download](https://powerbi.microsoft.com/desktop/)
- **Git** — [Download](https://git-scm.com/)

## Quick Start (5 minutes)

```bash
# Clone the repository
git clone https://github.com/yourusername/AGIS.git
cd AGIS

# Install Python dependencies
pip install -r requirements.txt

# Generate lite dataset (~20K rows, fast)
python python/generators/data_generator.py --lite

# Run ETL pipeline
python python/etl/pipeline.py

# Train ML models
python python/ml/predictive_maintenance.py

# Open web dashboard
start dashboard/index.html
```

## Full Dataset (10-15 minutes)

```bash
# Generate full dataset (~850K+ rows)
python python/generators/data_generator.py

# Run full ETL
python python/etl/pipeline.py

# Train and evaluate ML models
python python/ml/predictive_maintenance.py --evaluate
```

## Power BI Setup

### 1. Import Data
1. Open Power BI Desktop
2. Get Data → Text/CSV
3. Import all CSV files from `data/processed/`
4. Import `MLPredictions_Maintenance.csv`

### 2. Apply Theme
1. View → Themes → Browse for themes
2. Select `powerbi/themes/agis_dark_theme.json`

### 3. Create Data Model
1. Go to Model View
2. Create relationships:
   - `FactFlightTelemetry[DateKey]` → `DimDate[DateKey]`
   - `FactFlightTelemetry[AircraftID]` → `DimAircraft[AircraftID]`
   - `FactFlightTelemetry[PilotID]` → `DimPilot[PilotID]`
   - `FactFlightTelemetry[MissionID]` → `DimMission[MissionID]`
   - `FactMaintenance[AircraftID]` → `DimAircraft[AircraftID]`
   - `FactMaintenance[FailureTypeID]` → `DimFailureType[FailureTypeID]`
   - `FactManufacturing[ComponentID]` → `DimComponent[ComponentID]`
   - `FactManufacturing[FactoryID]` → `DimFactory[FactoryID]`
   - `FactFinance[DepartmentID]` → `DimDepartment[DepartmentID]`
3. All fact-to-dim relationships: Many-to-One, Single direction

### 4. Create DAX Measures
1. Copy measures from `powerbi/dax/measures.dax`
2. Create a dedicated Measures table
3. Organize by display folder (Executive, Flight Ops, etc.)

### 5. Configure RLS
1. Modeling → Manage Roles
2. Create roles per `powerbi/dax/rls_roles.dax`

### 6. Build Dashboards
1. Follow visual specifications in `docs/dashboard_design.md`
2. Use the Power BI theme for consistent styling
3. Add slicers, cross-filtering, and drill-through

## Database Connection (Optional PostgreSQL)

```bash
# If using PostgreSQL instead of SQLite:
# 1. Create database
createdb agis

# 2. Run schema
psql -d agis -f database/schema.sql

# 3. Update config/settings.py
# DB_URI = "postgresql://user:pass@localhost:5432/agis"

# 4. Re-run ETL
python python/etl/pipeline.py
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `UnicodeEncodeError` on Windows | Set `PYTHONIOENCODING=utf-8` environment variable |
| Missing dependencies | Run `pip install -r requirements.txt` |
| Power BI can't find data | Ensure CSV files are in `data/processed/` |
| ML accuracy is low | Generate full dataset (not lite mode) |
| SQLite locked | Close all connections before re-running ETL |

## Output Files

After running all pipelines, you should have:

```
data/raw/             → 12 CSV files (generated data)
data/processed/       → 12 CSV files (transformed) + 1 ML predictions
data/synthetic/       → Generation summary
database/agis.db      → SQLite database
python/ml/models/     → Trained ML models (.joblib)
```
