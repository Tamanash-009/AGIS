# AGIS — Architecture Documentation

## 1. System Architecture

```mermaid
graph TB
    subgraph "Data Generation Layer"
        A["Telemetry Generator<br/>500K+ records/run"]
        B["Maintenance Generator<br/>10K+ events"]
        C["Manufacturing Generator<br/>50K+ units"]
        D["Finance Generator<br/>720 records"]
    end

    subgraph "ETL Pipeline"
        E["Extract<br/>CSV/Parquet"]
        F["Transform<br/>Pandas + Cleaning"]
        G["Load<br/>SQLite Star Schema"]
    end

    subgraph "Analytics Engine"
        H["DAX Measures (88)<br/>Time Intelligence + KPIs"]
        I["ML Pipeline<br/>RF + GBR Classifiers"]
        J["Power BI Theme<br/>Enterprise Dark"]
    end

    subgraph "Presentation Layer"
        K["Page 1: Executive Overview"]
        L["Page 2: Flight Operations"]
        M["Page 3: Propulsion Analytics"]
        N["Page 4: Maintenance & Incidents"]
        O["Page 5: Manufacturing Intelligence"]
        P["Page 6: Financial Analysis"]
        Q["Page 7: Mission Intelligence"]
        R["Page 8: Geographic Intelligence"]
        S["Page 9: Predictive Analytics"]
        T["Page 10: Executive Insights"]
    end

    subgraph "Security Layer"
        U["RLS: Executive Role"]
        V["RLS: Engineer Role"]
        W["RLS: Operations Role"]
        X["RLS: Finance Role"]
        Y["RLS: Investor Role"]
    end

    A & B & C & D --> E
    E --> F --> G
    G --> H & I
    H --> K & L & M & N & O & P & Q & R & S & T
    I --> S
    U & V & W & X & Y -.-> H
```

---

## 2. Data Flow Diagram

```mermaid
flowchart LR
    GEN["Python Generators<br/>faker + numpy"] -->|CSV| RAW["data/raw/"]
    RAW -->|pandas.read_csv| ETL["ETL Pipeline<br/>python/etl/"]
    ETL -->|data cleaning<br/>type casting<br/>FK generation| PROC["data/processed/"]
    PROC -->|sqlite3 INSERT| DB["agis.db<br/>Star Schema"]
    DB -->|queries| PBI["Power BI<br/>DirectQuery / Import"]
    DB -->|chart data| WEB["Web Dashboard<br/>dashboard/"]
    DB -->|features| ML["ML Pipeline<br/>python/ml/"]
    ML -->|predictions CSV| PROC
    PBI -->|RLS filter| USERS["5 User Roles"]
```

---

## 3. Star Schema (ER Diagram)

```mermaid
erDiagram
    DimDate ||--o{ FactFlightTelemetry : "DateKey"
    DimDate ||--o{ FactMaintenance : "DateKey"
    DimDate ||--o{ FactManufacturing : "DateKey"
    DimDate ||--o{ FactFinance : "DateKey"
    DimAircraft ||--o{ FactFlightTelemetry : "AircraftKey"
    DimAircraft ||--o{ FactMaintenance : "AircraftKey"
    DimPilot ||--o{ FactFlightTelemetry : "PilotKey"
    DimMission ||--o{ FactFlightTelemetry : "MissionKey"
    DimFactory ||--o{ FactManufacturing : "FactoryKey"
    DimComponent ||--o{ FactManufacturing : "ComponentKey"
    DimDepartment ||--o{ FactFinance : "DepartmentKey"
    DimFailureType ||--o{ FactMaintenance : "FailureTypeKey"

    DimDate {
        int DateKey PK
        date FullDate
        int Year
        int Quarter
        int Month
        string MonthName
        int Week
        int DayOfWeek
        boolean IsWeekend
        int FiscalYear
        int FiscalQuarter
    }

    DimAircraft {
        int AircraftKey PK
        string AircraftID
        string Model
        string Status
        date CommissionDate
        string HomeBase
        float MaxAltitude
        float MaxSpeed
    }

    FactFlightTelemetry {
        int TelemetryKey PK
        int DateKey FK
        int AircraftKey FK
        int PilotKey FK
        int MissionKey FK
        float Altitude
        float Velocity
        float CoreTemperature
        float EnergyConsumption
        float FieldStability
        float PropulsionEfficiency
        string MissionOutcome
    }

    FactMaintenance {
        int MaintenanceKey PK
        int DateKey FK
        int AircraftKey FK
        int FailureTypeKey FK
        string MaintenanceType
        float Duration
        float Cost
        int Severity
        string Status
    }

    FactManufacturing {
        int ManufacturingKey PK
        int DateKey FK
        int FactoryKey FK
        int ComponentKey FK
        int UnitsProduced
        int UnitsDefective
        float ProductionCost
        string QualityGrade
    }

    FactFinance {
        int FinanceKey PK
        int DateKey FK
        int DepartmentKey FK
        float PlannedBudget
        float ActualSpend
        float Revenue
        string CostCategory
    }
```

---

## 4. ETL Pipeline Detail

```mermaid
flowchart TB
    subgraph "Stage 1: Extract"
        E1["Read CSV files"]
        E2["Validate file headers"]
        E3["Check row counts"]
    end

    subgraph "Stage 2: Transform"
        T1["Cast data types"]
        T2["Handle nulls"]
        T3["Generate surrogate keys"]
        T4["Apply business rules"]
        T5["Calculate derived columns"]
        T6["Validate referential integrity"]
    end

    subgraph "Stage 3: Load"
        L1["Create/verify schema"]
        L2["Truncate staging tables"]
        L3["Bulk insert dimensions"]
        L4["Bulk insert facts"]
        L5["Update load audit log"]
    end

    E1 --> E2 --> E3
    E3 --> T1 --> T2 --> T3 --> T4 --> T5 --> T6
    T6 --> L1 --> L2 --> L3 --> L4 --> L5
```

---

## 5. Security Architecture

```mermaid
graph TB
    subgraph "Data Layer"
        DB["SQLite Database"]
    end

    subgraph "Semantic Layer"
        DAX["88 DAX Measures"]
        RLS["Row-Level Security"]
    end

    subgraph "Roles"
        R1["Executive<br/>All data, all pages"]
        R2["Engineer<br/>Technical data, no finance"]
        R3["Operations<br/>Flight + maintenance data"]
        R4["Finance<br/>Financial data only"]
        R5["Investor<br/>Summary KPIs, no detail"]
    end

    DB --> DAX
    DAX --> RLS
    RLS --> R1 & R2 & R3 & R4 & R5
```

---

## 6. ML Pipeline Architecture

```mermaid
flowchart LR
    subgraph "Feature Engineering"
        F1["Sensor aggregates<br/>mean, std, max, min"]
        F2["Rolling windows<br/>7d, 30d"]
        F3["Lag features<br/>t-1, t-7"]
        F4["Categorical encoding"]
    end

    subgraph "Training"
        M1["Random Forest<br/>Classifier"]
        M2["Gradient Boosting<br/>Regressor"]
        M3["Cross-Validation<br/>5-fold"]
        M4["Hyperparameter<br/>Grid Search"]
    end

    subgraph "Output"
        O1["Failure Probability<br/>per aircraft"]
        O2["Remaining Useful Life<br/>in days"]
        O3["Confidence Score<br/>0-100%"]
        O4["Recommended Action"]
    end

    F1 & F2 & F3 & F4 --> M1 & M2
    M1 & M2 --> M3 --> M4
    M4 --> O1 & O2 & O3 & O4
```

---

## 7. Deployment Architecture

```mermaid
graph LR
    subgraph "Development"
        DEV["Local Development<br/>VS Code + Python"]
    end

    subgraph "Build"
        GEN["Data Generation"]
        ETL["ETL Pipeline"]
        ML["ML Training"]
    end

    subgraph "Publish"
        GH["GitHub Repository"]
        PBI["Power BI Service"]
        WEB["GitHub Pages<br/>Static Dashboard"]
    end

    DEV --> GEN --> ETL --> ML
    ML --> GH
    GH --> PBI
    GH --> WEB
```
