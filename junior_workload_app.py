import streamlit as st
import math
import pandas as pd
import plotly.express as px
import json
from io import StringIO

# ======================
# 🛠️ CONFIGURATION
# ======================
DEFAULT_SUBJECTS = {
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

LESSONS_PER_TEACHER = 27  # TSC standard
STUDENTS_PER_STREAM = 40  # CBC recommended class size
MAX_WORKLOAD = 27  # TSC maximum lessons/week

# ======================
# 🎨 PAGE SETUP
# ======================
st.set_page_config(
    page_title="CBC Teacher Workload Analyzer Pro",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🏫 CBC Junior School Staffing Analyzer Pro")
st.markdown("""
*Official tool for calculating teacher workload with qualification tracking under Kenya's CBC system.*  
🔴 **Red** = Critical staffing gap | 🟢 **Green** = Optimal staffing | 🟡 **Yellow** = Qualification mismatch
""")

# ======================
# 📊 CORE FUNCTIONS
# ======================
def calculate_streams(enrollment):
    return {grade: math.ceil(students / STUDENTS_PER_STREAM) 
            for grade, students in enrollment.items()}

def calculate_workload(streams, subjects):
    return {subject: lessons * sum(streams.values()) 
            for subject, lessons in subjects.items()}

def analyze_staffing(workload, available_teachers, qualified_teachers):
    total_lessons = sum(workload.values())
    required_teachers = math.ceil(total_lessons / LESSONS_PER_TEACHER)
    
    # Qualification analysis
    qualification_gaps = {}
    for subject, lessons in workload.items():
        required = math.ceil(lessons / LESSONS_PER_TEACHER)
        qualified = qualified_teachers.get(subject, 0)
        qualification_gaps[subject] = max(0, required - qualified)
    
    return {
        "total_lessons": total_lessons,
        "required_teachers": required_teachers,
        "staffing_gap": available_teachers - required_teachers,
        "qualification_gaps": qualification_gaps,
        "total_qualification_gap": sum(qualification_gaps.values())
    }

# ======================
# 📝 INPUT SECTION
# ======================
with st.sidebar:
    st.header("⚙️ School Configuration")
    
    # 1. Enrollment Input
    st.subheader("👩‍🎓 Student Enrollment")
    enrollment = {
        "Grade 7": st.number_input("Grade 7 Students", min_value=0, value=0),
        "Grade 8": st.number_input("Grade 8 Students", min_value=0, value=0),
        "Grade 9": st.number_input("Grade 9 Students", min_value=0, value=0)
    }
    
    # 2. Subject Configuration
    st.subheader("📚 Subjects Offered")
    subject_config = {}
    for subject, default_lessons in DEFAULT_SUBJECTS.items():
        subject_config[subject] = st.number_input(
            f"{subject} lessons/week",
            min_value=1,
            value=default_lessons,
            key=f"lessons_{subject}"
        )
    
    # 3. Teacher Input
    st.subheader("👨‍🏫 Staffing Data")
    available_teachers = st.number_input("Total Teachers Available", min_value=0, value=10)
    
    # 4. Teacher Qualifications
    st.subheader("🎓 Teacher Qualifications")
    qualified_teachers = {}
    for subject in subject_config.keys():
        qualified_teachers[subject] = st.number_input(
            f"Teachers qualified for {subject}",
            min_value=0,
            max_value=available_teachers,
            value=0,
            key=f"qual_{subject}"
        )
    
    # Validation
    if sum(qualified_teachers.values()) > available_teachers:
        st.error("❗ Total qualified teachers exceed available staff!")
    
    # 5. Advanced Options
    with st.expander("⚡ Advanced Settings"):
        
        LESSONS_PER_TEACHER = st.number_input(
            "Max Lessons/Teacher", 
            min_value=1, 
            value=27,
            help="TSC standard is 27 lessons/week"
        )
        
        # CSV Upload
        uploaded_file = st.file_uploader("Upload Staffing CSV", type=["csv"])
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.write("Uploaded Data Preview:", df.head())

# ======================
# 📊 CALCULATIONS
# ======================
streams = calculate_streams(enrollment)
workload = calculate_workload(streams, subject_config)
analysis = analyze_staffing(workload, available_teachers, qualified_teachers)

# ======================
# 📈 RESULTS DISPLAY
# ======================
tab1, tab2, tab3 = st.tabs(["📊 Summary", "📚 Subject Details", "📤 Export"])

with tab1:
    # 1. Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Streams", sum(streams.values()))
    with col2:
        st.metric("Weekly Lessons", analysis["total_lessons"])
    with col3:
        status_color = "red" if analysis["staffing_gap"] < 0 else "green"
        st.metric(
            "Teachers Needed", 
            analysis["required_teachers"],
            delta=f"{analysis['staffing_gap']} gap",
            delta_color=status_color
        )
    with col4:
        qual_color = "red" if analysis["total_qualification_gap"] > 0 else "green"
        st.metric(
            "Qualification Gaps",
            analysis["total_qualification_gap"],
            delta="subject mismatches",
            delta_color=qual_color
        )
    
    # 2. Stream Breakdown
    with st.expander("📝 Stream Details"):
        st.table(pd.DataFrame.from_dict(streams, orient="index", columns=["Streams"]))
    
    # 3. Workload Distribution
    st.plotly_chart(
        px.pie(
            names=list(workload.keys()),
            values=list(workload.values()),
            title="Lesson Distribution by Subject",
            hole=0.4
        ),
        use_container_width=True
    )

with tab2:
    # 1. Subject-Level Analysis
    st.subheader("Subject Workload & Qualifications")
    subject_df = pd.DataFrame({
        "Subject": list(workload.keys()),
        "Weekly Lessons": list(workload.values()),
        "Teachers Required": [math.ceil(lessons/LESSONS_PER_TEACHER) 
                            for lessons in workload.values()],
        "Teachers Qualified": list(qualified_teachers.values()),
        "Qualification Gap": list(analysis["qualification_gaps"].values())
    })
    
    # Color coding for gaps
    def color_gaps(val):
        color = 'red' if val > 0 else 'green'
        return f'background-color: {color}'
    
    st.dataframe(
        subject_df.style.applymap(color_gaps, subset=['Qualification Gap'])
    )
    
    # 2. Qualification Visualization
    st.plotly_chart(
        px.bar(
            subject_df,
            x="Subject",
            y=["Teachers Required", "Teachers Qualified"],
            barmode="group",
            title="Teacher Requirements vs Qualifications",
            labels={"value": "Teachers", "variable": "Type"}
        ),
        use_container_width=True
    )

with tab3:
    # 1. Report Generation
    st.subheader("Export Options")
    
    # JSON Export
    report_data = {
        "enrollment": enrollment,
        "streams": streams,
        "workload": workload,
        "qualifications": qualified_teachers,
        "analysis": analysis
    }
    st.download_button(
        label="📄 Download Full Report (JSON)",
        data=json.dumps(report_data, indent=2),
        file_name="cbc_staffing_report.json",
        mime="application/json"
    )
    
    # CSV Export
    csv = subject_df.to_csv(index=False)
    st.download_button(
        label="📊 Download Subject Data (CSV)",
        data=csv,
        file_name="subject_analysis.csv",
        mime="text/csv"
    )

# ======================
# 🚨 ENHANCED COMPLIANCE ALERTS
# ======================
if analysis["staffing_gap"] < 0 or analysis["total_qualification_gap"] > 0:
    alert_container = st.container()
    with alert_container:
        if analysis["staffing_gap"] < 0:
            st.error(f"""
            ❌ **Staffing Shortage**  
            Need {abs(analysis["staffing_gap"])} more teachers (Total required: {analysis["required_teachers"]})
            """)
        
        if analysis["total_qualification_gap"] > 0:
            deficit_subjects = [
                f"{sub} ({gap})" for sub, gap in analysis["qualification_gaps"].items() if gap > 0
            ]
            st.warning(f"""
            🟡 **Qualification Gaps**  
            Subjects with underqualified staff: {", ".join(deficit_subjects)}
            """)
else:
    st.success("✅ **Optimal Staffing**: All requirements met with qualified teachers.")

if any(lessons > MAX_WORKLOAD for lessons in workload.values()):
    st.warning("⚠️ Some subjects exceed recommended weekly lesson load!")

