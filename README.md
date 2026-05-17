# 💰 NusaArtha AI — Asisten Keuangan Personal AI & RAG

> **NusaArtha AI** (Nusantara Harta AI) adalah asisten finansial cerdas yang dirancang khusus untuk memandu pengguna dalam navigasi regulasi perpajakan Indonesia terbaru (PPh 21 TER PMK 168/2023), analisis investasi lokal (Saham IDX, Reksa Dana, Obligasi, Crypto), serta perencanaan keuangan rumah tangga yang adaptif.

Aplikasi ini dideploy menggunakan **Streamlit Cloud** dan dapat diakses langsung secara online melalui link berikut:
🔗 **[nusaartha-ai.streamlit.app](https://nusaartha-ai.streamlit.app/)**

---

## 🧭 1. Visi & Misi Proyek (README)

Mengelola keuangan pribadi di Indonesia sering kali membingungkan akibat regulasi pajak yang dinamis dan kompleksitas instrumen pasar modal. **NusaArtha AI** hadir sebagai *Copilot* finansial yang menyederhanakan perhitungan pajak, memberikan wawasan investasi yang patuh regulasi OJK/DJP, serta mempermudah akses literasi keuangan berbasis dokumen ringkasan (*Lightweight RAG*).

### 🌟 Fitur Utama:
*   **Lightweight RAG (Knowledge Base)**: Bertanya langsung seputar pajak dan investasi berbasis data teks ringkasan regulasi resmi tanpa membebani performa server.
*   **Function Calling Agent**: Menghitung PPh 21 TER, kalkulasi pajak aset investasi, cek kurs valuta asing (USD/IDR), serta memantau pergerakan harga saham teratas di BEI secara dinamis menggunakan Gemini 2.5 Flash.
*   **Premium Glassmorphic UI**: Dashboard bertema gelap modern dengan visualisasi data pasar real-time dan panel riwayat interaktif.

---

## 👥 2. Kontributor & Apresiasi (AUTHORS & THANKS)

### ✍️ Penulis & Pengembang Utama
*   **Wahyugading** — *Lead AI Engineer & Developer* ([GitHub Profile](https://github.com/wahyugading))

### 🤝 Terima Kasih Kepada
*   **Google DeepMind Team** & program **Maju Bareng AI 26** atas bimbingan teknologi Generative AI & Streamlit.
*   **Direktorat Jenderal Pajak (DJP)** & **Otoritas Jasa Keuangan (OJK)** atas dokumen regulasi publik yang menjadi basis pengetahuan sistem ini.

---

## ⚙️ 3. Panduan Instalasi & Persyaratan (INSTALL)

Ikuti langkah-langkah di bawah ini untuk menjalankan NusaArtha AI di komputer lokal Anda.

### 📋 Prasyarat Sistem
*   Python 3.10 - 3.12
*   Git
*   Gemini API Key (Dapatkan gratis di [Google AI Studio](https://aistudio.google.com))

### 🛠️ Langkah Pemasangan Lokal

1.  **Clone Repositori**:
    ```bash
    git clone https://github.com/wahyugading/final-project-llm.git
    cd final-project-llm
    ```

2.  **Buat & Aktifkan Virtual Environment**:
    ```bash
    python -m venv venv
    # Di Windows (PowerShell):
    .\venv\Scripts\Activate.ps1
    # Di Linux/macOS:
    source venv/bin/activate
    ```

3.  **Instal Dependensi**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Konfigurasi API Key**:
    *   Buat file `.env` di direktori utama proyek (pastikan file ini masuk ke `.gitignore` Anda):
        ```env
        GEMINI_API_KEY=AIzaSyD-xxxxxx...
        ```
    *   *Alternatif (Streamlit Cloud)*: Tambahkan kunci Anda langsung di panel **⚙️ Pengaturan** saat aplikasi berjalan untuk isolasi keamanan per sesi browser.

5.  **Jalankan Aplikasi**:
    ```bash
    streamlit run app.py
    ```

---

## 🔄 4. Catatan Rilis & Pembaruan (CHANGELOG & NEWS)

### 📢 Berita Terbaru (NEWS - Untuk Pengguna)
*   **Mei 2026**: Rilis NusaArtha AI v2.0! Antarmuka baru menggunakan navigasi Sidebar Glassmorphism, integrasi RAG super cepat berbasis dokumen teks, dan fitur hapus riwayat chat instan.

### 🛠️ Log Perubahan Teknis (CHANGELOG - Untuk Developer)
```diff
v2.0.0 (2026-05-17)
+ Mengubah sistem RAG dari ChromaDB (Vector Store berat) ke Lightweight RAG berbasis In-Memory Keyword scoring.
+ Menambahkan form input API Key manual dengan perlindungan session state agar tidak ada kebocoran kunci di browser frontend.
+ Memperbaiki error "TextFileLoader not found" dengan beralih ke native Langchain TextLoader.
+ Restrukturisasi total file app.py untuk menyelaraskan sidebar dengan referensi tata letak layout.png.
- Menghapus dependensi berat seperti chromadb dan pysqlite3-binary untuk menjamin stabilitas Streamlit Cloud.
```

---

## 🐛 5. Penanganan Masalah & Laporan Bug (BUG)

### 🚨 Masalah yang Sering Ditemui (Troubleshooting)

*   **Error: "403 API key was reported as leaked"**
    *   *Solusi*: Google mendeteksi API Key Anda terpublikasi di repositori publik GitHub. Buka Google AI Studio, hapus key yang bocor, buat key baru, dan pastikan file `.env` dimasukkan ke dalam `.gitignore` sebelum melakukan git push.
*   **Error: "400 API key expired"**
    *   *Solusi*: Masa aktif key Anda telah habis atau dinonaktifkan. Silakan perbarui key Anda di Google AI Studio dan simpan kembali di menu Pengaturan aplikasi.
*   **Knowledge Base Belum Terbaca**
    *   *Solusi*: Saat pertama kali membuka mode RAG, buka menu **⚙️ Pengaturan** dan klik tombol **▶ Muat KB** untuk mengindeks ringkasan dokumen keuangan ke memori.

### 📬 Cara Melaporkan Bug
Jika Anda menemukan kendala teknis lainnya, buat Issue di repositori dengan format:
1. Deskripsi masalah yang dihadapi.
2. Langkah-langkah untuk mereproduksi error.
3. Screenshot konsol terminal / tampilan error di layar.

---

## 🙋‍♂️ 6. Pertanyaan Umum (FAQ)

**Q: Apakah data API Key saya aman saat dimasukkan ke dashboard online?**  
*A: Ya. Jika Anda menggunakan input manual di panel Pengaturan, key hanya disimpan di `st.session_state` memori server Streamlit selama sesi browser Anda aktif. Kunci tidak akan disimpan di database atau diekspos ke publik.*

**Q: Dari mana sumber kalkulator PPh 21 yang digunakan?**  
*A: Kalkulator PPh 21 menggunakan basis tarif efektif rata-rata (TER) yang sesuai dengan Peraturan Menteri Keuangan Nomor 168 Tahun 2023 (PMK 168/2023) yang berlaku di Indonesia.*

**Q: Mengapa sistem tidak lagi menggunakan database ChromaDB?**  
*A: Streamlit Cloud memiliki batasan memori dan penyimpanan sementara. Pendekatan in-memory Lightweight RAG yang kami terapkan di v2.0 menjamin startup aplikasi instan dan stabilitas tinggi bebas dari error library SQLite lokal.*

---

## 📝 7. Rencana Tugas Mendatang (TODO)

- [ ] Integrasi grafik pergerakan harga saham live (menggunakan library `yfinance`).
- [ ] Menambahkan fitur ekspor laporan simulasi PPh 21 ke file PDF/Excel.
- [ ] Menambahkan support dokumen berformat `.docx` dan `.xlsx` di menu Upload Dokumen.
- [ ] Implementasi sistem deteksi status wajib pajak otomatis berbasis NPWP/NIK.

---

## ⚖️ 8. Lisensi & Distribusi (LICENSE)

Proyek ini dilisensikan di bawah **MIT License**. Anda bebas menggunakan, memodifikasi, dan mendistribusikan kode ini untuk tujuan komersial maupun non-komersial dengan tetap mencantumkan kredit penulis asli.

---
*NusaArtha AI — Kelola Harta, Bangun Nusantara. 💰🇮🇩*
