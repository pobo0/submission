# Dicoding Collection Dashboard 

Dashboard ini dibuat untuk menampilkan hasil analisis data kualitas udara Beijing secara interaktif menggunakan Streamlit.

## Deskripsi Proyek
Proyek ini menganalisis data kualitas udara Beijing menggunakan beberapa tahapan, yaitu:
- Data Wrangling
- Exploratory Data Analysis (EDA)
- Visualization & Explanatory Analysis
- Conclusion & Recommendation

Dashboard Streamlit digunakan untuk menampilkan hasil analisis secara interaktif.

## Setup Environment

### 1. Buat virtual environment
```bash
python -m venv venv
```

### 2. Aktifkan virtual environment

**Windows**
```bash
venv\Scripts\activate
```

**Mac/Linux**
```bash
source venv/bin/activate
```

### 3. Install dependensi
```bash
python -m pip install -r requirements.txt
```

## Cara Menjalankan Dashboard
Pastikan file dataset CSV berada di folder `data/` dengan pola nama:

```text
PRSA_Data_*20130301-20170228.csv
```

Lalu jalankan dashboard dengan perintah berikut:

```bash
python -m streamlit run dashboard/dashboard.py
```

## Isi Dashboard
Dashboard menampilkan:
- Ringkasan data
- Insight Pertanyaan 1: rata-rata PM2.5 per bulan
- Insight Pertanyaan 2: rata-rata PM2.5 berdasarkan stasiun
- Preview data hasil cleaning

## Struktur Folder
```text
submission/
├── dashboard/
│   └── dashboard.py
├── data/
│   ├── PRSA_Data_Aotizhongxin_20130301-20170228.csv
│   ├── PRSA_Data_Changping_20130301-20170228.csv
│   ├── PRSA_Data_Dingling_20130301-20170228.csv
│   ├── PRSA_Data_Dongsi_20130301-20170228.csv
│   ├── PRSA_Data_Guanyuan_20130301-20170228.csv
│   ├── PRSA_Data_Gucheng_20130301-20170228.csv
│   ├── PRSA_Data_Huairou_20130301-20170228.csv
│   ├── PRSA_Data_Nongzhanguan_20130301-20170228.csv
│   ├── PRSA_Data_Shunyi_20130301-20170228.csv
│   ├── PRSA_Data_Tiantan_20130301-20170228.csv
│   ├── PRSA_Data_Wanliu_20130301-20170228.csv
│   └── PRSA_Data_Wanshouxigong_20130301-20170228.csv
├── notebook.ipynb
├── requirements.txt
├── README.md
└── url.txt
```

## Catatan
- Pastikan semua file CSV dataset sudah ada di folder `data/`.
- File `url.txt` harus berisi link deployment Streamlit Cloud dengan domain `.streamlit.app`.