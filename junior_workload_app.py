import streamlit as st
import math
import pandas as pd
import plotly.express as px

# Constants
JUNIOR_SUBJECTS = {
    "English": 5,
    "Kiswahili/KSL": 4,
    "Mathematics": 5,
    "Integrated Science": 5,
    "Pre-Technical and Pre-Career Education": 4,
    "Social Studies": 4,
    "Religious Education": 4,
    "Agriculture": 4,
    "Sports and Physical Education": 5
}
LESSONS_PER_TEACHER = 27
STUDENTS_PER_STREAM = 50

# App Config
st.set_page_config(page_title="Junior School Workload Calculator", layout="wide")
st.title("📘 Junior School Workload Calculator")

# Tabs for Input & Results
tab1, tab2 = st.tabs(["📥 Input", "📊 Workload Report"])

with tab1:
    st.header("🔢 Enrollment Data")
    col1, col2, col3 = st.columns(3)
    with col1:
        grade7 = st.number_input("Grade 7 Students", min_value=0, value=0)
    with col2:
        grade8 = st.number_input("Grade 8 Students", min_value=0, value=0)
    with col3:
        grade9 = st.number_input("Grade 9 Students", min_value=0, value=0)

    streams = {
        "Grade 7": math.ceil(grade7 / STUDENTS_PER_STREAM),
        "Grade 8": math.ceil(grade8 / STUDENTS_PER_STREAM),
        "Grade 9": math.ceil(grade9 / STUDENTS_PER_STREAM),
    }
    total_streams = sum(streams.values())

    st.markdown("### 🎓 Stream Allocation")
    st.info(
        f"**Grade 7**: {streams['Grade 7']} stream(s)\n\n"
        f"**Grade 8**: {streams['Grade 8']} stream(s)\n\n"
        f"**Grade 9**: {streams['Grade 9']} stream(s)\n\n"
        f"**Total Streams**: {total_streams}"
    )

    st.header("📚 Subjects & Teachers")
    selected_subjects = st.multiselect("Select Subjects Offered", list(JUNIOR_SUBJECTS.keys()))
    teachers_available = st.number_input("Number of Teachers Available", min_value=0, value=0)

with tab2:
    st.header("🧮 Workload Calculation")

    if not selected_subjects:
        st.warning("Please go to the Input tab and select at least one subject.")
    else:
        subject_loads = {}
        total_lessons = 0

        for subject in selected_subjects:
            lessons = JUNIOR_SUBJECTS[subject]
            total = total_streams * lessons
            subject_loads[subject] = total
            total_lessons += total

        required_teachers = math.ceil(total_lessons / LESSONS_PER_TEACHER)

        # Metrics
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📚 Total Weekly Lessons", total_lessons)
        with col2:
            st.metric("👩‍🏫 Teachers Required", required_teachers)

        # Subject Breakdown Table
        st.subheader("📘 Lessons Breakdown by Subject")
        df = pd.DataFrame({
            "Subject": list(subject_loads.keys()),
            "Total Lessons": list(subject_loads.values())
        })
        st.dataframe(df, use_container_width=True)

        # Chart
        st.subheader("📊 Lessons Distribution Chart")
        fig = px.pie(df, names="Subject", values="Total Lessons", title="Subject Lesson Shares")
        st.plotly_chart(fig, use_container_width=True)

        # Staffing Summary
        st.subheader("👥 Staffing Status")
        difference = teachers_available - required_teachers
        if difference > 0:
            st.success(f"✅ You have **{difference} extra teacher(s)**.")
        elif difference == 0:
            st.success("✅ You have exactly the required number of teachers.")
        else:
            st.error(f"❌ You need **{abs(difference)} more teacher(s)**.")

