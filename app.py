import os
import streamlit as st
import pandas as pd
from io import BytesIO

# Install dependencies
os.system('pip install -r requirements.txt')

# Set Streamlit page configuration
st.set_page_config(page_title="Khalil Page Converter Service")

# Styled Title with Color and Size
st.markdown(
    "<h1 style='text-align: center; color: #4CAF50; font-size: 40px;'>📄 Khalil Page Converter Service 🚀</h1>",
    unsafe_allow_html=True,
)

st.write("Upload CSV or Excel files, clean data, and convert formats.")

# File uploader for CSV and Excel files
files = st.file_uploader("Upload CSV or Excel Files:", type=["csv", "xlsx"], accept_multiple_files=True)

if files:
    for file in files:
        ext = file.name.split(".")[-1].lower()  # Extract file extension
        df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file, engine="openpyxl")

        st.subheader(f"{file.name} - Preview")
        st.dataframe(df.head())

        # Remove Duplicates
        if st.checkbox(f"Remove Duplicates - {file.name}"):
            df = df.drop_duplicates()
            st.success("✅ Duplicates Removed")
            st.dataframe(df.head())

        # Fill Missing Values
        if st.checkbox(f"Fill Missing Values - {file.name}"):
            df.fillna(df.select_dtypes(include=["number"]).mean(), inplace=True)
            st.success("✅ Missing values filled with column mean")
            st.dataframe(df.head())

        # Select Columns
        selected_columns = st.multiselect(f"Select Columns - {file.name}", df.columns, default=list(df.columns))
        df = df[selected_columns]
        st.dataframe(df.head())

        # Show Chart (if numeric data exists)
        if st.checkbox(f"Show Chart - {file.name}") and not df.select_dtypes(include="number").empty:
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

        # Convert & Download File
        format_choice = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"Download {file.name} as {format_choice}"):
            output = BytesIO()

            if format_choice == "CSV":
                df.to_csv(output, index=False)
                mime = "text/csv"
                new_name = file.name.replace(ext, "csv")
            else:
                df.to_excel(output, index=False, engine="openpyxl")
                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                new_name = file.name.replace(ext, "xlsx")

            st.download_button(label="Download File", data=output.getvalue(), file_name=new_name, mime=mime)
