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
st.subheader("⏳ Tren Peminjaman Sepeda Per Jam")
avg_hourly_rentals = filtered_df.groupby('hr')['cnt'].mean().reset_index()
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x=avg_hourly_rentals['hr'], y=avg_hourly_rentals['cnt'], ax=ax, marker='o')
plt.xlabel("Jam")
plt.ylabel("Rata-rata Peminjaman")
st.pyplot(fig)

# Bar Chart - Perbandingan Casual vs Registered
st.subheader("👥 Perbandingan Pengguna Casual vs Registered")
user_type = filtered_df[['casual', 'registered']].sum()
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=user_type.index, y=user_type.values, palette=['red', 'blue'], ax=ax)
plt.xlabel("Jenis Pengguna")
plt.ylabel("Total Peminjaman")
st.pyplot(fig)

# Box Plot - Distribusi Peminjaman Sepeda Berdasarkan Hari
st.subheader("📅 Distribusi Peminjaman Sepeda per Hari")
fig, ax = plt.subplots(figsize=(10, 5))
sns.boxplot(x=filtered_df['weekday'], y=filtered_df['cnt'], palette='coolwarm')
plt.xlabel("Hari dalam Seminggu (0 = Minggu, 6 = Sabtu)")
plt.ylabel("Jumlah Peminjaman")
st.pyplot(fig)

# Conclusion
st.subheader("📌 Kesimpulan")
st.write("1. Peminjaman sepeda tertinggi terjadi pada jam sibuk pagi dan sore.")
st.write("2. Pengguna terdaftar lebih dominan dibanding pengguna kasual.")
st.write("3. Cuaca dan hari kerja berpengaruh terhadap jumlah peminjaman.")