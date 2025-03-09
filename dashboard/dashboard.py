import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Dataset
df = pd.read_csv("https://raw.githubusercontent.com/ferdita29/submission-data-ferdita/main/dashboard/all_data.csv")

# Convert date column to datetime
df['dteday'] = pd.to_datetime(df['dteday'])

# Copy dataset
setdata_hour = df.copy()

# Streamlit Layout
st.title("🚴Bike Sharing Dashboard")
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

# Mapping musim
weather_mapping = {1: "Semi", 2: "Panas", 3: "Gugur", 4: "Dingin"}
weather_option = st.sidebar.multiselect("Kategori Musim", sorted(df['weathersit'].unique()), format_func=lambda x: weather_mapping.get(x, f"Cuaca {x}"))
if weather_option:
    filtered_df = filtered_df[filtered_df['weathersit'].isin(weather_option)]

# Distribusi jumlah Peminjaman Sepeda Per Jam
st.subheader("Distribusi Jumlah Peminjaman Sepeda per Jam")
plt.figure(figsize=(8, 4))
sns.histplot(setdata_hour["cnt"], bins=30, kde=True, color="#0D47A1")
plt.xlabel("Jumlah Peminjaman")
plt.ylabel("Frekuensi")
st.pyplot(plt.gcf())

# Peminjaman sepeda sepanjang hari
st.subheader("Peminjaman Sepeda per Jam dalam Sehari")
plt.figure(figsize=(10, 5))
hourly_counts = setdata_hour.groupby("hr", as_index=False)["cnt"].mean()
max_val = hourly_counts["cnt"].max()
colors = ["#0D47A1" if cnt == max_val else "#BBDEFB" for cnt in hourly_counts["cnt"]]
plt.bar(hourly_counts["hr"], hourly_counts["cnt"], color=colors)
plt.xticks(range(0, 24), [f"{i}:00" for i in range(0, 24)], rotation=45)
plt.xlabel("Jam dalam Sehari")
plt.ylabel("Rata-rata Jumlah Peminjaman")
st.pyplot(plt.gcf())

# Tren peminjaman sepeda berdasarkan hari dalam seminggu
st.subheader("Rata-rata Peminjaman Sepeda Berdasarkan Hari")
plt.figure(figsize=(8, 4))
sns.barplot(x="weekday", y="cnt", data=setdata_hour, dodge=False, legend=False)
plt.xticks(ticks=range(7), labels=['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'])
plt.xlabel("Hari dalam Seminggu")
plt.ylabel("Jumlah Peminjaman")
st.pyplot(plt.gcf())

# Perbandingan pengguna kasual vs terdaftar
st.subheader("Perbandingan Peminjaman Sepeda: Casual vs Registered Users")
hourly_usage = setdata_hour.groupby("hr")[["casual", "registered"]].mean()
plt.figure(figsize=(10, 5))
sns.lineplot(x=hourly_usage.index, y=hourly_usage["casual"], marker="o", label="Casual Users", color="red")
sns.lineplot(x=hourly_usage.index, y=hourly_usage["registered"], marker="o", label="Registered Users", color="blue")
plt.xticks(ticks=range(0, 24), labels=[f"{i}:00" for i in range(0, 24)], rotation=45)
plt.xlabel("Jam dalam Sehari")
plt.ylabel("Rata-rata Jumlah Peminjaman")
st.pyplot(plt.gcf())

# Conclusion
st.subheader("Conclusion")
st.write("""
**1. Distribusi Peminjaman Sepeda**:
- Peminjaman tertinggi terjadi pada sore hari (17:00 - 19:00), kemungkinan saat pulang kerja.
- Pola peminjaman lebih tinggi pada hari kerja dibandingkan akhir pekan.

**2. Perbandingan Casual vs Registered Users**:
- Pengguna terdaftar meminjam lebih banyak di jam sibuk (pagi dan sore), sedangkan pengguna kasual cenderung siang hingga sore.
""")