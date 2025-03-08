import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Dataset
df = pd.read_csv("https://raw.githubusercontent.com/ferdita29/submission-data-ferdita/main/dashboard/all_data.csv")

# Convert date column to datetime
df['dteday'] = pd.to_datetime(df['dteday'])

# Streamlit Layout
st.title("🚴Bike Sharing Dashboard")
st.sidebar.header("🗓Filter Data")

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
    "Kondisi Musim",
    sorted(df['weathersit'].unique()), 
    format_func=lambda x: weather_mapping.get(x, f"Cuaca {x}")  # Mengubah angka jadi teks
)
# Filter DataFrame berdasarkan pilihan cuaca
if weather_option:
    filtered_df = filtered_df[filtered_df['weathersit'].isin(weather_option)]

# Bar chart - Distribusi jumlah Peminjaman Sepeda Per Jam
plt.figure(figsize=(12, 6))
sns.histplot(filtered_df["cnt"], bins=30, kde=True, color="blue")
plt.title("Distribusi Jumlah Peminjaman Sepeda per Jam")
plt.xlabel("Jumlah Peminjaman")
plt.ylabel("Frekuensi")
st.pyplot(plt)

# Bar chart - Peminjaman sepeda sepanjang hari
plt.figure(figsize=(12, 6))
sns.set_style("whitegrid")
hourly_counts = filtered_df.groupby("hr", as_index=False)["cnt"].mean()
sns.barplot(x="hr", y="cnt", hue="hr", data=hourly_counts, palette="coolwarm", dodge=False)

# Menyesuaikan label sumbu x
plt.xticks(ticks=range(0, 24), labels=[f"{i}:00" for i in range(0, 24)], rotation=45)
plt.xlabel("Jam dalam Sehari")
plt.ylabel("Rata-rata Jumlah Peminjaman")
plt.title("Peminjaman Sepeda per Jam dalam Sehari")
plt.legend([], [], frameon=False)  # Sembunyikan legend agar tidak redundant
st.pyplot(plt)

# Bar chart - Tren Peminjaman sepeda berdasarkan hari dalam seminggu
plt.figure(figsize=(10, 5))
# Gunakan hue="weekday" agar palette dapat diterapkan tanpa warning
sns.barplot(x="weekday", y="cnt", hue="weekday", data=filtered_df, palette="coolwarm", dodge=False)
plt.xlabel("Hari dalam Seminggu")
plt.ylabel("Jumlah Peminjaman")
plt.title("Rata-rata Peminjaman Sepeda Berdasarkan Hari")

# Pastikan weekday berisi angka 0-6 sebelum mengganti labelnya
if filtered_df["weekday"].nunique() == 7:
    plt.xticks(
        ticks=range(7),  # Memastikan label sesuai dengan jumlah hari
        labels=['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu']
    )
plt.legend([], [], frameon=False)  # Sembunyikan legend agar tidak redundant
st.pyplot(plt)

# Line Chart - Perbandingan peminjaman antara pengguna kasual dan terdaftar
hourly_usage = filtered_df.groupby("hr")[["casual", "registered"]].mean()

plt.figure(figsize=(12, 6))
sns.lineplot(x=hourly_usage.index, y=hourly_usage["casual"], marker="o", label="Casual Users", color="r")
sns.lineplot(x=hourly_usage.index, y=hourly_usage["registered"], marker="o", label="Registered Users", color="b")

plt.xticks(ticks=range(0, 24), labels=[f"{i}:00" for i in range(0, 24)], rotation=45)
plt.xlabel("Jam dalam Sehari")
plt.ylabel("Rata-rata Jumlah Peminjaman")
plt.title("Perbandingan Peminjaman Sepeda: Casual vs Registered Users")
plt.legend()
st.pyplot(plt)

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