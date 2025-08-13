import streamlit as st
import pandas as pd
import os
from datetime import datetime
from fpdf import FPDF

st.set_page_config(page_title="Face Recognition Attendance Viewer", layout="centered")

st.title("📋 Face Recognition Attendance Viewer")

# List available attendance dates
attendance_files = [f for f in os.listdir("Attendance") if f.endswith(".csv")]
if not attendance_files:
    st.warning("No attendance records found.")
    st.stop()

# Extract dates from filenames
dates = [f.replace("Attendance_", "").replace(".csv", "") for f in attendance_files]
selected_date = st.selectbox("📅 Select a date", sorted(dates, reverse=True))

file_path = f"Attendance/Attendance_{selected_date}.csv"

try:
    df = pd.read_csv(file_path)
    # Split "Name_Roll" into two columns
    if "NAME" in df.columns:
        split_cols = df['NAME'].str.split("_", n=1, expand=True)
        df['NAME'] = split_cols[0]
        # df['ROLL'] = split_cols[1].fillna('not mentioned')
        if split_cols.shape[1] > 1:
            df['ROLL'] = split_cols[1].fillna('not mentioned')
        else:
            df['ROLL'] = 'not mentioned'


    st.success(f"✅ Attendance for {selected_date}")
    st.dataframe(df[['NAME', 'ROLL', 'TIME']], use_container_width=True)

    # CSV Download
    csv_data = df[['NAME', 'ROLL', 'TIME']].to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download as CSV",
        data=csv_data,
        file_name=f"{selected_date}_attendance.csv",
        mime="text/csv"
    )

    # PDF Download
    def create_pdf(dataframe, filename):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Title
        pdf.cell(200, 10, txt=f"Attendance for {selected_date}", ln=True, align='C')
        pdf.ln(10)

        # Header
        pdf.set_font("Arial", style='B', size=12)
        pdf.cell(60, 10, txt="Name", border=1)
        pdf.cell(40, 10, txt="Roll No", border=1)
        pdf.cell(60, 10, txt="Time", border=1)
        pdf.ln()

        # Rows
        pdf.set_font("Arial", size=12)
        for _, row in dataframe.iterrows():
            pdf.cell(60, 10, txt=str(row['NAME']), border=1)
            pdf.cell(40, 10, txt=str(row['ROLL']), border=1)
            pdf.cell(60, 10, txt=str(row['TIME']), border=1)
            pdf.ln()

        pdf.output(filename)

    pdf_filename = f"{selected_date}_attendance.pdf"
    create_pdf(df[['NAME', 'ROLL', 'TIME']], pdf_filename)
    with open(pdf_filename, "rb") as pdf_file:
        st.download_button(
            label="⬇️ Download as PDF",
            data=pdf_file,
            file_name=pdf_filename,
            mime="application/pdf"
        )

except FileNotFoundError:
    st.error("⚠️ Attendance file not found.")
