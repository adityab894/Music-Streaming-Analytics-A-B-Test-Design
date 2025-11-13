# Beats and Bytes | Product Analyst Challenge | Submission

This document outlines the solution for the Product Analyst Challenge.

## 0. Data

The solution is based on three core datasets:

*   **`users.csv`**: Contains user information, including their ID, country, and subscription tier (`FREEMIUM` or `PREMIUM`).
*   **`tracks.csv`**: Contains track metadata, such as track ID, artist ID, and genre.
*   **`plays.jsonl`**: A record of user listening events in JSONL format, with each line representing a single play event, including user ID, track ID, and timestamp.

Due to the potential scale of the data (terabytes), a representative sample dataset was generated using the `scripts/sample_data_generation.py` script to allow for local development and testing. The analysis and Python/SQL scripts are designed to be scalable to the full dataset in a production environment.

## Tools Used & Rationale

The following tools were used throughout the project, each chosen for specific strengths:

* **Google BigQuery:** I selected BigQuery as the primary data warehouse for processing and analyzing large-scale datasets. My prior experience with BigQuery in academic projects made it a natural choice, as I am comfortable with its SQL dialect and scalable architecture. Additionally, BigQuery integrates seamlessly with Looker Studio, enabling efficient data visualization workflows.
* **Python:** Used for data generation and preprocessing scripts, leveraging libraries such as `pandas` and `faker` for flexible data manipulation and synthetic data creation.
* **Looker Studio:** Chosen for dashboarding and visualization due to its interactive features and direct connectivity with BigQuery, which streamlines the process of building dynamic, real-time dashboards.

This combination of tools ensured scalability, reproducibility, and clear data presentation throughout the project.

## 1. How would you approach the problem?

My approach involved several key stages:

1.  **Data Exploration and Generation:** I began by analyzing the schema of the provided datasets (`tracks`, `plays`, `users`). Given the large potential data volumes, I created a Python script (`scripts/sample_data_generation.py`) to generate a realistic, smaller-scale dataset. This script was carefully designed to ensure there was enough data density for meaningful monthly and country-based analysis.

2.  **Data Processing and Analysis:** I used SQL to perform the main data transformations. The queries are designed to be scalable and can be executed on a distributed system like BigQuery or Spark for the full-terabyte dataset. The queries aggregate the data to create the specific views required for the dashboards.

3.  **Visualization:** I chose Looker Studio to build the dashboards. This tool allows for interactive filtering and clear data presentation, which is ideal for exploring the Top 50 tracks and Top 10 artists.

4.  **A/B Test Design:** For the A/B test, I focused on developing a clear hypothesis and a robust experimental design. The plan outlines the business case, key metrics, and the steps needed for implementation and analysis.

## 2. How would you run your solution?

To reproduce the results, please follow these steps:

1.  **Prerequisites:**
    *   Python 3 with `pandas` and `faker` libraries installed.
    *   A Google Cloud Platform account with access to BigQuery.

2.  **Generate Sample Data:** Run the data generation script from the root directory of the project:
    ```bash
    python scripts/sample_data_generation.py
    ```
    This will create `users.csv`, `tracks.csv`, and `plays.jsonl` in the `input-sample/` directory.

3.  **Process Data with BigQuery:**
    a.  In the Google Cloud Console, create a new BigQuery dataset (e.g., `submission_dataset`).
    b.  Create tables in the dataset by uploading the generated sample data from the `input-sample/` directory.
    c.  Execute the SQL queries located in the `scripts/` folder. **Note:** You may need to update the table names within the queries to match your BigQuery project and dataset (e.g., `your-project.submission_dataset.plays`).
        *   `top_50_tracks_per_country_per_month_last_3_months.sql`
        *   `top_10_artists_by_genre_last_30_days.sql`
    d.  Export the results of these queries to `results/Task1.csv` and `results/Task2.csv`.

4.  **View Dashboards:** A video recording of the dashboards is included in the submission zip file. To interact with them directly, you can connect the generated CSV files (`results/Task1.csv`, `results/Task2.csv`) as data sources in Looker Studio.

## 3. How would you verify your solution?

I took the following steps to verify the solution:

*   **Unit Testing Data Logic:** I performed manual checks on the generated data and the output of the SQL queries using a small subset of the data to ensure the aggregations and joins were correct.
*   **Dashboard Validation:** I cross-referenced the data displayed in the dashboard widgets with the underlying CSV files to ensure accuracy.
*   **Code Review:** The Python and SQL scripts are commented and structured for clarity and maintainability.

## 4. What would be the pros and cons of your solution?

**Pros:**

*   **Scalability:** The SQL-based approach is highly scalable and can be easily adapted to run on a production data warehouse like BigQuery or Snowflake.
*   **Reproducibility:** The entire workflow, from data generation to analysis, is scripted and can be easily reproduced.
*   **Clarity:** The dashboards provide a clear and interactive way to explore the data.

**Cons:**

*   **Sample Data Limitations:** The generated sample data may not perfectly reflect the complexities and edge cases of the real production data.
*   **Local Execution:** While the solution is designed for scalability, running the analysis on the full 1TB dataset would require a distributed computing environment.

## 5. How would you optimize your solution?

For a production environment with terabyte-scale data, I would make the following optimizations:

*   **Use a Distributed Computing Framework:** I would use Apache Spark or a cloud-based data warehouse like Google BigQuery to process the data in a distributed manner.
*   **Optimize Data Storage:** I would store the data in a columnar format like Parquet, which is highly efficient for analytical queries.
*   **Dashboard Performance:** I would use materialized views or pre-aggregated tables to improve dashboard loading times.

## 6. What other considerations would you have?

*   **Data Quality:** In a real-world scenario, I would perform a thorough data quality assessment to check for issues like missing values, duplicates, and inconsistencies.
*   **Deeper Analysis:** With more time, I would explore other aspects of the data, such as user segmentation, churn analysis, and the impact of new releases on listening behavior.

---

## Dashboards

*(A video of the dashboards is included in the submission zip file.)*

### Dashboard 1: TOP 50 Monthly Tracks by Country

This dashboard shows the top 50 most played tracks in the last 3 months, grouped by country in Central Europe.

*[Screenshot of Dashboard 1]*

### Dashboard 2: TOP 10 Artists by Genre

This dashboard displays the top 10 artists for the last 30 days, grouped by genre.

*[Screenshot of Dashboard 2]*

---

## A/B Test Plan: Improving Listening Duration with a Personalized Recommendation Algorithm

### 1. Business Context & Objective

The primary goal of the "Beats and Bytes" department is to leverage data to enhance the user experience and drive business growth. A key factor in user satisfaction and retention is engagement, and a strong proxy for engagement is **listening duration**. Longer listening sessions correlate with higher user satisfaction, lower churn rates, and an increased likelihood of converting from a freemium to a premium subscription. 

Our objective is to test a new feature designed to increase this key metric.

### 2. Insight & Hypothesis

**Insight from the Dashboard:** The "Top 10 Artists by Genre" dashboard reveals that listening is often concentrated around a small number of superstar artists within each genre. While popular artists are crucial, this concentration suggests an opportunity to improve music discovery and broaden users' tastes. If users only listen to the same few artists, they may get bored and end their session sooner.

**Hypothesis:**
*   **H₀ (Null Hypothesis):** A new personalized recommendation algorithm, designed to introduce users to a wider variety of relevant artists, will have **no effect** on the average listening duration per user session.
*   **H₁ (Alternative Hypothesis):** The new personalized recommendation algorithm will **increase** the average listening duration per user session by helping users discover new music they enjoy, thus keeping them engaged for longer.

### 3. Experiment Design

*   **Participants:** The experiment will target a segment of active users on both `FREEMIUM` and `PREMIUM` tiers within Germany (`DE`). We will select a random sample of 100,000 users to ensure statistical power.
*   **Groups:**
    *   **Control Group (A):** 50% of participants (50,000 users) will continue to experience the current, standard recommendation algorithm.
    *   **Treatment Group (B):** 50% of participants (50,000 users) will be exposed to the new personalized recommendation algorithm.
*   **Duration:** The test will run for **4 weeks**. This duration is long enough to capture weekly listening patterns and account for novelty effects.

### 4. Metrics

*   **Primary Metric (Success Metric):**
    *   **Average Listening Duration per Session:** This will be the key indicator of success. We will measure if Group B shows a statistically significant increase in this metric.

*   **Secondary Metrics (Guardrail Metrics):**
    *   **Unique Tracks Played per User:** To ensure we are actually broadening user taste.
    *   **Skip Rate:** To monitor if the new recommendations are relevant. A significant increase in skip rate would be a negative sign.
    *   **User Retention Rate:** To see if better recommendations lead to users returning more frequently.
    *   **Freemium-to-Premium Conversion Rate:** To track the downstream impact on revenue.

### 5. Implementation & Analysis

1.  **Rollout:** The new algorithm will be deployed via a feature flag system, allowing us to easily assign users to the correct group. We will start with a 1% rollout to validate technical stability before ramping up to the full 100,000 users.
2.  **Data Collection:** We will log every play, session start/end, and user interaction for both groups throughout the 4-week period.
3.  **Statistical Analysis:** After the test concludes, we will use a **two-sample t-test** to compare the mean of the primary metric (Average Listening Duration) between the control and treatment groups. A **p-value of < 0.05** will be considered statistically significant.

### 6. Success Criteria & Business Value

The experiment will be considered a success if the treatment group shows a **statistically significant increase of 2% or more** in the average listening duration per session, without negatively impacting any of the secondary metrics.

A successful outcome would validate the new algorithm and provide a strong business case for a full rollout. A 2% increase in engagement, when scaled across the entire user base, would translate to a substantial increase in user satisfaction, retention, and ultimately, revenue for the company.

