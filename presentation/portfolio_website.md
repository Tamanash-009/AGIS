# AGIS — Portfolio Website Package

Use this content to build a dedicated page for AGIS on your personal portfolio website (e.g., WordPress, Webflow, Notion, GitHub Pages).

---

## 1. Hero Section
**Title:** AGIS (Anti-Gravity Intelligence System)
**Subtitle:** From Raw Telemetry to Predictive Enterprise Intelligence
**Hero Image:** Use `01_executive_overview.png` (or the composite 3-image banner)

---

## 2. Project Summary
AGIS is an enterprise-grade analytics platform built to monitor a simulated fleet of experimental aerospace vehicles. By processing over 1 million telemetry, maintenance, and financial records through a robust Kimball Star Schema, AGIS transforms siloed raw data into a 10-page interactive command center. Featuring machine learning for predictive maintenance and custom DAX for composite KPIs, this project demonstrates end-to-end data product development.

---

## 3. Feature Highlights
- **10-Page Intelligence Suite:** Dedicated modules for Flight Operations, Manufacturing, Finance, and Executive Insights.
- **Predictive Maintenance:** Machine learning pipeline forecasting component failure and Remaining Useful Life (RUL).
- **Geospatial Analytics:** Custom-built global operations map tracking 7 facilities and live flight routes.
- **AI-Driven Insights:** Automated generation of plain-English operational observations based on statistical thresholds.
- **Enterprise Governance:** 5-role Row-Level Security (RLS) ensuring strict data access.

---

## 4. Technology Stack
**Data Engineering:** Python, Pandas, SQLite
**Data Modeling:** Kimball Star Schema, SQL
**Business Intelligence:** Power BI, DAX (88 Measures)
**Machine Learning:** Scikit-learn (Random Forest, Gradient Boosting)
**Frontend/Viz:** HTML/CSS/JS, Chart.js, CSS Grid

---

## 5. Architecture Overview
*(Embed `architecture.md` System Architecture Mermaid diagram here)*

To ensure sub-second query performance and absolute reporting accuracy, AGIS avoids "flat file" dashboards. Instead, data flows through a strict ETL pipeline into a relational Star Schema containing 4 Fact tables (Telemetry, Maintenance, Manufacturing, Finance) connected to 8 conformed Dimensions. This semantic layer powers the 88 DAX measures that feed the visual frontend.

---

## 6. Business Impact & Outcomes
Building an analytics tool is only half the job; the other half is driving ROI. By implementing predictive analytics and unified KPIs, the simulated impact of AGIS includes:
- **$12.4M** in estimated annual savings via predictive maintenance.
- **38 prevented equipment failures** during the testing window.
- **68% faster** identification of propulsion anomalies.
- **31% improvement** in maintenance scheduling accuracy.

---

## 7. Screenshots Gallery
*(Embed the following images in a grid or carousel)*
1. `01_executive_overview.png` - *Executive Command Center*
2. `09_predictive_analytics.png` - *Predictive Maintenance Engine*
3. `08_geographic_intelligence.png` - *Global Operations Map*
4. `07_mission_intelligence.png` - *Mission Intelligence Center*

---

## 8. Call To Action (Buttons)
[ View Live Dashboard ] *(Link to GitHub Pages)*
[ View Source Code (GitHub) ] *(Link to Repo)*
[ Read Full Case Study ] *(Link to Medium/LinkedIn Article)*
