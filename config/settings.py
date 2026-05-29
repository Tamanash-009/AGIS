"""
AGIS — Anti-Gravity Intelligence System
Centralized configuration for the entire project.
"""
import os
from pathlib import Path

# ─── Project Root ─────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ─── Data Paths ───────────────────────────────────────────────
DATA_DIR        = PROJECT_ROOT / "data"
RAW_DATA_DIR    = DATA_DIR / "raw"
PROCESSED_DIR   = DATA_DIR / "processed"
SYNTHETIC_DIR   = DATA_DIR / "synthetic"

# ─── Database ─────────────────────────────────────────────────
DATABASE_DIR    = PROJECT_ROOT / "database"
DB_PATH         = DATABASE_DIR / "agis.db"            # SQLite
DB_URI          = f"sqlite:///{DB_PATH}"

# ─── ML Models ────────────────────────────────────────────────
ML_MODEL_DIR    = PROJECT_ROOT / "python" / "ml" / "models"

# ─── Random Seed (reproducibility) ───────────────────────────
RANDOM_SEED = 42

# ─── Data Generation Volume ──────────────────────────────────
RECORD_COUNTS = {
    # Dimensions
    "dim_date_years":       5,          # 2021-01-01 → 2025-12-31
    "dim_aircraft":         50,
    "dim_pilot":            100,
    "dim_mission":          500,
    "dim_factory":          8,
    "dim_component":        200,
    "dim_department":       12,
    "dim_failure_type":     30,
    # Facts
    "fact_flight_telemetry": 500_000,
    "fact_maintenance":      50_000,
    "fact_manufacturing":    300_000,
    "fact_finance":          5_000,     # monthly × departments × 5 yrs
}

# ─── Date Range ───────────────────────────────────────────────
DATE_START = "2021-01-01"
DATE_END   = "2025-12-31"

# ─── Aircraft Configuration ──────────────────────────────────
AIRCRAFT_MODELS = [
    {"model": "AG-X1", "class": "Light Scout",       "max_alt": 15000, "max_vel": 800,  "crew": 1},
    {"model": "AG-X2", "class": "Tactical Fighter",  "max_alt": 25000, "max_vel": 1200, "crew": 1},
    {"model": "AG-X3", "class": "Heavy Lifter",       "max_alt": 12000, "max_vel": 500,  "crew": 3},
    {"model": "AG-X4", "class": "Stealth Recon",      "max_alt": 35000, "max_vel": 1500, "crew": 1},
    {"model": "AG-X5", "class": "Cargo Transport",    "max_alt": 10000, "max_vel": 400,  "crew": 4},
    {"model": "AG-X6", "class": "Research Platform",  "max_alt": 20000, "max_vel": 600,  "crew": 2},
    {"model": "AG-X7", "class": "Command Cruiser",    "max_alt": 30000, "max_vel": 900,  "crew": 6},
]

# ─── Factory Locations ────────────────────────────────────────
FACTORY_LOCATIONS = [
    {"name": "Titan Works",        "city": "Phoenix",     "country": "USA",       "capacity": 5000},
    {"name": "Aurora Assembly",    "city": "Seattle",     "country": "USA",       "capacity": 8000},
    {"name": "Nebula Forge",       "city": "Munich",      "country": "Germany",   "capacity": 6000},
    {"name": "Quantum Bay",        "city": "Yokohama",    "country": "Japan",     "capacity": 7000},
    {"name": "Vortex Plant",       "city": "Bangalore",   "country": "India",     "capacity": 4500},
    {"name": "Eclipse Foundry",    "city": "Manchester",  "country": "UK",        "capacity": 5500},
    {"name": "Helios Hub",         "city": "São Paulo",   "country": "Brazil",    "capacity": 3500},
    {"name": "Zenith Station",     "city": "Sydney",      "country": "Australia", "capacity": 4000},
]

# ─── Component Categories ────────────────────────────────────
COMPONENT_CATEGORIES = [
    "AG Core Unit",
    "Graviton Stabilizer",
    "Plasma Power Cell",
    "Thermal Shield Array",
    "Flight Control Unit",
    "Inertial Dampener",
    "Quantum Processor",
    "Lift Vectoring Nozzle",
    "Energy Distribution Grid",
    "Structural Frame Module",
]

# ─── Department List ──────────────────────────────────────────
DEPARTMENTS = [
    "R&D — Propulsion",
    "R&D — Materials",
    "Engineering",
    "Flight Operations",
    "Manufacturing",
    "Quality Assurance",
    "Supply Chain",
    "Finance",
    "Human Resources",
    "IT & Cybersecurity",
    "Executive Office",
    "Investor Relations",
]

# ─── Mission Types ────────────────────────────────────────────
MISSION_TYPES = [
    "Test Flight",
    "Calibration Run",
    "Endurance Trial",
    "Combat Simulation",
    "Cargo Delivery",
    "Reconnaissance",
    "Formation Drill",
    "Emergency Response",
    "High-Altitude Stress Test",
    "Stealth Validation",
]

# ─── Failure Categories ──────────────────────────────────────
FAILURE_CATEGORIES = [
    "Mechanical",
    "Electrical",
    "Software",
    "Thermal",
    "Structural",
    "Hydraulic",
]

# ─── Ensure directories exist ─────────────────────────────────
for d in [RAW_DATA_DIR, PROCESSED_DIR, SYNTHETIC_DIR, ML_MODEL_DIR, DATABASE_DIR]:
    d.mkdir(parents=True, exist_ok=True)
