-- ═══════════════════════════════════════════════════════════════
-- AGIS — Anti-Gravity Intelligence System
-- Database Schema (Star Schema — Kimball Dimensional Model)
-- Compatible with: PostgreSQL / SQLite
-- ═══════════════════════════════════════════════════════════════

-- ─── DIMENSION TABLES ─────────────────────────────────────────

CREATE TABLE IF NOT EXISTS DimDate (
    DateKey             INTEGER PRIMARY KEY,      -- YYYYMMDD format
    Date                DATE NOT NULL,
    Year                INTEGER NOT NULL,
    Quarter             INTEGER NOT NULL,         -- 1-4
    Month               INTEGER NOT NULL,         -- 1-12
    MonthName           VARCHAR(20) NOT NULL,
    Week                INTEGER NOT NULL,
    DayOfWeek           INTEGER NOT NULL,         -- 0=Monday
    DayName             VARCHAR(15) NOT NULL,
    DayOfMonth          INTEGER NOT NULL,
    DayOfYear           INTEGER NOT NULL,
    IsWeekend           INTEGER NOT NULL,         -- 0 or 1
    FiscalYear          INTEGER NOT NULL,
    FiscalQuarter       INTEGER NOT NULL,
    YearMonth           VARCHAR(7) NOT NULL,      -- YYYY-MM
    YearQuarter         VARCHAR(7) NOT NULL,      -- YYYY-QN
    IsHoliday           INTEGER DEFAULT 0,
    HolidayName         VARCHAR(50) DEFAULT ''
);

CREATE TABLE IF NOT EXISTS DimAircraft (
    AircraftID          VARCHAR(10) PRIMARY KEY,
    SerialNumber        VARCHAR(20) NOT NULL,
    Model               VARCHAR(10) NOT NULL,     -- AG-X1 through AG-X7
    AircraftClass       VARCHAR(30) NOT NULL,
    MaxAltitude         INTEGER NOT NULL,         -- meters
    MaxVelocity         INTEGER NOT NULL,         -- m/s
    CrewCapacity        INTEGER NOT NULL,
    CommissionDate      DATE NOT NULL,
    FleetAssignment     VARCHAR(20) NOT NULL,
    Status              VARCHAR(20) NOT NULL,     -- Active / Maintenance / Standby / Decommissioned
    CoreHealthIndex     REAL NOT NULL,            -- 0.0 to 1.0
    TotalFlightHours    INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS DimPilot (
    PilotID             VARCHAR(10) PRIMARY KEY,
    FirstName           VARCHAR(30) NOT NULL,
    LastName            VARCHAR(30) NOT NULL,
    Rank                VARCHAR(30) NOT NULL,
    Certifications      VARCHAR(200),
    FlightHours         INTEGER NOT NULL,
    Specialization      VARCHAR(50),
    HireDate            DATE NOT NULL,
    Status              VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS DimMission (
    MissionID           VARCHAR(12) PRIMARY KEY,
    MissionName         VARCHAR(60) NOT NULL,
    MissionType         VARCHAR(30) NOT NULL,
    Priority            VARCHAR(15) NOT NULL,     -- Critical / High / Medium / Low
    TargetAltitude      INTEGER NOT NULL,
    TargetVelocity      INTEGER NOT NULL,
    DurationPlanned     INTEGER NOT NULL,         -- seconds
    Classification      VARCHAR(20) NOT NULL      -- Unclassified / Confidential / Secret / Top Secret
);

CREATE TABLE IF NOT EXISTS DimFactory (
    FactoryID           VARCHAR(10) PRIMARY KEY,
    FactoryName         VARCHAR(30) NOT NULL,
    City                VARCHAR(30) NOT NULL,
    Country             VARCHAR(30) NOT NULL,
    AnnualCapacity      INTEGER NOT NULL,
    CertificationLevel  VARCHAR(20) NOT NULL,
    OperatingSince      INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS DimComponent (
    ComponentID         VARCHAR(12) PRIMARY KEY,
    ComponentName       VARCHAR(50) NOT NULL,
    Category            VARCHAR(40) NOT NULL,
    Supplier            VARCHAR(40) NOT NULL,
    UnitCost            REAL NOT NULL,
    CriticalityRating   VARCHAR(15) NOT NULL,
    LeadTimeDays        INTEGER NOT NULL,
    LifespanHours       INTEGER NOT NULL,
    Weight_kg           REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS DimDepartment (
    DepartmentID        VARCHAR(12) PRIMARY KEY,
    DepartmentName      VARCHAR(40) NOT NULL,
    HeadCount           INTEGER NOT NULL,
    AnnualBudget        REAL NOT NULL,
    CostCenter          VARCHAR(10) NOT NULL
);

CREATE TABLE IF NOT EXISTS DimFailureType (
    FailureTypeID       VARCHAR(10) PRIMARY KEY,
    FailureCode         VARCHAR(10) NOT NULL,
    FailureName         VARCHAR(50) NOT NULL,
    Category            VARCHAR(20) NOT NULL,     -- Mechanical / Electrical / Software / Thermal / Structural / Hydraulic
    AvgRepairCost       REAL NOT NULL,
    AvgDowntimeHours    REAL NOT NULL,
    Severity            INTEGER NOT NULL,         -- 1-5
    SafetyImpact        VARCHAR(15) NOT NULL
);


-- ─── FACT TABLES ──────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS FactFlightTelemetry (
    FlightID            VARCHAR(12) NOT NULL,
    AircraftID          VARCHAR(10) NOT NULL,
    PilotID             VARCHAR(10) NOT NULL,
    MissionID           VARCHAR(12) NOT NULL,
    Timestamp           DATETIME NOT NULL,
    FlightPhase         VARCHAR(15) NOT NULL,     -- Takeoff / Climb / Cruise / Descent / Landing
    Altitude_m          REAL NOT NULL,
    Velocity_mps        REAL NOT NULL,
    LiftOutput_kN       REAL NOT NULL,
    EnergyConsumed_kW   REAL NOT NULL,
    StabilityScore      REAL NOT NULL,            -- 0-100
    CoreTemp_C          REAL NOT NULL,
    Turbulence          REAL NOT NULL,            -- 0-1
    MissionStatus       VARCHAR(20) NOT NULL,
    DateKey             INTEGER NOT NULL,

    FOREIGN KEY (AircraftID) REFERENCES DimAircraft(AircraftID),
    FOREIGN KEY (PilotID)    REFERENCES DimPilot(PilotID),
    FOREIGN KEY (MissionID)  REFERENCES DimMission(MissionID),
    FOREIGN KEY (DateKey)    REFERENCES DimDate(DateKey)
);

CREATE TABLE IF NOT EXISTS FactMaintenance (
    MaintenanceID       VARCHAR(12) PRIMARY KEY,
    AircraftID          VARCHAR(10) NOT NULL,
    FailureTypeID       VARCHAR(10) NOT NULL,
    MaintenanceDate     DATE NOT NULL,
    MaintenanceType     VARCHAR(15) NOT NULL,     -- Corrective / Preventive / Predictive / Emergency
    FailureSeverity     INTEGER NOT NULL,
    RepairCost          REAL NOT NULL,
    DowntimeHours       REAL NOT NULL,
    Resolution          VARCHAR(20) NOT NULL,
    PartsReplaced       INTEGER NOT NULL,
    TechnicianCount     INTEGER NOT NULL,
    DateKey             INTEGER NOT NULL,

    FOREIGN KEY (AircraftID)    REFERENCES DimAircraft(AircraftID),
    FOREIGN KEY (FailureTypeID) REFERENCES DimFailureType(FailureTypeID),
    FOREIGN KEY (DateKey)       REFERENCES DimDate(DateKey)
);

CREATE TABLE IF NOT EXISTS FactManufacturing (
    ProductionID        VARCHAR(14) PRIMARY KEY,
    ComponentID         VARCHAR(12) NOT NULL,
    FactoryID           VARCHAR(10) NOT NULL,
    ProductionDate      DATE NOT NULL,
    ProductionCost      REAL NOT NULL,
    AssemblyTime_hrs    REAL NOT NULL,
    DefectRate          REAL NOT NULL,            -- 0.0 to 1.0
    BatchSize           INTEGER NOT NULL,
    QualityGrade        VARCHAR(5) NOT NULL,      -- A+ / A / B / C / D
    YieldRate           REAL NOT NULL,
    ShiftType           VARCHAR(10) NOT NULL,     -- Day / Swing / Night
    DateKey             INTEGER NOT NULL,

    FOREIGN KEY (ComponentID) REFERENCES DimComponent(ComponentID),
    FOREIGN KEY (FactoryID)   REFERENCES DimFactory(FactoryID),
    FOREIGN KEY (DateKey)     REFERENCES DimDate(DateKey)
);

CREATE TABLE IF NOT EXISTS FactFinance (
    BudgetID            VARCHAR(12) PRIMARY KEY,
    DepartmentID        VARCHAR(12) NOT NULL,
    Month               DATE NOT NULL,
    Year                INTEGER NOT NULL,
    MonthNum            INTEGER NOT NULL,
    BudgetPlanned       REAL NOT NULL,
    OperationalCost     REAL NOT NULL,
    RDCost              REAL NOT NULL,
    Revenue             REAL NOT NULL,
    Investment          REAL NOT NULL,
    HeadcountCost       REAL NOT NULL,
    BudgetVariance      REAL NOT NULL,
    BudgetVariancePct   REAL NOT NULL,
    DateKey             INTEGER NOT NULL,

    FOREIGN KEY (DepartmentID) REFERENCES DimDepartment(DepartmentID),
    FOREIGN KEY (DateKey)      REFERENCES DimDate(DateKey)
);


-- ─── INDEXES ──────────────────────────────────────────────────

CREATE INDEX IF NOT EXISTS idx_telemetry_aircraft   ON FactFlightTelemetry(AircraftID);
CREATE INDEX IF NOT EXISTS idx_telemetry_date       ON FactFlightTelemetry(DateKey);
CREATE INDEX IF NOT EXISTS idx_telemetry_flight     ON FactFlightTelemetry(FlightID);
CREATE INDEX IF NOT EXISTS idx_telemetry_mission    ON FactFlightTelemetry(MissionID);
CREATE INDEX IF NOT EXISTS idx_telemetry_pilot      ON FactFlightTelemetry(PilotID);

CREATE INDEX IF NOT EXISTS idx_maintenance_aircraft ON FactMaintenance(AircraftID);
CREATE INDEX IF NOT EXISTS idx_maintenance_date     ON FactMaintenance(DateKey);
CREATE INDEX IF NOT EXISTS idx_maintenance_failure  ON FactMaintenance(FailureTypeID);

CREATE INDEX IF NOT EXISTS idx_manufacturing_comp   ON FactManufacturing(ComponentID);
CREATE INDEX IF NOT EXISTS idx_manufacturing_factory ON FactManufacturing(FactoryID);
CREATE INDEX IF NOT EXISTS idx_manufacturing_date   ON FactManufacturing(DateKey);

CREATE INDEX IF NOT EXISTS idx_finance_dept         ON FactFinance(DepartmentID);
CREATE INDEX IF NOT EXISTS idx_finance_date         ON FactFinance(DateKey);


-- ─── ANALYTICAL VIEWS ─────────────────────────────────────────

CREATE VIEW IF NOT EXISTS vw_FlightPerformanceSummary AS
SELECT
    ft.FlightID,
    ft.AircraftID,
    a.Model,
    a.AircraftClass,
    ft.MissionStatus,
    COUNT(*)                    AS ReadingCount,
    MAX(ft.Altitude_m)          AS MaxAltitude,
    MAX(ft.Velocity_mps)        AS MaxVelocity,
    AVG(ft.StabilityScore)      AS AvgStability,
    AVG(ft.EnergyConsumed_kW)   AS AvgEnergy,
    AVG(ft.LiftOutput_kN)       AS AvgLift,
    MAX(ft.CoreTemp_C)          AS MaxCoreTemp,
    AVG(ft.LiftOutput_kN) / NULLIF(AVG(ft.EnergyConsumed_kW), 0) AS PropulsionEfficiency
FROM FactFlightTelemetry ft
JOIN DimAircraft a ON ft.AircraftID = a.AircraftID
GROUP BY ft.FlightID, ft.AircraftID, a.Model, a.AircraftClass, ft.MissionStatus;


CREATE VIEW IF NOT EXISTS vw_MaintenanceSummary AS
SELECT
    m.AircraftID,
    a.Model,
    a.AircraftClass,
    COUNT(*)                AS TotalEvents,
    SUM(m.RepairCost)       AS TotalRepairCost,
    AVG(m.RepairCost)       AS AvgRepairCost,
    SUM(m.DowntimeHours)    AS TotalDowntime,
    AVG(m.DowntimeHours)    AS AvgDowntime,
    AVG(m.FailureSeverity)  AS AvgSeverity
FROM FactMaintenance m
JOIN DimAircraft a ON m.AircraftID = a.AircraftID
GROUP BY m.AircraftID, a.Model, a.AircraftClass;


CREATE VIEW IF NOT EXISTS vw_ManufacturingYield AS
SELECT
    mf.FactoryID,
    f.FactoryName,
    f.Country,
    c.Category              AS ComponentCategory,
    COUNT(*)                AS ProductionRuns,
    AVG(mf.DefectRate)      AS AvgDefectRate,
    AVG(mf.YieldRate)       AS AvgYieldRate,
    AVG(mf.ProductionCost)  AS AvgCost,
    AVG(mf.AssemblyTime_hrs) AS AvgAssemblyTime
FROM FactManufacturing mf
JOIN DimFactory f ON mf.FactoryID = f.FactoryID
JOIN DimComponent c ON mf.ComponentID = c.ComponentID
GROUP BY mf.FactoryID, f.FactoryName, f.Country, c.Category;


CREATE VIEW IF NOT EXISTS vw_FinancialOverview AS
SELECT
    fi.DepartmentID,
    d.DepartmentName,
    fi.Year,
    SUM(fi.BudgetPlanned)    AS AnnualBudget,
    SUM(fi.OperationalCost)  AS AnnualActual,
    SUM(fi.RDCost)           AS AnnualRD,
    SUM(fi.Revenue)          AS AnnualRevenue,
    SUM(fi.Investment)       AS AnnualInvestment,
    SUM(fi.OperationalCost) - SUM(fi.BudgetPlanned) AS AnnualVariance
FROM FactFinance fi
JOIN DimDepartment d ON fi.DepartmentID = d.DepartmentID
GROUP BY fi.DepartmentID, d.DepartmentName, fi.Year;


CREATE VIEW IF NOT EXISTS vw_FleetReadiness AS
SELECT
    a.AircraftID,
    a.Model,
    a.AircraftClass,
    a.Status,
    a.CoreHealthIndex,
    a.TotalFlightHours,
    COALESCE(ms.TotalDowntime, 0)   AS TotalDowntimeHours,
    COALESCE(ms.TotalRepairCost, 0) AS TotalMaintenanceCost,
    COALESCE(ms.AvgSeverity, 0)     AS AvgFailureSeverity,
    CASE
        WHEN a.Status = 'Active' AND a.CoreHealthIndex > 0.7 THEN 'Mission Ready'
        WHEN a.Status = 'Active' AND a.CoreHealthIndex > 0.5 THEN 'Limited Ready'
        WHEN a.Status = 'Maintenance' THEN 'Under Maintenance'
        WHEN a.Status = 'Standby' THEN 'Standby'
        ELSE 'Not Available'
    END AS ReadinessLevel
FROM DimAircraft a
LEFT JOIN vw_MaintenanceSummary ms ON a.AircraftID = ms.AircraftID;


-- ─── ROW-LEVEL SECURITY (PostgreSQL syntax, reference for Power BI) ────

-- Role: Executive — sees everything
-- Role: Engineer  — sees Flight Telemetry + Maintenance only
-- Role: Finance   — sees Finance + Manufacturing only
-- Role: Operations — sees Flight Ops + Manufacturing

-- These are implemented as DAX filters in Power BI RLS.
-- See powerbi/dax/rls_roles.dax for implementation.
