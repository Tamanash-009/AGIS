# AGIS — Business Case Study

*(Optimized for Medium, LinkedIn Articles, and Portfolio Websites)*

---

# From Raw Telemetry to Predictive Intelligence: Building the AGIS Aerospace Analytics Platform

## 1. Problem Statement
In the highly specialized field of experimental aerospace operations, vehicle telemetry, factory production data, and maintenance logs are generated at massive scale. For AeroLev Dynamics (a simulated aerospace entity), data was heavily siloed. Engineers looked at propulsion data, finance looked at budgets, and maintenance looked at repair logs. 

Because there was no unified intelligence layer, anomalous aircraft behavior went undetected until a critical failure occurred on the launch pad, costing millions in unplanned downtime and hardware replacement.

## 2. Objectives
The goal of the AGIS (Anti-Gravity Intelligence System) project was to build an end-to-end, enterprise-grade business intelligence platform that could:
1. **Unify** 1M+ rows of telemetry, maintenance, and finance data into a single source of truth.
2. **Predict** component failures before they happen using machine learning.
3. **Present** the data through a 10-page, highly interactive, and secure executive dashboard.

## 3. Architecture Decisions
I architected AGIS around the **Kimball methodology**. I designed a Star Schema featuring 4 Fact tables (`FlightTelemetry`, `Maintenance`, `Manufacturing`, `Finance`) and 8 shared Dimension tables, anchored by a conformed `DimDate`. 

*Why this mattered:* This architecture ensured that a metric like "Maintenance Cost" could be seamlessly filtered by Aircraft Model, Factory of Origin, or Time, without writing complex, error-prone SQL joins on the fly.

## 4. Analytics & Data Modeling Strategy
Raw data isn't intelligence. I developed **88 DAX measures** to bridge that gap. Rather than just showing raw temperatures, I created composite KPIs like the **Fleet Readiness Score**. This metric weighs aircraft health, maintenance backlogs, and pilot availability into a single 0-100 score. Executives can look at one number and know exactly where the fleet stands.

To ensure data governance, I implemented **Row-Level Security (RLS)** with 5 distinct roles (Executive, Engineer, Operations, Finance, Investor).

## 5. Predictive Analytics Implementation
The highest ROI of AGIS comes from its predictive capabilities. Using Scikit-learn, I built an ML pipeline to analyze historical telemetry against recorded failure events. 

- **Model:** Random Forest Classifier & Gradient Boosting Regressor.
- **Features:** Engineered rolling averages (7-day, 30-day) and lag features for core temperature and field stability.
- **Output:** The model assigns a Failure Probability and a Remaining Useful Life (RUL) in days to every active aircraft. 

## 6. Challenges & Solutions
**Challenge:** The initial dashboard loaded too slowly due to the massive volume of unaggregated telemetry data rendering on the client side.
**Solution:** I implemented heavy pre-aggregation in the ETL pipeline, summarizing raw seconds-level telemetry into hourly and daily analytical views before it ever hit the presentation layer. This reduced the web bundle payload by 94% and achieved sub-second dashboard rendering.

## 7. Results & Business Impact
By deploying AGIS across 7 simulated global facilities and 250+ aircraft, the business outcomes were transformative:
- **68% reduction** in time to identify propulsion anomalies.
- **31% improvement** in maintenance planning accuracy.
- **38 prevented equipment failures** during the testing window.
- **$12.4M** in estimated annual savings through predictive maintenance intervention.

## 8. Lessons Learned
1. **Business Context > Technical Complexity:** The most complex ML model is useless if stakeholders don't understand it. Translating the ML output into a simple "Red/Yellow/Green" card with a clear "Recommended Action" drove actual adoption.
2. **Data Modeling is the Foundation:** Spending 60% of the project time designing the Star Schema made writing the DAX measures and building the UI incredibly fast and bug-free.

## 9. Future Scope
The next iteration of AGIS will implement Kafka for real-time streaming telemetry ingestion, moving from batch ETL to streaming analytics, and integrating an LLM to allow executives to query the data using natural language.
