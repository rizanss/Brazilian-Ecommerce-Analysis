import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

# Load data
order_delivery_satisfaction_df = pd.read_csv('./order_delivery_satisfaction_df.csv')
avg_popularity_product_df = pd.read_csv('./avg_popularity_product.csv')
products_order_df = pd.read_csv('./products_order_df.csv')
daily_orders_df = pd.read_csv('./daily_orders.csv')
monthly_orders_df = pd.read_csv('./monthly_orders.csv')

# Dashboard
st.title('Brazilian E-commerce Analysis Dashboard')

# Analisis Pertanyaan 1
st.header('Analisis Pertanyaan 1: Korelasi antara waktu pengiriman pesanan dan tingkat kepuasan pelanggan')
st.write("Korelasi antara waktu pengiriman pesanan dan tingkat kepuasan pelanggan sebesar -0.2001 menunjukkan adanya korelasi negatif yang lemah antara kedua variabel tersebut.")
st.write("Dari scatter plot tersebut, kita dapat melihat pola distribusi titik-titik data antara waktu pengiriman pesanan dan tingkat kepuasan pelanggan. Jika ada korelasi antara kedua variabel tersebut, kita dapat melihat pola linear atau non-linear yang menunjukkan hubungan antara waktu pengiriman dan tingkat kepuasan pelanggan.")
st.write("Namun, jika scatter plot menunjukkan pola yang acak dan tersebar secara merata, ini menunjukkan bahwa tidak ada hubungan yang jelas antara waktu pengiriman pesanan dan tingkat kepuasan pelanggan.")

fig = plt.figure(figsize=(8, 4))
plt.scatter(order_delivery_satisfaction_df['delivery_time'], order_delivery_satisfaction_df['review_score'], alpha=0.5)
plt.title('Korelasi antara Waktu Pengiriman Pesanan dan Tingkat Kepuasan Pelanggan')
plt.ylabel('Tingkat Kepuasan Pelanggan')
plt.xlabel('Waktu Pengiriman Pesanan (hari)')
plt.grid(True)
st.pyplot(fig)

# Analisis Pertanyaan 2
st.header('Analisis Pertanyaan 2: Rata-rata harga produk per kategori dan popularitas kategori')
st.write("Berikut adalah visualisasi rata-rata harga produk per kategori dan popularitas kategori berdasarkan jumlah produk yang terjual.")

fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(12, 10))

colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

# Subplot pertama: Bar plot untuk rata-rata harga produk per kategori
sns.barplot(data=avg_popularity_product_df.head(5), x='price', y='product_category_name_english', palette=colors, ax=ax1)
ax1.set_title('Rata-rata Harga Produk per Kategori')
ax1.set_xlabel('Kategori Produk')
ax1.set_ylabel('Harga Rata-rata Produk')

# Subplot kedua: Bar plot untuk popularitas kategori berdasarkan jumlah produk yang terjual
sns.barplot(data=avg_popularity_product_df.sort_values(by='product_id', ascending=False).head(5), x='product_id', y='product_category_name_english', palette=colors, ax=ax2)
ax2.set_title('Popularitas Kategori Berdasarkan Jumlah Produk yang Terjual')
ax2.set_xlabel('Jumlah Produk Terjual')
ax2.set_ylabel('Kategori Produk')

plt.tight_layout()
st.pyplot(fig)

st.write("Berdasarkan analisis ini, kita dapat menyarankan untuk lebih fokus pada kategori-kategori yang memiliki jumlah produk terjual tinggi namun harga produknya tidak terlalu tinggi. Selain itu, melakukan penyesuaian harga atau promosi pada kategori-kategori dengan harga tinggi namun jumlah produk terjual rendah dapat meningkatkan daya tarik bagi pelanggan.")

# Analisis Pertanyaan 3
st.header('Analisis Pertanyaan 3: Pola pembelian dalam seminggu')
st.write("Berikut adalah pola pembelian dalam seminggu berdasarkan jumlah pesanan.")

fig = plt.figure(figsize=(10, 6))
sns.barplot(data=daily_orders_df, x='Day of Week', y='Number of Orders', palette='viridis')
plt.title('Pola Pembelian dalam Seminggu')
plt.xlabel('Hari dalam Seminggu')
plt.ylabel('Jumlah Pesanan')
plt.xticks(rotation=45)
st.pyplot(fig)

st.write("Dari visualisasi, kita dapat melihat hari senin, selasa, dan rabu merupakan hari dimana pelanggan paling banyak membeli barang. Hal ini menunjukan bahwa hari tersebut memiliki jumlah pesanan yang lebih tinggi dibandingkan dengan hari yang lain.")
st.write("Perusahaan harus tetap memantau stok dan proses logistik mereka setiap hari untuk memastikan dapat mengakomodasi fluktuasi permintaan yang mungkin terjadi, namun diutamakan stok lebih banyak pada hari pembelian senin, selasa dan rabu dikarenakan permintaan yang tinggi pada hari tersebut.")
st.write("Analisis pola pembelian ini dapat menjadi dasar untuk merencanakan strategi pemasaran lanjutan, seperti penetapan harga produk, promosi, dan strategi pemasaran lainnya.")

# Analisis Pertanyaan 4

# Menggabungkan data dan mengatur kolom waktu sebagai indeks DataFrame
all_df = pd.merge(
    left=order_delivery_satisfaction_df,
    right=products_order_df[['order_id', 'product_id']],
    how='left',
    on='order_id'
)
all_df['order_purchase_timestamp'] = pd.to_datetime(all_df['order_purchase_timestamp'])
all_df.set_index('order_purchase_timestamp', inplace=True)

# Menghitung jumlah pesanan per bulan
monthly_orders = all_df.resample('M').size().reset_index()
monthly_orders.columns = ['Date', 'Number of Orders']

st.header('Analisis Pertanyaan 4: Tren penjualan bulanan')
st.write("Berikut adalah tren penjualan bulanan berdasarkan jumlah pesanan.")

fig = plt.figure(figsize=(12, 6))
sns.lineplot(data=monthly_orders, x='Date', y='Number of Orders', marker='o', color='blue')
plt.title('Tren Penjualan Bulanan')
plt.xlabel('Bulan')
plt.ylabel('Jumlah Pesanan')
plt.xticks(rotation=45)
plt.grid(True)
st.pyplot(fig)

st.write("Peningkatan penjualan yang signifikan pada bulan Desember 2017 dapat disebabkan oleh berbagai faktor, termasuk musim liburan dan perayaan seperti Natal dan Tahun Baru. Pelanggan cenderung melakukan pembelian lebih banyak untuk keperluan hadiah dan merayakan liburan.")
st.write("Bulan Februari 2018 juga menunjukkan peningkatan penjualan yang cukup besar. Ini mungkin disebabkan oleh perayaan Hari Valentine atau faktor musiman lainnya yang mendorong konsumen untuk melakukan pembelian tambahan.")
st.write("Berdasarkan tren penjualan yang ditemukan, perusahaan dapat merencanakan strategi pemasaran yang lebih efektif untuk mengoptimalkan penjualan di masa depan. Misalnya, mereka dapat meningkatkan promosi atau menawarkan diskon khusus selama periode puncak penjualan seperti bulan Desember dan Februari.")