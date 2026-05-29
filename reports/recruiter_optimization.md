# AGIS — Recruiter Optimization Report

This report analyzes the AGIS project through the lens of 5 different hiring personas, identifying strengths, potential friction points, and interview preparation.

---

## 1. Data Analyst Recruiter (Entry/Mid-Level)
**What they look for:** SQL skills, BI tool proficiency (Power BI/Tableau), dashboard aesthetics, communication.
**Strengths:** The dashboard looks stunning. 10 pages of high-density, well-organized visuals prove extreme proficiency in visualization and DAX.
**Weaknesses:** Might think the ML portion is "too advanced" or assume someone else did it.
**Interview Q:** *"Walk me through how you designed the Executive Overview page."*
**Suggested Answer:** *"I started by asking what the C-suite cares about: overall readiness and financial burn. I created composite KPIs like the Fleet Readiness Score using DAX, which aggregates 12 underlying metrics. Then I used a strict dark-mode color palette to ensure the data was the focal point, not the charts."*

## 2. BI Developer Recruiter
**What they look for:** Data modeling (Star Schema), ETL, DAX optimization, RLS, semantic layer design.
**Strengths:** The architecture documentation (Kimball schema, 4 facts/8 dims) and 88 DAX measures are exactly what they want to see.
**Weaknesses:** None. This is a perfect match.
**Interview Q:** *"Why did you use a Star Schema instead of a flat table?"*
**Suggested Answer:** *"With 1M+ rows across 4 different domains (Telemetry, Finance, Maintenance, Manufacturing), a flat table would cause massive data duplication and cross-filtering nightmares. The Star Schema with a conformed Date dimension allowed me to slice Maintenance Costs and Flight Anomalies on the same visual seamlessly."*

## 3. Analytics Manager (The direct boss)
**What they look for:** Problem-solving, business acumen, translating data into action.
**Strengths:** The "Executive Insights" page and the focus on Business ROI ($12.4M saved).
**Weaknesses:** Will want to know if you can handle messy, real-world data, not just synthetic data.
**Interview Q:** *"Real data is never this clean. How would you handle this pipeline if the sensors were dropping packets?"*
**Suggested Answer:** *"In the Python ETL pipeline, I would add a data validation stage. If a sensor drops packets, I could use Pandas to interpolate missing values using a rolling mean, or flag that specific flight for data quality review before it enters the Fact table."*

## 4. Hiring Manager (Director/VP)
**What they look for:** Can this person present to the C-suite? Will they require hand-holding? Do they understand ROI?
**Strengths:** The presentation quality, the clear ROI metrics in the README.
**Weaknesses:** Might ask for a live demo to ensure you actually built it.
**Interview Q:** *"How did you arrive at the $12.4M savings figure?"*
**Suggested Answer:** *"I calculated the average cost of an unplanned catastrophic core failure vs. a planned maintenance intervention. By multiplying the cost delta by the 38 failures the ML model successfully predicted, I reached the estimated cost avoidance."*

## 5. Consulting Firm Reviewer (Big 4 / MBB)
**What they look for:** Enterprise scale, governance, framework application, flawless presentation.
**Strengths:** RLS implementation, comprehensive documentation (BRD, Data Dictionary, Architecture), enterprise color theme.
**Weaknesses:** Will scrutinize the formatting of the documentation.
**Interview Q:** *"If we deployed this for a Fortune 500 aerospace client, how would you scale the architecture?"*
**Suggested Answer:** *"I would migrate the SQLite backend to Snowflake or Databricks for distributed computing. The Python ETL would move to Apache Airflow or dbt for orchestration. However, the Kimball Star Schema and the Power BI semantic layer would remain largely intact, as the logic scales perfectly."*
