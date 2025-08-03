import streamlit as st
import math
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

st.set_page_config(page_title="Junior School Workload Calculator", layout="centered")
st.title("📘 Junior School Workload Calculator")
st.markdown("Use this tool to calculate streams, workload, and staffing requirements for Junior School (Grades 7–9).")

# 📌 Enrollment Section
st.header("📋 Enrollment")
col1, col2, col3 = st.columns(3)
with col1:
    grade7 = st.number_input("👨‍🎓 Grade 7 Students", min_value=0, value=0)
with col2:
    grade8 = st.number_input("👩‍🎓 Grade 8 Students", min_value=0, value=0)
with col3:
    grade9 = st.number_input("🎓 Grade 9 Students", min_value=0, value=0)

# Calculate Streams
streams = {
    "Grade 7": math.ceil(grade7 / STUDENTS_PER_STREAM),
    "Grade 8": math.ceil(grade8 / STUDENTS_PER_STREAM),
    "Grade 9": math.ceil(grade9 / STUDENTS_PER_STREAM),
}
total_streams = sum(streams.values())

st.success(
    f"✅ Streams Calculated:\n\n"
    f"- Grade 7: {streams['Grade 7']} stream(s)\n"
    f"- Grade 8: {streams['Grade 8']} stream(s)\n"
    f"- Grade 9: {streams['Grade 9']} stream(s)\n"
    f"**Total Streams: {total_streams}**"
)

# 📌 Subject and Teacher Inputs
st.header("📚 Subject Selection and Staffing")
selected_subjects = st.multiselect("📝 Select Subjects Offered", list(JUNIOR_SUBJECTS.keys()), default=list(JUNIOR_SUBJECTS.keys()))
teachers_available = st.number_input("👩‍🏫 Number of Teachers Available", min_value=0, value=0)

# 📌 Calculate Button
if st.button("🧮 Calculate Workload"):
    if not selected_subjects:
        st.error("⚠️ Please select at least one subject.")
    else:
        subject_loads = {}
        total_lessons = 0

        for subject in selected_subjects:
            lessons_per_stream = JUNIOR_SUBJECTS[subject]
            total = total_streams * lessons_per_stream
            subject_loads[subject] = total
            total_lessons += total

        required_teachers = math.ceil(total_lessons / LESSONS_PER_TEACHER)
        difference = teachers_available - required_teachers

        # 📊 Workload Summary
        st.header("📊 Workload Summary")
        st.metric("Total Weekly Lessons", total_lessons)

        # Determine delta color
        if difference > 0:
            delta_color = "inverse"
        elif difference < 0:
            delta_color = "normal"
        else:
            delta_color = "off"

        st.metric(
            "Teachers Needed",
            required_teachers,
            delta=difference,
            delta_color=delta_color
        )

        # Table
        st.subheader("📘 Subject Lesson Breakdown")
        st.table([(subject, subject_loads[subject]) for subject in selected_subjects])

        # Bar Chart
        st.subheader("📊 Lessons per Subject (Bar Chart)")
        bar_fig = px.bar(
            x=list(subject_loads.keys()),
            y=list(subject_loads.values()),
            labels={"x": "Subject", "y": "Weekly Lessons"},
            title="Weekly Lessons per Subject",
            color=list(subject_loads.keys()),
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(bar_fig, use_container_width=True)

        # Pie Chart
        st.subheader("🎯 Teacher Distribution (Pie Chart)")
        pie_fig = px.pie(
            names=list(subject_loads.keys()),
            values=list(subject_loads.values()),
            title="Proportion of Weekly Lessons by Subject",
            hole=0.3,
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        st.plotly_chart(pie_fig, use_container_width=True)

        # Status Message
        st.header("📌 Staffing Status")
        if difference > 0:
            st.success(f"✅ You have {difference} extra teacher(s).")
        elif difference == 0:
            st.info("✅ You have exactly the required number of teachers.")
        else:
            st.error(f"❌ You need {abs(difference)} more teacher(s).")
