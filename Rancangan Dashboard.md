Saya akan langsung fokus pada analisis, bukan pujian.

Berdasarkan materi kelas yang kamu pelajari, ada **tiga kelemahan besar** kalau kamu memilih use case yang terlalu generik seperti customer service atau education bot:

1. **Tidak memanfaatkan RAG (Sesi 2\)** — Sebagian besar project kelas akan memilih chatbot sederhana tanpa knowledge base eksternal. Kalau kamu hanya pakai LLM mentah, kamu bakal menghadapi halusinasi masif.

2. **Semua orang bikin hal yang sama** — Customer service bot dan education bot sudah jadi template. Demonstrasi keterampilanmu akan terlihat biasa saja.

3. **Kesulitan menunjukkan nilai nyata** — Generic use case susah dijelaskan "kenapa ini berguna di dunia nyata?" dan susah diuji kredibilitasnya.

---

## **Rekomendasi: Personal Finance Copilot (Asisten Keuangan Personal)**

### **Alasan spesifik mengapa ini cocok:**

**1\. Memanfaatkan semua teknologi yang kamu pelajari:**

* **RAG (Sesi 2\)**: Kamu bisa upload dokumen PDF (contoh: laporan keuangan, catatan pengeluaran bulanan, atau buku panduan pajak lokal). Chatbot akan menjawab berdasarkan data *mereka*, bukan halusinasi.  
* **Function Calling (Sesi 1\)**: Integrasi dengan API eksternal seperti:  
  * Exchange rate API (untuk konversi mata uang real-time)  
  * Stock/crypto API (untuk data harga saham lokal)  
  * Indonesian tax calculator API (jika ada)  
* **Parameter tuning (Sesi 1 & 2\)**: Temperature rendah agar output lebih konsisten dan akurat (penting untuk keuangan—kamu tidak ingin chatbot "kreatif" tentang pajak).  
* **Streamlit UI (Sesi 3\)**: Tampilan clean untuk input pengeluaran, visualisasi budget, dan pertanyaan keuangan.

**2\. Solves a real problem:**

* Indonesia punya **literasi keuangan rendah** — mayoritas orang bingung soal pengelolaan keuangan, pajak, investasi.  
* Chatbot ini bisa membantu pengguna lokal menjawab pertanyaan spesifik tentang pajak Indonesia, produk investasi lokal, atau cara mengelola keuangan harian.  
* Tidak semua orang punya akses ke financial advisor yang baik, chatbot ini bisa menjadi "first layer" konsultasi.

**3\. Mudah dibuktikan kualitasnya:**

* Kamu bisa menunjukkan: "Saya tanya soal pajak PP21, chatbot menjawab dengan benar berdasarkan dokumen yang saya upload."  
* Beda dengan education bot generik yang sulit divalidasi kebenarannya.

**4\. Punya parameter kreatif yang meaningful:**

* Kamu bisa set temperature rendah (0.2-0.3) supaya output fokus pada akurasi.  
* Bisa nambahin personality: "Tone of voice: helpful, cautious, encouraging" — penting buat financial advice.  
* Bisa tambah fitur: kategorisasi pengeluaran otomatis, rekomendasi saving goals, alert jika pengeluaran exceed budget.

---

## **Scope praktis yang bisa diselesaikan dalam 2 hari:**

### **MVP (Minimum Viable Product):**

1. **Upload PDF keuangan pribadi** (contoh: laporan kartu kredit, catatan pengeluaran)  
2. **RAG dengan vector database** (Chroma atau Faiss yang sudah diajarkan)  
3. **Query berbasis natural language**: "Berapa total pengeluaran saya untuk makanan bulan lalu?" → Chatbot cari di dokumen dan jawab  
4. **Plus function calling** ke 1 API eksternal (contoh: exchange rate untuk "Berapa USD 1 juta rupiah hari ini?")  
5. **Streamlit UI** dengan chat input/output sederhana  
6. **Memory minimal**: Simpan riwayat konversasi dalam satu session

### **Bonus (jika ada waktu):**

* Visualisasi pie chart pengeluaran berdasarkan kategori  
* Kalkulasi pajak sederhana  
* Rekomendasi berdasarkan pola pengeluaran

---

## **Kenapa ini lebih baik dari "personal productivity assistant"?**

**Personal productivity assistant** (todo list, notes) juga ide bagus, tapi:

* Lebih mudah diimplementasikan → kurang menunjukkan kemampuan teknis  
* Gampang di-build ulang oleh app biasa (Notion, Todoist sudah ada)  
* Sulit menunjukkan nilai "AI-nya" kecuali kalau kamu integrasi dengan banyak tools

Finance copilot:

* **Butuh RAG \+ function calling** → menunjukkan mastery teknis lebih tinggi  
* **Punya data lokal spesifik** (laporan keuangan pribadi) → lebih realistis dan mudah divalidasi  
* **Langsung bisa digunakan** orang lain (upload dokumen mereka, tanya soal keuangan mereka)

---

## **Challenge checklist untuk project ini:**

* \[ \] Bisa akses PDF financial documents via RAG? (Test: upload, query, dapat jawaban dari dokumen)  
* \[ \] Bisa integrasi ≥1 API eksternal? (Test: tanya harga mata uang, dapat jawaban real-time)  
* \[ \] Parameter temperature tuned tepat? (Test: jawaban konsisten, tidak halusinasi soal angka)  
* \[ \] Streamlit UI intuitif? (Test: user baru bisa upload doc dan tanya tanpa bingung)  
* \[ \] Rekomendasi meaningful? (Bukan hanya jawab, tapi beri insight: "Pengeluaran makananmu naik 30% bulan ini")

**Pertanyaan untuk kamu:** Apakah kamu punya akses ke dokumen finansial pribadi (receipt, tagihan, laporan) yang bisa dijadikan test data? Atau preferensi kamu untuk use case lain?

