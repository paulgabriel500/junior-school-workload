import streamlit as st
import math
import plotly.express as px

# 🎓 Subject data: Lessons per week
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

# 🎨 Page setup
st.set_page_config(page_title="Junior School Workload", page_icon="📘", layout="wide")
st.title("📘 Junior School Workload Calculator")
st.markdown("This tool helps you calculate the required number of teachers based on your enrollment and subject selection.")

# 🧮 Enrollment Inputs
st.header("👩‍🏫 Enrollment Per Grade")
col1, col2, col3 = st.columns(3)
with col1:
    grade7 = st.number_input("Grade 7", min_value=0, value=0)
with col2:
    grade8 = st.number_input("Grade 8", min_value=0, value=0)
with col3:
    grade9 = st.number_input("Grade 9", min_value=0, value=0)

# 📊 Stream Calculation
streams = {
    "Grade 7": math.ceil(grade7 / STUDENTS_PER_STREAM),
    "Grade 8": math.ceil(grade8 / STUDENTS_PER_STREAM),
    "Grade 9": math.ceil(grade9 / STUDENTS_PER_STREAM),
}
total_streams = sum(streams.values())

with st.expander("📚 View Stream Breakdown"):
    st.info(f"""
    - Grade 7 Streams: {streams['Grade 7']}
    - Grade 8 Streams: {streams['Grade 8']}
    - Grade 9 Streams: {streams['Grade 9']}
    - **Total Streams:** {total_streams}
    """)

# 📘 Subject Selection
st.header("📘 Select Subjects Offered")
selected_subjects = st.multiselect("Choose Subjects", list(JUNIOR_SUBJECTS.keys()), default=list(JUNIOR_SUBJECTS.keys()))

# 👥 Teacher Input
teachers_available = st.number_input("👨‍🏫 Number of Teachers Available", min_value=0, value=0)

# 🚀 Start Calculation
if st.button("🧮 Calculate Workload"):
    if not selected_subjects:
        st.warning("Please select at least one subject.")
    else:
        subject_loads = {}
        total_lessons = 0

        for subject in selected_subjects:
            lessons = JUNIOR_SUBJECTS[subject]
            total = total_streams * lessons
            subject_loads[subject] = total
            total_lessons += total

        required_teachers = math.ceil(total_lessons / LESSONS_PER_TEACHER)

        st.header("📊 Workload Summary")
        st.success(f"""
        - **Total Weekly Lessons:** {total_lessons}  
        - **Teachers Required (at {LESSONS_PER_TEACHER} lessons/teacher):** {required_teachers}
        """)

        # 📘 Table of Subject Lessons
        st.subheader("📚 Weekly Lessons by Subject")
        st.table([(subject, subject_loads[subject]) for subject in selected_subjects])

        # 📊 Bar Chart: Lessons per Subject
        st.subheader("📈 Lessons Per Subject (Bar Chart)")
        bar_data = {
            "Subject": list(subject_loads.keys()),
            "Lessons": list(subject_loads.values())
        }
        fig_bar = px.bar(
            bar_data,
            x="Subject",
            y="Lessons",
            color="Subject",
            text="Lessons",
            title="Weekly Lessons per Subject",
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        # 🥧 Pie Chart: Teacher Distribution
        st.subheader("🥧 Estimated Teacher Distribution (Pie Chart)")
        pie_data = {
            "Subject": [],
            "Teachers Required": []
        }

        for subject, lesson_count in subject_loads.items():
            teachers_for_subject = lesson_count / LESSONS_PER_TEACHER
            pie_data["Subject"].append(subject)
            pie_data["Teachers Required"].append(round(teachers_for_subject, 2))

        fig_pie = px.pie(
            pie_data,
            names="Subject",
            values="Teachers Required",
            title="Proportion of Teachers Needed per Subject",
            hole=0.4
        )
        st.plotly_chart(fig_pie, use_container_width=True)

        # 🧑‍🏫 Staffing Gap
        st.subheader("📌 Staffing Status")
        difference = teachers_available - required_teachers
        if difference > 0:
            st.success(f"✅ You have **{difference} extra** teacher(s).")
        elif difference == 0:
            st.info("✅ You have exactly the **required number** of teachers.")
        else:
            st.error(f"❌ You need **{abs(difference)} more** teacher(s).")
