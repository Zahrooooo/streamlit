import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# Load Dataframe
df = pd.read_csv("day.csv")

# Function
def create_daily_rentals_df(df):
    daily_rentals_df = df.resample(rule='D', on='dteday').agg({
        "registered": "sum",
        "cnt": "sum"
    })
    daily_rentals_df = daily_rentals_df.reset_index()
    daily_rentals_df.rename(columns={
        "registered": "registered_count",
        "cnt": "rentals_count"
    }, inplace=True)
    
    return daily_rentals_df

def create_rental_year_df(df):
    rental_year_df = df.groupby(by="yr").cnt.sum()
    rental_year_df.rename(columns={
        "cnt": "sum"
    }, inplace=True)
    
    return rental_year_df

def create_daily_plot_df(df):
    daily_plot_df = df.resample(rule='D', on='dteday').agg({
        "instant": "nunique",
        "cnt": "sum"
    })
    daily_plot_df = daily_rentals_df.reset_index()
    daily_plot_df.rename(columns={
        "instant": "id_count",
        "cnt": "rentals_count"
    }, inplace=True)
    
    return daily_plot_df

def create_byseason_df(df):
    byseason_df = df.groupby(by="season").cnt.sum()
    byseason_df.rename(columns={
        "cnt": "sum"
    }, inplace=True)
    
    return byseason_df

def create_byholiday_df(df):
    byholiday_df = df.groupby(by="holiday").cnt.sum()
    byholiday_df.rename(columns={
        "cnt": "sum"
    }, inplace=True)
    
    return byholiday_df

# Filter 
datetime_columns = ["dteday"]
df.sort_values(by="dteday", inplace=True)
df.reset_index(inplace=True)
 
for column in datetime_columns:
    df[column] = pd.to_datetime(df[column])
    

# widget date input serta menambahkan logo perusahaan pada sidebar    
min_date = df["dteday"].min()
max_date = df["dteday"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("rental3.jpg")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Set Data Waktu
# untuk memfilter all_df dari semua function
main_df = df[(df["dteday"] >= str(start_date)) & 
                (df["dteday"] <= str(end_date))]

daily_rentals_df = create_daily_rentals_df(main_df)
daily_plot_df = create_daily_plot_df(main_df)
# byseason_df = create_byseason_df(main_df)
# byholiday_df = create_byholiday_df(main_df)
# rfm_df = create_rfm_df(main_df)

# Tulis header
st.header('Bike Sharing - Dashboard')

st.subheader('Daily Rentals')
 
col1, col2 = st.columns(2)
with col1:
    total_registered = daily_rentals_df.registered_count.sum()
    st.metric("Total Registered", value=total_registered)
 
with col2:
    total_rentals = daily_rentals_df.rentals_count.sum() 
    st.metric("Total Bike Rentals", value=total_rentals)
    

# Viz 1
st.subheader('Grafik Total Rental Sepeda per Tahun')

fig, ax = plt.subplots(figsize=(20, 10))
colors = ["#D3D3D3", "#90CAF9"]
sns.barplot(
    x="yr", 
    y="cnt",
    data=df.sort_values(by="yr", ascending=True),
    palette=colors,
    ax=ax
)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

# Viz 2
st.subheader('Grafik Line Plot Rental Sepeda per Tahun')

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_plot_df["dteday"],
    daily_plot_df["rentals_count"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

# Viz 3
st.subheader("Grafik Musim dan Liburan")
 
col1, col2 = st.columns(2)
 
with col1:
    fig, ax = plt.subplots(figsize=(20, 10))
    
    colors = ["#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
    sns.barplot(
        y="cnt", 
        x="season",
        data=df.sort_values(by="season", ascending=True),
        palette=colors,
        ax=ax
    )
    ax.set_title("Total Rental per Musim", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
 
with col2:
    fig, ax = plt.subplots(figsize=(20, 10))
    
    colors = ["#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
    sns.barplot(
        y="cnt", 
        x="holiday",
        data=df.sort_values(by="holiday", ascending=True),
        palette=colors,
        ax=ax
    )
    ax.set_title("Total Rental per Liburan", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

# Caption
st.caption('Copyright (c) Zahro 2023')