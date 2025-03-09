import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Dataset
setdata_hour = pd.read_csv("hour.csv")
df = pd.read_csv("https://raw.githubusercontent.com/ferdita29/submission-data-ferdita/main/dashboard/all_data.csv")

# Convert date column to datetime
setdata_hour['dteday'] = pd.to_datetime(setdata_hour['dteday'])
df['dteday'] = pd.to_datetime(df['dteday'])

# Streamlit Layout
st.title("🚴Bike Sharing Dashboard")
#Menambahkan logo
st.sidebar.header("🗓Filter Data")
st.image("BikeRental.jpg")

# Filter by Year
year_option = st.sidebar.selectbox("Pilih Tahun", df['yr'].unique(), format_func=lambda x: f"{2011 + x}")
filtered_df = df[df['yr'] == year_option]

# Filter by Month
month_option = st.sidebar.multiselect("Pilih Bulan", sorted(df['mnth'].unique()), format_func=lambda x: f"Bulan {x}")
if month_option:
    filtered_df = filtered_df[filtered_df['mnth'].isin(month_option)]

# Filter by Working Day
workingday_option = st.sidebar.radio("Hari Kerja atau Libur?", ["Semua", "Hari Kerja", "Hari Libur"])
if workingday_option == "Hari Kerja":
    filtered_df = filtered_df[filtered_df['workingday'] == 1]
elif workingday_option == "Hari Libur":
    filtered_df = filtered_df[filtered_df['workingday'] == 0]

# Mapping untuk mengganti angka dengan deskripsi Musim
weather_mapping = {
    1: "Semi",
    2: "Panas",
    3: "Gugur",
    4: "Dingin"
}
# Menambahkan sidebar filter berdasarkan kondisi musim
weather_option = st.sidebar.multiselect(
    "Kategori Musim",
    sorted(df['weathersit'].unique()), 
    format_func=lambda x: weather_mapping.get(x, f"Cuaca {x}")  # Mengubah angka jadi teks
)
# Filter DataFrame berdasarkan pilihan musim
if weather_option:
    filtered_df = filtered_df[filtered_df['weathersit'].isin(weather_option)]

# Bar chart - Distribusi jumlah Peminjaman Sepeda Per Jam
sns.histplot(setdata_hour["cnt"], bins=30, kde=True, color="#0D47A1" )
plt.title("Distribusi Jumlah Peminjaman Sepeda per Jam")
plt.xlabel("Jumlah Peminjaman")
plt.ylabel("Frekuensi")
plt.show()

# Bar chart - Peminjaman sepeda sepanjang hari
plt.figure(figsize=(12, 6))
sns.set_style("whitegrid")
# Menghitung rata-rata peminjaman per jam
hourly_counts = setdata_hour.groupby("hr", as_index=False)["cnt"].mean()
# Menentukan jam dengan peminjaman tertinggi
max_val = hourly_counts["cnt"].max()
# Membuat bar chart secara manual dengan warna yang ditentukan
bars = plt.bar(hourly_counts["hr"], hourly_counts["cnt"], 
               color=["#0D47A1" if cnt == max_val else "#BBDEFB" for cnt in hourly_counts["cnt"]])
# Menyesuaikan label sumbu x
plt.xticks(ticks=range(0, 24), labels=[f"{i}:00" for i in range(0, 24)], rotation=45)
plt.xlabel("Jam dalam Sehari")
plt.ylabel("Rata-rata Jumlah Peminjaman")
plt.title("Peminjaman Sepeda per Jam dalam Sehari")
plt.show()

# Bar chart - Tren Peminjaman sepeda berdasarkan hari dalam seminggu
plt.figure(figsize=(10, 5))
# Menambahkan hue agar palette bisa digunakan tanpa warning
sns.barplot(x="weekday", y="cnt", hue="weekday", data=setdata_hour, 
            palette=["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3"], 
            dodge=False, legend=False)
plt.xlabel("Hari dalam Seminggu")
plt.ylabel("Jumlah Peminjaman")
plt.title("Rata-rata Peminjaman Sepeda Berdasarkan Hari")
# Pastikan weekday berisi angka 0-6 sebelum mengganti labelnya
if setdata_hour["weekday"].nunique() == 7:
    plt.xticks(
        ticks=range(7),  # Memastikan label sesuai dengan jumlah hari
        labels=['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu']
    )
plt.show()

# Line Chart - Perbandingan peminjaman antara pengguna kasual dan terdaftar
hourly_usage = setdata_hour.groupby("hr")[["casual", "registered"]].mean()

plt.figure(figsize=(12, 6))
sns.lineplot(x=hourly_usage.index, y=hourly_usage["casual"], marker="o", label="Casual Users", color="red")
sns.lineplot(x=hourly_usage.index, y=hourly_usage["registered"], marker="o", label="Registered Users", color="blue")

plt.xticks(ticks=range(0, 24), labels=[f"{i}:00" for i in range(0, 24)], rotation=45)
plt.xlabel("Jam dalam Sehari")
plt.ylabel("Rata-rata Jumlah Peminjaman")
plt.title("Perbandingan Peminjaman Sepeda: Casual vs Registered Users")
plt.legend()
plt.show()

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