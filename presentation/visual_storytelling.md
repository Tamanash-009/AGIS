# AGIS — Visual Storytelling & Screenshot Strategy

This document defines the screenshot narrative strategy for the AGIS portfolio presentation. Each image is paired with business context and technical explanations to demonstrate depth to recruiters.

---

## 1. Executive Command Center
**Filename:** `01_executive_overview.png`

**Description:** The primary C-suite landing page showing a high-level summary of fleet operations, revenue, and mission readiness.
**Business Explanation:** Executives do not have time to parse raw data. This dashboard aggregates thousands of telemetry and financial records into composite KPIs (e.g., Fleet Readiness Score) so leadership can instantly gauge organizational health.
**Technical Explanation:** Powered by 12 distinct DAX measures. Uses conditional formatting in Chart.js to highlight metric variances against predefined monthly targets dynamically.

---

## 2. Mission Intelligence Center
**Filename:** `07_mission_intelligence.png`

**Description:** Real-time mission tracking, status distributions, and risk vs. duration correlation.
**Business Explanation:** Allows operations managers to identify which types of missions are failing and whether external factors (like weather) are impacting success rates, enabling better mission planning.
**Technical Explanation:** Features a complex scatter plot (Risk vs Duration) identifying outliers, and a combo bar/line chart mapping categorical weather data against success percentages.

---

## 3. Flight Operations
**Filename:** `02_flight_operations.png`

**Description:** Telemetry breakdown focusing on altitude, velocity, and mission outcome.
**Business Explanation:** Provides aerospace engineers with macro-level trends on flight performance, helping them identify if specific flight profiles are causing structural stress.
**Technical Explanation:** Aggregates over 500,000 raw telemetry rows into manageable hourly time-series visualizations using a star schema conformed date dimension.

---

## 4. Predictive Maintenance
**Filename:** `09_predictive_analytics.png`

**Description:** Machine learning output dashboard showing aircraft failure probabilities and remaining useful life (RUL).
**Business Explanation:** The most critical ROI generator of AGIS. By shifting from reactive maintenance to predictive intervention, the company avoids $12.4M in catastrophic failures and reduces downtime.
**Technical Explanation:** Visualizes the output of a Scikit-learn Random Forest classifier and Gradient Boosting regressor. The prediction cards use a responsive CSS grid and dynamic color coding based on risk thresholds (Critical > 70%).

---

## 5. Global Operations Map
**Filename:** `08_geographic_intelligence.png`

**Description:** A geospatial view of the 7 global facilities, flight routes, and regional metrics.
**Business Explanation:** Gives supply chain and logistics leaders a geographical understanding of where incidents are happening and which facilities are underperforming.
**Technical Explanation:** Built without external map libraries using absolute CSS positioning and SVG `<path>` elements to draw bezier curves between facilities, ensuring zero external API dependencies and instant load times.

---

## 6. Incident Management
**Filename:** `04_maintenance_incidents.png`

**Description:** Tracks equipment failures, severity matrix, and maintenance downtime.
**Business Explanation:** Helps maintenance crews prioritize their backlog based on severity and historical cost-to-repair metrics.
**Technical Explanation:** Utilizes a heat matrix visualization to cross-reference incident frequency with severity, pulling from the `FactMaintenance` table.

---

## 7. Manufacturing Intelligence
**Filename:** `05_manufacturing.png`

**Description:** Factory floor analytics showing defect rates and production costs.
**Business Explanation:** Connects upstream manufacturing quality to downstream flight failures. If Factory B has a high defect rate, operations can preemptively ground aircraft using Factory B's components.
**Technical Explanation:** Joins the `FactManufacturing` table with `DimFactory` and `DimComponent` to track yield percentages across the supply chain.

---

## 8. Financial Command Center
**Filename:** `06_financial_analysis.png`

**Description:** Tracks budget vs. actuals, OPEX, and R&D burn rates.
**Business Explanation:** Ensures the R&D and operations teams are staying within their allocated budgets, providing CFOs with real-time financial oversight.
**Technical Explanation:** Features advanced DAX time-intelligence (YTD, MoM) to calculate budget variances and run-rate projections.

---

## 9. Executive Insights
**Filename:** `10_executive_insights.png`

**Description:** AI-driven text observations and KPI diagnostic drill-downs.
**Business Explanation:** Automates the job of a junior analyst by explicitly pointing out "What happened, Why it happened, and What to do next."
**Technical Explanation:** Uses programmatic logic in JavaScript to evaluate KPI thresholds and generate dynamic text strings (e.g., "Fleet readiness declined 2.1% due to AG-X4 thermal shields"), acting as a deterministic insight engine.
