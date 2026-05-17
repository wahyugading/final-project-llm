# app.py — Finance Copilot: Personal Finance AI Assistant
# Menggabungkan: RAG (ChromaDB + Gemini) + Function Calling + Streamlit UI

import os
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Finance Copilot — Asisten Keuangan AI",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS premium (dark glassmorphism) ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Base */
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #0F172A; color: #E2E8F0; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(15,23,42,0.95);
    border-right: 1px solid rgba(255,255,255,0.06);
}

/* Hide default streamlit header */
#MainMenu, footer, header { visibility: hidden; }

/* Chat messages */
.user-bubble {
    background: rgba(16,185,129,0.12);
    border: 1px solid rgba(16,185,129,0.3);
    border-radius: 18px 18px 4px 18px;
    padding: 14px 18px; margin: 8px 0;
    margin-left: 20%; color: #E2E8F0;
}
.ai-bubble {
    background: rgba(30,41,59,0.9);
    border-left: 3px solid #10B981;
    border-radius: 4px 18px 18px 18px;
    padding: 14px 18px; margin: 8px 0;
    margin-right: 20%; color: #E2E8F0;
}
.ai-bubble strong { color: #10B981; }

/* Cards */
.metric-card {
    background: rgba(30,41,59,0.8);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px; padding: 16px;
    margin: 6px 0;
}
.metric-card .label { color:#94A3B8; font-size:12px; font-weight:600; text-transform:uppercase; }
.metric-card .value { color:#E2E8F0; font-size:22px; font-weight:700; margin-top:4px; }
.metric-card .trend-up { color:#10B981; font-size:12px; }
.metric-card .trend-down { color:#F87171; font-size:12px; }

/* Quick chips */
.chip {
    display:inline-block; background:rgba(16,185,129,0.1);
    border:1px solid rgba(16,185,129,0.4); border-radius:20px;
    padding:6px 14px; margin:3px; font-size:13px; cursor:pointer;
}

/* Source expander */
.source-item {
    background:rgba(15,23,42,0.6); border-radius:8px;
    padding:10px; margin:4px 0; border-left:2px solid #F59E0B;
    font-size:13px; color:#94A3B8;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg,#10B981,#059669);
    color:white; border:none; border-radius:10px;
    font-weight:600; padding:10px 20px;
    transition: all 0.2s;
}
.stButton > button:hover { transform:translateY(-1px); box-shadow:0 4px 15px rgba(16,185,129,0.4); }

/* Inputs */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: rgba(30,41,59,0.8) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important; color: #E2E8F0 !important;
}
.stSelectbox > div { background: rgba(30,41,59,0.8) !important; }

/* Divider */
.divider { border-top: 1px solid rgba(255,255,255,0.06); margin: 16px 0; }
</style>
""", unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "rag_db" not in st.session_state:
    st.session_state.rag_db = None
if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None
if "retriever" not in st.session_state:
    st.session_state.retriever = None
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = None
if "gemini_history" not in st.session_state:
    st.session_state.gemini_history = []
if "mode" not in st.session_state:
    st.session_state.mode = "rag"  # "rag" atau "agent"
if "db_loaded" not in st.session_state:
    st.session_state.db_loaded = False
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    # Logo + Title
    st.markdown("""
    <div style="text-align:center;padding:20px 0 10px;">
        <div style="font-size:48px;">💰</div>
        <div style="font-size:20px;font-weight:700;color:#10B981;">Finance Copilot</div>
        <div style="font-size:12px;color:#64748B;">Asisten Keuangan AI Pribadi</div>
    </div>
    <div class="divider"></div>
    """, unsafe_allow_html=True)

    # API Key
    st.markdown("**🔑 Konfigurasi**")
    api_key = st.text_input(
        "Google Gemini API Key",
        value=os.getenv("GEMINI_API_KEY", ""),
        type="password",
        placeholder="AIza...",
        help="Dapatkan di: aistudio.google.com",
    )

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Mode selector
    st.markdown("**⚙️ Mode AI**")
    mode = st.radio(
        "Pilih mode:",
        ["🔍 RAG (Knowledge Base)", "🤖 Agent (Function Calling)"],
        label_visibility="collapsed",
    )
    st.session_state.mode = "rag" if "RAG" in mode else "agent"

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Load Knowledge Base
    st.markdown("**📚 Knowledge Base**")
    col1, col2 = st.columns(2)
    with col1:
        load_btn = st.button("▶ Muat KB", use_container_width=True)
    with col2:
        rebuild_btn = st.button("🔄 Rebuild", use_container_width=True)

    if (load_btn or rebuild_btn) and api_key:
        try:
            from rag_engine import build_vector_db, build_rag_chain
            force = rebuild_btn
            with st.spinner("Memuat knowledge base..."):
                db = build_vector_db(api_key, force_rebuild=force)
            if db:
                rag_chain, retriever = build_rag_chain(api_key, db)
                st.session_state.rag_db = db
                st.session_state.rag_chain = rag_chain
                st.session_state.retriever = retriever
                st.session_state.db_loaded = True
                st.success("✅ Knowledge base siap!")
        except Exception as e:
            st.error(f"Error: {e}")
    elif (load_btn or rebuild_btn) and not api_key:
        st.warning("Masukkan API key terlebih dahulu.")

    # Status indicator
    if st.session_state.db_loaded:
        st.markdown('<div style="color:#10B981;font-size:13px;">● Knowledge base aktif</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="color:#F59E0B;font-size:13px;">○ Knowledge base belum dimuat</div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Upload dokumen
    st.markdown("**📎 Upload Dokumen Keuangan**")
    uploaded = st.file_uploader(
        "Upload PDF (laporan, rekening, dll)",
        type=["pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )
    if uploaded and api_key and st.button("📥 Index Dokumen", use_container_width=True):
        from rag_engine import index_uploaded_file
        for uf in uploaded:
            with st.spinner(f"Indexing {uf.name}..."):
                try:
                    n_chunks, n_pages = index_uploaded_file(uf.read(), uf.name, api_key)
                    st.success(f"✅ {uf.name}: {n_pages} hal, {n_chunks} chunks")
                    if uf.name not in st.session_state.uploaded_files:
                        st.session_state.uploaded_files.append(uf.name)
                except Exception as e:
                    st.error(f"Gagal: {e}")

    if st.session_state.uploaded_files:
        st.markdown("**File terindex:**")
        for f in st.session_state.uploaded_files:
            st.markdown(f'<div style="font-size:12px;color:#94A3B8;">📄 {f}</div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Real-time widgets
    st.markdown("**📊 Pasar Real-time**")
    st.markdown("""
    <div class="metric-card">
        <div class="label">USD/IDR</div>
        <div class="value">Rp 15.740</div>
        <div class="trend-up">▲ +0.20%</div>
    </div>
    <div class="metric-card">
        <div class="label">BBCA</div>
        <div class="value">Rp 9.275</div>
        <div class="trend-up">▲ +0.82%</div>
    </div>
    <div class="metric-card">
        <div class="label">BBRI</div>
        <div class="value">Rp 4.210</div>
        <div class="trend-down">▼ -0.71%</div>
    </div>
    """, unsafe_allow_html=True)
    st.caption("*Gunakan tool 'Info Saham' untuk data terkini*")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center;font-size:11px;color:#475569;">Powered by Gemini AI ✨</div>', unsafe_allow_html=True)


# ── MAIN AREA ─────────────────────────────────────────────────────────────────
from datetime import datetime

now = datetime.now()
hour = now.hour
greeting = "Selamat Pagi" if hour < 11 else "Selamat Siang" if hour < 15 else "Selamat Sore"

st.markdown(f"""
<div style="padding:20px 0 10px;">
    <div style="font-size:28px;font-weight:700;color:#F8FAFC;">{greeting}! 👋</div>
    <div style="color:#64748B;font-size:14px;">{now.strftime('%A, %d %B %Y')} •
        <span style="background:rgba(245,158,11,0.15);color:#F59E0B;
        padding:2px 10px;border-radius:20px;font-size:12px;">
        ⚠️ Edukasi saja — bukan saran investasi profesional
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# Quick action chips
st.markdown("**Aksi Cepat:**")
cols = st.columns(5)
quick_actions = [
    ("💰", "Hitung PPh 21", "Saya bergaji Rp 9 juta/bulan status TK/0, berapa PPh 21 saya?"),
    ("📈", "Info Saham", "Berapa harga saham BBCA sekarang?"),
    ("💱", "Kurs Hari Ini", "Berapa kurs USD ke IDR sekarang?"),
    ("📊", "Tips Investasi", "Apa rekomendasi alokasi portfolio untuk pemula?"),
    ("🧾", "Pajak Crypto", "Saya jual crypto profit Rp 5 juta, berapa pajaknya?"),
]
for i, (icon, label, prompt) in enumerate(quick_actions):
    with cols[i]:
        if st.button(f"{icon} {label}", use_container_width=True, key=f"chip_{i}"):
            st.session_state.pending_prompt = prompt

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Chat History ──────────────────────────────────────────────────────────────
chat_container = st.container()

# Pesan selamat datang jika belum ada history
if not st.session_state.messages:
    with chat_container:
        st.markdown("""
        <div class="ai-bubble">
        <strong>Finance Copilot 🤖</strong><br><br>
        Halo! Saya <b>Finance Copilot</b>, asisten keuangan AI pribadi Anda. Saya dapat membantu:<br><br>
        💼 <b>Pajak</b> — PPh 21, pajak investasi saham/crypto/reksadana, SPT<br>
        📈 <b>Investasi</b> — Saham, obligasi, reksadana, crypto<br>
        💱 <b>Kurs Real-time</b> — Konversi mata uang USD, EUR, dll.<br>
        📊 <b>Portofolio</b> — Analisis dan strategi alokasi aset<br><br>
        <i>Muat Knowledge Base di sidebar, lalu mulai bertanya!</i>
        </div>
        """, unsafe_allow_html=True)

# Tampilkan history
with chat_container:
    for i, msg in enumerate(st.session_state.messages):
        if msg["role"] == "user":
            st.markdown(f'<div class="user-bubble">👤 {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            content = msg["content"].replace("\n", "<br>")
            st.markdown(f'<div class="ai-bubble"><strong>Finance Copilot 🤖</strong><br><br>{content}</div>', unsafe_allow_html=True)
            # Tampilkan sumber jika ada
            if "sources" in msg and msg["sources"]:
                with st.expander(f"📚 {len(msg['sources'])} Sumber Dokumen"):
                    for src in msg["sources"]:
                        st.markdown(f"""
                        <div class="source-item">
                        📄 <b>{src['source']}</b> {f"(Hal. {src['page']+1})" if src.get('page') != '' else ''}<br>
                        <span style="color:#CBD5E1">{src['preview']}</span>
                        </div>
                        """, unsafe_allow_html=True)

# ── Chat Input ────────────────────────────────────────────────────────────────
# Cek apakah ada pending prompt dari quick action
default_val = st.session_state.pop("pending_prompt", "")

user_input = st.chat_input(
    "Tanya soal pajak, investasi, kurs, portofolio...",
)

# Proses input (baik dari chat_input maupun dari quick chip)
query = user_input or default_val

if query:
    if not api_key:
        st.error("⚠️ Masukkan Gemini API Key di sidebar terlebih dahulu.")
        st.stop()

    # Tampilkan pesan user
    st.markdown(f'<div class="user-bubble">👤 {query}</div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role": "user", "content": query})

    mode = st.session_state.mode

    with st.spinner("🤔 Finance Copilot sedang berpikir..."):
        try:
            if mode == "rag":
                # ── Mode RAG ──────────────────────────────
                if not st.session_state.db_loaded:
                    response_text = (
                        "⚠️ Knowledge base belum dimuat. "
                        "Klik tombol **▶ Muat KB** di sidebar terlebih dahulu."
                    )
                    sources = []
                else:
                    rag_chain = st.session_state.rag_chain
                    retriever = st.session_state.retriever
                    response_text = rag_chain.invoke(query)
                    from rag_engine import get_source_docs
                    sources = get_source_docs(retriever, query)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response_text,
                    "sources": sources if mode == "rag" else [],
                })

            else:
                # ── Mode Agent (Function Calling) ─────────
                from gemini_agent import create_finance_agent, chat_with_function_calling
                if st.session_state.gemini_client is None:
                    st.session_state.gemini_client = create_finance_agent(api_key)

                response_text, updated_history = chat_with_function_calling(
                    client=st.session_state.gemini_client,
                    user_message=query,
                    chat_history=st.session_state.gemini_history,
                )
                st.session_state.gemini_history = updated_history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response_text,
                    "sources": [],
                })

        except Exception as e:
            err_msg = f"Terjadi error: {str(e)}"
            st.session_state.messages.append({
                "role": "assistant", "content": err_msg, "sources": []
            })

    st.rerun()

# ── Bottom controls ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    if st.button("🗑️ Bersihkan Percakapan", use_container_width=True):
        st.session_state.messages = []
        st.session_state.gemini_history = []
        st.rerun()
