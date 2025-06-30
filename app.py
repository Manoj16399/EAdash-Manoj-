import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="Employee Attrition Dashboard", layout="wide")

# Load the data
@st.cache_data
def load_data():
    return pd.read_csv("EA.csv")

df = load_data()

st.title("📊 Employee Attrition Dashboard")
st.markdown("""
This dashboard provides HR Directors and stakeholders with macro and micro insights into employee attrition.
Explore patterns using interactive filters, dropdowns, sliders, and tabs.
""")

# Sidebar Filters
st.sidebar.header("🔎 Filters")
selected_gender = st.sidebar.selectbox("Select Gender", options=["All"] + list(df["Gender"].unique()))
selected_department = st.sidebar.selectbox("Select Department", options=["All"] + list(df["Department"].unique()))
selected_age = st.sidebar.slider("Select Age Range", int(df.Age.min()), int(df.Age.max()), (25, 45))

# Apply filters
filtered_df = df.copy()
if selected_gender != "All":
    filtered_df = filtered_df[filtered_df["Gender"] == selected_gender]
if selected_department != "All":
    filtered_df = filtered_df[filtered_df["Department"] == selected_department]
filtered_df = filtered_df[(filtered_df["Age"] >= selected_age[0]) & (filtered_df["Age"] <= selected_age[1])]

# Tab Layout
tabs = st.tabs(["Overview", "By Demographics", "Satisfaction", "Job Details", "Performance & Promotions"])

# -------- TAB 1: Overview --------
with tabs[0]:
    st.subheader("1. Overall Attrition Count")
    st.markdown("This chart shows how many employees have left vs stayed.")
    st.bar_chart(filtered_df["Attrition"].value_counts())

    st.subheader("2. Attrition Rate Pie Chart")
    st.markdown("Shows percentage share of attrition.")
    pie_df = filtered_df["Attrition"].value_counts().reset_index()
    fig = px.pie(pie_df, names="index", values="Attrition", title="Attrition Distribution")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("3. Correlation Heatmap")
    st.markdown("Heatmap showing correlations among numerical features.")
    corr = filtered_df.select_dtypes(include='number').corr()
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(corr, annot=False, cmap="coolwarm", ax=ax)
    st.pyplot(fig)

# -------- TAB 2: Demographics --------
with tabs[1]:
    st.subheader("4. Attrition by Gender")
    st.markdown("Check gender-wise attrition trends.")
    st.bar_chart(filtered_df.groupby("Gender")["Attrition"].value_counts().unstack().fillna(0))

    st.subheader("5. Attrition by Marital Status")
    st.markdown("Marital status and attrition correlation.")
    st.bar_chart(filtered_df.groupby("MaritalStatus")["Attrition"].value_counts().unstack().fillna(0))

    st.subheader("6. Age Distribution")
    st.markdown("Histogram of employee ages filtered by attrition.")
    fig = px.histogram(filtered_df, x="Age", color="Attrition", nbins=20)
    st.plotly_chart(fig, use_container_width=True)

# -------- TAB 3: Satisfaction --------
with tabs[2]:
    st.subheader("7. Job Satisfaction vs Attrition")
    st.markdown("Explore if job satisfaction affects attrition.")
    fig = px.box(filtered_df, x="Attrition", y="JobSatisfaction", points="all")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("8. Environment Satisfaction vs Attrition")
    fig = px.box(filtered_df, x="Attrition", y="EnvironmentSatisfaction", points="all")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("9. Work-Life Balance vs Attrition")
    fig = px.box(filtered_df, x="Attrition", y="WorkLifeBalance", points="all")
    st.plotly_chart(fig, use_container_width=True)

# -------- TAB 4: Job Details --------
with tabs[3]:
    st.subheader("10. Attrition by Job Role")
    st.markdown("Some roles may have higher attrition.")
    fig = px.histogram(filtered_df, x="JobRole", color="Attrition", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("11. Distance from Home")
    st.markdown("Distance might impact employee turnover.")
    fig = px.box(filtered_df, x="Attrition", y="DistanceFromHome")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("12. Monthly Income vs Attrition")
    fig = px.box(filtered_df, x="Attrition", y="MonthlyIncome")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("13. Years at Company vs Attrition")
    fig = px.box(filtered_df, x="Attrition", y="YearsAtCompany")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("14. Business Travel vs Attrition")
    fig = px.histogram(filtered_df, x="BusinessTravel", color="Attrition", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

# -------- TAB 5: Performance & Promotions --------
with tabs[4]:
    st.subheader("15. Performance Rating vs Attrition")
    st.markdown("Check whether high performers also leave.")
    fig = px.histogram(filtered_df, x="PerformanceRating", color="Attrition", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("16. Years Since Last Promotion")
    fig = px.box(filtered_df, x="Attrition", y="YearsSinceLastPromotion")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("17. Years with Current Manager")
    fig = px.box(filtered_df, x="Attrition", y="YearsWithCurrManager")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("18. Education Field vs Attrition")
    fig = px.histogram(filtered_df, x="EducationField", color="Attrition", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("19. Education Level vs Attrition")
    fig = px.histogram(filtered_df, x="Education", color="Attrition", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("20. Overtime vs Attrition")
    if "OverTime" in filtered_df.columns:
        fig = px.histogram(filtered_df, x="OverTime", color="Attrition", barmode="group")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("OverTime column not found in dataset.")
