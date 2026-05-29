# AGIS Data Dictionary

## Overview

This document describes all tables, columns, data types, and business rules in the AGIS star schema.

---

## Dimension Tables

### DimDate
> Conformed date dimension covering 2021-01-01 to 2025-12-31

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| DateKey | INT (PK) | YYYYMMDD surrogate key | 20250115 |
| Date | DATE | Calendar date | 2025-01-15 |
| Year | INT | Calendar year | 2025 |
| Quarter | INT | Quarter (1-4) | 1 |
| Month | INT | Month number (1-12) | 1 |
| MonthName | VARCHAR(20) | Full month name | January |
| Week | INT | ISO week number | 3 |
| DayOfWeek | INT | 0=Monday, 6=Sunday | 2 |
| DayName | VARCHAR(15) | Full day name | Wednesday |
| DayOfMonth | INT | Day of month | 15 |
| DayOfYear | INT | Day of year (1-366) | 15 |
| IsWeekend | INT | 1=Weekend, 0=Weekday | 0 |
| FiscalYear | INT | Fiscal year (Jul-Jun) | 2024 |
| FiscalQuarter | INT | Fiscal quarter | 3 |
| YearMonth | VARCHAR(7) | YYYY-MM format | 2025-01 |
| YearQuarter | VARCHAR(7) | YYYY-QN format | 2025-Q1 |
| IsHoliday | INT | 1=US Holiday | 0 |
| HolidayName | VARCHAR(50) | Holiday name if applicable | |

---

### DimAircraft
> Fleet inventory with 50 aircraft across 7 models

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| AircraftID | VARCHAR(10) (PK) | Unique aircraft ID | AG-0001 |
| SerialNumber | VARCHAR(20) | Manufacturing serial | SN-847293 |
| Model | VARCHAR(10) | Aircraft model | AG-X4 |
| AircraftClass | VARCHAR(30) | Classification | Stealth Recon |
| MaxAltitude | INT | Maximum altitude (meters) | 35000 |
| MaxVelocity | INT | Maximum velocity (m/s) | 1500 |
| CrewCapacity | INT | Number of crew | 1 |
| CommissionDate | DATE | Date entered service | 2022-03-15 |
| FleetAssignment | VARCHAR(20) | Fleet group | Alpha Fleet |
| Status | VARCHAR(20) | Operational status | Active |
| CoreHealthIndex | REAL | AG Core health (0-1) | 0.847 |
| TotalFlightHours | INT | Cumulative flight hours | 4523 |

**Aircraft Models:**
| Model | Class | Max Alt (m) | Max Vel (m/s) | Crew |
|-------|-------|-------------|---------------|------|
| AG-X1 | Light Scout | 15,000 | 800 | 1 |
| AG-X2 | Tactical Fighter | 25,000 | 1,200 | 1 |
| AG-X3 | Heavy Lifter | 12,000 | 500 | 3 |
| AG-X4 | Stealth Recon | 35,000 | 1,500 | 1 |
| AG-X5 | Cargo Transport | 10,000 | 400 | 4 |
| AG-X6 | Research Platform | 20,000 | 600 | 2 |
| AG-X7 | Command Cruiser | 30,000 | 900 | 6 |

---

### DimPilot
> 100 pilots with ranks, certifications, and specializations

| Column | Type | Description |
|--------|------|-------------|
| PilotID | VARCHAR(10) (PK) | Unique pilot ID |
| FirstName | VARCHAR(30) | First name |
| LastName | VARCHAR(30) | Last name |
| Rank | VARCHAR(30) | Military/test pilot rank |
| Certifications | VARCHAR(200) | Comma-separated certs |
| FlightHours | INT | Total flight hours |
| Specialization | VARCHAR(50) | Area of expertise |
| HireDate | DATE | Date hired |
| Status | VARCHAR(20) | Active/On Leave/Training/Retired |

---

### DimMission
> 500 unique missions with types and classifications

| Column | Type | Description |
|--------|------|-------------|
| MissionID | VARCHAR(12) (PK) | Unique mission ID |
| MissionName | VARCHAR(60) | Operation codename |
| MissionType | VARCHAR(30) | Type of mission |
| Priority | VARCHAR(15) | Critical/High/Medium/Low |
| TargetAltitude | INT | Target altitude (m) |
| TargetVelocity | INT | Target velocity (m/s) |
| DurationPlanned | INT | Planned duration (seconds) |
| Classification | VARCHAR(20) | Security classification |

---

### DimFactory, DimComponent, DimDepartment, DimFailureType
> See `database/schema.sql` for complete DDL with column comments.

---

## Fact Tables

### FactFlightTelemetry (~500K rows)
> Per-second flight telemetry readings from onboard sensors

| Column | Type | Description | Range |
|--------|------|-------------|-------|
| FlightID | VARCHAR(12) | Flight identifier | FLT-000001 |
| AircraftID | VARCHAR(10) (FK) | Aircraft reference | AG-0001 |
| PilotID | VARCHAR(10) (FK) | Pilot reference | PLT-0001 |
| MissionID | VARCHAR(12) (FK) | Mission reference | MSN-00001 |
| Timestamp | DATETIME | Reading timestamp | ISO 8601 |
| FlightPhase | VARCHAR(15) | Current phase | Takeoff/Climb/Cruise/Descent/Landing |
| Altitude_m | REAL | Altitude in meters | 0 - 35,000 |
| Velocity_mps | REAL | Velocity in m/s | 0 - 1,500 |
| LiftOutput_kN | REAL | AG lift force (kN) | 0 - 100 |
| EnergyConsumed_kW | REAL | Energy draw (kW) | 0 - 500 |
| StabilityScore | REAL | Stability index | 0 - 100 |
| CoreTemp_C | REAL | AG Core temperature | -56 to 400 |
| Turbulence | REAL | Turbulence factor | 0 - 1 |
| MissionStatus | VARCHAR(20) | Overall mission status | Completed/Aborted/Anomaly |
| DateKey | INT (FK) | Date dimension key | YYYYMMDD |

### FactMaintenance (~50K rows)
> Maintenance events per aircraft

### FactManufacturing (~300K rows)
> Production records per component per factory

### FactFinance (~5K rows)
> Monthly financial data per department

---

## Derived Columns (ETL)

| Table | Column | Formula |
|-------|--------|---------|
| FactFlightTelemetry | PropulsionEfficiency | LiftOutput / EnergyConsumed |
| FactFlightTelemetry | EnergyPerKm | (Energy / Velocity) * 1000 |
| DimAircraft | FleetAge_Years | (2025-12-31 - CommissionDate) / 365.25 |
| DimAircraft | HealthCategory | Binned CoreHealthIndex |
| FactMaintenance | CostCategory | Binned RepairCost |
| FactFinance | ROI | (Revenue - RDCost) / RDCost * 100 |
