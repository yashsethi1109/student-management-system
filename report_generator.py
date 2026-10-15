from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch

from datetime import datetime

def generate_report(student, marks, attendance, output_path):

    styles = getSampleStyleSheet()

    title_style = styles["Heading1"]
    title_style.alignment = TA_CENTER

    normal = styles["Normal"]

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4
    )

    elements = []

    elements.append(
        Paragraph(
            "AI STUDENT MANAGEMENT SYSTEM",
            title_style
        )
    )

    elements.append(
        Paragraph(
            "Student Report Card",
            styles["Heading2"]
        )
    )

    elements.append(
        Spacer(1, 0.25 * inch)
    )

    student_info = [
        ["Student ID", student[0]],
        ["Student Name", student[1]],
        ["Email", student[2]],
        ["Phone", student[3]],
        ["Course", student[4]],
        ["Semester", student[5]],
        ["Section", student[6]],
        ["Gender", student[7]],
        ["DOB", str(student[8])]
    ]

    info_table = Table(student_info)

    info_table.setStyle(TableStyle([
        ("GRID",(0,0),(-1,-1),1,colors.grey),
        ("BACKGROUND",(0,0),(0,-1),colors.lightgrey),
        ("BOTTOMPADDING",(0,0),(-1,-1),8),
    ]))

    elements.append(info_table)

    elements.append(
        Spacer(1,0.30*inch)
    )
    
    elements.append(
        Paragraph(
            "Subject Wise Marks",
            styles["Heading2"]
        )
    )

    table_data = [
        [
            "Subject",
            "Internal",
            "External",
            "Total",
            "%",
            "Grade"
        ]
    ]

    for row in marks:

        table_data.append([
            row[0],
            row[1],
            row[2],
            row[3],
            f"{row[4]:.2f}",
            row[5]
        ])

    marks_table = Table(table_data)

    marks_table.setStyle(TableStyle([

        ("GRID",(0,0),(-1,-1),1,colors.black),

        ("BACKGROUND",(0,0),(-1,0),colors.darkblue),

        ("TEXTCOLOR",(0,0),(-1,0),colors.white),

        ("ALIGN",(0,0),(-1,-1),"CENTER"),

        ("BACKGROUND",(0,1),(-1,-1),colors.beige),

        ("BOTTOMPADDING",(0,0),(-1,0),10)

    ]))

    elements.append(marks_table)

    elements.append(
        Spacer(1,0.30*inch)
    )

    total_classes = attendance[0] or 0
    present_classes = attendance[1] or 0

    attendance_percentage = 0

    if total_classes > 0:

        attendance_percentage = (
            present_classes / total_classes
        ) * 100

    attendance_text = f"""
    <b>Attendance Summary</b><br/><br/>
    Total Classes : {total_classes}<br/>
    Present : {present_classes}<br/>
    Attendance Percentage : {attendance_percentage:.2f}%
    """

    elements.append(
        Paragraph(
            attendance_text,
            normal
        )
    )

    elements.append(
        Spacer(1,0.30*inch)
    )

    elements.append(
        Paragraph(
            f"Generated on : {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}",
            normal
        )
    )

    doc.build(elements)