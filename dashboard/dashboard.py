import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Dataset
df = pd.read_csv("https://raw.githubusercontent.com/ferdita29/submission-data-ferdita/main/data/hour.csv")

# Convert date column to datetime
df['dteday'] = pd.to_datetime(df['dteday'])

# Streamlit Layout
st.title("🚴 Bike Sharing Dashboard")
st.sidebar.header("🔍 Filter Data")

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

# Filter by Weather Condition
weather_option = st.sidebar.multiselect("Kondisi Cuaca", sorted(df['weathersit'].unique()), format_func=lambda x: f"Cuaca {x}")
if weather_option:
    filtered_df = filtered_df[filtered_df['weathersit'].isin(weather_option)]

# Line Chart - Tren Peminjaman Sepeda Per Jam
plt.figure(figsize=(12, 6))
sns.lineplot(x='hr', y='cnt', data=hourly_trend, marker='o', color='b')
plt.xticks(range(0, 24))
plt.xlabel("Jam dalam Sehari")
plt.ylabel("Rata-rata Jumlah Peminjaman")
plt.title("Tren Peminjaman Sepeda Per Jam")
plt.grid(True)
plt.show()
max_hour = hourly_trend.loc[hourly_trend['cnt'].idxmax()]
min_hour = hourly_trend.loc[hourly_trend['cnt'].idxmin()]
print(f"Jam peminjaman tertinggi: {max_hour['hr']} dengan {max_hour['cnt']:.2f} peminjaman.")
print(f"Jam peminjaman terendah: {min_hour['hr']} dengan {min_hour['cnt']:.2f} peminjaman.")

# Bar Chart - Perbandingan Casual vs Registered
user_type_df = pd.DataFrame({'User Type': ['Casual', 'Registered'], 'Count': [user_type['casual'], user_type['registered']]})
plt.figure(figsize=(8, 5))
sns.barplot(x='User Type', y='Count', data=user_type_df, palette=['red', 'blue'])
plt.xlabel("Tipe Pengguna")
plt.ylabel("Jumlah Peminjaman")
plt.title("Perbandingan Peminjaman: Casual vs Registered")
plt.grid(axis='y')
for index, value in enumerate(user_type_df['Count']):
    plt.text(index, value + 100, str(value), ha='center', fontsize=12)

plt.show()

# Menampilkan total peminjaman di terminal
print(f"Total Peminjaman Casual: {user_type['casual']}")
print(f"Total Peminjaman Registered: {user_type['registered']}")

# Box Plot - Distribusi Peminjaman Sepeda Berdasarkan Hari
plt.figure(figsize=(10, 5))
sns.barplot(x='weekday', y='cnt', data=day_trend, palette='coolwarm')
plt.xlabel("Hari dalam Seminggu (0=Minggu, 6=Sabtu)")
plt.ylabel("Rata-rata Jumlah Peminjaman")
plt.title("Tren Peminjaman Sepeda Berdasarkan Hari")
plt.grid(axis='y')
plt.show()

#Bar chart - Heatmap kolerasi antar variabel
plt.figure(figsize=(10, 6))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Heatmap Korelasi Antar Variabel")
plt.show()

# Conclusion
st.subheader("📌 Kesimpulan")
st.write("Pertanyaan 1: Berdasarkan analisis bike sharing dataset waktu Peminjaman sepeda tertinggi terjadi pada jam sibuk pagi (07:00-09:00) dan sore (17:00-19:00).")
st.write("Pertanyaan 2: Berdasarkan analisis data Pengguna Registered mendominasi peminjaman sepeda dibandingkan dengan Casual dan Pengguna Casual masih cukup signifikan, meskipun jumlahnya lebih kecil dibandingkan pengguna terdaftar.")