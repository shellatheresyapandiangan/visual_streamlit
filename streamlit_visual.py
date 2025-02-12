import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Judul aplikasi
st.title("Visualisasi Interaktif Data Medis")

# Load dataset
@st.cache_data  # Cache data agar tidak dimuat ulang setiap kali
def load_data():
    data = pd.read_csv("heart.csv")  # Pastikan file CSV ada di direktori yang sama
    return data

data = load_data()

# Sidebar untuk filter
st.sidebar.header("Filter Data")
age_range = st.sidebar.slider("Rentang Usia", int(data['age'].min()), int(data['age'].max()), (40, 60))
sex_filter = st.sidebar.multiselect("Jenis Kelamin", options=["Pria", "Wanita"], default=["Pria", "Wanita"])
target_filter = st.sidebar.multiselect("Target", options=[0, 1], default=[0, 1])

# Mapping jenis kelamin
sex_map = {"Pria": 1, "Wanita": 0}
filtered_sex = [sex_map[sex] for sex in sex_filter]

# Filter data berdasarkan input pengguna
filtered_data = data[
    (data['age'] >= age_range[0]) & 
    (data['age'] <= age_range[1]) & 
    (data['sex'].isin(filtered_sex)) & 
    (data['target'].isin(target_filter))
]

# Visualisasi 1: Distribusi Usia
st.subheader("Distribusi Usia Pasien")
fig, ax = plt.subplots()
sns.histplot(filtered_data['age'], kde=True, bins=20, ax=ax)
st.pyplot(fig)

# Visualisasi 2: Jumlah Target (Penyakit Jantung Ya/Tidak)
st.subheader("Distribusi Target (Penyakit Jantung)")
target_counts = filtered_data['target'].value_counts()
fig, ax = plt.subplots()
ax.pie(target_counts, labels=["Tidak Sakit", "Sakit"], autopct='%1.1f%%', startangle=90)
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
st.pyplot(fig)

# Visualisasi 3: Korelasi Fitur
st.subheader("Korelasi Antar Fitur")
corr_matrix = filtered_data.corr()
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig)

# Visualisasi 4: Scatter Plot untuk Hubungan antara Cholesterol dan Tekanan Darah
st.subheader("Hubungan antara Kolesterol dan Tekanan Darah")
fig, ax = plt.subplots()
sns.scatterplot(data=filtered_data, x='chol', y='trestbps', hue='target', palette='Set1', ax=ax)
st.pyplot(fig)

# Tampilkan data yang difilter
st.subheader("Data yang Difilter")
st.dataframe(filtered_data)