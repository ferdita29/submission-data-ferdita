import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Load Dataset
setdata_hour = pd.read_csv("./data/hour.csv")
df = pd.read_csv("https://raw.githubusercontent.com/ferdita29/submission-data-ferdita/main/dashboard/all_data.csv")

# Convert date column to datetime
setdata_hour['dteday'] = pd.to_datetime(setdata_hour['dteday'])
df['dteday'] = pd.to_datetime(df['dteday'])

# Streamlit Layout
st.title("🚴Bike Sharing Dashboard")

# Sidebar Filters
with st.sidebar:
    st.image("BikeRental.jpg")
    st.header("🗓Filter Data")

    # Filter by Date Range
    start_date = st.date_input("Pilih Start Date", df['dteday'].min().date())
    end_date = st.date_input("Pilih End Date", df['dteday'].max().date())
    
    try:
        if start_date > end_date:
            st.warning("Start Date tidak boleh lebih besar dari End Date. Mohon periksa kembali.")
        else:
            filtered_df = df[(df['dteday'] >= pd.Timestamp(start_date)) & (df['dteday'] <= pd.Timestamp(end_date))]
            filtered_hour = setdata_hour[(setdata_hour['dteday'] >= pd.Timestamp(start_date)) & (setdata_hour['dteday'] <= pd.Timestamp(end_date))]
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
        filtered_df = df.copy()
        filtered_hour = setdata_hour.copy()
    
    # Filter by Working Day
    workingday_option = st.radio("Hari Kerja atau Libur?", ["Semua", "Hari Kerja", "Hari Libur"])
    if workingday_option == "Hari Kerja":
        filtered_df = filtered_df[filtered_df['workingday'] == 1]
    elif workingday_option == "Hari Libur":
        filtered_df = filtered_df[filtered_df['workingday'] == 0]
    
    # Filter by Season
    weather_mapping = {1: "Semi", 2: "Panas", 3: "Gugur", 4: "Dingin"}
    weather_option = st.multiselect("Kategori Musim", sorted(df['weathersit'].unique()),
                                    format_func=lambda x: weather_mapping.get(x, f"Cuaca {x}"))
    if weather_option:
        filtered_df = filtered_df[filtered_df['weathersit'].isin(weather_option)]

# Histogram - Distribusi Jumlah Peminjaman Sepeda
fig = px.histogram(filtered_df, x="cnt", nbins=30, title="Distribusi Jumlah Peminjaman Sepeda per Jam",
                   color_discrete_sequence=["#0D47A1"], opacity=0.7)
st.plotly_chart(fig)

# Line Chart - Peminjaman Sepeda Sepanjang Hari
hourly_counts = filtered_hour.groupby("hr", as_index=False)["cnt"].mean()
fig = px.bar(hourly_counts, x="hr", y="cnt", title="Peminjaman Sepeda per Jam dalam Sehari",
             labels={"hr": "Jam dalam Sehari", "cnt": "Rata-rata Jumlah Peminjaman"},
             color="cnt", color_continuous_scale="Blues")
st.plotly_chart(fig)

# Bar Chart - Tren Peminjaman Sepeda Berdasarkan Hari dalam Seminggu
fig = px.bar(filtered_hour, x="weekday", y="cnt", title="Rata-rata Peminjaman Sepeda Berdasarkan Hari",
             labels={"weekday": "Hari dalam Seminggu", "cnt": "Jumlah Peminjaman"},
             color="cnt", color_continuous_scale="Blues")
st.plotly_chart(fig)

# Line Chart - Perbandingan Pengguna Casual vs Registered
filtered_hourly_usage = filtered_hour.groupby("hr")[["casual", "registered"]].mean().reset_index()
fig = go.Figure()
fig.add_trace(go.Scatter(x=filtered_hourly_usage["hr"], y=filtered_hourly_usage["casual"],
                         mode='lines+markers', name='Casual Users', line=dict(color='red')))
fig.add_trace(go.Scatter(x=filtered_hourly_usage["hr"], y=filtered_hourly_usage["registered"],
                         mode='lines+markers', name='Registered Users', line=dict(color='blue')))
fig.update_layout(title="Perbandingan Peminjaman Sepeda: Casual vs Registered Users",
                  xaxis_title="Jam dalam Sehari", yaxis_title="Rata-rata Jumlah Peminjaman")
st.plotly_chart(fig)

st.subheader(" Conclusion")
st.write("""
###### Conclusion Pertanyaan 1:
- Distribusi jumlah peminjaman sepeda per jam menunjukkan pola yang cenderung tidak merata, dengan beberapa jam memiliki peminjaman yang jauh lebih tinggi dibandingkan lainnya. Grafik menunjukkan bahwa sebagian besar peminjaman berada pada jumlah tertentu, sementara ada juga beberapa jam dengan peminjaman yang sangat tinggi atau sangat rendah. Pola ini bisa mengindikasikan adanya jam-jam sibuk, seperti pagi atau sore hari saat orang berangkat dan pulang kerja.
- Peminjaman sepeda per jam dalam sehari cenderung rendah di pagi hari, mulai meningkat pada jam kerja (08:00 - 09:00), dan mencapai puncaknya pada sore hingga malam hari (17:00 - 19:00). Ini menunjukkan bahwa sepeda banyak digunakan untuk perjalanan kerja atau pulang kantor. Setelah jam malam, jumlah peminjaman kembali menurun.
- Peminjaman sepeda berdasarkan hari menunjukkan tren lebih tinggi pada hari kerja dibandingkan akhir pekan, mengindikasikan bahwa penggunaan sepeda lebih banyak untuk aktivitas rutin sehari-hari dibandingkan rekreasi.
""")

st.write("""
###### Conclusion Pertanyaan 2:
Grafik diatas dapat disimpulkan bahwa Pengguna terdaftar (registered) cenderung meminjam sepeda lebih banyak dibandingkan pengguna kasual (casual), terutama pada jam-jam sibuk seperti pagi dan sore hari, kemungkinan saat mereka pergi dan pulang kerja. Sementara itu, pengguna kasual lebih sering meminjam sepeda pada siang hingga sore hari, mungkin untuk rekreasi. Hal ini menunjukkan bahwa sepeda digunakan tidak hanya sebagai alat transportasi tetapi juga untuk aktivitas santai.
""")