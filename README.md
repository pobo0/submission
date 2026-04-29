# Dashboard Analisis Kualitas Udara Beijing
Dashboard ini dibuat untuk menampilkan hasil analisis data kualitas udara Beijing secara interaktif menggunakan Streamlit.

## Cara menjalankan
1. Pastikan file dataset CSV berada di folder `data/` dengan pola nama:
   `PRSA_Data_*20130301-20170228.csv`
2. Install library:
   ```bash
   python -m pip install -r requirements.txt
   ```
3. Jalankan dashboard:
   ```bash
   python -m streamlit run dashboard/dashboard.py
   ```

## Isi dashboard
- Ringkasan data
- Insight Pertanyaan 1: rata-rata PM2.5 per bulan
- Insight Pertanyaan 2: rata-rata PM2.5 berdasarkan kategori kecepatan angin
- Preview data hasil cleaning

## Struktur folder
```text
submission/
├── dashboard/
│   └── dashboard.py
├── data/
├── notebook.ipynb
├── requirements.txt
├── README.md
└── url.txt
```
