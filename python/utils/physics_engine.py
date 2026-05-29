"""
AGIS Physics Engine
───────────────────
Simulates anti-gravity propulsion physics for realistic telemetry generation.
All models are fictional but internally consistent and physics-plausible.
"""
import numpy as np


# ══════════════════════════════════════════════════════════════
# Constants
# ══════════════════════════════════════════════════════════════
GRAVITY       = 9.81          # m/s²
AIR_DENSITY_0 = 1.225         # kg/m³ at sea level
TEMP_LAPSE    = 0.0065        # °C per meter altitude
TEMP_SEA      = 288.15        # K at sea level
AG_CORE_EFF   = 0.72          # baseline AG core efficiency


def altitude_air_density(altitude_m: float) -> float:
    """Approximate air density at altitude using barometric formula."""
    temperature = TEMP_SEA - TEMP_LAPSE * altitude_m
    temperature = max(temperature, 216.65)  # tropopause floor
    return AIR_DENSITY_0 * (temperature / TEMP_SEA) ** 4.256


def lift_output(energy_kw: float, altitude_m: float, core_health: float = 1.0) -> float:
    """
    Calculate lift force (kN) from energy input.
    Lift degrades with altitude (thinner medium) and core health.
    """
    density_factor = altitude_air_density(altitude_m) / AIR_DENSITY_0
    efficiency = AG_CORE_EFF * core_health * (0.6 + 0.4 * density_factor)
    return energy_kw * efficiency * 0.45  # kN


def energy_consumption(velocity_mps: float, altitude_m: float,
                       mass_kg: float = 12000, core_health: float = 1.0) -> float:
    """
    Energy consumed (kW) to maintain flight at given velocity and altitude.
    Increases with velocity² and altitude, decreases with core health.
    """
    drag = 0.5 * altitude_air_density(altitude_m) * velocity_mps ** 2 * 0.02  # simplified
    gravity_cost = mass_kg * GRAVITY * 0.001  # kW baseline to hover
    health_penalty = 1.0 + (1.0 - core_health) * 0.5
    return (drag + gravity_cost) * health_penalty


def stability_score(velocity_mps: float, altitude_m: float,
                    turbulence: float = 0.0, core_health: float = 1.0) -> float:
    """
    Stability index 0-100.
    High velocity, high altitude, turbulence, and poor health reduce stability.
    """
    base = 95.0
    vel_penalty = (velocity_mps / 500) ** 1.5 * 10
    alt_penalty = (altitude_m / 30000) ** 1.2 * 8
    turb_penalty = turbulence * 25
    health_penalty = (1.0 - core_health) * 30
    score = base - vel_penalty - alt_penalty - turb_penalty - health_penalty
    return float(np.clip(score, 0, 100))


def temperature_model(energy_kw: float, altitude_m: float,
                      duration_s: float, cooling_eff: float = 0.85) -> float:
    """
    AG Core temperature (°C).
    Heat builds with energy and time, decreases with altitude (cold air) and cooling.
    """
    ambient = 15.0 - TEMP_LAPSE * altitude_m * 1000  # simplified
    ambient = max(ambient, -56.5)
    heat_gen = energy_kw * 0.08 * (1.0 - cooling_eff)
    time_factor = min(duration_s / 3600, 1.0)  # saturates at 1 hour
    return ambient + heat_gen * (0.3 + 0.7 * time_factor) + np.random.normal(0, 2)


def failure_probability(flight_hours: float, maintenance_age_days: int,
                        stress_events: int, core_health: float) -> float:
    """
    Predict failure probability (0-1) based on operational factors.
    Uses a simplified Weibull-inspired model.
    """
    hour_risk = 1 - np.exp(-(flight_hours / 2000) ** 1.8)
    age_risk = 1 - np.exp(-(maintenance_age_days / 365) ** 2.0)
    stress_risk = min(stress_events / 50, 1.0)
    health_risk = (1.0 - core_health) ** 0.8
    combined = 0.3 * hour_risk + 0.25 * age_risk + 0.25 * stress_risk + 0.2 * health_risk
    return float(np.clip(combined + np.random.normal(0, 0.03), 0, 1))


def remaining_useful_life(core_health: float, avg_daily_stress: float) -> int:
    """Estimate remaining useful life in days."""
    if core_health <= 0.05:
        return 0
    degradation_rate = 0.002 + avg_daily_stress * 0.005
    if degradation_rate <= 0:
        return 9999
    return max(1, int(core_health / degradation_rate))


def generate_flight_profile(duration_s: int, max_alt: float, max_vel: float,
                            rng: np.random.Generator) -> dict:
    """
    Generate a complete flight profile with phase-aware telemetry.
    Returns arrays for altitude, velocity, and phase labels.
    """
    n = duration_s
    altitudes = np.zeros(n)
    velocities = np.zeros(n)
    phases = []

    # Phase durations (fractions)
    takeoff_end   = int(n * 0.12)
    climb_end     = int(n * 0.28)
    cruise_end    = int(n * 0.65)
    descent_end   = int(n * 0.85)

    for t in range(n):
        if t < takeoff_end:
            # Takeoff: rapid altitude gain, moderate velocity
            frac = t / max(takeoff_end, 1)
            altitudes[t] = max_alt * 0.3 * frac ** 1.5
            velocities[t] = max_vel * 0.4 * frac
            phases.append("Takeoff")
        elif t < climb_end:
            frac = (t - takeoff_end) / max(climb_end - takeoff_end, 1)
            altitudes[t] = max_alt * (0.3 + 0.6 * frac)
            velocities[t] = max_vel * (0.4 + 0.4 * frac)
            phases.append("Climb")
        elif t < cruise_end:
            frac = (t - climb_end) / max(cruise_end - climb_end, 1)
            altitudes[t] = max_alt * (0.9 + 0.1 * np.sin(frac * np.pi))
            velocities[t] = max_vel * (0.8 + 0.15 * np.sin(frac * 2 * np.pi))
            phases.append("Cruise")
        elif t < descent_end:
            frac = (t - cruise_end) / max(descent_end - cruise_end, 1)
            altitudes[t] = max_alt * 0.9 * (1 - frac ** 1.3)
            velocities[t] = max_vel * 0.8 * (1 - 0.5 * frac)
            phases.append("Descent")
        else:
            frac = (t - descent_end) / max(n - descent_end, 1)
            altitudes[t] = max_alt * 0.9 * (1 - (descent_end - cruise_end) / max(descent_end - cruise_end, 1)) * (1 - frac)
            altitudes[t] = max(altitudes[t], 0)
            velocities[t] = max_vel * 0.3 * (1 - frac)
            phases.append("Landing")

    # Add noise
    altitudes += rng.normal(0, max_alt * 0.005, n)
    altitudes = np.clip(altitudes, 0, max_alt * 1.05)
    velocities += rng.normal(0, max_vel * 0.01, n)
    velocities = np.clip(velocities, 0, max_vel * 1.1)

    return {
        "altitudes": altitudes,
        "velocities": velocities,
        "phases": phases,
    }
