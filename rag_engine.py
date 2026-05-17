# rag_engine.py
# RAG Pipeline — diadaptasi dari salinan_dari_rag_gemini_avpn_it_data.py
# Menggunakan: Gemini Embedding + ChromaDB + LangChain LCEL

import os
import streamlit as st
from pathlib import Path

from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


# ─────────────────────────────────────────────
# Konstanta
# ─────────────────────────────────────────────

CHROMA_DIR = "./chroma_finance_db"
KNOWLEDGE_BASE_DIR = Path(__file__).parent / "BERKAS RAG PROJECT"

SYSTEM_PROMPT = """Kamu adalah **Finance Copilot**, asisten keuangan AI pribadi yang ahli dalam:
- Pajak Indonesia (PPh 21, pajak investasi, SPT)
- Instrumen investasi (saham, obligasi, reksadana, crypto)
- Perencanaan keuangan pribadi
- Regulasi OJK dan DJP terbaru

**Aturan menjawab:**
1. Jawab HANYA berdasarkan konteks dokumen yang diberikan
2. Jika tidak ada di konteks, katakan "Saya tidak menemukan informasi tersebut di knowledge base"
3. Gunakan bahasa Indonesia yang profesional namun ramah
4. Sertakan angka/perhitungan yang spesifik jika relevan
5. Selalu tambahkan disclaimer: "Ini adalah informasi edukasi, bukan saran investasi/pajak profesional"
6. Jika pertanyaan butuh data real-time (kurs, harga saham), arahkan ke fitur Function Calling

⚠️ Disclaimer: Finance Copilot adalah alat edukasi, bukan konsultan pajak/investasi berlisensi."""


def get_embeddings(api_key: str):
    """Inisialisasi model embedding Gemini."""
    return GoogleGenerativeAIEmbeddings(
        google_api_key=api_key,
        model="models/text-embedding-004",  # model embedding Google terbaru
    )


# ─────────────────────────────────────────────
# Load & Index Dokumen
# ─────────────────────────────────────────────

def load_documents():
    """Muat semua dokumen dari folder BERKAS RAG PROJECT."""
    docs = []

    if not KNOWLEDGE_BASE_DIR.exists():
        st.warning(f"Folder knowledge base tidak ditemukan: {KNOWLEDGE_BASE_DIR}")
        return docs

    # Load PDF files
    pdf_files = list(KNOWLEDGE_BASE_DIR.glob("*.pdf"))
    for pdf_path in pdf_files:
        try:
            loader = PyPDFLoader(str(pdf_path))
            pages = loader.load()
            docs.extend(pages)
        except Exception as e:
            st.warning(f"Gagal load {pdf_path.name}: {e}")

    # Load TXT files di root project
    txt_files = list(Path(__file__).parent.glob("*.txt"))
    for txt_path in txt_files:
        try:
            loader = TextLoader(str(txt_path), encoding="utf-8")
            pages = loader.load()
            docs.extend(pages)
        except Exception as e:
            st.warning(f"Gagal load {txt_path.name}: {e}")

    return docs


def build_vector_db(api_key: str, force_rebuild: bool = False):
    """
    Bangun atau muat ChromaDB.
    - Jika DB sudah ada dan force_rebuild=False → langsung pakai yang ada
    - Jika belum ada / force_rebuild=True → buat ulang dari dokumen
    """
    embeddings = get_embeddings(api_key)

    if Path(CHROMA_DIR).exists() and not force_rebuild:
        db = Chroma(
            persist_directory=CHROMA_DIR,
            embedding_function=embeddings
        )
        return db

    # Load dan chunk dokumen
    with st.spinner("📄 Memuat dokumen knowledge base..."):
        docs = load_documents()

    if not docs:
        st.error("Tidak ada dokumen ditemukan. Pastikan folder BERKAS RAG PROJECT ada.")
        return None

    with st.spinner(f"✂️ Memotong {len(docs)} halaman menjadi chunks..."):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            separators=["\n\n", "\n", " ", ""],
        )
        chunks = splitter.split_documents(docs)

    with st.spinner(f"🧠 Membuat embeddings untuk {len(chunks)} chunks... (ini mungkin memakan waktu)"):
        db = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=CHROMA_DIR,
        )
        db.persist()

    return db


def index_uploaded_file(file_bytes: bytes, filename: str, api_key: str):
    """Index file yang diupload user ke ChromaDB yang sudah ada."""
    import tempfile

    embeddings = get_embeddings(api_key)

    # Simpan ke temp file
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    try:
        loader = PyPDFLoader(tmp_path)
        pages = loader.load()
        # Tambahkan metadata filename
        for page in pages:
            page.metadata["source"] = filename

        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        chunks = splitter.split_documents(pages)

        # Tambah ke DB yang sudah ada
        if Path(CHROMA_DIR).exists():
            db = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
            db.add_documents(chunks)
            db.persist()
        else:
            db = Chroma.from_documents(chunks, embeddings, persist_directory=CHROMA_DIR)
            db.persist()

        return len(chunks), len(pages)
    finally:
        os.unlink(tmp_path)


# ─────────────────────────────────────────────
# RAG Chain — LCEL Pipeline
# (diadaptasi dari salinan_dari_rag_gemini_avpn_it_data.py)
# ─────────────────────────────────────────────

def build_rag_chain(api_key: str, db: Chroma, top_k: int = 8):
    """
    Bangun RAG chain menggunakan LCEL (LangChain Expression Language).

    Arsitektur (sama seperti notebook contoh):
    question → retriever → format_docs → ChatPromptTemplate → Gemini → StrOutputParser
    """
    chat_model = ChatGoogleGenerativeAI(
        google_api_key=api_key,
        model="gemini-2.5-flash",
        temperature=0.2,  # Rendah untuk akurasi keuangan (seperti rekomendasi QUICK_START.md)
        top_p=0.95,
    )

    retriever = db.as_retriever(search_kwargs={"k": top_k})

    def format_docs(docs):
        """Gabungkan chunks menjadi satu string konteks."""
        return "\n\n---\n\n".join(
            f"[Sumber: {doc.metadata.get('source', 'Knowledge Base')}]\n{doc.page_content}"
            for doc in docs
        )

    chat_template = ChatPromptTemplate.from_messages([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessagePromptTemplate.from_template(
            """Jawab pertanyaan berikut berdasarkan konteks dokumen.

Konteks:
{context}

Pertanyaan: {question}

Jawaban (dalam bahasa Indonesia):"""
        ),
    ])

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | chat_template
        | chat_model
        | StrOutputParser()
    )

    return rag_chain, retriever


def get_source_docs(retriever, question: str):
    """Ambil dokumen sumber yang relevan untuk pertanyaan."""
    docs = retriever.invoke(question)
    sources = []
    for doc in docs:
        source = doc.metadata.get("source", "Knowledge Base")
        # Ambil hanya nama file, bukan path penuh
        source_name = Path(source).name if source != "Knowledge Base" else source
        preview = doc.metadata.get("page", "")
        sources.append({
            "source": source_name,
            "page": preview,
            "preview": doc.page_content[:200] + "...",
        })
    return sources
