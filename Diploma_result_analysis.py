import streamlit as st
import pandas as pd

# Function to find and set the correct header
def find_and_set_header(df):
    for i in range(5):
        if 'Status' in df.iloc[i].values or 'RESULT' in df.iloc[i].values:
            df.columns = df.iloc[i]
            df = df.drop(index=list(range(i+1)))
            df.reset_index(drop=True, inplace=True)
            return df
    st.error("The uploaded file does not contain 'Status' or 'RESULT' column in the first five rows.")
    return None

# Function to analyze the status column
def analyze_status(df):
    if 'Status' in df.columns:
        status_counts = df['Status'].value_counts()
    elif 'RESULT' in df.columns:
        status_counts = df['RESULT'].value_counts()
    else:
        return None
    return status_counts

# Function to handle multiple sheets in Excel file
def analyze_excel(file):
    xls = pd.ExcelFile(file)
    results = {}
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(file, sheet_name=sheet_name)
        df = find_and_set_header(df)
        if df is not None:
            status_counts = analyze_status(df)
            if status_counts is not None:
                results[sheet_name] = status_counts
    return results

# Streamlit app
def main():
    st.title("Dimploma Students Result Analysis")
    st.write("Upload a CSV or Excel file to analyze student status.")

    uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx"])

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
                df = find_and_set_header(df)
                if df is not None:
                    st.write("File uploaded successfully!")
                    st.write("Here's a preview of the data:")
                    st.dataframe(df.head())

                    status_counts = analyze_status(df)
                    if status_counts is not None:
                        st.write("### Analysis of Student Status")
                        st.write(status_counts)
                        st.bar_chart(status_counts)

            elif uploaded_file.name.endswith('.xlsx'):
                results = analyze_excel(uploaded_file)
                if results:
                    for sheet, status_counts in results.items():
                        st.write(f"### Analysis of Student Status for sheet: {sheet}")
                        st.write(status_counts)
                        st.bar_chart(status_counts)
                else:
                    st.error("No valid 'Status' or 'RESULT' columns found in any sheets.")

            else:
                st.error("Unsupported file format.")

        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
