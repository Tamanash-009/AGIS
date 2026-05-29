"""
AGIS Flight Telemetry Fact Table Generator
──────────────────────────────────────────
Generates ~500K rows of physics-realistic flight telemetry data.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import pandas as pd
import numpy as np
from datetime import timedelta
from config.settings import RANDOM_SEED, DATE_START, DATE_END, RECORD_COUNTS
from python.utils.physics_engine import (
    energy_consumption, lift_output, stability_score,
    temperature_model, generate_flight_profile
)


def generate_fact_flight_telemetry(dim_aircraft: pd.DataFrame,
                                   dim_pilot: pd.DataFrame,
                                   dim_mission: pd.DataFrame,
                                   dim_date: pd.DataFrame,
                                   target_rows: int = None,
                                   seed: int = RANDOM_SEED) -> pd.DataFrame:
    """
    Generate flight telemetry fact table.
    Each row = one sampled telemetry reading from a flight.
    We generate ~2000 flights, sampling ~250 readings per flight → ~500K rows.
    """
    rng = np.random.default_rng(seed)
    target = target_rows or RECORD_COUNTS['fact_flight_telemetry']

    aircraft_ids = dim_aircraft['AircraftID'].values
    pilot_ids    = dim_pilot['PilotID'].values
    mission_ids  = dim_mission['MissionID'].values
    date_range   = pd.date_range(DATE_START, DATE_END, freq='D')

    # We'll generate flights and sample from each
    num_flights = target // 250  # ~250 readings per flight
    statuses = ['Completed', 'Completed', 'Completed', 'Completed',
                'Completed', 'Aborted', 'Anomaly Detected', 'In Progress']

    all_records = []
    flight_counter = 0

    print(f"  → Generating {num_flights:,} flights (~{target:,} telemetry readings)...")

    for f in range(num_flights):
        if f % 500 == 0 and f > 0:
            print(f"    ... {f:,}/{num_flights:,} flights generated")

        # Select random aircraft and get its specs
        ac_idx = rng.integers(0, len(dim_aircraft))
        ac = dim_aircraft.iloc[ac_idx]
        aircraft_id = ac['AircraftID']
        max_alt = float(ac['MaxAltitude'])
        max_vel = float(ac['MaxVelocity'])
        core_health = float(ac['CoreHealthIndex'])

        pilot_id = rng.choice(pilot_ids)
        mission_id = rng.choice(mission_ids)
        flight_date = pd.Timestamp(rng.choice(date_range))
        flight_id = f'FLT-{flight_counter+1:06d}'
        flight_counter += 1

        # Flight duration: 30 min to 4 hours
        duration_s = int(rng.integers(1800, 14400))

        # Generate physics profile
        profile = generate_flight_profile(duration_s, max_alt, max_vel, rng)

        # Sample ~250 evenly-spaced readings from the flight
        n_samples = min(250, duration_s)
        sample_indices = np.linspace(0, duration_s - 1, n_samples, dtype=int)

        mission_status = rng.choice(statuses)
        turbulence_base = float(rng.uniform(0, 0.4))

        for idx in sample_indices:
            t = int(idx)
            alt = float(profile['altitudes'][t])
            vel = float(profile['velocities'][t])
            phase = profile['phases'][t]

            turb = turbulence_base + float(rng.uniform(-0.1, 0.1))
            turb = max(0, min(1, turb))

            energy = energy_consumption(vel, alt, core_health=core_health)
            lift = lift_output(energy * 0.8, alt, core_health)
            stab = stability_score(vel, alt, turb, core_health)
            temp = temperature_model(energy, alt, t, cooling_eff=0.85)

            timestamp = flight_date + timedelta(seconds=t)

            all_records.append({
                'FlightID':        flight_id,
                'AircraftID':      aircraft_id,
                'PilotID':         pilot_id,
                'MissionID':       mission_id,
                'Timestamp':       timestamp.isoformat(),
                'FlightPhase':     phase,
                'Altitude_m':      round(alt, 1),
                'Velocity_mps':    round(vel, 1),
                'LiftOutput_kN':   round(lift, 2),
                'EnergyConsumed_kW': round(energy, 2),
                'StabilityScore':  round(stab, 2),
                'CoreTemp_C':      round(temp, 1),
                'Turbulence':      round(turb, 3),
                'MissionStatus':   mission_status,
                'DateKey':         int(flight_date.strftime('%Y%m%d')),
            })

    df = pd.DataFrame(all_records)
    print(f"    ✓ {len(df):,} telemetry readings generated")
    return df


if __name__ == '__main__':
    # Quick test with small dataset
    from python.generators.dimension_generators import generate_all_dimensions
    dims = generate_all_dimensions()
    df = generate_fact_flight_telemetry(
        dims['DimAircraft'], dims['DimPilot'], dims['DimMission'],
        dims['DimDate'], target_rows=5000
    )
    print(df.head())
    print(f"Shape: {df.shape}")
