import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="SalaryNex | Data & AI Career Intelligence",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }

    /* Main title */
    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: #f8fafc;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 17px;
        color: #94a3b8;
        margin-bottom: 25px;
    }

    /* KPI cards */
    .kpi-card {
        background: linear-gradient(135deg, #1e293b, #172033);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #334155;
        box-shadow: 0 4px 15px rgba(0,0,0,0.25);
    }

    .kpi-title {
        color: #94a3b8;
        font-size: 14px;
        font-weight: 600;
    }

    .kpi-value {
        color: #f8fafc;
        font-size: 28px;
        font-weight: 800;
        margin-top: 5px;
    }

    .kpi-description {
        color: #38bdf8;
        font-size: 13px;
        margin-top: 5px;
    }

    /* Section headings */
    .section-title {
        font-size: 24px;
        font-weight: 700;
        color: #f8fafc;
        margin-top: 15px;
        margin-bottom: 10px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #111827;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
    }

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.markdown(
    '<div class="main-title">💼 SalaryNex</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Global Data & AI Career Intelligence • Explore • Compare • Discover'
    '</div>',
    unsafe_allow_html=True
)
# ---------------------------------------------------------
# LOAD REAL KAGGLE DATASET
# ---------------------------------------------------------

@st.cache_data
def load_data():

    df = pd.read_csv("ds_salaries.csv")

    # Remove unnecessary index column if present
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    return df


df = load_data()


# ---------------------------------------------------------
# DATA PREPARATION
# ---------------------------------------------------------

# Convert experience level codes into readable names
experience_map = {
    "EN": "Entry Level",
    "MI": "Mid Level",
    "SE": "Senior Level",
    "EX": "Executive Level"
}

df["experience_level"] = df["experience_level"].map(experience_map)


# Convert employment type codes
employment_map = {
    "FT": "Full Time",
    "PT": "Part Time",
    "CT": "Contract",
    "FL": "Freelance"
}

df["employment_type"] = df["employment_type"].map(employment_map)


# Convert remote ratio into readable categories
def remote_category(value):

    if value == 0:
        return "On-site"
    elif value == 50:
        return "Hybrid"
    else:
        return "Fully Remote"


df["remote_status"] = df["remote_ratio"].apply(remote_category)


# ---------------------------------------------------------
# DATASET INFORMATION
# ---------------------------------------------------------


# ---------------------------------------------------------
# SIDEBAR — INTERACTIVE FILTERS
# ---------------------------------------------------------

# =========================================================
# SIDEBAR HEADER — FINAL UI
# =========================================================

st.sidebar.markdown(
    """
    <div style="text-align:center; padding:10px 0 20px 0;">
        <div style="font-size:32px;">⚡</div>
        <h2 style="margin:0;">SalaryNex</h2>
        <p style="margin-top:5px; opacity:0.7;">
            Data & AI Career Intelligence
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("---")

st.sidebar.markdown("### 🎛️ Filters")
st.sidebar.caption(
    "Customize the dashboard to explore salary trends."
)
# ---------------------------------------------------------
# RESET BUTTON
# ---------------------------------------------------------

if st.sidebar.button("🔄 Reset Filters", use_container_width=True):
    st.rerun()


# ---------------------------------------------------------
# JOB TITLE
# ---------------------------------------------------------

job_options = sorted(df["job_title"].dropna().unique())

selected_jobs = st.sidebar.multiselect(
    "💼 Job Title",
    options=job_options,
    default=job_options
)


# ---------------------------------------------------------
# EXPERIENCE LEVEL
# ---------------------------------------------------------

experience_options = [
    "Entry Level",
    "Mid Level",
    "Senior Level",
    "Executive Level"
]

selected_experience = st.sidebar.multiselect(
    "📊 Experience Level",
    options=experience_options,
    default=experience_options
)


# ---------------------------------------------------------
# EMPLOYMENT TYPE
# ---------------------------------------------------------

employment_options = sorted(
    df["employment_type"].dropna().unique()
)

selected_employment = st.sidebar.multiselect(
    "🧑‍💻 Employment Type",
    options=employment_options,
    default=employment_options
)


# ---------------------------------------------------------
# EMPLOYEE RESIDENCE
# ---------------------------------------------------------

country_options = sorted(
    df["employee_residence"].dropna().unique()
)

selected_countries = st.sidebar.multiselect(
    "🌎 Employee Residence",
    options=country_options,
    default=country_options
)


# ---------------------------------------------------------
# REMOTE WORK
# ---------------------------------------------------------

remote_options = [
    "On-site",
    "Hybrid",
    "Fully Remote"
]

selected_remote = st.sidebar.multiselect(
    "🏠 Work Mode",
    options=remote_options,
    default=remote_options
)


# ---------------------------------------------------------
# WORK YEAR
# ---------------------------------------------------------

year_options = sorted(
    df["work_year"].dropna().unique()
)

selected_years = st.sidebar.multiselect(
    "📅 Work Year",
    options=year_options,
    default=year_options
)


# ---------------------------------------------------------
# SALARY RANGE
# ---------------------------------------------------------

min_salary = int(df["salary_in_usd"].min())
max_salary = int(df["salary_in_usd"].max())

selected_salary = st.sidebar.slider(
    "💰 Salary Range (USD)",
    min_value=min_salary,
    max_value=max_salary,
    value=(min_salary, max_salary),
    step=5000,
    format="$%d"
)


# ---------------------------------------------------------
# APPLY FILTERS
# ---------------------------------------------------------

filtered_df = df[
    (df["job_title"].isin(selected_jobs)) &
    (df["experience_level"].isin(selected_experience)) &
    (df["employment_type"].isin(selected_employment)) &
    (df["employee_residence"].isin(selected_countries)) &
    (df["remote_status"].isin(selected_remote)) &
    (df["work_year"].isin(selected_years)) &
    (df["salary_in_usd"].between(
        selected_salary[0],
        selected_salary[1]
    ))
].copy()


# ---------------------------------------------------------
# FILTER SUMMARY
# ---------------------------------------------------------

st.sidebar.markdown("---")

st.sidebar.markdown(
    f"""
    **📌 Active Records**

    ### {len(filtered_df):,}

    out of **{len(df):,}** total records
    """
)
# =========================================================
# MACHINE LEARNING — SALARY PREDICTION MODEL
# =========================================================

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

features = [
    "work_year",
    "experience_level",
    "employment_type",
    "job_title",
    "employee_residence",
    "remote_ratio"
]

target = "salary_in_usd"

X = df[features]
y = df[target]

categorical_features = [
    "experience_level",
    "employment_type",
    "job_title",
    "employee_residence"
]

numerical_features = [
    "work_year",
    "remote_ratio"
]

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        )
    ],
    remainder="passthrough"
)

salary_model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        (
            "model",
            RandomForestRegressor(
                n_estimators=200,
                random_state=42
            )
        )
    ]
)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

salary_model.fit(X_train, y_train)

y_pred = salary_model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# =========================================================
# EXECUTIVE SUMMARY
# =========================================================

st.markdown("---")
st.markdown("## ⚡ Executive Summary")
st.caption(
    "A quick overview of the current salary market selection."
)

if len(filtered_df) > 0:

    summary_avg_salary = filtered_df["salary_in_usd"].mean()

    summary_top_job = (
        filtered_df["job_title"]
        .value_counts()
        .idxmax()
    )

    summary_top_country = (
        filtered_df
        .groupby("employee_residence")["salary_in_usd"]
        .mean()
        .idxmax()
    )

    summary_top_experience = (
        filtered_df
        .groupby("experience_level")["salary_in_usd"]
        .mean()
        .idxmax()
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "💰 Average Salary",
            f"${summary_avg_salary:,.0f}"
        )

    with col2:
        st.metric(
            "🏆 Most Represented Career",
            summary_top_job
        )

    with col3:
        st.metric(
            "🌎 Highest-Paying Country",
            summary_top_country
        )

    with col4:
        st.metric(
            "📈 Highest Salary Level",
            summary_top_experience
        )

    st.markdown("### 💡 Key Finding")

    st.success(
        f"""
        **{summary_top_experience}** positions currently show the
        highest average salary, while **{summary_top_job}** is the
        most represented career in the selected dataset.
        """
    )

else:

    st.warning(
        "⚠️ No records match the current filters."
    )
# =========================================================
# DASHBOARD TABS
# =========================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Market Overview",
    "🔬 Advanced Analytics",
    "🧠 Career Intelligence",
    "🤖 ML & Dataset"
])
with tab1:
    st.markdown("## 📊 Salary Market Snapshot")

    if len(filtered_df) == 0:
        st.warning("⚠️ No records match your selected filters.")
    else:
        total_records = len(filtered_df)

        avg_salary = filtered_df["salary_in_usd"].mean()
        median_salary = filtered_df["salary_in_usd"].median()
        highest_salary = filtered_df["salary_in_usd"].max()

        top_job = (
            filtered_df["job_title"]
            .value_counts()
            .idxmax()
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("📁 Records", f"{total_records:,}")

        with col2:
            st.metric("💰 Average Salary", f"${avg_salary:,.0f}")

        with col3:
            st.metric("📈 Median Salary", f"${median_salary:,.0f}")

        with col4:
            st.metric("🏆 Highest Salary", f"${highest_salary:,.0f}")

        st.caption(
            f"Most represented career in the current selection: **{top_job}**"
        )

#st.info("Select different filters to explore global salaries.")
# ---------------------------------------------------------
# TAB 2 — CAREER INTELLIGENCE
# ---------------------------------------------------------

with tab2:

    st.markdown("## 🧠 Career Intelligence")
    st.caption(
        "Explore job demand and salary opportunities across different career roles."
    )
    # ============================================================
# 🔬 ADVANCED ANALYTICS
# ============================================================

with tab2:

    st.markdown("## 🔬 Advanced Analytics")
    st.caption("Explore salary patterns, employment structure, remote work and experience-level trends.")

    # ========================================================
    # ROW 1 — EMPLOYMENT TYPE + EXPERIENCE LEVEL
    # ========================================================

    col1, col2 = st.columns(2)

    # --------------------------------------------------------
    # 1. Employment Type Donut
    # --------------------------------------------------------
    with col1:

        st.markdown("### 💼 Employment Type")

        employment_counts = (
            filtered_df["employment_type"]
            .value_counts()
            .reset_index()
        )

        employment_counts.columns = [
            "employment_type",
            "count"
        ]

        fig_employment = px.pie(
            employment_counts,
            names="employment_type",
            values="count",
            hole=0.55,
            title="Employment Type Distribution"
        )

        fig_employment.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )

        fig_employment.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=60, b=20),
            showlegend=True
        )

        st.plotly_chart(
            fig_employment,
            use_container_width=True
        )

    # --------------------------------------------------------
    # 2. Experience Level Pie
    # --------------------------------------------------------
    with col2:

        st.markdown("### 🎓 Experience Level")

        experience_counts = (
            filtered_df["experience_level"]
            .value_counts()
            .reset_index()
        )

        experience_counts.columns = [
            "experience_level",
            "count"
        ]

        fig_experience = px.pie(
            experience_counts,
            names="experience_level",
            values="count",
            hole=0.45,
            title="Experience Level Distribution"
        )

        fig_experience.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )

        fig_experience.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=60, b=20),
            showlegend=True
        )

        st.plotly_chart(
            fig_experience,
            use_container_width=True
        )


    # ========================================================
    # ROW 2 — HISTOGRAM + BOX PLOT
    # ========================================================

    col1, col2 = st.columns(2)

    # --------------------------------------------------------
    # 3. Salary Distribution Histogram
    # --------------------------------------------------------
    with col1:

        st.markdown("### 💰 Salary Distribution")

        fig_hist = px.histogram(
            filtered_df,
            x="salary_in_usd",
            nbins=30,
            title="Salary Distribution",
            labels={
                "salary_in_usd": "Salary (USD)"
            }
        )

        fig_hist.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=60, b=20),
            xaxis_title="Salary (USD)",
            yaxis_title="Number of Employees"
        )

        st.plotly_chart(
            fig_hist,
            use_container_width=True
        )

    # --------------------------------------------------------
    # 4. Salary Spread & Outliers Box Plot
    # --------------------------------------------------------
    with col2:

        st.markdown("### 📦 Salary Spread & Outliers")

        fig_box = px.box(
            filtered_df,
            x="experience_level",
            y="salary_in_usd",
            color="experience_level",
            title="Salary Spread by Experience Level",
            labels={
                "experience_level": "Experience Level",
                "salary_in_usd": "Salary (USD)"
            }
        )

        fig_box.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=60, b=20),
            showlegend=False
        )

        st.plotly_chart(
            fig_box,
            use_container_width=True
        )


    # ========================================================
    # ROW 3 — HEATMAP + REMOTE WORK SCATTER
    # ========================================================

    col1, col2 = st.columns(2)

    # --------------------------------------------------------
    # 5. Salary Heatmap
    # --------------------------------------------------------
    with col1:

        st.markdown("### 🔥 Salary Heatmap")

        heatmap_data = (
            filtered_df
            .groupby(
                ["experience_level", "remote_status"]
            )["salary_in_usd"]
            .mean()
            .reset_index()
        )

        heatmap_pivot = heatmap_data.pivot(
            index="experience_level",
            columns="remote_status",
            values="salary_in_usd"
        )

        fig_heatmap = px.imshow(
            heatmap_pivot,
            text_auto=".0f",
            aspect="auto",
            title="Average Salary by Experience & Work Mode",
            labels={
                "x": "Work Mode",
                "y": "Experience Level",
                "color": "Average Salary (USD)"
            }
        )

        fig_heatmap.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=60, b=20)
        )

        st.plotly_chart(
            fig_heatmap,
            use_container_width=True
        )

    # --------------------------------------------------------
    # 6. Salary vs Remote Work Scatter
    # --------------------------------------------------------
    with col2:

        st.markdown("### 🌍 Salary vs Remote Work")

        fig_remote = px.scatter(
            filtered_df,
            x="remote_ratio",
            y="salary_in_usd",
            color="experience_level",
            hover_data=[
                "job_title",
                "employee_residence",
                "employment_type"
            ],
            title="Salary vs Remote Work Ratio",
            labels={
                "remote_ratio": "Remote Work (%)",
                "salary_in_usd": "Salary (USD)"
            }
        )

        fig_remote.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=60, b=20)
        )

        st.plotly_chart(
            fig_remote,
            use_container_width=True
        )


    # ========================================================
    # ROW 4 — VIOLIN + YEAR TREND
    # ========================================================

    col1, col2 = st.columns(2)

    # --------------------------------------------------------
    # 7. Salary Distribution Density Violin
    # --------------------------------------------------------
    with col1:

        st.markdown("### 🎻 Salary Density")

        fig_violin = px.violin(
            filtered_df,
            y="salary_in_usd",
            x="experience_level",
            color="experience_level",
            box=True,
            points="outliers",
            title="Salary Density by Experience Level",
            labels={
                "experience_level": "Experience Level",
                "salary_in_usd": "Salary (USD)"
            }
        )

        fig_violin.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=60, b=20),
            showlegend=False
        )

        st.plotly_chart(
            fig_violin,
            use_container_width=True
        )

    # --------------------------------------------------------
    # 8. Salary Trend by Work Year
    # --------------------------------------------------------
    with col2:

        st.markdown("### 📈 Salary Trend")

        yearly_salary = (
            filtered_df
            .groupby("work_year")["salary_in_usd"]
            .mean()
            .reset_index()
        )

        fig_year = px.line(
            yearly_salary,
            x="work_year",
            y="salary_in_usd",
            markers=True,
            title="Average Salary Trend by Year",
            labels={
                "work_year": "Work Year",
                "salary_in_usd": "Average Salary (USD)"
            }
        )

        fig_year.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=60, b=20)
        )

        st.plotly_chart(
            fig_year,
            use_container_width=True
        )

    if len(filtered_df) > 0:

        # =================================================
        # SECTION 1 — TOP JOB ROLES BY DEMAND
        # =================================================

        st.markdown("### 📊 Most Represented Career Roles")

        top_jobs = (
            filtered_df["job_title"]
            .value_counts()
            .head(10)
            .reset_index()
        )

        top_jobs.columns = [
            "job_title",
            "job_count"
        ]

        fig_jobs = px.bar(
            top_jobs,
            x="job_count",
            y="job_title",
            orientation="h",
            color="job_title",
            title="Top 10 Job Roles by Demand",
            labels={
                "job_title": "Job Role",
                "job_count": "Number of Records"
            }
        )

        fig_jobs.update_layout(
            height=500,
            yaxis={"categoryorder": "total ascending"},
            showlegend=False
        )

        st.plotly_chart(
            fig_jobs,
            use_container_width=True
        )


        # =================================================
        # SECTION 2 — HIGHEST PAYING JOB ROLES
        # =================================================

        st.markdown("### 💰 Highest-Paying Career Roles")

        job_salary = (
            filtered_df
            .groupby("job_title")["salary_in_usd"]
            .mean()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        fig_job_salary = px.bar(
            job_salary,
            x="salary_in_usd",
            y="job_title",
            orientation="h",
            color="job_title",
            title="Top 10 Job Roles by Average Salary",
            labels={
                "job_title": "Job Role",
                "salary_in_usd": "Average Salary (USD)"
            },
            text_auto=".2s"
        )

        fig_job_salary.update_layout(
            height=500,
            yaxis={"categoryorder": "total ascending"},
            showlegend=False
        )

        st.plotly_chart(
            fig_job_salary,
            use_container_width=True
        )


        # =================================================
        # SECTION 3 — CAREER SUMMARY
        # =================================================

        st.markdown("### 🏆 Career Highlights")

        highest_paid_role = (
            filtered_df
            .groupby("job_title")["salary_in_usd"]
            .mean()
            .idxmax()
        )

        highest_paid_salary = (
            filtered_df
            .groupby("job_title")["salary_in_usd"]
            .mean()
            .max()
        )

        most_demanded_role = (
            filtered_df["job_title"]
            .value_counts()
            .idxmax()
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "🏆 Highest-Paying Role",
                highest_paid_role
            )

        with col2:
            st.metric(
                "💰 Average Salary",
                f"${highest_paid_salary:,.0f}"
            )

        with col3:
            st.metric(
                "🔥 Most Represented Role",
                most_demanded_role
            )

    else:

        st.warning(
            "⚠️ No records match your current filters. "
            "Try changing the selections in the sidebar."
        )
    # =========================================================
# CAREER GROWTH SIMULATOR
# =========================================================

st.markdown("---")
st.markdown("### 📈 Career Growth Simulator")
st.caption(
    "See how average salary changes as experience increases."
)

growth_job = st.selectbox(
    "💼 Select a Career",
    sorted(filtered_df["job_title"].dropna().unique()),
    key="growth_job"
)

growth_data = (
    filtered_df[
        filtered_df["job_title"] == growth_job
    ]
    .groupby("experience_level")["salary_in_usd"]
    .mean()
    .reindex([
        "Entry Level",
        "Mid Level",
        "Senior Level",
        "Executive Level"
    ])
    .reset_index()
)

growth_data = growth_data.dropna()

if len(growth_data) >= 2:

    fig_growth = px.line(
        growth_data,
        x="experience_level",
        y="salary_in_usd",
        markers=True,
        title=f"Salary Growth Path — {growth_job}",
        labels={
            "experience_level": "Experience Level",
            "salary_in_usd": "Average Salary (USD)"
        }
    )

    fig_growth.update_layout(
        height=450,
        xaxis_title=None,
        yaxis_title="Average Salary (USD)"
    )

    st.plotly_chart(
        fig_growth,
        use_container_width=True
    )

    # ---------------------------------------------
    # Growth Summary
    # ---------------------------------------------

    first_salary = growth_data["salary_in_usd"].iloc[0]
    last_salary = growth_data["salary_in_usd"].iloc[-1]

    salary_difference = last_salary - first_salary

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "💰 Salary Difference",
            f"${salary_difference:,.0f}"
        )

    with col2:
        if first_salary > 0:
            growth_percentage = (
                salary_difference / first_salary
            ) * 100

            st.metric(
                "📈 Growth",
                f"{growth_percentage:.1f}%"
            )

else:

    st.info(
        "Not enough experience-level data for this career "
        "to display a growth path."
    )
# =========================================================
# AUTOMATIC CAREER INSIGHTS
# =========================================================

st.markdown("---")
st.markdown("### 🧠 Automatic Career Insights")
st.caption(
    "Key insights generated automatically from the selected data."
)

if len(filtered_df) > 0:

    # Highest-paying experience level
    experience_salary = (
        filtered_df
        .groupby("experience_level")["salary_in_usd"]
        .mean()
    )

    highest_experience = experience_salary.idxmax()
    highest_experience_salary = experience_salary.max()

    # Most demanded job
    most_demanded = (
        filtered_df["job_title"]
        .value_counts()
        .idxmax()
    )

    most_demanded_count = (
        filtered_df["job_title"]
        .value_counts()
        .max()
    )

    # Highest-paying country
    country_salary = (
        filtered_df
        .groupby("employee_residence")["salary_in_usd"]
        .mean()
        .sort_values(ascending=False)
    )

    highest_country = country_salary.idxmax()
    highest_country_salary = country_salary.max()

    # Best work mode
    remote_salary = (
        filtered_df
        .groupby("remote_status")["salary_in_usd"]
        .mean()
        .sort_values(ascending=False)
    )

    best_work_mode = remote_salary.idxmax()
    best_work_mode_salary = remote_salary.max()

    col1, col2 = st.columns(2)

    with col1:

        st.success(
            f"💰 **Salary Insight**\n\n"
            f"{highest_experience} roles have the highest "
            f"average salary at **${highest_experience_salary:,.0f}**."
        )

        st.info(
            f"🔥 **Demand Insight**\n\n"
            f"**{most_demanded}** is the most represented career "
            f"with **{most_demanded_count:,} records**."
        )

    with col2:

        st.warning(
            f"🌎 **Geography Insight**\n\n"
            f"**{highest_country}** has the highest average salary "
            f"at **${highest_country_salary:,.0f}**."
        )

        st.info(
            f"🏠 **Work Mode Insight**\n\n"
            f"**{best_work_mode}** has the highest average salary "
            f"at **${best_work_mode_salary:,.0f}**."
        )

else:

    st.info(
        "Select some records using the sidebar filters "
        "to generate career insights."
    )
# =========================================================
# CAREER RECOMMENDATION ENGINE
# =========================================================

st.markdown("---")
st.markdown("### 🎯 Career Recommendation Engine")
st.caption(
    "Discover career options based on salary and market demand."
)

if len(filtered_df) > 0:

    recommendation_level = st.selectbox(
        "📊 Select Experience Level",
        [
            "Entry Level",
            "Mid Level",
            "Senior Level",
            "Executive Level"
        ],
        key="recommendation_level"
    )

    recommendation_data = filtered_df[
        filtered_df["experience_level"] == recommendation_level
    ]

    if len(recommendation_data) > 0:

        career_recommendations = (
            recommendation_data
            .groupby("job_title")
            .agg(
                Average_Salary=("salary_in_usd", "mean"),
                Demand=("salary_in_usd", "count")
            )
            .reset_index()
        )

        # Normalize salary and demand
        salary_min = career_recommendations["Average_Salary"].min()
        salary_max = career_recommendations["Average_Salary"].max()

        demand_min = career_recommendations["Demand"].min()
        demand_max = career_recommendations["Demand"].max()

        if salary_max != salary_min:
            career_recommendations["Salary_Score"] = (
                (career_recommendations["Average_Salary"] - salary_min)
                / (salary_max - salary_min)
            )
        else:
            career_recommendations["Salary_Score"] = 1

        if demand_max != demand_min:
            career_recommendations["Demand_Score"] = (
                (career_recommendations["Demand"] - demand_min)
                / (demand_max - demand_min)
            )
        else:
            career_recommendations["Demand_Score"] = 1

        # Combined career score
        career_recommendations["Career_Score"] = (
            career_recommendations["Salary_Score"] * 0.6
            + career_recommendations["Demand_Score"] * 0.4
        ) * 100

        career_recommendations = (
            career_recommendations
            .sort_values("Career_Score", ascending=False)
            .head(10)
        )

        career_recommendations["Average_Salary"] = (
            career_recommendations["Average_Salary"]
            .round(0)
        )

        career_recommendations["Career_Score"] = (
            career_recommendations["Career_Score"]
            .round(1)
        )

        st.dataframe(
            career_recommendations[
                [
                    "job_title",
                    "Average_Salary",
                    "Demand",
                    "Career_Score"
                ]
            ],
            use_container_width=True,
            hide_index=True,
            column_config={
                "job_title": "💼 Career",
                "Average_Salary": st.column_config.NumberColumn(
                    "💰 Average Salary",
                    format="$%d"
                ),
                "Demand": "🔥 Demand",
                "Career_Score": st.column_config.NumberColumn(
                    "🎯 Career Score",
                    format="%.1f"
                )
            }
        )

    else:
        st.info(
            "Not enough data for this experience level."
        )

else:
    st.warning(
        "⚠️ Select records using the sidebar filters first."
    )
# ---------------------------------------------------------
# TAB 3 — ML SALARY PREDICTOR
# ---------------------------------------------------------

with tab3:

    st.markdown("## 🤖 ML Salary Predictor")
    st.caption(
        "Predict an estimated salary using a machine-learning model "
        "trained on the historical dataset."
    )

    st.info(
        "ℹ️ The prediction is an estimate based on historical "
        "salary patterns in the dataset."
    )

    col1, col2 = st.columns(2)

    with col1:

        predictor_job = st.selectbox(
            "💼 Job Title",
            sorted(df["job_title"].dropna().unique()),
            key="ml_job"
        )

        predictor_experience = st.selectbox(
            "📊 Experience Level",
            [
                "Entry Level",
                "Mid Level",
                "Senior Level",
                "Executive Level"
            ],
            key="ml_experience"
        )

        predictor_employment = st.selectbox(
            "🧑‍💻 Employment Type",
            sorted(
                df["employment_type"]
                .dropna()
                .unique()
            ),
            key="ml_employment"
        )

    with col2:

        predictor_country = st.selectbox(
            "🌎 Employee Residence",
            sorted(
                df["employee_residence"]
                .dropna()
                .unique()
            ),
            key="ml_country"
        )

        predictor_remote = st.selectbox(
            "🏠 Work Mode",
            [
                "On-site",
                "Hybrid",
                "Fully Remote"
            ],
            key="ml_remote"
        )

        predictor_year = st.selectbox(
            "📅 Work Year",
            sorted(
                df["work_year"]
                .dropna()
                .unique()
            ),
            key="ml_year"
        )

    st.markdown("---")

    if st.button(
        "🔮 Predict Salary",
        use_container_width=True,
        key="predict_salary"
    ):

        remote_map = {
            "On-site": 0,
            "Hybrid": 50,
            "Fully Remote": 100
        }

        input_data = pd.DataFrame({
            "work_year": [predictor_year],
            "experience_level": [predictor_experience],
            "employment_type": [predictor_employment],
            "job_title": [predictor_job],
            "employee_residence": [predictor_country],
            "remote_ratio": [
                remote_map[predictor_remote]
            ]
        })

        predicted_salary = salary_model.predict(
            input_data
        )[0]

        st.success("✅ ML salary prediction generated!")

        st.metric(
            "💰 Predicted Salary",
            f"${predicted_salary:,.0f}"
        )

        st.caption(
            "Prediction generated using the trained "
            "Random Forest model."
        )
# =========================================================
# ML MODEL PERFORMANCE
# =========================================================

st.markdown("---")
st.markdown("### 📊 Model Performance")
st.caption(
    "Evaluation of the Random Forest model on unseen test data."
)

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "🎯 R² Score",
        f"{r2:.2f}"
    )

with col2:
    st.metric(
        "📉 Mean Absolute Error",
        f"${mae:,.0f}"
    )

st.info(
    f"""
    **What do these numbers mean?**

    • **R² Score:** {r2:.2f} — shows how well the model explains
    salary variation in the test data.

    • **MAE:** ${mae:,.0f} — on average, the model's prediction
    differs from the actual salary by approximately this amount.
    """
)
# =========================================================
# ACTUAL VS PREDICTED SALARY
# =========================================================

st.markdown("---")
st.markdown("### 📈 Actual vs Predicted Salary")
st.caption(
    "Comparison of actual salaries with the model's predictions."
)

comparison_df = pd.DataFrame({
    "Actual Salary": y_test.values,
    "Predicted Salary": y_pred
})

# Calculate prediction error percentage
comparison_df["Error %"] = (
    abs(
        comparison_df["Actual Salary"]
        - comparison_df["Predicted Salary"]
    )
    / comparison_df["Actual Salary"]
) * 100

# Identify outliers
comparison_df["Prediction Type"] = np.where(
    comparison_df["Error %"] > 30,
    "High Error / Outlier",
    "Normal Prediction"
)

fig_prediction = px.scatter(
    comparison_df,
    x="Actual Salary",
    y="Predicted Salary",
    color="Prediction Type",
    title="Actual vs Predicted Salary",
    labels={
        "Actual Salary": "Actual Salary (USD)",
        "Predicted Salary": "Predicted Salary (USD)",
        "Prediction Type": "Prediction"
    },
    hover_data={
        "Error %": ":.1f%",
        "Prediction Type": True
    }
)

# Perfect prediction reference line
min_value = min(
    comparison_df["Actual Salary"].min(),
    comparison_df["Predicted Salary"].min()
)

max_value = max(
    comparison_df["Actual Salary"].max(),
    comparison_df["Predicted Salary"].max()
)

fig_prediction.add_trace(
    go.Scatter(
        x=[min_value, max_value],
        y=[min_value, max_value],
        mode="lines",
        name="Perfect Prediction"
    )
)

fig_prediction.update_layout(
    height=500
)

st.plotly_chart(
    fig_prediction,
    use_container_width=True
)
# ---------------------------------------------------------
# TAB 4 — DATASET STUDIO
# ---------------------------------------------------------

with tab4:


    st.markdown("## 🗂️ Dataset Studio")
    st.caption(
        "Inspect, explore and download the salary dataset."
    )

    # -----------------------------------------------------
# MISSING VALUE CHECK
# -----------------------------------------------------

st.markdown("### 🔎 Missing Value Analysis")

missing_data = (
    df.isnull()
    .sum()
    .reset_index()
)

missing_data.columns = [
    "Column",
    "Missing Values"
]

missing_data = missing_data[
    missing_data["Missing Values"] > 0
]

if len(missing_data) == 0:
    st.success("✅ No missing values found in the dataset.")
else:
    st.warning("⚠️ Missing values were found.")

    st.dataframe(
        missing_data,
        use_container_width=True,
        hide_index=True
    )

    # -----------------------------------------------------
# DATASET OVERVIEW
# -----------------------------------------------------

st.markdown("### 📊 Dataset Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📁 Total Records",
        f"{len(df):,}"
    )

with col2:
    st.metric(
        "📋 Total Columns",
        f"{len(df.columns)}"
    )

with col3:
    st.metric(
        "💼 Unique Job Titles",
        f"{df['job_title'].nunique():,}"
    )

with col4:
    st.metric(
        "🌎 Countries",
        f"{df['employee_residence'].nunique():,}"
    )

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    missing_values = df.isnull().sum().sum()

    st.metric(
        "⚠️ Missing Values",
        f"{missing_values:,}"
    )

with col2:
    duplicate_records = df.duplicated().sum()

    st.metric(
        "🔁 Duplicate Records",
        f"{duplicate_records:,}"
    )

with col3:
    salary_range = (
        df["salary_in_usd"].max()
        - df["salary_in_usd"].min()
    )

    st.metric(
        "💰 Salary Range",
        f"${salary_range:,.0f}"
    )

st.markdown("---")

    # -----------------------------------------------------
    # COLUMN INFORMATION
    # -----------------------------------------------------

st.markdown("### 🔎 Column Information")

column_info = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str).values,
        "Missing Values": df.isnull().sum().values,
        "Unique Values": df.nunique().values
    })

st.dataframe(
        column_info,
        use_container_width=True,
        hide_index=True
    )

st.markdown("---")

    # -----------------------------------------------------
    # DOWNLOAD DATASET
    # -----------------------------------------------------

st.markdown("### 📥 Download Data")

csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
        "⬇️ Download Filtered Dataset",
        data=csv_data,
        file_name="filtered_salary_dataset.csv",
        mime="text/csv",
        use_container_width=True
    )