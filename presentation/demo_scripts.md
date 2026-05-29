# AGIS — Demo Video Scripts

Use these scripts to record loom/YouTube walkthroughs of your project.

---

## 1. The 2-Minute Elevator Pitch (For LinkedIn/Twitter)
**Goal:** Hook the viewer, show the UI, state the business impact.

**[Visual: Executive Overview Page]**
"Hi, I'm [Name]. Aerospace operations generate massive amounts of telemetry data, but it's often siloed. To solve this, I built AGIS, an enterprise intelligence platform. I ingested over 1 million telemetry and finance records using a Python ETL pipeline and built a Kimball Star Schema to power this 10-page executive dashboard."

**[Visual: Switch to Geographic Intelligence Map]**
"AGIS monitors 250 aircraft across 7 global facilities in real-time."

**[Visual: Switch to Predictive Analytics]**
"But I wanted to go beyond just reporting. I built a machine learning pipeline using Random Forest that predicts equipment failure *before* it happens. This screen translates complex ML probabilities into actionable business intelligence—resulting in 38 prevented failures and 12.4 million dollars in estimated cost savings."

**[Visual: Switch back to Executive Overview]**
"If you're looking for a Data Professional who can build end-to-end data products that drive real ROI, let's connect. Thanks for watching."

---

## 2. The Recruiter Walkthrough (5 Minutes)
**Goal:** Show technical depth without getting bogged down in code.

**[Visual: Executive Overview]**
"Welcome to the AGIS platform. My goal was to build a production-grade analytics suite. The data you see here is powered by 88 DAX measures. For example, this Fleet Readiness Score isn't a single metric—it's a composite KPI I designed that weighs aircraft health and maintenance backlogs."

**[Visual: Architecture Diagram on GitHub or Docs]**
"Before building the UI, I focused on the foundation. I wrote a Python pipeline to extract raw telemetry, transform it, and load it into a relational Star Schema with 4 Fact tables and 8 Dimensions. This ensures the dashboard renders instantly despite querying over a million rows."

**[Visual: Predictive Analytics]**
"The highest ROI feature is the Predictive Maintenance module. I trained a Scikit-learn model on historical degradation data. It outputs a Failure Probability and Remaining Useful Life. As you can see on these cards, if an aircraft crosses a 70% threshold, it automatically recommends grounding it. This simulates saving $12.4M in unplanned maintenance."

**[Visual: Executive Insights]**
"Finally, I built an Executive Insights engine. It programmatically analyzes the data and writes plain-English observations, acting like an automated junior analyst."

---

## 3. The Technical Deep-Dive (For Technical Interviews)
**Goal:** Prove you wrote the code and understand the architecture.

**[Visual: VS Code showing `pipeline.py` or SQL schema]**
"Let's look under the hood of AGIS. The biggest challenge was data modeling. I initially started with a flat table, but it didn't scale. I refactored the database into a Kimball Star Schema. Here you can see the conformed Date Dimension which connects the Telemetry Fact table to the Finance Fact table."

**[Visual: VS Code showing `predictive_maintenance.py`]**
"For the ML pipeline, I used a Random Forest Classifier to handle the non-linear relationships in the sensor data. I engineered rolling 7-day averages for core temperatures. To prevent data leakage, I was careful to split the train/test sets chronologically rather than randomly."

**[Visual: Dashboard - Geographic Intelligence]**
"For the frontend, I wanted zero external API dependencies. So for the global map, I used custom CSS grid absolute positioning and SVG bezier curves to draw the flight routes. It's lightweight and loads instantly."

---

## 4. Portfolio Auto-Play Video (Silent, 30 seconds)
**Goal:** A fast-paced, silent video for the header of your personal website.

- **0:00 - 0:05:** Scroll through Executive Overview.
- **0:05 - 0:10:** Click through to Predictive Analytics, hover over a high-risk card.
- **0:10 - 0:15:** Switch to Geographic Intelligence, show the pulsing map markers.
- **0:15 - 0:20:** Switch to Mission Intelligence, hover over the scatter plot.
- **0:20 - 0:30:** Show the GitHub architecture diagram, fade to "AGIS - Enterprise Analytics".
