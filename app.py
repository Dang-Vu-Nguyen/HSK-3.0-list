import pandas as pd
import streamlit as st

# Load the Excel file from GitHub (raw link)
excel_file = 'https://github.com/Dang-Vu-Nguyen/HSK-3.0-list/raw/main/NewHSKvunotes.xlsx'

# Specify the columns you want to display
columns_to_display = ['STT - All', 'Level', 'STT - Per Level', 'Label', '中文', 'Pinyin', 
                      '中文解释', '越南语意思', '中文例句', '越南语例句', '汉越', '例句汉越', '繁体中文例句']

# Load the data into a dataframe
df = pd.read_excel(excel_file, usecols=columns_to_display)

# Set up Streamlit
st.set_page_config(page_title='HSK Vocabulary App')

# App Title and Description
st.title('Toàn Bộ 11092 Từ Vựng HSK 3.0 - Từ HSK1 đến HSK9')
st.subheader('Đã Hoàn thành Từ Vựng Đến Hết HSK 5')

# Additional information for users
st.markdown('''
- Xem video có audio: [YouTube Channel](https://www.youtube.com/@luyentiengtrung2)  
- Xem thẻ từ vựng: [vunotes.com/tieng-trung](https://vunotes.com/tieng-trung)
''')

# Display the dataframe in Streamlit
st.dataframe(df)

# If you want to allow users to download the data:
@st.cache_data  # Updated to st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

csv_data = convert_df(df)

# Button for downloading the filtered data
# Comment out this part to disable downloading
# st.download_button(label="Download data as CSV", data=csv_data, file_name='hsk_vocabulary.csv', mime='text/csv')
