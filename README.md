# 🚗 Ride Pulse Semarang: Analisis Perjalanan & Tarif Ride-Hailing

🔗 **Dashboard:** https://ride-hailing.streamlit.app/

<img width="1904" height="954" alt="image" src="https://github.com/user-attachments/assets/3d66cc49-9003-4c74-abf3-7c3adffdabab" />


## Latar Belakang (Studi Kasus)
**Skenario:** Sebuah layanan transportasi online lokal di Semarang memiliki data 6 bulan perjalanan. Tim operasional ingin tahu kapan armada harus siaga, ke mana orang bergerak, bagaimana tarif terbentuk, dan apakah pelanggan tetap setia.

**Deliverable:**
1. Data perjalanan yang sudah dibersihkan
2. Analisis permintaan, tarif, dan retensi beserta rekomendasi
3. Dashboard interaktif satu halaman yang bisa dipantau secara mandiri

> Catatan: project ini adalah studi kasus portofolio dengan dataset simulasi.

## Pertanyaan Bisnis
1. Jam berapa armada harus paling siaga?
2. Dari area mana ke area mana perjalanan paling sering terjadi?
3. Apakah perjalanan pendek terlalu mahal per kilometer?
4. Adakah pola kemacetan sepanjang hari?
5. Apakah pelanggan lama tetap setia dari bulan ke bulan?

## Pembersihan Data
Dataset: 4.015 baris perjalanan (Januari–Juni 2026) di 10 area Semarang.
- 15 perjalanan dobel dihapus (4.015 → 4.000 perjalanan)
- Data kosong di `dropoff_area`, `payment_method`, dan `customer_type` diisi `Unknown`
- Ditambah fitur: jam, bulan, nama hari, tarif per km, dan kecepatan

## Temuan Utama
- Total pendapatan **Rp112,9 juta**, rata-rata tarif **Rp28.237** per perjalanan
- Dua puncak permintaan: pagi (jam 07.00) dan sore (jam 17.00–19.00); dini hari paling sepi
- Motor 67,6% perjalanan; jarak rata-rata mirip (±5 km), tetapi tarif Mobil ±Rp9.100/km vs Motor ±Rp5.400/km
- Perjalanan ≤ 2 km bertarif ±Rp10.500/km, lebih dari dua kali perjalanan > 10 km (±Rp4.500/km)
- Kecepatan rata-rata datar di ±13–14 km/jam sepanjang hari, tidak ada pola kemacetan jelas
- Permintaan antar area merata, tidak ada satu koridor yang mendominasi
- Pembayaran non-tunai ±82% (QRIS ±41%, E-Wallet ±31%)
- Porsi pelanggan lama turun dari ±74% (Jan–Feb) menjadi ±69,6% (April dan Juni)

## Rekomendasi
- Tambah insentif driver dan ketersediaan armada di jam 07.00 dan 17.00–19.00
- Promosikan Mobil untuk perjalanan jauh atau berkelompok
- Tinjau struktur tarif dasar untuk perjalanan pendek
- Fokuskan promo berdasarkan jam, bukan hanya area
- Pertahankan pelanggan lama dengan program loyalitas

## Dashboard
Satu halaman dengan filter di atas: jam radial 24 jam, diagram aliran antar area (Sankey), tarif per km menurut jarak, kecepatan per jam, dan retensi pelanggan.

## Tools
Python · Pandas · Matplotlib · Seaborn · Plotly · Streamlit · Google Colab

## Isi Repository
- `app.py`: dashboard Streamlit
- `Analisis_Ride_Hailing.ipynb`: notebook analisis (cleaning, EDA, insight)
- `data/`: dataset
- `.streamlit/config.toml`: tema dashboard

---
Dibuat oleh **Ihsan Amiruddin**. Terbuka untuk jasa analisis data dan dashboard.
