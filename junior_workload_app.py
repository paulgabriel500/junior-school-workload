import streamlit as st
import math

# Junior School subjects and weekly lessons
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

st.title("📘 Junior School Workload Calculator")

# Enrollment inputs
st.header("Enrollment")
col1, col2, col3 = st.columns(3)
with col1:
    grade7 = st.number_input("Grade 7", min_value=0, value=0)
with col2:
    grade8 = st.number_input("Grade 8", min_value=0, value=0)
with col3:
    grade9 = st.number_input("Grade 9", min_value=0, value=0)

# Stream calculations
streams = {
    "Grade 7": math.ceil(grade7 / STUDENTS_PER_STREAM),
    "Grade 8": math.ceil(grade8 / STUDENTS_PER_STREAM),
    "Grade 9": math.ceil(grade9 / STUDENTS_PER_STREAM),
}

total_streams = sum(streams.values())

st.success(f"✅ Streams Calculated:\n\n"
           f"Grade 7: {streams['Grade 7']} | "
           f"Grade 8: {streams['Grade 8']} | "
           f"Grade 9: {streams['Grade 9']} | "
           f"Total Streams: {total_streams}")

# Subject selection
st.header("Select Subjects Offered")
selected_subjects = st.multiselect("Subjects", list(JUNIOR_SUBJECTS.keys()))

# Teachers available
teachers_available = st.number_input("Number of Teachers Available", min_value=0, value=0)

# Workload button
if st.button("🧮 Calculate Workload"):
    if not selected_subjects:
        st.error("Please select at least one subject.")
    else:
        subject_loads = {}
        total_lessons = 0

        for subject in selected_subjects:
            lessons = JUNIOR_SUBJECTS[subject]
            total = total_streams * lessons
            subject_loads[subject] = total
            total_lessons += total

        required_teachers = math.ceil(total_lessons / LESSONS_PER_TEACHER)

        st.subheader("📊 Workload Summary")
        st.write(f"**Total Weekly Lessons:** {total_lessons}")
        st.write(f"**Teachers Required (at {LESSONS_PER_TEACHER} lessons/teacher):** {required_teachers}")

        # Table of subject breakdown
        st.subheader("📘 Lessons Breakdown")
        st.table([(subj, load) for subj, load in subject_loads.items()])

        # Staffing result
        difference = teachers_available - required_teachers
        if difference > 0:
            st.success(f"✅ You have {difference} extra teacher(s).")
        elif difference == 0:
            st.success("✅ You have exactly the required number of teachers.")
        else:
            st.error(f"❌ You need {abs(difference)} more teacher(s).")
