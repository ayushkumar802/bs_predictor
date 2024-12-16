# import matplotlib.pyplot as plt
# import streamlit as st
# import seaborn.colors as snsc
# import helper
# import preprocessor
# import pandas as pd
# import numpy as np
# import seaborn as sns
#
# st.sidebar.title('Small-Big Analysis')
# w = list(snsc.crayons.values())
# o = list(snsc.xkcd_rgb.values())
# df = st.sidebar.file_uploader('Upload your Data in CSV format', type="csv")
# if df is not None:
#     df = pd.read_csv(df)
#     # st.dataframe(df)
#
# st.sidebar.subheader('Select the option')
# days = st.sidebar.selectbox('Choose one',
#                             ('All days', 'Last 10 days', 'Last 7 days', 'Any Particular Day', 'Any Particular Weekday'))
# abc = None
# if days == 'Any Particular Day':
#     temp = list(df.columns[2:])
#     temp.insert(0, 'Select Date')
#     abc = st.sidebar.selectbox('Choose a day', (temp))
# if days == 'Any Particular Weekday':
#     abc = st.sidebar.selectbox('Choose day', (
#     'Select Weekday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'))
#
# st.sidebar.subheader('Select a Time Duration')
# start_ = st.sidebar.selectbox("Select Start time:", (
# None, '00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18',
# '19', '20', '21', '22', '23'))
# end_ = st.sidebar.selectbox("Select End time:", (
# None, '00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18',
# '19', '20', '21', '22', '23'))
# if df is not None:
#     df = preprocessor.preprocessor(df, days, abc, start_, end_)
#     st.title('Pattern Analysis')
#     pattern = st.text_input('Make a Pattern:')
#     st.write("Note: Make pattern in only 'S' & 'B', else it throw error")
#
#     if pattern:
#
#         inv = ""
#         for i in pattern:
#             if i == "B":
#                 inv += "S"
#             elif i == "S":
#                 inv += "B"
#         st.subheader("Analysis on: " + pattern)

import matplotlib.pyplot as plt
import streamlit as st
import seaborn.colors as snsc
import helper
import preprocessor
import pandas as pd
import numpy as np
import seaborn as sns

st.sidebar.title('Small-Big Analysis')
w = list(snsc.crayons.values())
o = list(snsc.xkcd_rgb.values())

# Caching Data Load
@st.cache_data
def load_data(file):
    return pd.read_csv(file)

# File Upload
df = st.sidebar.file_uploader('Upload your Data in CSV format', type="csv")
if df is not None:
    df = load_data(df)

st.sidebar.subheader('Select the option')
days = st.sidebar.selectbox(
    'Choose one',
    ('All days', 'Last 10 days', 'Last 7 days', 'Any Particular Day', 'Any Particular Weekday')
)
abc = None
if days == 'Any Particular Day':
    temp = list(df.columns[2:])
    temp.insert(0, 'Select Date')
    abc = st.sidebar.selectbox('Choose a day', (temp), key='specific_day')
if days == 'Any Particular Weekday':
    abc = st.sidebar.selectbox(
        'Choose day',
        ('Select Weekday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'),
        key='specific_weekday'
    )

st.sidebar.subheader('Select a Time Duration')
start_ = st.sidebar.selectbox(
    "Select Start time:",
    (None, *[f'{i:02}' for i in range(24)]),
    key='start_time'
)
end_ = st.sidebar.selectbox(
    "Select End time:",
    (None, *[f'{i:02}' for i in range(24)]),
    key='end_time'
)

if df is not None:
    # Preprocess Data
    df = preprocessor.preprocessor(df, days, abc, start_, end_)

    st.title('Pattern Analysis')
    pattern = st.text_input('Make a Pattern:')
    st.write("Note: Make pattern in only 'S' & 'B', else it will throw an error")

    if pattern:
        inv=""
        for i in pattern:
            if i == "B":
                inv += "S"
            elif i == "S":
                inv += "B"
        st.subheader(f"Analysis on: {pattern}")
        # (Rest of your visualization and analysis code here)

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(helper.pattern_table1(df, pattern))
        with col2:
            st.dataframe(helper.pattern_table2(df, pattern))

        # ---------------------------------------------Inverse Pattern Analysis----------------------------------------------

        st.subheader("Analysis on: " + inv + " (inverse)")
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(helper.pattern_table1(df, inv))
        with col2:
            st.dataframe(helper.pattern_table2(df, inv))

        #-------------------------------------------------Pattern Round Analysis---------------------------------------------

        prob_df = helper.prob_table(df, pattern)
        prob_df_inv = helper.prob_table(df, inv)
        if prob_df is not None:
            st.subheader("Round Analysis")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"Pattern: {pattern}")
                st.table(prob_df)
            with col2:
                if prob_df_inv is not None:
                    st.write(f"Pattern: {inv}")
                    st.table(prob_df_inv)


        #------------------------------------------------24 analysis-------------------------------------------------------
        st.subheader('24hr Analysis')
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            pattern_1 = st.selectbox('Selected Pattern', (pattern, inv),key="pattern_11")
        a = helper.analysis_24H(df, pattern_1)
        if a is not None:

            fig, ax = plt.subplots(figsize=(10, 4.6))
            ax.bar(a['period'], a[0], color=w, width=0.5)
            for i, value in enumerate(a[0]):
                plt.text(i, value + 0.02,
                         str(value),
                         ha='center',
                         va='bottom',
                         color=(0, 0, 0, 0.6))
            plt.xticks(rotation="vertical")
            plt.show()
            st.pyplot(fig)
        else:
            st.write("No Data!!")


        #---------------------------------------------Day count of a Pattern-------------------------------------------------

        if days in ['All days', 'Last 10 days', 'Last 7 days', 'Any Particular Weekday']:
            st.subheader("Pattern Count per Day")
            abc = helper.pattern_bar(df, pattern)
            fig, ax = plt.subplots(figsize=(9, 4))
            p = np.arange(len(df.columns[1:]))
            width = 0.4
            p1 = [i + width + 0.03 for i in p]
            bar1 = ax.bar(p, abc.iloc[:, 1], width, color=["#9F8170"], label=abc.iloc[:, 1].name)
            for bar in bar1:
                plt.text(bar.get_x() + 0.23, bar.get_height() + 0.02,
                         str(bar.get_height()),
                         color=(0, 0, 0, 0.6),
                         ha='center',
                         va='bottom')
            bar2 = ax.bar(p1, abc.iloc[:, 2], width, color=["#FD7C6E"], label=abc.iloc[:, 2].name)
            for bar in bar2:
                plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                         str(bar.get_height()),
                         color=(0, 0, 0, 0.6),
                         ha='center',
                         va='bottom')
            plt.xticks(p + width / 2, df.columns[1:], rotation="vertical")
            plt.legend()
            st.pyplot(fig)

        #-----------------------------------------------heat map----------------------------------------------------

        if days in ['All days', 'Last 10 days', 'Last 7 days']:

            st.subheader("24hr vs Week Heatmap")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                pattern_1 = st.selectbox('Selected Pattern', (pattern, inv),key='pattern_2')
            pivot_table = helper.analysis_week(df, pattern_1)
            plt.figure(figsize=(10, 4.5))
            sns.heatmap(pivot_table, annot=True, cmap="coolwarm", cbar_kws={'label': 'num'})
            st.pyplot(plt)



        #--------------------------------------------Popular Patterns Analysis---------------------------------------

        st.subheader('Popular Patterns Analysis')
        abc = helper.popular_patterns(df)
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<br>",unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            fig, ax = plt.subplots(figsize=(5, 6))
            ax.pie(abc['Counts'], labels=abc['Patterns'], explode=[0.02 for _ in range(abc.shape[0])],
                   autopct="%0.2f%%",colors=w)
            plt.legend(title='Patterns',loc="center left",bbox_to_anchor=(1,0.5))
            st.pyplot(fig)

        with col2:
            st.table(abc)

