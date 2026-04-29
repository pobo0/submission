
import glob
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


st.set_page_config(
    page_title="Dashboard Kualitas Udara Beijing",
    page_icon="🌫️",
    layout="wide",
)


@st.cache_data(show_spinner=False)
def load_raw_data():
    patterns = [
        "data/PRSA_Data_*20130301-20170228.csv",
        "PRSA_Data_*20130301-20170228.csv",
        "data/*.csv",
    ]
    csv_files = []
    for pattern in patterns:
        csv_files.extend(glob.glob(pattern))

    # buang duplikat sambil menjaga urutan
    seen = set()
    unique_files = []
    for f in csv_files:
        if f not in seen:
            seen.add(f)
            unique_files.append(f)

    if not unique_files:
        return None, []

    dfs = []
    for file in unique_files:
        try:
            df_part = pd.read_csv(file)
            dfs.append(df_part)
        except Exception:
            continue

    if not dfs:
        return None, unique_files

    df = pd.concat(dfs, ignore_index=True)
    return df, unique_files


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df_clean = df.copy()

    # Pastikan kolom tanggal tersedia
    if {"year", "month", "day", "hour"}.issubset(df_clean.columns):
        df_clean["datetime"] = pd.to_datetime(df_clean[["year", "month", "day", "hour"]])

    # Ubah placeholder menjadi NaN
    for col in ["PM2.5", "PM10"]:
        if col in df_clean.columns:
            df_clean.loc[df_clean[col] == 999, col] = np.nan

    # Imputasi numerik dengan median per stasiun, lalu median global
    num_cols = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3", "TEMP", "PRES", "DEWP", "RAIN", "WSPM"]
    for col in num_cols:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].fillna(df_clean.groupby("station")[col].transform("median"))
            df_clean[col] = df_clean[col].fillna(df_clean[col].median())

    # Imputasi kategorikal
    if "wd" in df_clean.columns:
        mode_wd = df_clean["wd"].mode(dropna=True)
        if not mode_wd.empty:
            df_clean["wd"] = df_clean["wd"].fillna(mode_wd.iloc[0])

    # Hapus kolom nomor urut
    if "No" in df_clean.columns:
        df_clean = df_clean.drop(columns=["No"])

    # Kategori kecepatan angin
    if "WSPM" in df_clean.columns:
        df_clean["wind_category"] = pd.cut(
            df_clean["WSPM"],
            bins=[-0.001, 1, 3, 6, np.inf],
            labels=["Lemah", "Sedang", "Kuat", "Sangat Kuat"],
        )

    return df_clean


def month_name(month_num: int) -> str:
    month_labels = {
        1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "Mei", 6: "Jun",
        7: "Jul", 8: "Agu", 9: "Sep", 10: "Okt", 11: "Nov", 12: "Des"
    }
    return month_labels.get(int(month_num), str(month_num))


def make_monthly_series(df: pd.DataFrame) -> pd.Series:
    return df.groupby("month")["PM2.5"].mean().reindex(range(1, 13))


def make_wind_series(df: pd.DataFrame) -> pd.Series:
    return (
        df.groupby("wind_category", observed=True)["PM2.5"]
        .mean()
        .reindex(["Lemah", "Sedang", "Kuat", "Sangat Kuat"])
    )


raw_df, files_found = load_raw_data()

st.title("Dashboard Analisis Kualitas Udara Beijing")
st.caption("Ringkasan insight untuk pertanyaan 1 dan 2 dari notebook analisis data.")

if raw_df is None:
    st.error(
        "File CSV tidak ditemukan. Pastikan dataset PRSA_Data_*20130301-20170228.csv "
        "sudah diletakkan di folder data/ atau di folder yang sama dengan app.py."
    )
    st.stop()

df = clean_data(raw_df)

# Sidebar filter
st.sidebar.header("Filter Data")
stations = ["Semua"] + sorted(df["station"].dropna().unique().tolist())
selected_station = st.sidebar.selectbox("Pilih stasiun", stations)

min_year = int(df["year"].min())
max_year = int(df["year"].max())
year_range = st.sidebar.slider(
    "Rentang tahun",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year),
)

filtered_df = df.copy()
if selected_station != "Semua":
    filtered_df = filtered_df[filtered_df["station"] == selected_station]

filtered_df = filtered_df[
    (filtered_df["year"] >= year_range[0]) &
    (filtered_df["year"] <= year_range[1])
]

# KPI
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Jumlah baris", f"{len(filtered_df):,}")
with col2:
    st.metric("Jumlah stasiun", f"{filtered_df['station'].nunique():,}")
with col3:
    st.metric("Rata-rata PM2.5", f"{filtered_df['PM2.5'].mean():.2f}")
with col4:
    if "datetime" in filtered_df.columns:
        st.metric(
            "Periode data",
            f"{filtered_df['datetime'].min().date()} s/d {filtered_df['datetime'].max().date()}",
        )

st.divider()

tab1, tab2, tab3 = st.tabs(["Pertanyaan 1", "Pertanyaan 2", "Data Preview"])

with tab1:
    st.subheader("Pertanyaan 1: Bagaimana pola rata-rata PM2.5 per bulan?")
    monthly_pm25 = make_monthly_series(filtered_df)

    c1, c2 = st.columns([1.2, 1])
    with c1:
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(monthly_pm25.index, monthly_pm25.values, marker="o")
        ax.set_xticks(range(1, 13))
        ax.set_xticklabels([month_name(i) for i in range(1, 13)])
        ax.set_xlabel("Bulan")
        ax.set_ylabel("Rata-rata PM2.5")
        title = "Rata-rata PM2.5 per Bulan"
        if selected_station != "Semua":
            title += f" - {selected_station}"
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
        st.pyplot(fig, clear_figure=True)

    # with c2:
    #     if monthly_pm25.notna().any():
    #         peak_month = int(monthly_pm25.idxmax())
    #         low_month = int(monthly_pm25.idxmin())
    #         peak_value = float(monthly_pm25.max())
    #         low_value = float(monthly_pm25.min())

    #         st.markdown("**Insight utama**")
    #         st.write(
    #             f"Rata-rata PM2.5 paling tinggi terjadi pada **{month_name(peak_month)}** "
    #             f"({peak_value:.2f}), sedangkan yang paling rendah terjadi pada "
    #             f"**{month_name(low_month)}** ({low_value:.2f})."
    #         )
    #         st.write(
    #             "Pola ini menunjukkan kualitas udara cenderung memburuk pada bulan-bulan tertentu "
    #             "dan membaik pada periode lain."
    #         )
    #     else:
    #         st.info("Data tidak cukup untuk menghitung rata-rata PM2.5 per bulan.")

with tab2:
    st.subheader("Pertanyaan 2: Bagaimana PM2.5 berdasarkan kategori kecepatan angin?")
    wind_pm25 = make_wind_series(filtered_df)

    c1, c2 = st.columns([1.2, 1])
    with c1:
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(wind_pm25.index.astype(str), wind_pm25.values)
        ax.set_xlabel("Kategori Kecepatan Angin")
        ax.set_ylabel("Rata-rata PM2.5")
        title = "Rata-rata PM2.5 berdasarkan Kategori Kecepatan Angin"
        if selected_station != "Semua":
            title += f" - {selected_station}"
        ax.set_title(title)
        ax.grid(axis="y", alpha=0.3)
        st.pyplot(fig, clear_figure=True)

    # with c2:
    #     if wind_pm25.notna().any():
    #         best_category = wind_pm25.idxmin()
    #         worst_category = wind_pm25.idxmax()

    #         st.markdown("**Insight utama**")
    #         st.write(
    #             f"Semakin tinggi kategori kecepatan angin, rata-rata PM2.5 cenderung menurun. "
    #             f"Kategori dengan PM2.5 terendah adalah **{best_category}**, sedangkan yang tertinggi "
    #             f"adalah **{worst_category}**."
    #         )
    #         st.write(
    #             "Artinya, angin yang lebih kuat cenderung membantu menyebarkan polutan sehingga "
    #             "konsentrasi PM2.5 menjadi lebih rendah."
    #         )
    #     else:
    #         st.info("Data tidak cukup untuk menghitung rata-rata PM2.5 berdasarkan angin.")

# with tab3:
#     st.subheader("Data Preview")
#     st.write("Beberapa baris data setelah cleaning:")
#     st.dataframe(filtered_df.head(20), use_container_width=True)

#     csv_data = filtered_df.to_csv(index=False).encode("utf-8")
#     st.download_button(
#         label="Download data terfilter",
#         data=csv_data,
#         file_name="filtered_beijing_air_quality.csv",
#         mime="text/csv",
#     )

# st.divider()
# st.subheader("Ringkasan Proses Cleaning")
# st.write(
#     "Nilai placeholder 999 pada PM2.5 dan PM10 diubah menjadi NaN, lalu diimputasi dengan median "
#     "per stasiun dan median global. Kolom wd diisi dengan modus, dan kolom No dihapus."
# )

with st.expander("Lihat daftar file yang terbaca"):
    st.write(files_found)
