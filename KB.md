# Knowledge Base: Personal Finance AI Assistant

Direktori ini berisi ringkasan dokumen yang akan digunakan sebagai knowledge base untuk RAG (Retrieval-Augmented Generation) chatbot keuangan pribadi kamu.

## 📁 Struktur Folder

```
knowledge_base/
├── pajak/                          # Regulasi pajak & perhitungan PPh
│   ├── pajak_pph21_ringkasan.txt   # PPh 21, TER, contoh perhitungan
│   └── regulasi_pajak_ringkasan.txt # Regulasi komprehensif semua instrumen
├── investasi/                       # Instrumen & cara kerja investasi
│   └── investasi_ringkasan.txt      # Saham, obligasi, reksadana, crypto
└── data_personal/                   # Data & template keuangan pribadi
    └── laporan_keuangan_sample.txt  # Laporan keuangan + portfolio sample
```

## 📄 Deskripsi File

### 1. **pajak/pajak_pph21_ringkasan.txt** (13 KB)
Fokus: Pajak Penghasilan Pasal 21 untuk karyawan

**Isi:**
- Definisi & subjek PPh 21
- PTKP 2024-2025 berdasarkan status pernikahan
- Komponen pengurang penghasilan
- **Skema PROGRESIF vs TER** (skema baru 2024)
- Tabel TER bulanan dengan bracket penghasilan
- 3 contoh perhitungan detail (gaji normal, bonus, honor)
- Tarif Pasal 17 untuk akhir tahun
- Proses bulanan + akhir tahun

**Gunakan untuk:** Diskusi gaji, bonus, perhitungan pajak bulanan, planning PPh 21

---

### 2. **pajak/regulasi_pajak_ringkasan.txt** (24 KB)
Fokus: Regulasi pajak untuk SEMUA instrumen investasi

**Isi:**
- PPh Final Saham (0,1%) + Dividen (10%)
- PPh Final Reksadana (10% capital gain + dividen)
- PPh Final Obligasi (10% kupon + 0,1% capital gain)
- **PPh Crypto (0,21% per 2025 - BARU!)** ← Penting
- PPN Jasa Broker 12% (per 2024)
- PPh Penghasilan Tidak Tetap (honor 10%, komisi 10%)
- Pelaporan SPT (Masa & Tahunan)
- Peraturan terbaru Q1-Q2 2025

**Gunakan untuk:** Tanya pajak investasi spesifik, capital gain, dividen, crypto, honor, SPT

---

### 3. **investasi/investasi_ringkasan.txt** (24 KB)
Fokus: Instrumen investasi & cara kerjanya

**Isi:**

#### SAHAM (7 halaman)
- Definisi & cara kerja
- Jenis saham (blue chip, mid cap, small cap, syariah)
- Risiko, biaya transaksi, pajak
- Cara membeli, settlement
- Keuntungan & kerugian

#### OBLIGASI (6 halaman)
- ORI, SR, SBR (Sukuk), SBPU
- Kupon & pajak (10% final)
- Obligasi Korporasi (AAA, A, BBB rating)
- Cara membeli, settlement
- Keuntungan: stabil; Kerugian: return rendah

#### REKSADANA (8 halaman)
- 5 jenis: Pasar uang, pendapatan tetap, campuran, saham, syariah
- NAB (Nilai Aktiva Bersih), UP (Unit Penyertaan)
- Management fee, pajak (10%)
- SIP (Systematic Investment Plan)
- Risk profiling: konservatif → agresif

#### CRYPTO (6 halaman)
- Blockchain, wallet, public/private key
- Regulasi POJK 27/2024
- **Pajak 0,21% per PMK 50/2025** ← Baru
- Platform OJK licensed (Pintu, Indodax, dll)
- Risk SANGAT TINGGI, volatilitas ekstrem
- ⚠️ Bukan alat pembayaran sah di Indonesia

#### PERBANDINGAN & TIPS
- Tabel return vs risiko
- Alokasi portfolio berdasarkan umur/profil
- Diversifikasi & rebalancing
- 10 tips investasi sehat

**Gunakan untuk:** Tanya instrumen apa itu? Cara kerja? Risiko? Pajak? Pilihan saham vs obligasi? Reksadana mana yang bagus?

---

### 4. **data_personal/laporan_keuangan_sample.txt** (14 KB)
Fokus: Template & contoh laporan keuangan pribadi

**Isi:**

#### LAPORAN BULANAN (Januari, Februari, Maret 2025)
- Penghasilan bruto + tunjangan
- PPh 21 (TER) bulanan
- Pengeluaran tetap & variabel
- Investasi & tabungan
- Sisa/surplus
- Keterangan khusus

#### PORTFOLIO SNAPSHOT (per Maret 2025)
- Reksadana Saham Bibit: ~Rp 2 juta
- Saham lokal (BBCA, BBRI): ~Rp 1,4 juta
- Obligasi ORI: Rp 5 juta
- Tabungan darurat: Rp 14 juta
- Total asset: Rp 22,9 juta

#### SUMMARY & INSIGHTS
- Total penghasilan Q1: Rp 30,5 juta
- Ratio spending: 63% (sehat)
- Tax paid: Rp 2,1 juta (effective rate 2,1%)
- Goals Q2 2025

**Gunakan untuk:** 
- Upload dokumen kamu & bandingkan
- Tanya soal pengeluaran, alokasi asset
- Planning investasi bulanan
- Tax planning

---

## 🔍 Cara Menggunakan Knowledge Base

### Scenario 1: Tanya Pajak Gaji
**Kamu:** "Gaji saya Rp 9 juta/bulan, berapa PPh 21 yang dipotong?"
**Chatbot akan:** 
1. Retrieve dari `pajak_pph21_ringkasan.txt` (TER 5%)
2. Hitung: Rp 9 juta × 5% = Rp 450.000
3. Berikan penjelasan + contoh

### Scenario 2: Tanya Pajak Saham
**Kamu:** "Saya jual saham untung Rp 500.000, berapa pajaknya?"
**Chatbot akan:**
1. Retrieve dari `regulasi_pajak_ringkasan.txt` (PPh Final 0,1%)
2. Hitung: Rp 500.000 × 0,1% = Rp 500
3. Jelaskan sudah final, tidak perlu lapor SPT

### Scenario 3: Perbandingan Instrumen
**Kamu:** "Lebih bagus saham atau reksadana?"
**Chatbot akan:**
1. Retrieve dari `investasi_ringkasan.txt`
2. Compare return, risiko, volatilitas, pajak
3. Berikan rekomendasi berdasarkan profil kamu

### Scenario 4: Analisis Portfolio Kamu
**Kamu:** "Saya upload laporan keuangan, bagaimana dengan alokasi saya?"
**Chatbot akan:**
1. Retrieve `laporan_keuangan_sample.txt` (sebagai benchmark)
2. Analisis portfolio kamu
3. Bandingkan, beri rekomendasi

### Scenario 5: Planning & Strategy
**Kamu:** "Saya dapat bonus Rp 2 juta, bagaimana mengalokasikannya?"
**Chatbot akan:**
1. Retrieve allocation strategy dari `investasi_ringkasan.txt`
2. Retrieve tax implication dari `regulasi_pajak_ringkasan.txt`
3. Beri saran investasi, pajak, alokasi

---

## 📊 Data Coverage

| Topik | Covered | Level |
|-------|---------|-------|
| **PPh 21** | ✅ | Comprehensive (TER, progresif, contoh) |
| **Saham** | ✅ | Comprehensive (cara, risiko, pajak, biaya) |
| **Obligasi** | ✅ | Comprehensive (ORI, obligasi korporat, kupon) |
| **Reksadana** | ✅ | Comprehensive (5 jenis, NAB, fee, SIP) |
| **Crypto** | ✅ | Comprehensive (blockchain, OJK, pajak baru) |
| **Dividen Tax** | ✅ | Good (10%, mechanism) |
| **Capital Gain** | ✅ | Good (tarif, contoh, final) |
| **PPN Broker** | ✅ | Good (12% per 2024) |
| **SPT** | ✅ | Good (jenis, cara isi, lampiran) |
| **Data Personal** | ✅ | Sample (template, portfolio) |
| **Crypto Pajak** | ✅ | Good (0,21% baru 2025) |
| **ETF & Derivatif** | ⚠️ | Minimal (belum jadi regulasi) |

---

## ⚙️ Cara Setup RAG untuk Chatbot

### Tools & Library:
```python
# Chunking & Embeddings
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings  # or local embedding

# Vector Database
from langchain.vectorstores import Chroma  # atau Faiss, Qdrant

# LLM & RAG Chain
from langchain.llms import OpenAI  # atau Llama via Groq
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
```

### Setup Steps:
1. **Load documents** dari `/knowledge_base/` folder
2. **Split text** menjadi chunks (~500 chars per chunk)
3. **Create embeddings** & index ke vector DB
4. **Setup RAG chain** dengan prompt template
5. **Integrate dengan Streamlit UI** (Sesi 3 materi)

---

## 🔄 Update & Maintenance

### Update Kapan:
- ✅ Ada regulasi pajak baru
- ✅ OJK/DJP keluar peraturan baru
- ✅ PMK/PP ada perubahan
- ✅ Data sampel portfolio perlu refresh

### Cara Update:
1. Edit `.txt` file yang relevan
2. Re-load documents ke vector DB
3. Re-index (Chroma akan otomatis)
4. Test dengan beberapa query

---

## 📝 Catatan Penting

1. **Akurasi:** Ringkasan ini akurat per Mei 2026. Peraturan pajak sering berubah—selalu cross-check dengan sumber resmi (pajak.go.id, ojk.go.id).

2. **Disclaimers di Chatbot:**
   - "Saya AI assistant, bukan konsultan pajak"
   - "Untuk kasus spesifik, konsultasi dengan tax professional"
   - "Ringkasan ini untuk edukasi, bukan legal advice"

3. **Halusinasi Risk:**
   - Set temperature RENDAH (0.2-0.3) agar jawaban akurat soal angka/pajak
   - Jangan allow hallucination untuk perhitungan kuantitatif
   - Always cite sumber dokumen saat jawab

4. **Data Privacy:**
   - Tidak ada data pribadi real di sini (semua sample/template)
   - Nanti saat user upload dokumen mereka → encrypt & handle sensitif
   - Jangan store personal data di vector DB selamanya

---

## 📞 Contact & Support

**Sumber Resmi:**
- DJP: www.pajak.go.id / Aplikasi Cek Pajak
- OJK: www.ojk.go.id / www.sikapiuangmu.ojk.go.id
- Kemenkeu: www.kemenkeu.go.id

**Tax Consultant:**
- Kantor pajak terdekat (KPP)
- Akuntan publik / Tax consultant registered
- Konsultasi gratis di kantor pajak

---

**Knowledge Base ready! 🎉**

Next step: Setup LangChain + Groq LLM + Streamlit untuk demo chatbot.

