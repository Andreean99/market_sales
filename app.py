import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import plotly.express as px
from PIL import Image

st.set_page_config(
    page_title="Supermarket Sales",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.google.com',
        'Report a bug': "https://github.com/Andreean99?tab=repositories",
        'About': " Visualisasi dan Hipotesis Testing Supermarket Sales Milestone 1"
    }
)


st.sidebar.title('Select a Page')
selected = st.sidebar.selectbox('Page:', ['Data Visualisasi', 'Hipotesis Testing'])


if selected == 'Data Visualisasi':
    st.title('Data Visualisasi')

    PAYMENT_COLUMN = 'payment'
    PRODUCT_COLUMN = 'product line'
    TOTAL_COLUMN = 'total'
    GENDER_COLUMN = 'gender'
    GROSS_INCOME_COLUMN = 'gross income'
    CITY_COLUMN = 'city'
    DATE_COLUMN = 'date'
    TIME_COLUMN = 'time'
    CUSTOMER_TYPE_COLUMN = 'customer type'
    DATA_URL = ('supermarket_sales - Sheet1.csv')


    @st.cache_data
    def load_data(nrows):
        data = pd.read_csv(DATA_URL, nrows=nrows)
        lowercase = lambda x: str(x).lower()
        data.rename(lowercase, axis='columns', inplace=True)
        data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
        return data
    
    data_load_state = st.text('Loading data...')
    data = load_data(10000)
    data_load_state.text("Done! (using st.cache)")

    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.write(data)


    st.subheader('Sebaran data gross income tiap kota')
    selected_city=st.selectbox('Pilih Kota', options=('Yangon', 'Naypyitaw', 'Mandalay'))
    fig1, ax1= plt.subplots(figsize=[8,5])
    sns.histplot(data[data[CITY_COLUMN]==selected_city][GROSS_INCOME_COLUMN])
    st.pyplot(fig1)

    average_yangon = data[data[CITY_COLUMN]=='Yangon'][[DATE_COLUMN,'gross income']].groupby(DATE_COLUMN).sum() 
    average_naypyitaw = data[data[CITY_COLUMN]=='Naypyitaw'][[DATE_COLUMN,'gross income']].groupby(DATE_COLUMN).sum()
    average_mandalay = data[data[CITY_COLUMN]=='Mandalay'][[DATE_COLUMN,'gross income']].groupby(DATE_COLUMN).sum()
  
    st.subheader('Rata - rata Gross Income harian Yangon')
    st.line_chart(average_yangon)
    st.subheader('Rata - rata Gross Income harian Naypyitaw')
    st.line_chart(average_naypyitaw)
    st.subheader('Rata - rata Gross Income harian Mandalay')
    st.line_chart(average_mandalay)

    st.subheader('Total Pendapatan tiap kota')    
    tipe = data.groupby(CITY_COLUMN)[TOTAL_COLUMN].sum()
    st.bar_chart(tipe)


    st.subheader('Jumlah pelanggan berdasarkan Gender')
    gen = data[GENDER_COLUMN].value_counts()
    st.bar_chart(gen)

    st.subheader('Jumlah tipe pelanggan berdasarkan gender')
    selected_type = st.radio(label='Pilih Gender', options=data[GENDER_COLUMN].unique())
    st.write('Female = Member : 261, Normal : 240')
    st.write('Male = Normal : 259, Member : 240 ')
    fig2, ax2= plt.subplots(figsize=[8,5])
    sns.histplot(data[data[GENDER_COLUMN]==selected_type][CUSTOMER_TYPE_COLUMN])
    st.pyplot(fig2)

    st.subheader('Total pembayaran berdasarkan Gender')
    st.write('Total pembayaran Female 167882, sedangkan Male 155083')
    gender_total = data.groupby(GENDER_COLUMN)[TOTAL_COLUMN].sum()
    fig3, ax3 = plt.subplots(figsize=[8,5])
    sns.barplot(x=gender_total.index,y=gender_total,orient='v')
    st.pyplot(fig3)


    



else :
    st.title('Hipotesis Testing')

    st.write('Berdasarkan hasil pengujian Hipotesis Testing, didapatkan p-value sebesar 0.5762514561129986 yang mana lebih besar dari alpha 0.05. Maka disimpulkan dengan rentang kepercayaan 95%, rata-rata gross income harian Yangon secara signifikan hampir sama dengan rata-rata gross income harian Naypyitaw, maka di simpulkan bahwa H0 gagal di tolak.')
    
    img = Image.open('hipotesis.png')

    st.subheader('H0 : μ Gross Income Yangon   =  Gross Income Mandalay')
    st.subheader('H1 : μ Gross Income Yangon  !=  Gross Income Mandalay')

    st.header('Plot Hipotesis testing')
    st.image(img, caption='Hipotesis Testing', width=400, use_column_width=True)

    
    st.write('Untuk pembuktian hipotesis testing pada gambar di atas bisa dilihat garis confidence interval berada diluar garis alternate hypotesis maka bisa di katakan bahwa H0 gagal di tolak dan bisa dikatakan μ gross income harian Yangon secara signifikan hampir sama dengan μ gross income harian Naypyitaw ')
 
