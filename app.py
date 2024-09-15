import pandas as pd
import streamlit as st
import time
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
df = df.drop(columns=['STT - All', 'Label', '中文解释','STT - Per Level'])

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
columns_to_display = ['Level', 'Từ vựng', 'Pinyin', 'Hán Việt',  
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
st.subheader('Đã hoàn thành từ HSK1 đến HSK5 (2024.09.14)')
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

Tại đây, mình sẽ lập danh sách tất cả 11092 từ vựng. Mỗi từ vựng bao gồm Pinyin, Hán Việt, nghĩa tiếng Việt, câu ví dụ, và cả dạng Phồn Thể nữa.

Phía dưới, bạn sẽ thấy có hai phần:

1. Bảng tổng hợp toàn bộ từ vựng. 

Các bạn cũng có thể dùng chức năng lọc, tìm kiếm và hiển thị để chọn/tìm xem những nội dung mong muốn.

2. Bảng từ vựng ngẫu nhiên. 

Mỗi cấp độ sẽ chọn ra một từ vựng bất kỳ và hiển thị trong 10 giây.

Hy vọng danh sách này sẽ hữu ích cho các bạn! Chúc các bạn học thật tốt nhé!

Các link khác:

- Học bằng video và audio: [Kênh YouTube Luyện Tiếng Trung 2](https://www.youtube.com/@luyentiengtrung2)  
- Học bằng thẻ từ vựng: [vunotes.com/tieng-trung](https://vunotes.com/tieng-trung)  
- Học theo cấu trúc HSK 2.0 (cũ): [Kênh YouTube Luyện Tiếng Trung](https://www.youtube.com/@luyentiengtrung)




''')

st.divider()
st.markdown('''

Tài liệu được tổng hợp và biên soạn bởi Luyện Tiếng Trung 2. Xin vui lòng không sử dụng với mục đích thương mại mà không có sự cho phép của chúng mình.

Nếu bạn thấy nội dung hữu ích và muốn ủng hộ chúng mình, bạn có thể cân nhắc tặng chúng mình một cốc cà phê tại:
- Techcombank
- 290667040209
- NGUYEN THI HONG KHANH

Cám ơn bạn rất nhiều ạ!


''')

st.divider()

st.header("1. Bảng tổng hợp toàn bộ từ vựng")

# Allow users to select which columns to display
selected_columns = st.multiselect(
    "Chọn các cột bạn muốn xem:", 
    options=columns_to_display,  # Provide all available columns
    default=columns_to_display  # Display all by default
)


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

    # modify = st.checkbox("Tìm kiếm...", value=True)

    # if not modify:
    #     return df

    df = df.copy()

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Lọc/Tìm kiếm...", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Tìm trong {column}...",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100 if (_max - _min) != 0 else 1
                user_num_input = right.slider(
                    f"Tìm trong {column}...",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            else:
                user_text_input = right.text_input(
                    f"Tìm trong {column}...",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input, na=False, regex=False)]

    return df

# Filterable DataFrame UI
filtered_df = filter_dataframe(df)

# Display the filtered dataframe with only the selected columns
if selected_columns:
    st.dataframe(filtered_df[selected_columns], use_container_width=True)
else:
    st.write("Hãy chọn ít nhất một cột để xem.")

#######################
# New Section: Từ vựng ngẫu nhiên (with Titles in st.write)
#######################

st.header("2. Từ vựng ngẫu nhiên")

# Function to display a random row from a given dataframe
def display_random_row(df, section_title):
    if df.empty:
        st.write(f"No data available for {section_title}")
        return
    
    random_row = df.sample(n=1).iloc[0]
    
    # Combine the section title and all fields into one string for display
    row_display = (
        f"{section_title}\n"  # Display section title, e.g., "HSK 1"
        f"- {random_row.get('Từ vựng', 'N/A')} /{random_row.get('Pinyin', 'N/A')} - {random_row.get('Hán Việt', 'N/A')}/ {random_row.get('Nghĩa Việt', 'N/A')}\n\n"
        f"- {random_row.get('Câu mẫu', 'N/A')}\n\n"
        f"- {random_row.get('Phồn thể', 'N/A')}\n\n"
        f"- {random_row.get('Pinyin câu mẫu', 'N/A')}\n\n"
        f"- {random_row.get('Hán Việt câu mẫu', 'N/A')}\n\n"
        f"- {random_row.get('Nghĩa câu mẫu', 'N/A')}"
    )
    
    # Display all combined fields at once
    st.write(row_display)


# Split the dataframe by levels (HSK1 to HSK5)
hsk1_df = df[df['Level'] == 'HSK 1']
hsk2_df = df[df['Level'] == 'HSK 2']
hsk3_df = df[df['Level'] == 'HSK 3']
hsk4_df = df[df['Level'] == 'HSK 4']
hsk5_df = df[df['Level'] == 'HSK 5']

# Create empty slots for each HSK level subsection
hsk1_section = st.empty()
hsk2_section = st.empty()
hsk3_section = st.empty()
hsk4_section = st.empty()
hsk5_section = st.empty()


while True:
    with hsk1_section:
        display_random_row(hsk1_df, "HSK 1")
    
    with hsk2_section:
        display_random_row(hsk2_df, "HSK 2")
    
    with hsk3_section:
        display_random_row(hsk3_df, "HSK 3")
    
    with hsk4_section:
        display_random_row(hsk4_df, "HSK 4")
    
    with hsk5_section:
        display_random_row(hsk5_df, "HSK 5")
    
    # Wait 10 seconds before refreshing all sections again
    time.sleep(10)
