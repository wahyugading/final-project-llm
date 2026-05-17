# rag_engine.py — Lightweight RAG menggunakan TXT files
# Tidak membutuhkan ChromaDB atau embedding API
# Menggunakan keyword-based retrieval + Gemini untuk generasi jawaban

import os
import re
import streamlit as st
from pathlib import Path
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
from langchain_core.output_parsers import StrOutputParser

# ─────────────────────────────────────────────
# Konstanta
# ─────────────────────────────────────────────

KNOWLEDGE_BASE_DIR = Path(__file__).parent / "BERKAS RAG PROJECT"

# File TXT yang digunakan sebagai knowledge base
KB_FILES = [
    "pajak_pph21_ringkasan.txt",
    "regulasi_pajak_ringkasan.txt",
    "investasi_ringkasan.txt",
    "laporan_keuangan_sample.txt",
]

SYSTEM_PROMPT = """Kamu adalah **NusaArtha AI**, asisten keuangan AI pribadi yang ahli dalam:
- Pajak Indonesia (PPh 21 TER, pajak investasi, SPT, regulasi DJP)
- Instrumen investasi (saham IDX, obligasi, reksadana, crypto)
- Perencanaan keuangan pribadi untuk masyarakat Indonesia
- Regulasi OJK dan DJP terbaru (2024-2025)

**Aturan menjawab:**
1. Jawab berdasarkan konteks dokumen yang diberikan
2. Jika tidak ada di konteks, gunakan pengetahuan umum tapi tandai dengan "(informasi umum)"
3. Gunakan bahasa Indonesia yang profesional namun ramah
4. Sertakan angka/perhitungan yang spesifik jika relevan
5. Jika ada tabel perbandingan atau perhitungan, tampilkan dengan rapi menggunakan format teks

⚠️ Disclaimer: NusaArtha AI adalah alat edukasi, bukan konsultan pajak/investasi berlisensi."""


# ─────────────────────────────────────────────
# Load Knowledge Base ke Memori
# ─────────────────────────────────────────────

@st.cache_data(show_spinner=False)
def load_knowledge_base() -> dict[str, str]:
    """
    Muat semua file TXT dari BERKAS RAG PROJECT ke dalam dictionary.
    Di-cache oleh Streamlit agar tidak reload setiap request.
    Returns: {filename: content}
    """
    kb = {}
    for fname in KB_FILES:
        fpath = KNOWLEDGE_BASE_DIR / fname
        if fpath.exists():
            try:
                text = fpath.read_text(encoding="utf-8")
                kb[fname] = text
            except Exception as e:
                st.warning(f"Gagal baca {fname}: {e}")
        else:
            st.warning(f"File tidak ditemukan: {fpath}")
    return kb


def chunk_text(text: str, chunk_size: int = 600, overlap: int = 100) -> list[str]:
    """
    Potong teks menjadi chunks dengan overlap.
    Mencoba memotong pada batas paragraf atau kalimat.
    """
    # Split per paragraf dulu
    paragraphs = [p.strip() for p in re.split(r'\n{2,}', text) if p.strip()]
    chunks = []
    current = ""

    for para in paragraphs:
        if len(current) + len(para) + 2 <= chunk_size:
            current = current + "\n\n" + para if current else para
        else:
            if current:
                chunks.append(current)
            # Jika paragraf lebih panjang dari chunk_size, potong lebih lanjut
            if len(para) > chunk_size:
                words = para.split()
                sub = ""
                for w in words:
                    if len(sub) + len(w) + 1 <= chunk_size:
                        sub = sub + " " + w if sub else w
                    else:
                        if sub:
                            chunks.append(sub)
                        sub = w
                if sub:
                    current = sub
                else:
                    current = ""
            else:
                current = para

    if current:
        chunks.append(current)

    return chunks


def keyword_score(chunk: str, query: str) -> float:
    """
    Hitung relevansi chunk terhadap query menggunakan keyword matching.
    Score = jumlah keyword yang cocok / total keyword query.
    """
    query_lower = query.lower()
    chunk_lower = chunk.lower()

    # Tokenisasi sederhana — buang stop words pendek
    stopwords = {"dan", "atau", "yang", "di", "ke", "dari", "untuk",
                 "dengan", "pada", "adalah", "ini", "itu", "jika", "saya",
                 "anda", "kamu", "bisa", "akan", "ada", "sudah", "juga",
                 "berapa", "apa", "bagaimana", "kenapa", "siapa"}
    
    keywords = [w for w in re.findall(r'\b\w+\b', query_lower)
                if w not in stopwords and len(w) > 2]
    
    if not keywords:
        return 0.0

    score = sum(1 for kw in keywords if kw in chunk_lower)

    # Bonus: exact phrase match
    if query_lower[:30] in chunk_lower:
        score += 3

    return score / len(keywords)


def retrieve_relevant_chunks(
    kb: dict[str, str],
    query: str,
    top_k: int = 6,
    chunk_size: int = 600,
) -> list[dict]:
    """
    Cari chunks paling relevan dari knowledge base berdasarkan keyword matching.
    Returns: list of {"source": filename, "content": text, "score": float}
    """
    all_chunks = []

    for fname, content in kb.items():
        chunks = chunk_text(content, chunk_size=chunk_size)
        for chunk in chunks:
            score = keyword_score(chunk, query)
            all_chunks.append({
                "source": fname,
                "content": chunk,
                "score": score,
            })

    # Urutkan berdasarkan score, ambil top_k
    all_chunks.sort(key=lambda x: x["score"], reverse=True)
    
    # Ambil top_k dengan score > 0, sisanya ambil dari file yang relevan secara nama
    relevant = [c for c in all_chunks[:top_k] if c["score"] > 0]
    
    if not relevant:
        # Fallback: ambil chunks pertama dari setiap file
        for fname, content in kb.items():
            chunks = chunk_text(content, chunk_size=chunk_size)
            if chunks:
                relevant.append({"source": fname, "content": chunks[0], "score": 0})
    
    return relevant[:top_k]


# ─────────────────────────────────────────────
# RAG Chain
# ─────────────────────────────────────────────

def build_rag_chain(api_key: str, kb: dict[str, str]):
    """
    Bangun lightweight RAG chain.
    kb: dictionary {filename: content} dari load_knowledge_base()
    Returns: callable chain function
    """
    chat_model = ChatGoogleGenerativeAI(
        google_api_key=api_key,
        model="gemini-2.5-flash",
        temperature=0.2,
        top_p=0.95,
    )

    chat_template = ChatPromptTemplate.from_messages([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessagePromptTemplate.from_template(
            """Berikut adalah konteks dari knowledge base keuangan:

{context}

---
Pertanyaan: {question}

Jawab dalam bahasa Indonesia yang jelas dan terstruktur:"""
        ),
    ])

    chain = chat_template | chat_model | StrOutputParser()

    def rag_invoke(question: str) -> tuple[str, list[dict]]:
        """
        Jalankan RAG: retrieve → format context → generate.
        Returns: (jawaban, sumber_chunks)
        """
        # Retrieve
        relevant_chunks = retrieve_relevant_chunks(kb, question)

        # Format context
        context_parts = []
        for chunk in relevant_chunks:
            src = chunk["source"].replace("_", " ").replace(".txt", "").title()
            context_parts.append(f"[Sumber: {src}]\n{chunk['content']}")
        context = "\n\n---\n\n".join(context_parts)

        # Generate
        answer = chain.invoke({"context": context, "question": question})

        # Format sources untuk ditampilkan
        sources = [
            {
                "source": c["source"].replace("_", " ").replace(".txt", "").title(),
                "page": "",
                "preview": c["content"][:200] + "...",
                "score": round(c["score"], 2),
            }
            for c in relevant_chunks if c["score"] > 0
        ]

        return answer, sources

    return rag_invoke


# ─────────────────────────────────────────────
# Index Uploaded File (PDF → TXT sederhana)
# ─────────────────────────────────────────────

def index_uploaded_file(file_bytes: bytes, filename: str, kb: dict[str, str]) -> tuple[int, int]:
    """
    Baca PDF yang diupload dan tambahkan teksnya ke knowledge base in-memory.
    Returns: (jumlah_chunks, jumlah_halaman)
    """
    import tempfile, os
    from langchain_community.document_loaders import PyPDFLoader

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    try:
        loader = PyPDFLoader(tmp_path)
        pages = loader.load()
        full_text = "\n\n".join(p.page_content for p in pages)
        kb[filename] = full_text  # tambah ke kb in-memory
        chunks = chunk_text(full_text)
        return len(chunks), len(pages)
    finally:
        os.unlink(tmp_path)
