# 🤖 Polymarket x BetDEX Arbitrage Bot

Bot Arbitrase Lintas-Chain (Cross-Chain) otomatis yang dirancang untuk mendeteksi peluang keuntungan antara **Polymarket** (Polygon/ERC20) dan **BetDEX** (Solana/Monaco Protocol). Bot ini menggunakan analisis kedalaman pasar (*Market Depth*) untuk memastikan eksekusi yang aman dari risiko *slippage*.

---

## 📂 Struktur Proyek

Proyek ini dibangun dengan arsitektur modular untuk memisahkan logika bisnis, penyedia data, dan manajemen risiko:

- **`core/`**: Orchestrator utama yang menghubungkan data pasar dengan logika eksekusi.
- **`engine/`**: Otak kalkulasi yang menangani matematika arbitrase, Kelly Criterion, dan analisis slippage.
- **`providers/`**: Modul komunikasi API untuk Polymarket (Polygon) dan BetDEX (Solana).
- **`discovery.py`**: Alat bantu untuk mencari Token ID pertandingan yang sedang aktif secara otomatis.
- **`main.py`**: File utama untuk menjalankan bot dalam mode pemantauan (Scanning).

---

## 🛠️ Fitur Unggulan

* **Slippage Protection**: Menggunakan `MarketDepthAnalyzer` untuk menghitung harga efektif berdasarkan ukuran taruhan, bukan hanya harga teratas (Top of Book).
* **Kelly Criterion Management**: Mengoptimalkan ukuran taruhan secara otomatis untuk memaksimalkan pertumbuhan modal jangka panjang dan meminimalkan risiko kebangkrutan.
* **Asynchronous Scanning**: Memantau banyak pasar sekaligus secara paralel menggunakan `asyncio` untuk latensi minimal.
* **Professional Logging**: Pencatatan riwayat peluang yang bersih, berwarna, dan informatif di terminal.

---

## 🚀 Panduan Instalasi

### 1. Kloning Repositori
```bash
git clone [https://github.com/username/polymarket-betdex-arb.git](https://github.com/username/polymarket-betdex-arb.git)
cd polymarket-betdex-arb

---

2. Instalasi Dependensi
Pastikan Anda memiliki Python 3.10 atau lebih baru, lalu jalankan:

Bash
pip install -r requirements.txt
3. Konfigurasi Environment
Salin template .env.example menjadi .env dan masukkan Private Key serta RPC Node Anda:

Bash
cp .env.example .env
4. Konfigurasi Market
Gunakan skrip discovery untuk mendapatkan daftar pasar terbaru atau salin template config:

Bash
cp example.config.json config.json
python discovery.py
⚙️ Cara Menjalankan
Mode Pemantauan (Dry-Run)
Untuk menjalankan bot dalam mode memantau peluang tanpa melakukan transaksi asli (Aman untuk tes):

Bash
python main.py
Mode Pencarian Market
Untuk memperbarui file config.json dengan daftar pertandingan yang sedang aktif di Polymarket:

Bash
python discovery.py
🛡️ Strategi Keamanan Modal
Untuk mencapai Winrate 70%+ dan menjaga modal tetap utuh, bot ini menerapkan:

Atomic Logic Check: Memastikan harga di kedua bursa sinkron sebelum memberikan sinyal.

Conservative Kelly: Hanya menggunakan sebagian kecil dari saldo (Fractional Kelly) untuk setiap perdagangan.

Liquidity Filter: Mengabaikan pasar dengan volume rendah yang berisiko menjebak modal.

⚠️ Disclaimer
Penggunaan bot ini melibatkan risiko finansial tinggi.

Execution Risk: Ada kemungkinan satu sisi taruhan tereksekusi sementara sisi lainnya gagal karena perubahan harga mendadak.

Smart Contract Risk: Risiko bug pada protokol pihak ketiga (Polymarket/BetDEX).

API Latency: Keterlambatan data RPC dapat mempengaruhi keakuratan peluang.

Gunakan hanya dana yang Anda siap untuk rugi. Penulis tidak bertanggung jawab atas segala kerugian yang timbul dari penggunaan software ini.

📄 Lisensi
Proyek ini dilisensikan di bawah MIT License.
