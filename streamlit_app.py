import streamlit as st
import os
import csv
from io import BytesIO
import re

# Function to extract the first 250 words from a text file
def extract_text_from_file(uploaded_file):
    content = uploaded_file.read().decode('utf-8')
    words = re.findall(r'\b\w+\b', content)
    extracted_text = " ".join(words[:250])
    return extracted_text

# Streamlit interface
st.title("Text File Extractor and CSV Generator")

uploaded_files = st.file_uploader("Upload multiple .txt files", type=["txt"], accept_multiple_files=True)

if uploaded_files:
    st.write("Uploaded files:")
    text_contents = []
    for uploaded_file in uploaded_files:
        text = extract_text_from_file(uploaded_file)
        text_contents.append(text)

    if st.button("Generate CSV"):
        csv_filename = "generated_data.csv"
        with open(csv_filename, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['File Name', 'Extracted Text'])
            for i, text in enumerate(text_contents):
                csv_writer.writerow([uploaded_files[i].name, text])
        st.success("CSV file generated successfully! You can download it below.")

        # Download link for the generated CSV file
        with open(csv_filename, "rb") as csv_file:
            st.download_button(
                label="Download CSV",
                data=csv_file,
                key="csv_download",
                file_name=csv_filename,
            )

else:
    st.info("Please upload some .txt files.")

# Cleanup: remove the generated CSV file
if os.path.exists("generated_data.csv"):
    os.remove("generated_data.csv")
