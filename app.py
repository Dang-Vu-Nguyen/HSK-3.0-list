import pandas as pd
import streamlit as st

# Load the Excel file from GitHub (raw link)
excel_file = 'https://github.com/Dang-Vu-Nguyen/HSK-3.0-list/raw/main/NewHSKvunotes.xlsx'

# Specify the columns to load (including those that need to be removed later)
columns_to_load = ['STT - All', 'Level', 'STT - Per Level', 'Label', '中文', 'Pinyin', '汉越',  
                   '中文解释', '越南语意思', '中文例句', '越南语例句', '繁体中文例句', '例句汉越']

# Load the data into a dataframe
df = pd.read_excel(excel_file, usecols=columns_to_load)

# Remove unwanted columns: "Label", "中文解释"
df = df.drop(columns=['Label', '中文解释'])

# Rename the columns
df = df.rename(columns={
    'STT - All': 'No. (All)',
    'STT - Per Level': 'No. (Per level)',
    '中文': 'Từ vựng',
    '越南语意思': 'Nghĩa Việt',
    '汉越': 'Hán Việt',
    '中文例句': 'Câu ví dụ',
    '越南语例句': 'Nghĩa câu ví dụ',
    '繁体中文例句': 'Phồn thể',
    '例句汉越': 'Hán Việt của ví dụ'
})

# Re-select the columns to ensure correct order after renaming and dropping unwanted columns
columns_to_display = ['No. (All)', 'Level', 'No. (Per level)', 'Từ vựng', 'Pinyin', 'Hán Việt',  
                      'Nghĩa Việt', 'Câu ví dụ', 'Nghĩa câu ví dụ', 'Phồn thể', 'Hán Việt của ví dụ']
df = df[columns_to_display]

# Set up Streamlit
st.set_page_config(page_title='HSK Vocabulary App')

# App Title and Description
st.title('Toàn Bộ 11092 Từ Vựng HSK 3.0')
st.subheader('Đã hoàn thành từ HSK1 đến HSK5')
st.markdown('''
Theo cấu trúc HSK 3.0 mới, sau 2021, mỗi cấp độ sẽ cần số từ vựng như sau:
- HSK1: 500 từ
- HSK2: 772 từ
- HSK3: 973 từ
- HSK4: 1000 từ
- HSK5: 1071 từ
- HSK6: 1140 từ
- HSK7-9: 5636 từ

Tổng cộng là 11092 từ.

Tại đây, mình đã lập danh sách tất cả 11092 từ vựng. Mỗi từ vựng bao gồm Pinyin, Hán Việt, nghĩa tiếng Việt, câu ví dụ, và cả dạng Phồn Thể nữa.

Hy vọng danh sách này sẽ hữu ích cho các bạn! Chúc các bạn học thật tốt nhé!

- Học bằng video và audio: [Kênh YouTube Luyện Tiếng Trung 2](https://www.youtube.com/@luyentiengtrung2)  
- Học bằng thẻ từ vựng: [vunotes.com/tieng-trung](https://vunotes.com/tieng-trung)  
- Học theo cấu trúc HSK 2.0 (cũ): [Kênh YouTube Luyện Tiếng Trung](https://www.youtube.com/@luyentiengtrung)
''')

# Display the dataframe in Streamlit without the index
st.dataframe(df, use_container_width=True)

# If you want to allow users to download the data:
@st.cache_data  # Updated to st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

csv_data = convert_df(df)

# Button for downloading the filtered data
# st.download_button(label="Download data as CSV", data=csv_data, file_name='hsk_vocabulary.csv', mime='text/csv')
