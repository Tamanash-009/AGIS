# AGIS Dashboard Design Specification

## Design System

### Color Palette
| Token | Hex | Usage |
|-------|-----|-------|
| Primary Background | `#060A1F` | Page background |
| Card Background | `#0F1538` | Card/panel fill |
| Cyan Accent | `#00E5FF` | Primary data, KPIs, selected |
| Purple Accent | `#7C4DFF` | Secondary data, gradients |
| Orange | `#FF6D00` | Warnings, tertiary data |
| Green | `#00E676` | Positive trends, success |
| Red | `#FF1744` | Alerts, failures, negative |
| Amber | `#FFEA00` | Caution, medium severity |
| Text Primary | `#E8EDF5` | Headings, values |
| Text Secondary | `#8892B0` | Labels, descriptions |

### Typography
- **KPI Values**: Inter 800, 24px
- **Card Titles**: Inter 600, 13px
- **Labels**: Inter 400, 11px
- **Monospace**: JetBrains Mono (code, IDs, dates)

---

## Page 1: Executive Command Center

### KPI Cards (6)
| KPI | Source Measure | Format |
|-----|---------------|--------|
| Total Flights | `DISTINCTCOUNT(FlightID)` | #,##0 |
| Mission Success Rate | `Successful / Total` | 0.0% |
| Propulsion Efficiency | `AVG(Lift) / AVG(Energy)` | 0.000 |
| Avg Stability Score | `AVG(StabilityScore)` | 0.0 |
| Fleet Readiness | `Active+Healthy / Total` | 0% |
| R&D Spending YTD | `TOTALYTD(RDCost)` | $#M |

### Visuals
1. **Flight Volume & Success Trend** — Combo (bar + line), 12 months
2. **Fleet Performance Radar** — Radar chart, 3 aircraft models
3. **Mission Type Distribution** — Doughnut chart
4. **Revenue vs R&D Investment** — Area chart, 5 years
5. **Executive Scorecard** — Horizontal bar gauges, 6 metrics

---

## Page 2: Flight Operations
- Altitude profile line chart (multi-flight overlay)
- Velocity vs Stability scatter plot
- Flight phase horizontal bar
- Mission status doughnut

## Page 3: AG Core Monitoring
- Energy vs Lift dual-axis line
- Core temperature trend with critical threshold
- Health by aircraft model bar chart
- Stability vs Stress Index scatter

## Page 4: Predictive Maintenance
- Risk assessment heatmap grid (25 aircraft)
- Maintenance cost by type (grouped bar)
- Failure category polar area chart
- Downtime trend with target line

## Page 5: Manufacturing Intelligence
- Defect rate by component (horizontal bar)
- Factory performance (bar + line combo)
- Quality grade doughnut
- Production cost learning curve

## Page 6: Financial Command Center
- Budget vs Actual (grouped bar)
- R&D spending by department (bar)
- Revenue growth trajectory (line with forecast)
- Cost breakdown doughnut

---

## Interactions
- **Cross-filtering**: All visuals on same page
- **Drill-through**: Aircraft ID → detailed telemetry
- **Slicers**: Date range, Aircraft Model, Mission Type, Factory
- **Tooltips**: Custom tooltips with KPI context
