import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Dataset
setdata_hour = pd.read_csv("data/hour.csv")
df = pd.read_csv("https://raw.githubusercontent.com/ferdita29/submission-data-ferdita/main/dashboard/all_data.csv")

# Convert date column to datetime
setdata_hour['dteday'] = pd.to_datetime(setdata_hour['dteday'])
df['dteday'] = pd.to_datetime(df['dteday'])

# Streamlit Layout
st.title("🚴Bike Sharing Dashboard")
# Sidebar
with st.sidebar:
    st.image("BikeRental.jpg")
    st.header("🗓Filter Data")

    # Filter dataset 'setdata_hour' sesuai dengan filter di sidebar
    filtered_hour = setdata_hour.copy()
    
    # Filter by Year
    year_option = st.selectbox("Pilih Tahun", df['yr'].unique(), format_func=lambda x: f"{2011 + x}")
    filtered_df = df[df['yr'] == year_option]

    # Filter by Month
    month_option = st.multiselect("Pilih Bulan", sorted(df['mnth'].unique()), format_func=lambda x: f"Bulan {x}")
    if month_option:
        filtered_df = filtered_df[filtered_df['mnth'].isin(month_option)]

    # Filter by Working Day
    workingday_option = st.radio("Hari Kerja atau Libur?", ["Semua", "Hari Kerja", "Hari Libur"])
    if workingday_option == "Hari Kerja":
        filtered_df = filtered_df[filtered_df['workingday'] == 1]
    elif workingday_option == "Hari Libur":
        filtered_df = filtered_df[filtered_df['workingday'] == 0]

    # Mapping untuk mengganti angka dengan deskripsi Musim
    weather_mapping = {1: "Semi", 2: "Panas", 3: "Gugur", 4: "Dingin"}
    weather_option = st.multiselect(
        "Kategori Musim",
        sorted(df['weathersit'].unique()),
        format_func=lambda x: weather_mapping.get(x, f"Cuaca {x}")
    )
    if weather_option:
        filtered_df = filtered_df[filtered_df['weathersit'].isin(weather_option)]

# Bar chart - Distribusi jumlah Peminjaman Sepeda Per Jam
fig, ax = plt.subplots()
sns.histplot(filtered_df["cnt"], bins=30, kde=True, color="#0D47A1", ax=ax)
ax.set_title("Distribusi Jumlah Peminjaman Sepeda per Jam")
ax.set_xlabel("Jumlah Peminjaman")
ax.set_ylabel("Frekuensi")
st.pyplot(fig)


# Bar chart - Peminjaman sepeda sepanjang hari
st.subheader("Peminjaman Sepeda per Jam dalam Sehari")
fig, ax = plt.subplots(figsize=(12, 6))
sns.set_style("whitegrid")
hourly_counts = setdata_hour.groupby("hr", as_index=False)["cnt"].mean()
max_val = hourly_counts["cnt"].max()
ax.bar(hourly_counts["hr"], hourly_counts["cnt"], 
       color=["#0D47A1" if cnt == max_val else "#BBDEFB" for cnt in hourly_counts["cnt"]])
ax.set_xticks(range(0, 24))
ax.set_xticklabels([f"{i}:00" for i in range(0, 24)], rotation=45)
ax.set_xlabel("Jam dalam Sehari")
ax.set_ylabel("Rata-rata Jumlah Peminjaman")
ax.set_title("Peminjaman Sepeda per Jam dalam Sehari")
st.pyplot(fig)

# Bar chart - Tren Peminjaman sepeda berdasarkan hari dalam seminggu
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x="weekday", y="cnt", hue="weekday", data=filtered_hour, 
            palette=["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3"], 
            dodge=False, legend=False, ax=ax)
ax.set_xlabel("Hari dalam Seminggu")
ax.set_ylabel("Jumlah Peminjaman")
ax.set_title("Rata-rata Peminjaman Sepeda Berdasarkan Hari")

if filtered_hour["weekday"].nunique() == 7:
    ax.set_xticks(range(7))
    ax.set_xticklabels(['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'])
st.pyplot(fig)


# Line Chart - Perbandingan peminjaman antara pengguna kasual dan terdaftar
filtered_hourly_usage = filtered_hour.groupby("hr")[["casual", "registered"]].mean()
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x=filtered_hourly_usage.index, y=filtered_hourly_usage["casual"], marker="o", label="Casual Users", color="red", ax=ax)
sns.lineplot(x=filtered_hourly_usage.index, y=filtered_hourly_usage["registered"], marker="o", label="Registered Users", color="blue", ax=ax)
ax.set_xticks(range(0, 24))
ax.set_xticklabels([f"{i}:00" for i in range(0, 24)], rotation=45)
ax.set_xlabel("Jam dalam Sehari")
ax.set_ylabel("Rata-rata Jumlah Peminjaman")
ax.set_title("Perbandingan Peminjaman Sepeda: Casual vs Registered Users")
ax.legend()
st.pyplot(fig)


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