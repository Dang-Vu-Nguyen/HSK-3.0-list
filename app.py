import pandas as pd
import streamlit as st

# Load the Excel file from GitHub (raw link)
excel_file = 'https://github.com/Dang-Vu-Nguyen/HSK-3.0-list/raw/main/TestNewHSK.xlsx'

# Specify the columns you want to display
columns_to_display = ['STT - All', 'Level', 'STT - Per Level', 'Label', '中文', 'Pinyin', 
                      '中文解释', '越南语意思', '中文例句', '越南语例句', '汉越', '例句汉越', '繁体中文例句']

# Load the data into a dataframe
df = pd.read_excel(excel_file, usecols=columns_to_display)

# Set up Streamlit
st.set_page_config(page_title='HSK Vocabulary App')

# Add title and subtitle to the app
st.title('HSK Vocabulary Web App')
st.subheader('Displaying the selected columns from the Excel file')

# Display the dataframe in Streamlit
st.dataframe(df)

# If you want to allow users to download the data:
@st.cache
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

csv_data = convert_df(df)

# Button for downloading the filtered data
st.download_button(label="Download data as CSV", data=csv_data, file_name='hsk_vocabulary.csv', mime='text/csv')
