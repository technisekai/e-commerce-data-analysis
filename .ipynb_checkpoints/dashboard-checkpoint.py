import pandas as pd
import plotly.express as px
import warnings
import streamlit as st
warnings.filterwarnings('ignore')

final_df = pd.read_csv('dataset/clean_dataset.csv')
final_df['date_order'] = pd.to_datetime(final_df['date_order'])

st.header('E-Commerce Analysis by Widi Afandi')
st.caption('Untuk menyelesaikan kelas Data Analisis untuk Pemula')

st.title('Jumlah Transaksi Per Hari')
# besaran transaksi
# Jumlah Transaksi Per Hari
col1, col2 = st.columns([4, 1])
fig_sold_product = px.area(
    final_df.groupby(['date_order']).count(),
    labels = {
        'date_order': 'Tanggal Pesanan',
        'order_id': 'Jumlah Transaksi'
    },
    title='Jumlah Transaksi per Hari dari 2016 - 2018',
    y='order_id'
    )
fig_sold_product.update_layout(showlegend=False)
fig_sold_product.update_traces(line_color='#19A7CE')
# Plot!
col1.plotly_chart(fig_sold_product, use_container_width=True)
col2.caption('Rata-rata transaksi berada dalam rentang minimal 1 dan paling tinggi 429 transaksi. Namun, di tanggal 24 November 2017 terjadi lonjakan transaksi hingga 300% dari biasanya')

st.title('Top Seller & Kategori Produk Terfavorit')
st.caption('Top seller dan produk terlaris di E-commerce')
# Produk terlaris
fig_product = px.bar(
    final_df['product_name'].value_counts()[:5],
    labels = {
        'index': 'Kategori Produk',
        'value': 'Jumlah Terjual'
    },
    title='Top 5 Kategori Produk Terlaris di E-commerce',
    )
fig_product.update_traces(marker_color='#1B9C85')
fig_product.update_layout(showlegend=False) 
# Seller terlaris
fig_seller = px.bar(
    final_df['seller_id'].value_counts()[:5],
    labels = {
        'index': 'Seller ID',
        'value': 'Produk Terjual'
    },
    title='Top 5 Seller ID Terlaris di E-commerce',
    color=final_df['seller_id'].value_counts()[:5].index
    )
fig_seller.update_traces(marker_color='#068DA9')
fig_seller.update_layout(showlegend=False) 
fig_seller.update_xaxes(tickangle=30)
# plot
col1, col2 = st.columns(2)
col1.plotly_chart(fig_product, use_container_width=True)
col2.plotly_chart(fig_seller, use_container_width=True)

# rfm analysis
rfm_df = final_df.groupby(by="customer_id", as_index=False).agg({
    "date_order": "max", 
    "order_id": "nunique", 
    "price": "sum" 
})
rfm_df.columns = ["customer_id", "max_order_date", "frequency", "monetary"]
recent_date = final_df["date_order"].max() # mencari tahu kapan customer id terakhir kali melakukan transaksi
rfm_df["recency"] = rfm_df["max_order_date"].apply(lambda x: (recent_date - x).days) # kalkulasi sudah berapa lama pelanggan tidak melakukan transaksi
rfm_df.drop("max_order_date", axis=1, inplace=True)

st.title('Customer yang Layak Mendapatkan Berbagai Kupon dari E-Commerce')
st.caption('Berdasarkan RFM analysis di dapatkan daftar Customer yang Terakhir Melakukan Transaksi dan dengan Transaksi yang Besar')
# besaran transaksi
fig_monetary = px.bar(
    rfm_df.sort_values(by=['monetary'])[-5:], 
    title='Top 5 Customer ID dengan Transaksi Terbesar',
    x='customer_id',
    y='monetary'
)
fig_monetary.update_traces(marker_color=['gray', 'gray', '#FFB84C', '#FFB84C', '#FFB84C'])
fig_monetary.update_layout(showlegend=False) 
fig_monetary.update_xaxes(tickangle=30)
# terakhir transaksi
fig_recency = px.bar(
    rfm_df.sort_values(by=['recency'])[:5], 
    title='Top 5 Customer ID dengan Recency Paling Sedikit',
    x='customer_id',
    y='recency'
)
fig_recency.update_traces(marker_color=['#FFB84C', '#FFB84C', '#FFB84C', 'gray', 'gray'])
fig_recency.update_layout(showlegend=False)
fig_recency.update_xaxes(tickangle=30)
# plot
col1, col2 = st.columns(2)
col1.plotly_chart(fig_monetary, use_container_width=True)
col2.plotly_chart(fig_recency, use_container_width=True)


def is_puas(star):
  if star > 3:
    return 'puas'
  if star < 3:
    return 'tidak_puas'
  return 'netral'
st.title('Kepuasan Terhadap E-Commerce')
st.caption('Kepuasan customer terhadap E-Commerce berdasarkan review yang diberikan kepada barang yang dibeli')
# besaran transaksi
final_df['kepuasan'] = final_df['review_score'].apply(is_puas)
count1 = final_df["kepuasan"].value_counts()
dff = pd.DataFrame()
dff["name"]=[str(i) for i in count1.index]
dff["number"] = count1.values
fig_kepuasan = px.pie(dff, values="number", names="name", title='Tingkat Kepuasan Customer')
st.plotly_chart(fig_kepuasan, use_container_width=True)