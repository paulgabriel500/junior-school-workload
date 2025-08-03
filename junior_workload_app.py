import streamlit as st
import math
import plotly.express as px

# Constants
LESSONS_PER_TEACHER = 27
STUDENTS_PER_STREAM = 50

# Junior School Subjects - Expanded list
JUNIOR_SUBJECTS = {
    "English": 5,
    "Kiswahili/KSL": 4,
    "Mathematics": 5,
    "Integrated Science (Bio, Chem, Physics)": 5,
    "Pre-Technical and Pre-Career Education": 4,
    "Social Studies": 4,
    "Religious Education (CRE/IRE/HRE)": 4,
    "Agriculture": 4,
    "Sports and Physical Education": 5,
    "Life Skills Education": 1,
    "Computer Science": 2,
    "Business Studies": 2,
    "Home Science": 2,
    "Visual Arts": 2,
    "Performing Arts": 2,
    "Kenya Sign Language": 2,
    "French / German / Arabic": 2,
}

# App layout
st.set_page_config(page_title="Junior School Workload", layout="wide")
st.title("🏫 Junior School Workload Calculator")

# Enrollment section
st.header("👨‍👩‍👧‍👦 Learner Enrollment")
col1, col2, col3 = st.columns(3)
grade7 = col1.number_input("Grade 7 Students", min_value=0, value=0)
grade8 = col2.number_input("Grade 8 Students", min_value=0, value=0)
grade9 = col3.number_input("Grade 9 Students", min_value=0, value=0)

# Stream calculation
streams = {
    "Grade 7": math.ceil(grade7 / STUDENTS_PER_STREAM),
    "Grade 8": math.ceil(grade8 / STUDENTS_PER_STREAM),
    "Grade 9": math.ceil(grade9 / STUDENTS_PER_STREAM),
}
total_streams = sum(streams.values())

with st.expander("📊 Stream Summary", expanded=True):
    st.write(f"• Grade 7: **{streams['Grade 7']}** stream(s)")
    st.write(f"• Grade 8: **{streams['Grade 8']}** stream(s)")
    st.write(f"• Grade 9: **{streams['Grade 9']}** stream(s)")
    st.success(f"🎯 Total Streams: **{total_streams}**")

# Subject selection
st.header("📚 Select Subjects Offered")
selected_subjects = st.multiselect(
    "Tick the subjects taught in your school:",
    list(JUNIOR_SUBJECTS.keys()),
    default=list(JUNIOR_SUBJECTS.keys())[:9]
)

# Number of teachers available
teachers_available = st.number_input("👩‍🏫 Teachers Available", min_value=0, value=0)

# Calculate workload
if st.button("🧮 Calculate Workload"):
    if not selected_subjects:
        st.error("⚠️ Please select at least one subject.")
    else:
        subject_loads = {}
        total_lessons = 0

        for subject in selected_subjects:
            lessons_per_stream = JUNIOR_SUBJECTS[subject]
            subject_total = total_streams * lessons_per_stream
            subject_loads[subject] = subject_total
            total_lessons += subject_total

        teachers_required = math.ceil(total_lessons / LESSONS_PER_TEACHER)
        delta_teachers = teachers_available - teachers_required
        delta_color = "normal"
        if delta_teachers > 0:
            delta_color = "normal"
        elif delta_teachers < 0:
            delta_color = "inverse"

        # Metrics
        st.header("📊 Staffing Summary")
        col1, col2 = st.columns(2)
        col1.metric("Total Weekly Lessons", total_lessons)
        col2.metric(
            "Teachers Needed",
            teachers_required,
            delta=delta_teachers,
            delta_color=delta_color
        )

        # Subject workload table
        st.subheader("📘 Lessons Per Subject")
        st.table([(subject, load) for subject, load in subject_loads.items()])

        # Bar chart
        st.subheader("📊 Bar Chart: Lessons Per Subject")
        bar_fig = px.bar(
            x=list(subject_loads.keys()),
            y=list(subject_loads.values()),
            labels={'x': 'Subjects', 'y': 'Weekly Lessons'},
            title="Lesson Distribution by Subject",
            color=list(subject_loads.values()),
            color_continuous_scale='blues'
        )
        st.plotly_chart(bar_fig, use_container_width=True)

        # Pie chart
        st.subheader("🧮 Teacher Distribution (Estimated)")
        pie_data = {
            subject: round(load / LESSONS_PER_TEACHER, 2)
            for subject, load in subject_loads.items()
        }
        pie_fig = px.pie(
            names=list(pie_data.keys()),
            values=list(pie_data.values()),
            title="Estimated Teacher Allocation Per Subject",
        )
        st.plotly_chart(pie_fig, use_container_width=True)

        # Feedback
        if delta_teachers < 0:
            st.error(f"❌ You need **{abs(delta_teachers)}** more teacher(s).")
        elif delta_teachers == 0:
            st.success("✅ You have the exact number of teachers required.")
        else:
            st.success(f"✅ You have **{delta_teachers}** extra teacher(s).")
