# QUICK START: Personal Finance AI Assistant Knowledge Base

## ✅ Yang Sudah Kamu Punya

Saya sudah buatkan **4 dokumen ringkasan** untuk knowledge base RAG chatbot kamu:

```
📦 knowledge_base/
├── 📄 README.md                                [Index & Penjelasan]
├── 📁 pajak/
│   ├── pajak_pph21_ringkasan.txt              [13 KB] PPh 21, TER, contoh
│   └── regulasi_pajak_ringkasan.txt           [24 KB] Semua pajak investasi
├── 📁 investasi/
│   └── investasi_ringkasan.txt                [24 KB] Saham, obligasi, reksadana, crypto
└── 📁 data_personal/
    └── laporan_keuangan_sample.txt             [14 KB] Template laporan + portfolio
```

**Total:** 4 file `.txt` + 1 file `README.md` = ~75 KB structured knowledge

---

## 🎯 Apa yang Bisa Chatbot Kamu Lakukan

Dengan knowledge base ini, chatbot bisa jawab:

### Kategori 1: Pajak & Perhitungan
- ✅ "Gaji saya Rp X, berapa PPh 21?" → Auto hitung TER
- ✅ "Bonus Rp 2 juta, ada pajak?" → Jelaskan bracket TER naik
- ✅ "Jual saham untung berapa pajaknya?" → 0,1% final
- ✅ "Dividen obligasi kena pajak?" → 10% final
- ✅ "Jual crypto, ada pajak?" → 0,21% baru (PMK 50/2025)
- ✅ "Kapan lapor SPT?" → Deadline & cara isi

### Kategori 2: Instrumen Investasi
- ✅ "Apa itu reksadana? Cara kerjanya?" → Detail NAB, UP, fee
- ✅ "Saham vs obligasi?" → Compare return, risiko, volatilitas
- ✅ "ORI itu apa? Berapa return?" → Kupon, jatuh tempo
- ✅ "Crypto aman gak?" → POJK, regulated, BUT volatil
- ✅ "Blue chip saham apa saja?" → BBCA, BBRI, BMRI, UNVR
- ✅ "Biaya investasi berapa?" → Broker fee, PPN 12%, pajak

### Kategori 3: Portfolio & Strategy
- ✅ "Alokasi portfolio untuk umur 30?" → 30% obligasi, 40% reksadana, 20% saham, 10% crypto
- ✅ "Saya dapat bonus, investasi mana?" → Diversifikasi, SIP bulanan
- ✅ "Tabungan darurat berapa?" → 3-6 bulan pengeluaran
- ✅ "Leverage/margin trading?" → NOT recommended, high risk
- ✅ "Rebalancing portfolio kapan?" → Setiap 6 bulan

### Kategori 4: Planning & Diskusi
- ✅ "Saya mau beli saham 100 juta, strategi?" → Growth, fundamental analysis, diversify
- ✅ "Tax planning tahun ini?" → Timing jual, capital loss offset
- ✅ "Dari mana modal investasi?" → Gaji + surplus pengeluaran
- ✅ "Long-term vs short-term?" → Hold 5-10 tahun untuk growth

---

## 🚀 Setup Implementation (3 Steps)

### STEP 1: Load Knowledge Base ke Vector DB

```python
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings  # Local, faster
from langchain.vectorstores import Chroma

# Load documents
loader = DirectoryLoader("knowledge_base/", glob="**/*.txt")
documents = loader.load()

# Split into chunks (500 chars, 50 overlap)
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", " "]
)
chunks = splitter.split_documents(documents)

# Create embeddings & vector DB
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_db = Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_db")
```

### STEP 2: Setup RAG Chain dengan Groq LLM

```python
from langchain.llms import Groq
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Initialize Groq (kamu butuh API key dari console.groq.com)
llm = Groq(
    model_name="mixtral-8x7b-32768",  # atau "llama2-70b-4096"
    groq_api_key="your_groq_api_key",
    temperature=0.2  # Rendah untuk akurasi (penting untuk pajak!)
)

# Custom prompt untuk tone finansial
template = """Kamu adalah personal finance assistant yang ahli tentang keuangan Indonesia.
Gunakan konteks di bawah untuk menjawab pertanyaan.
Jika tidak tahu jawaban, katakan "Saya tidak yakin" DARIPADA membuat-buat.

KONTEKS:
{context}

PERTANYAAN: {question}

JAWAB DALAM BAHASA INDONESIA, PROFESSIONAL TAPI FRIENDLY:"""

prompt = PromptTemplate(template=template, input_variables=["context", "question"])

# Setup RAG chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",  # atau "map_reduce" untuk dokumen panjang
    retriever=vector_db.as_retriever(search_kwargs={"k": 5}),
    chain_type_kwargs={"prompt": prompt},
    return_source_documents=True
)
```

### STEP 3: Setup Streamlit UI (dari Sesi 3)

```python
import streamlit as st

st.set_page_config(page_title="💰 Asisten Keuangan", layout="wide")
st.title("💰 Personal Finance Assistant")
st.subheader("Diskusi Keuangan, Pajak, & Investasi dengan AI")

# Chat interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
user_input = st.chat_input("Tanya soal gaji, pajak, saham, obligasi, reksadana, crypto...")

if user_input:
    # Add to history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.write(user_input)
    
    # Get response from RAG chain
    with st.chat_message("assistant"):
        with st.spinner("🤔 Sedang mencari jawaban..."):
            result = qa_chain({"query": user_input})
            response = result["result"]
            sources = result["source_documents"]
            
            st.write(response)
            
            # Show sources
            with st.expander("📚 Sumber Dokumen"):
                for i, doc in enumerate(sources, 1):
                    st.write(f"**{i}. {doc.metadata.get('source', 'Unknown')}**")
                    st.write(doc.page_content[:200] + "...")
    
    st.session_state.messages.append({"role": "assistant", "content": response})
```

---

## 📋 Knowledge Base Content Summary

### pajak_pph21_ringkasan.txt
**13 KB | Topik: Pajak Gaji & PPh 21**

Isi:
- PTKP (Rp 54-72 juta/tahun tergantung status)
- **TER Bulanan** (5-20% tergantung gaji, dari Rp 4,5-100+ juta)
- Contoh perhitungan 3 skenario
- Tarif Pasal 17 untuk akhir tahun

Contoh Query:
```
Q: "Gaji saya Rp 9.5 juta/bulan, TK/0, berapa PPh 21?"
A: Masuk bracket 4,5-10 juta → TER 5%
   PPh = Rp 9.500.000 × 5% = Rp 475.000/bulan
   Setahun = Rp 5.7 juta (tapi akhir tahun direkonsiliasi dengan tarif progresif)
```

---

### regulasi_pajak_ringkasan.txt
**24 KB | Topik: Semua Pajak Investasi**

Isi:
- Saham: Capital gain 0,1% final, dividen 10% final
- Obligasi: Kupon 10% final, capital gain 0,1%
- Reksadana: Capital gain 10%, dividen 10%
- **Crypto: 0,21% PPh 22 Final (BARU 2025!)**
- PPN Broker 12%
- Honor/Komisi: 10% PPh
- SPT cara isi

Contoh Query:
```
Q: "Saya jual crypto profit Rp 8 juta, berapa pajak?"
A: PPh 22 = 0,21% × Rp 8 juta = Rp 16.800 (final, sudah dipotong otomatis)
   Jadi netto = Rp 7.983.200
   Tidak perlu lapor SPT khusus, platform yang lapor ke DJP.
```

---

### investasi_ringkasan.txt
**24 KB | Topik: Instrumen Investasi**

Isi:
- SAHAM: Cara beli, risiko, biaya, pajak, contoh BBCA vs BBRI
- OBLIGASI: ORI (kupon 5-6%), SBN, obligasi korporat
- REKSADANA: 5 jenis, NAB, SIP, fee, pajak
- CRYPTO: POJK 27/2024, exchange OJK, volatilitas tinggi
- Perbandingan return vs risiko
- Alokasi portfolio berdasarkan umur

Contoh Query:
```
Q: "Saya umur 30, total Rp 50 juta. Alokasi portfolio gimana?"
A: Rekomendasi:
   - 40% Obligasi (Rp 20 juta) → ORI + Obligasi korporat
   - 40% Reksadana Saham (Rp 20 juta) → Bibit atau Vanguard
   - 15% Saham Lokal (Rp 7.5 juta) → 3-5 saham diversified
   - 5% Crypto (Rp 2.5 juta) → BTC/ETH jika berani risiko
```

---

### laporan_keuangan_sample.txt
**14 KB | Topik: Template Laporan & Portfolio**

Isi:
- 3 bulan laporan keuangan detail (Jan, Feb, Mar 2025)
- Penghasilan, pengeluaran, investasi, sisa
- Portfolio snapshot (reksadana, saham, obligasi, tabungan)
- Summary & insights
- Target Q2 2025

Contoh Query:
```
Q: "Saya upload laporan keuangan saya, apa sarannya?"
A: [Upload → Chatbot compare dengan sample]
   Analisis:
   - Spending ratio: 63% (sehat, target 50-70%)
   - Investasi: 20% dari netto (bagus!)
   - Alokasi: Lebih banyak growth, bisa tambah saham
   - Tax: PPh otomatis, no issue
```

---

## 💡 Key Features

### ✅ Temperature Setting (Penting!)
```
temperature=0.2  # Rendah untuk akurasi pajak/angka
# Jangan use 0.7+ untuk keuangan, bisa hallucinate
```

### ✅ RAG Best Practices
- Chunk size 500 chars (bukan 1000) → lebih precise
- Top-k retrieval = 5 dokumen (cukup, tidak bloated)
- Show source documents (user percaya)
- Temperature rendah = less creative, more accurate

### ✅ Disclaimers Built-in
Tambahkan di system prompt:
```
"Saya AI assistant untuk edukasi keuangan.
BUKAN konsultan pajak / investment advisor.
Untuk kasus spesifik, hubungi tax professional atau OJK."
```

---

## 🔧 Troubleshooting

### Problem 1: Chatbot "Hallucinate" (Bikin Angka)
**Solusi:** Turunkan temperature ke 0.1-0.2, tambah system prompt strict

### Problem 2: Slow Response
**Solusi:** Reduce chunk size, use faster embedding model (MiniLM), cache vector DB

### Problem 3: "Tidak ada di knowledge base"
**Solusi:** Normal jika query out of scope → Chatbot harus honest & suggest sumber resmi

### Problem 4: Update Regulasi
**Solusi:** Edit `.txt` file, re-load documents, vector DB auto-update (Chroma)

---

## 📅 Next Steps (untuk Kamu)

1. **Cleanup folder**
   - Rename files jika perlu
   - Struktur sudah rapi: `pajak/`, `investasi/`, `data_personal/`

2. **Setup Lokal**
   - Install requirements: `langchain`, `groq`, `streamlit`, `chroma`
   - Dapatkan Groq API key (free tier ada)
   - Test RAG chain dengan sample query

3. **Customize**
   - Tambah data pribadi kamu ke `laporan_keuangan_sample.txt`
   - Update portfolio snapshot dengan data real
   - Adapt prompt template ke voice kamu

4. **Deploy**
   - Host di Streamlit Cloud (free)
   - Atau deploy di VPS (Heroku, Render, dll)
   - Share link ke teman/keluarga untuk feedback

5. **Monitor**
   - Log user queries (untuk understand needs)
   - Update knowledge base setiap ada regulasi baru
   - Improve RAG prompt berdasarkan feedback

---

## 📚 Sumber Resmi (untuk Update)

- **Pajak:** www.pajak.go.id, siaran pers DJP
- **OJK:** www.ojk.go.id, POJK terbaru
- **Kemenkeu:** www.kemenkeu.go.id, PMK terbaru
- **BEI:** www.idx.co.id (untuk berita saham)
- **Literasi:** sikapiuangmu.ojk.go.id (gratis)

---

## 🎓 Materi Referensi (dari kelas Hacktiv8)

- **Sesi 1:** Konsep AI, prompting, Gemini API → untuk improve LLM tuning
- **Sesi 2:** RAG dengan LangChain, vector DB → ini yang dipakai!
- **Sesi 3:** Streamlit UI, agents → untuk build frontend

Kamu sudah punya semua materi, tinggal assemble dengan knowledge base ini.

---

## ✨ Final Checklist

- [x] Knowledge base documents created (4 files)
- [x] Structured folder (pajak, investasi, data_personal)
- [x] README dengan penjelasan lengkap
- [x] Sample implementation code
- [x] Troubleshooting guide
- [ ] **NEXT: Kamu setup lokal & test!**

---

## 💬 Questions & Support

Kalau ada masalah atau mau customize, tanyakan:
- "Gimana cara update knowledge base?"
- "Bisa tambah fitur currency converter?"
- "Bagaimana integrasi dengan real-time crypto price?"
- "Gimana deploy ke Streamlit Cloud?"

---

**Knowledge base siap digunakan! Happy coding! 🚀**

