import pandas as pd
import streamlit as st
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

# Load the Excel file from GitHub (raw link)
excel_file = 'https://github.com/Dang-Vu-Nguyen/HSK-3.0-list/raw/main/NewHSKvunotes.xlsx'

# Specify the columns to load (including those that need to be removed later)
columns_to_load = ['STT - All', 'Level', 'STT - Per Level', 'Label', '中文', 'Pinyin', '汉越',  
                   '中文解释', '越南语意思', '中文例句', 'Pinyin例句', '越南语例句', '繁体中文例句', '例句汉越']

# Load the data into a dataframe
df = pd.read_excel(excel_file, usecols=columns_to_load)

# Remove unwanted columns: "Label", "中文解释"
df = df.drop(columns=['STT - All', 'Label', '中文解释'])

# Rename the columns
df = df.rename(columns={
    'STT - All': 'No. (All)',
    'STT - Per Level': 'STT (of level)',
    '中文': 'Từ vựng',
    '越南语意思': 'Nghĩa Việt',
    '汉越': 'Hán Việt',
    '中文例句': 'Câu mẫu',
    '越南语例句': 'Nghĩa câu mẫu',
    '繁体中文例句': 'Phồn thể',
    '例句汉越': 'Hán Việt câu mẫu',
    'Pinyin例句': 'Pinyin câu mẫu',
})

# Re-select the columns to ensure correct order after renaming and dropping unwanted columns
columns_to_display = ['Level', 'STT (of level)', 'Từ vựng', 'Pinyin', 'Hán Việt',  
                      'Nghĩa Việt', 'Câu mẫu', 'Phồn thể', 'Pinyin câu mẫu', 'Nghĩa câu mẫu', 'Hán Việt câu mẫu']
df = df[columns_to_display]

# Reset index to start from 1 instead of 0
df.index = df.index + 1

# Set up Streamlit
st.set_page_config(page_title='HSK Vocabulary App')

# Custom CSS to hide the toolbar (including download button)
st.markdown(
    """
    <style>
    [data-testid="stElementToolbar"] {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

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

def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    import pandas as pd
    import streamlit as st
    from pandas.api.types import (
        is_categorical_dtype,
        is_numeric_dtype,
    )

    modify = st.checkbox("Tìm kiếm...", value=True)

    if not modify:
        return df

    df = df.copy()

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Tìm kiếm theo cột...", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100 if (_max - _min) != 0 else 1
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            else:
                user_text_input = right.text_input(
                    f"Search in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input, na=False, regex=False)]

    return df

# Filterable DataFrame UI
filtered_df = filter_dataframe(df)

# Display the filtered dataframe in Streamlit with custom header size
st.dataframe(filtered_df, use_container_width=True)

# Display the dataframe in Streamlit without the index
# st.dataframe(df, use_container_width=True)

# Remove the download button section completely
# If you want to allow users to download the data:
# @st.cache_data
# def convert_df(df):
#     return df.to_csv(index=False).encode('utf-8')
#
# csv_data = convert_df(df)
#
# Button for downloading the filtered data
# st.download_button(label="Download data as CSV", data=csv_data, file_name='hsk_vocabulary.csv', mime='text/csv')
