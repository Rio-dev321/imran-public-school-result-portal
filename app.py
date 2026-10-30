
import streamlit as st
import pandas as pd
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

# PAGE SETTINGS
st.set_page_config(
    page_title="IPSC Student Result Portal",
    page_icon="🎓",
    layout="wide"
)

# PROFESSIONAL DESIGN
st.markdown("""
<style>
.stApp {
    background-color: #f3f6fb;
}
.hero {
    background: linear-gradient(120deg,#102a56,#176b87);
    padding: 30px;
    border-radius: 18px;
    color: white;
    text-align: center;
}
.hero h1 {
    color: white;
    font-size: 32px;
}
.card {
    background: white;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #e2e8f0;
    margin-bottom: 12px;
}
.metric {
    font-size: 28px;
    font-weight: bold;
    color: #176b87;
}
.stButton button, .stDownloadButton button {
    background: #176b87;
    color: white;
    border-radius: 9px;
}
</style>
""", unsafe_allow_html=True)

# SAMPLE STUDENT DATA
columns = [
    "Roll Number", "Student Name", "Class", "Group",
    "Year", "Subject", "Obtained Marks", "Total Marks"
]

sample_data = [
    ["IPS-1001","Ayesha Khan","10th","Science","2026","English",86,100],
    ["IPS-1001","Ayesha Khan","10th","Science","2026","Mathematics",94,100],
    ["IPS-1001","Ayesha Khan","10th","Science","2026","Physics",88,100],
    ["IPS-1001","Ayesha Khan","10th","Science","2026","Chemistry",91,100],
    ["IPS-1001","Ayesha Khan","10th","Science","2026","Biology",89,100],

    ["IPS-1002","Ali Raza","10th","Science","2026","English",76,100],
    ["IPS-1002","Ali Raza","10th","Science","2026","Mathematics",82,100],
    ["IPS-1002","Ali Raza","10th","Science","2026","Physics",79,100],
    ["IPS-1002","Ali Raza","10th","Science","2026","Chemistry",84,100],
    ["IPS-1002","Ali Raza","10th","Science","2026","Biology",80,100],

    ["IPS-1003","Sara Ahmed","9th","General","2026","English",92,100],
    ["IPS-1003","Sara Ahmed","9th","General","2026","Mathematics",87,100],
    ["IPS-1003","Sara Ahmed","9th","General","2026","Physics",90,100],
    ["IPS-1003","Sara Ahmed","9th","General","2026","Chemistry",85,100],
    ["IPS-1003","Sara Ahmed","9th","General","2026","Computer",96,100],
]

if "results" not in st.session_state:
    st.session_state.results = pd.DataFrame(
        sample_data, columns=columns
    )

df = st.session_state.results

# GRADE CALCULATION
def calculate_grade(percentage):
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    return "F"

# STUDENT SUMMARY
def summary(data):
    obtained = data["Obtained Marks"].sum()
    total = data["Total Marks"].sum()
    percentage = obtained / total * 100 if total else 0
    grade = calculate_grade(percentage)
    return obtained, total, percentage, grade

# PDF RESULT CARD
def create_pdf(data):
    obtained, total, percentage, grade = summary(data)

    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "SchoolTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        textColor=colors.HexColor("#12345b"),
        fontSize=18
    )

    story = [
        Paragraph(
            "IMRAN PUBLIC SCHOOL AND COLLEGE",
            title_style
        ),
        Paragraph(
            "STUDENT RESULT CARD",
            styles["Heading2"]
        ),
        Spacer(1, 20)
    ]

    info = [
        ["Student Name", str(data["Student Name"].iloc[0])],
        ["Roll Number", str(data["Roll Number"].iloc[0])],
        ["Class", str(data["Class"].iloc[0])],
        ["Group", str(data["Group"].iloc[0])],
        ["Year", str(data["Year"].iloc[0])]
    ]

    info_table = Table(info, colWidths=[130, 350])
    info_table.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(0,-1),colors.HexColor("#eaf2f8")),
        ("FONTNAME",(0,0),(0,-1),"Helvetica-Bold"),
        ("GRID",(0,0),(-1,-1),0.5,colors.grey),
        ("PADDING",(0,0),(-1,-1),9)
    ]))

    story += [info_table, Spacer(1,20)]

    rows = [
        ["Subject","Obtained","Total","Percentage","Grade"]
    ]

    for _, row in data.iterrows():
        pct = row["Obtained Marks"] / row["Total Marks"] * 100

        rows.append([
            row["Subject"],
            str(row["Obtained Marks"]),
            str(row["Total Marks"]),
            f"{pct:.1f}%",
            calculate_grade(pct)
        ])

    marks_table = Table(
        rows,
        colWidths=[150,80,80,90,80]
    )

    marks_table.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#176b87")),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("GRID",(0,0),(-1,-1),0.5,colors.grey),
        ("ALIGN",(1,1),(-1,-1),"CENTER"),
        ("PADDING",(0,0),(-1,-1),8)
    ]))

    story += [marks_table, Spacer(1,20)]

    story.append(Paragraph(
        f"Obtained Marks: {obtained} / {total}",
        styles["Heading3"]
    ))

    story.append(Paragraph(
        f"Percentage: {percentage:.2f}%",
        styles["Heading3"]
    ))

    story.append(Paragraph(
        f"Overall Grade: {grade}",
        styles["Heading3"]
    ))

    pdf.build(story)
    return buffer.getvalue()

# SIDEBAR NAVIGATION
st.sidebar.title("🎓 IPSC Portal")
st.sidebar.caption("Imran Public School & College")

page = st.sidebar.radio(
    "Select Page",
    ["Dashboard", "Find Student", "Upload Results", "About"]
)

# HEADER
st.markdown("""
<div class="hero">
<h1>🎓 Imran Public School & College</h1>
<p>Student Result Management Portal</p>
</div>
""", unsafe_allow_html=True)

# DASHBOARD
if page == "Dashboard":

    st.subheader("📊 Dashboard Overview")

    students = df.drop_duplicates("Roll Number")

    total_students = len(students)
    total_marks = df["Total Marks"].sum()
    obtained_marks = df["Obtained Marks"].sum()

    average = (
        obtained_marks / total_marks * 100
        if total_marks else 0
    )

    c1, c2, c3 = st.columns(3)

    c1.metric("Total Students", total_students)
    c2.metric("Total Subjects", len(df))
    c3.metric("Average Percentage", f"{average:.1f}%")

    st.subheader("📈 Class Wise Students")

    class_counts = students["Class"].value_counts()
    st.bar_chart(class_counts)

    st.subheader("📋 Student Records")

    st.dataframe(
        students[["Roll Number","Student Name","Class"]],
        use_container_width=True,
        hide_index=True
    )

# FIND STUDENT
elif page == "Find Student":

    st.subheader("🔍 Search Student Result")

    search = st.text_input(
        "Enter Student Name or Roll Number"
    )

    if search:

        matching = df[
            df["Student Name"].str.contains(
                search, case=False, na=False
            ) |
            df["Roll Number"].str.contains(
                search, case=False, na=False
            )
        ]

        if matching.empty:
            st.error("Student not found!")

        else:
            options = matching[
                ["Roll Number","Student Name"]
            ].drop_duplicates()

            selected = st.selectbox(
                "Select Student",
                options["Roll Number"].tolist()
            )

            student = df[
                df["Roll Number"] == selected
            ].copy()

            obtained, total, percentage, grade = summary(student)

            st.success("Student Record Found!")

            st.subheader("👨‍🎓 Student Details")

            st.write("Name:", student["Student Name"].iloc[0])
            st.write("Roll Number:", selected)
            st.write("Class:", student["Class"].iloc[0])
            st.write("Group:", student["Group"].iloc[0])
            st.write("Exam Year:", student["Year"].iloc[0])

            st.subheader("📊 Result Summary")

            a, b, c, d = st.columns(4)

            a.metric("Obtained Marks", obtained)
            b.metric("Total Marks", total)
            c.metric("Percentage", f"{percentage:.2f}%")
            d.metric("Grade", grade)

            st.subheader("📚 Subject Wise Marks")

            display = student[
                ["Subject","Obtained Marks","Total Marks"]
            ].copy()

            display["Percentage"] = (
                display["Obtained Marks"] /
                display["Total Marks"] * 100
            ).round(2)

            display["Grade"] = display[
                "Percentage"
            ].apply(calculate_grade)

            st.dataframe(
                display,
                use_container_width=True,
                hide_index=True
            )

            st.progress(
                min(percentage / 100, 1.0),
                text=f"Result: {percentage:.2f}%"
            )

            pdf = create_pdf(student)

            st.download_button(
                "📄 Download Result PDF",
                data=pdf,
                file_name=f"{selected}_result.pdf",
                mime="application/pdf"
            )

# UPLOAD RESULTS
elif page == "Upload Results":

    st.subheader("📤 Upload Student Results")

    st.info(
        "CSV file mein student records upload karein."
    )

    template = pd.DataFrame(columns=columns)

    st.download_button(
        "Download CSV Template",
        template.to_csv(index=False),
        "student_results_template.csv",
        "text/csv"
    )

    uploaded = st.file_uploader(
        "Choose CSV File",
        type=["csv"]
    )

    if uploaded:

        try:
            new_data = pd.read_csv(uploaded)

            if list(new_data.columns) != columns:
                st.error("CSV columns sahi nahi hain.")

            else:
                new_data["Obtained Marks"] = pd.to_numeric(
                    new_data["Obtained Marks"], errors="raise"
                )
                new_data["Total Marks"] = pd.to_numeric(
                    new_data["Total Marks"], errors="raise"
                )

                if (
                    (new_data["Total Marks"] <= 0).any()
                    or (new_data["Obtained Marks"] < 0).any()
                    or (
                        new_data["Obtained Marks"] >
                        new_data["Total Marks"]
                    ).any()
                ):
                    st.error("Marks ki values check karein.")

                elif st.button("Import Results"):
                    st.session_state.results = new_data
                    st.success("Results uploaded successfully!")
                    st.rerun()

        except Exception as error:
            st.error(f"Upload Error: {error}")

    st.subheader("Current Student Records")
    st.dataframe(df, use_container_width=True)

# ABOUT
else:

    st.subheader("About Our Portal")

    st.write("""
    Welcome to Imran Public School and College
    Student Result Portal.

    Features:
    - Student Search
    - Student Details
    - Subject Wise Marks
    - Percentage Calculation
    - Automatic Grades
    - PDF Result Download
    - CSV Result Upload
    """)

    st.info(
        "This project uses fictional sample data. "
        "Use verified school records before real-world use."
    )

st.sidebar.markdown("---")
st.sidebar.caption("© 2026 Imran Public School & College")
