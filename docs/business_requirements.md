# Business Requirements Document (BRD)
## AGIS — Anti-Gravity Intelligence System

| Field | Value |
|-------|-------|
| **Document Version** | 2.0 |
| **Date** | May 2025 |
| **Author** | Data Analytics Team |
| **Sponsor** | CTO, AeroLev Dynamics |
| **Status** | Approved |

---

## 1. Executive Summary

AeroLev Dynamics requires an integrated analytics platform to monitor and analyze operations across its experimental anti-gravity propulsion program. The current operational environment relies on disconnected spreadsheets, manual reports, and siloed departmental data, resulting in delayed decision-making, undetected equipment degradation, and budget overruns.

AGIS will consolidate telemetry, maintenance, manufacturing, and financial data into a single source of truth, enabling real-time operational visibility for executives, engineers, and operations teams.

---

## 2. Business Objectives

| ID | Objective | Success Criteria |
|----|-----------|-----------------|
| BO-01 | Reduce time to detect propulsion anomalies | < 15 minutes from occurrence |
| BO-02 | Improve fleet readiness visibility | Single-view readiness for all 50 aircraft |
| BO-03 | Enable predictive maintenance | ML model with AUC ≥ 0.70 for failure prediction |
| BO-04 | Reduce unplanned maintenance costs | ≥ 25% reduction via early failure detection |
| BO-05 | Centralize financial tracking | Budget vs actual variance visible within 24 hours |
| BO-06 | Track manufacturing quality | Real-time yield rates across all 8 factories |

---

## 3. Stakeholders

| Role | Responsibilities | Data Access |
|------|-----------------|-------------|
| CTO / Executive | Strategic decisions, budget approval | Full access |
| Aerospace Engineers | Propulsion analysis, flight data review | Telemetry + Maintenance |
| Operations Team | Fleet scheduling, mission planning | Flight Ops + Manufacturing |
| Manufacturing Lead | Quality control, production optimization | Manufacturing data |
| Finance Controller | Budget tracking, R&D ROI analysis | Financial data |
| Investors | Quarterly performance review | Executive summary only |

---

## 4. Functional Requirements

### 4.1 Data Ingestion
- FR-01: Ingest flight telemetry data from 50 aircraft (1-second intervals during flight)
- FR-02: Ingest maintenance records including failure type, severity, cost, and downtime
- FR-03: Ingest manufacturing data from 8 factories including yield, defects, and quality grades
- FR-04: Ingest financial data with budget, actuals, R&D costs, and revenue by department

### 4.2 Data Model
- FR-05: Implement Kimball star schema with conformed date dimension
- FR-06: Support minimum 4 fact tables and 8 dimension tables
- FR-07: Enable incremental refresh for telemetry data
- FR-08: Maintain referential integrity across all relationships

### 4.3 Analytics & KPIs
- FR-09: Calculate 80+ DAX measures organized by dashboard page
- FR-10: Implement composite executive KPIs: Mission Risk, Fleet Readiness, Maintenance Health, Safety Compliance, Budget Utilization, Component Reliability, Propulsion Efficiency Index, R&D Burn Rate
- FR-11: Each KPI must display: current value, target, variance, trend direction, risk indicator
- FR-12: Support time intelligence: MoM, YoY, YTD, rolling averages

### 4.4 Predictive Analytics
- FR-13: Train failure classification model (target AUC ≥ 0.70)
- FR-14: Train remaining useful life regression model
- FR-15: Generate explainable predictions (feature importance)
- FR-16: Retrain models on a monthly cadence

### 4.5 Dashboard
- FR-17: 6 dashboard pages: Executive, Flight Ops, Propulsion, Maintenance, Manufacturing, Finance
- FR-18: Responsive layout supporting 1920px, 1440px, and 768px viewports
- FR-19: Incident management table with severity, status, team assignment
- FR-20: Real-time clock and system status indicator

### 4.6 Security
- FR-21: Implement Row-Level Security with 5 roles (Executive, Engineer, Operations, Finance, Investor)
- FR-22: Finance data restricted from Engineering and Operations roles
- FR-23: Investor role limited to executive summary data only

---

## 5. Non-Functional Requirements

| ID | Requirement | Target |
|----|------------|--------|
| NF-01 | Dashboard page load time | < 3 seconds |
| NF-02 | ETL pipeline execution | < 5 minutes for full refresh |
| NF-03 | Data freshness | Updated within 1 hour of source change |
| NF-04 | Accessibility | WCAG 2.1 AA compliant color contrast |
| NF-05 | Browser support | Chrome, Edge, Firefox (latest 2 versions) |

---

## 6. Data Volume Estimates

| Data Source | Records/Year | Growth Rate |
|------------|-------------|-------------|
| Flight Telemetry | ~500,000 | 15% |
| Maintenance Events | ~10,000 | 5% |
| Manufacturing Runs | ~50,000 | 12% |
| Financial Records | ~1,200 | Stable |

---

## 7. Acceptance Criteria

- [ ] All 6 dashboard pages render without errors
- [ ] 0 broken visuals, 0 DAX errors, 0 relationship errors
- [ ] All KPIs display with target, variance, and trend
- [ ] Incident log displays 8+ realistic incidents
- [ ] ML model achieves AUC ≥ 0.70
- [ ] RLS roles filter data correctly per role definition
- [ ] Dashboard responsive at all 3 viewport sizes
- [ ] Documentation complete: Architecture, Data Dictionary, BRD, Deployment Guide
