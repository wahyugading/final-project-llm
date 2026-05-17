# app.py — NusaArtha AI: Personal Finance AI Copilot
import os
import base64
import streamlit as st
from pathlib import Path
from datetime import datetime

# ── Ambil API key dengan aman (TIDAK pernah dikirim ke browser) ───────────────
def get_api_key() -> str:
    """
    Urutan prioritas (manual input SELALU diutamakan agar user bisa override):
    1. Session state — input manual user (prioritas tertinggi)
    2. st.secrets — Streamlit Cloud Secrets (admin)
    3. Environment variable — .env lokal
    """
    # 1. Manual input dari user (prioritas tertinggi)
    manual = st.session_state.get("_manual_api_key", "")
    if manual:
        return manual
    # 2. Streamlit Cloud Secrets
    try:
        key = st.secrets.get("GEMINI_API_KEY", "")
        if key:
            return key
    except Exception:
        pass
    # 3. Environment variable
    return os.environ.get("GEMINI_API_KEY", "")

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NusaArtha AI — Asisten Keuangan Personal",
    page_icon="BERKAS RAG PROJECT/images/logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Helper: encode image to base64 ───────────────────────────────────────────
def img_to_b64(path: str) -> str:
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""

LOGO_B64 = img_to_b64("BERKAS RAG PROJECT/images/logo.png")

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #0F172A; color: #E2E8F0; }
#MainMenu, footer, header { visibility: hidden; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: #111827 !important;
    border-right: 1px solid rgba(255,255,255,0.06);
    width: 260px !important;
}
[data-testid="stSidebar"] > div { padding: 0 !important; }

/* Nav items */
.nav-item {
    display: flex; align-items: center; gap: 12px;
    padding: 12px 20px; border-radius: 10px;
    color: #94A3B8; font-size: 15px; font-weight: 500;
    cursor: pointer; transition: all 0.2s; margin: 2px 12px;
}
.nav-item:hover { background: rgba(16,185,129,0.1); color: #E2E8F0; }
.nav-item.active { background: rgba(16,185,129,0.15); color: #10B981;
    border-left: 3px solid #10B981; }

/* Chat bubbles */
.ai-row { display:flex; align-items:flex-start; gap:12px; margin:16px 0; }
.ai-avatar {
    width:36px; height:36px; border-radius:50%;
    background: linear-gradient(135deg,#10B981,#059669);
    display:flex; align-items:center; justify-content:center;
    font-size:16px; flex-shrink:0;
}
.ai-bubble {
    background: #1E293B; border-left: 3px solid #10B981;
    border-radius: 4px 16px 16px 16px;
    padding: 14px 18px; color: #E2E8F0;
    max-width: calc(100% - 60px); line-height: 1.6;
}
.user-bubble {
    background: rgba(16,185,129,0.1);
    border: 1px solid rgba(16,185,129,0.25);
    border-radius: 16px 4px 16px 16px;
    padding: 12px 18px; color: #E2E8F0;
    margin-left: auto; max-width: 70%; line-height: 1.6;
}
.user-row { display:flex; justify-content:flex-end; margin:16px 0; }

/* Metric cards */
.mcard {
    background: #1E293B; border: 1px solid rgba(255,255,255,0.06);
    border-radius: 10px; padding: 12px 16px; margin: 6px 12px;
}
.mcard .lbl { color:#64748B; font-size:11px; font-weight:600; text-transform:uppercase; }
.mcard .val { color:#F8FAFC; font-size:20px; font-weight:700; margin:2px 0; }
.mcard .up  { color:#10B981; font-size:11px; }
.mcard .dn  { color:#F87171; font-size:11px; }

/* Saham grid */
.saham-grid { display:grid; grid-template-columns:1fr 1fr; gap:6px; margin:0 12px; }
.saham-card {
    background:#1E293B; border-radius:8px; padding:10px 12px;
    border: 1px solid rgba(255,255,255,0.04);
}
.saham-card .ticker { color:#E2E8F0; font-size:13px; font-weight:600; }
.saham-card .chg-up { color:#10B981; font-size:11px; }
.saham-card .chg-dn { color:#F87171; font-size:11px; }

/* Quick chips */
.chip-row { display:flex; flex-wrap:wrap; gap:8px; margin:12px 0; }
.chip {
    background: rgba(16,185,129,0.08);
    border: 1px solid rgba(16,185,129,0.3);
    border-radius: 20px; padding: 7px 16px;
    font-size: 13px; color: #10B981; cursor: pointer;
}

/* Source box */
.src-box {
    background: rgba(15,23,42,0.8); border-left:2px solid #F59E0B;
    border-radius:8px; padding:10px 14px; margin:4px 0;
    font-size:12px; color:#94A3B8;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg,#10B981,#059669) !important;
    color:white !important; border:none !important;
    border-radius:10px !important; font-weight:600 !important;
    transition: all 0.2s !important;
}
.stButton > button:hover { transform:translateY(-1px) !important;
    box-shadow:0 4px 15px rgba(16,185,129,0.4) !important; }

/* Inputs */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: #1E293B !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important; color: #E2E8F0 !important;
}
.stRadio > div { gap: 4px !important; }
label[data-baseweb="radio"] { color: #94A3B8 !important; }

/* Divider */
.div { border-top:1px solid rgba(255,255,255,0.06); margin:12px 0; }

/* User profile */
.profile {
    display:flex; align-items:center; gap:10px;
    padding: 12px 20px; margin-top:8px;
}
.avatar {
    width:38px; height:38px; border-radius:50%;
    background: linear-gradient(135deg,#6366F1,#8B5CF6);
    display:flex; align-items:center; justify-content:center;
    font-size:16px; font-weight:700; color:white;
}
.disclaimer-badge {
    background: rgba(245,158,11,0.1); border:1px solid rgba(245,158,11,0.3);
    color:#F59E0B; padding:4px 12px; border-radius:20px;
    font-size:11px; font-weight:600;
}
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
defaults = {
    "messages": [], "rag_kb": None, "rag_chain": None,
    "gemini_client": None, "gemini_history": [],
    "mode": "rag", "db_loaded": False, "uploaded_files": [],
    "active_nav": "Chat", "pending_prompt": "",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    # Logo + Brand
    logo_html = f'<img src="data:image/png;base64,{LOGO_B64}" width="40" style="border-radius:8px;">' if LOGO_B64 else "💰"
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:12px;padding:20px 20px 16px;">
        {logo_html}
        <div>
            <div style="font-size:17px;font-weight:700;color:#10B981;">NusaArtha AI</div>
            <div style="font-size:11px;color:#64748B;">Asisten Keuangan AI</div>
        </div>
    </div>
    <div class="div"></div>
    """, unsafe_allow_html=True)

    # Navigasi
    nav_items = [
        ("Chat", "💬", "Chat"),
        ("Upload Dokumen", "📎", "Upload Dokumen"),
        ("Riwayat", "🕐", "Riwayat"),
        ("Pengaturan", "⚙️", "Pengaturan"),
    ]
    for key, icon, label in nav_items:
        active_cls = "active" if st.session_state.active_nav == key else ""
        if st.button(f"{icon}  {label}", key=f"nav_{key}", use_container_width=True):
            st.session_state.active_nav = key
            st.rerun()

    st.markdown('<div class="div"></div>', unsafe_allow_html=True)

    # ── Konten berdasarkan navigasi aktif ─────────────────────────────────────
    nav = st.session_state.active_nav

    if nav == "Pengaturan":
        st.markdown("**🔑 Gemini API Key**")
        st.caption("Key hanya tersimpan selama sesi ini di browser Anda dan tidak dikirim ke mana pun.")

        # Tampilkan status key yang sedang aktif
        _active_key = st.session_state.get("_manual_api_key", "")
        if _active_key:
            masked = _active_key[:8] + "•" * 20
            st.markdown(
                f'<div style="background:rgba(16,185,129,0.08);border:1px solid rgba(16,185,129,0.3);'
                f'border-radius:8px;padding:10px 14px;font-size:13px;color:#10B981;margin-bottom:8px;">'
                f'✅ Key aktif: <code style="color:#34D399;font-size:12px">{masked}</code></div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<div style="background:rgba(245,158,11,0.08);border:1px solid rgba(245,158,11,0.3);'
                'border-radius:8px;padding:10px 14px;font-size:13px;color:#F59E0B;margin-bottom:8px;">'
                '⚠️ Belum ada API Key — masukkan di bawah ini'
                '</div>', unsafe_allow_html=True
            )

        # Form input — selalu tampil agar user bisa update kapanpun
        manual_key = st.text_input(
            "API Key",
            type="password",
            placeholder="AIza...",
            label_visibility="collapsed",
        )
        col_save, col_clear = st.columns(2)
        if col_save.button("💾 Simpan", use_container_width=True):
            if manual_key.strip():
                st.session_state["_manual_api_key"] = manual_key.strip()
                st.success("✅ API Key disimpan!")
                st.rerun()
            else:
                st.warning("Masukkan API Key terlebih dahulu.")
        if col_clear.button("🗑️ Hapus Key", use_container_width=True):
            st.session_state.pop("_manual_api_key", None)
            st.info("API Key dihapus dari sesi.")
            st.rerun()
        st.caption("🔗 Dapatkan API Key gratis: [aistudio.google.com](https://aistudio.google.com)")
        st.markdown("**⚙️ Mode AI**")
        mode = st.radio("Mode", ["🔍 RAG (Knowledge Base)", "🤖 Agent (Function Calling)"],
                        label_visibility="collapsed")
        st.session_state.mode = "rag" if "RAG" in mode else "agent"

        st.markdown('<div class="div"></div>', unsafe_allow_html=True)
        st.markdown("**📚 Knowledge Base**")
        c1, c2 = st.columns(2)
        load_btn = c1.button("▶ Muat KB", use_container_width=True)
        rebuild_btn = c2.button("🔄 Rebuild", use_container_width=True)

        if (load_btn or rebuild_btn):
            api_key_val = get_api_key()
            if api_key_val:
                try:
                    from rag_engine import load_knowledge_base, build_rag_chain
                    # Jika rebuild, clear cache dulu
                    if rebuild_btn:
                        load_knowledge_base.clear()
                    with st.spinner("📄 Memuat knowledge base dari file TXT..."):
                        kb = load_knowledge_base()
                    if kb:
                        rag_chain = build_rag_chain(api_key_val, kb)
                        st.session_state.rag_kb = kb
                        st.session_state.rag_chain = rag_chain
                        st.session_state.db_loaded = True
                        n_files = len(kb)
                        st.success(f"✅ Knowledge base siap! ({n_files} file dimuat)")
                    else:
                        st.error("Tidak ada file TXT ditemukan di BERKAS RAG PROJECT.")
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Masukkan API Key dulu di kolom di atas.")

    elif nav == "Upload Dokumen":
        st.markdown("**📎 Upload Dokumen PDF**")
        uploaded = st.file_uploader("Upload PDF", type=["pdf"],
                                    accept_multiple_files=True, label_visibility="collapsed")
        api_key_env = os.getenv("GEMINI_API_KEY", "")
        if uploaded and st.button("📥 Index Dokumen", use_container_width=True):
            from rag_engine import index_uploaded_file
            # Pastikan kb sudah ada
            if st.session_state.rag_kb is None:
                from rag_engine import load_knowledge_base
                st.session_state.rag_kb = load_knowledge_base()
            for uf in uploaded:
                with st.spinner(f"Membaca {uf.name}..."):
                    try:
                        n_chunks, n_pages = index_uploaded_file(
                            uf.read(), uf.name, st.session_state.rag_kb)
                        st.success(f"✅ {uf.name}: {n_pages} hal, {n_chunks} chunks")
                        if uf.name not in st.session_state.uploaded_files:
                            st.session_state.uploaded_files.append(uf.name)
                    except Exception as e:
                        st.error(f"Gagal: {e}")
        if st.session_state.uploaded_files:
            st.markdown("**File terindex:**")
            for f in st.session_state.uploaded_files:
                st.markdown(f'<div style="font-size:12px;color:#94A3B8;padding:4px 0;">📄 {f}</div>',
                            unsafe_allow_html=True)

    elif nav == "Riwayat":
        st.markdown("**🕐 Riwayat Percakapan**")
        if st.session_state.messages:
            user_msgs = [m for m in st.session_state.messages if m["role"] == "user"]
            for i, m in enumerate(user_msgs[-10:], 1):
                preview = m["content"][:50] + "..." if len(m["content"]) > 50 else m["content"]
                st.markdown(f'<div style="font-size:12px;color:#94A3B8;padding:6px 0;'
                            f'border-bottom:1px solid rgba(255,255,255,0.04);">'
                            f'💬 {preview}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="color:#475569;font-size:13px;">Belum ada riwayat.</div>',
                        unsafe_allow_html=True)
        if st.button("🗑️ Hapus Semua", use_container_width=True):
            st.session_state.messages = []
            st.session_state.gemini_history = []
            st.rerun()

    else:  # nav == "Chat" — tampilkan widget pasar
        # Status KB
        if st.session_state.db_loaded:
            st.markdown('<div style="color:#10B981;font-size:12px;padding:0 20px 8px;">● Knowledge base aktif</div>',
                        unsafe_allow_html=True)
        else:
            st.markdown('<div style="color:#F59E0B;font-size:12px;padding:0 20px 8px;">○ KB belum dimuat — buka Pengaturan</div>',
                        unsafe_allow_html=True)

        # Pasar Real-time
        st.markdown('<div style="padding:0 20px;font-size:12px;font-weight:600;color:#64748B;text-transform:uppercase;">Pasar Real-time</div>',
                    unsafe_allow_html=True)
        st.markdown("""
        <div class="mcard">
            <div class="lbl">USD / IDR</div>
            <div class="val">Rp 15.740</div>
            <div class="up">↗ +0.2%</div>
        </div>
        <div style="padding:8px 12px;font-size:12px;font-weight:600;color:#64748B;text-transform:uppercase;">
            SAHAM IDX
        </div>
        <div class="saham-grid">
            <div class="saham-card"><div class="ticker">BBCA</div><div class="chg-up">+0.5%</div></div>
            <div class="saham-card"><div class="ticker">BBRI</div><div class="chg-dn">-0.2%</div></div>
            <div class="saham-card"><div class="ticker">BMRI</div><div class="chg-up">+0.4%</div></div>
            <div class="saham-card"><div class="ticker">TLKM</div><div class="chg-dn">-0.3%</div></div>
        </div>
        """, unsafe_allow_html=True)

    # User profile (selalu di bawah)
    st.markdown('<div class="div" style="margin-top:auto;"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="profile">
        <div class="avatar">W</div>
        <div>
            <div style="font-size:13px;font-weight:600;color:#E2E8F0;">User Account</div>
            <div style="font-size:11px;color:#10B981;">Premium Member</div>
        </div>
    </div>
    <div style="text-align:center;font-size:11px;color:#334155;padding:8px 0 16px;">
        Powered by Gemini AI ✨
    </div>
    """, unsafe_allow_html=True)

# Ambil API key secara aman — server-side only, tidak dikirim ke browser
api_key = get_api_key()

# Banner jika API key belum dikonfigurasi
if not api_key:
    st.markdown("""
    <div style="background:rgba(245,158,11,0.1);border:1px solid rgba(245,158,11,0.4);
    border-radius:12px;padding:16px 20px;margin-bottom:16px;">
        <div style="font-size:15px;font-weight:600;color:#F59E0B;margin-bottom:6px;">
            ⚠️ API Key Belum Dikonfigurasi
        </div>
        <div style="font-size:13px;color:#94A3B8;line-height:1.6;">
            Untuk menggunakan NusaArtha AI, Anda perlu memasukkan <b>Gemini API Key</b> terlebih dahulu.<br>
            1. Buka menu <b>⚙️ Pengaturan</b> di sidebar kiri<br>
            2. Masukkan API Key Anda dan klik <b>💾 Simpan API Key</b><br>
            3. Dapatkan API Key gratis di 
            <a href="https://aistudio.google.com" target="_blank" 
               style="color:#10B981;">aistudio.google.com</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── MAIN AREA ─────────────────────────────────────────────────────────────────
now = datetime.now()
hour = now.hour
greeting = "Selamat Pagi" if hour < 11 else "Selamat Siang" if hour < 15 else "Selamat Sore"

# Header
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown(f"""
    <div style="padding:20px 0 8px;">
        <div style="font-size:28px;font-weight:700;color:#F8FAFC;">{greeting}! 👋</div>
        <div style="color:#64748B;font-size:14px;">{now.strftime('%A, %d %B %Y')}</div>
    </div>
    """, unsafe_allow_html=True)
with col_h2:
    st.markdown(f"""
    <div style="padding:20px 0 8px;display:flex;justify-content:flex-end;align-items:center;gap:12px;">
        <span class="disclaimer-badge">⚠️ Disclaimer: AI Advisor</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="div"></div>', unsafe_allow_html=True)

# ── Chat Area ─────────────────────────────────────────────────────────────────
LOGO_AVATAR = f'<img src="data:image/png;base64,{LOGO_B64}" width="22" style="border-radius:4px;">' if LOGO_B64 else "🤖"

# Pesan sambutan
if not st.session_state.messages:
    st.markdown(f"""
    <div class="ai-row">
        <div class="ai-avatar">{LOGO_AVATAR}</div>
        <div class="ai-bubble">
            Halo! Saya <b>NusaArtha AI</b>, asisten keuangan berbasis AI Anda.
            Ada yang bisa saya bantu hari ini terkait pajak, investasi, atau manajemen anggaran?
        </div>
    </div>
    """, unsafe_allow_html=True)

# Tampilkan riwayat chat
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="user-row">
            <div class="user-bubble">{msg["content"]}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        content = msg["content"].replace("\n", "<br>")
        sources_html = ""
        if msg.get("sources"):
            src_parts = []
            for s in msg["sources"]:
                page_val = s.get("page", "")
                page_txt = f" — Hal. {page_val + 1}" if page_val != "" else ""
                src_parts.append(
                    f'<div class="src-box">📄 <b>{s["source"]}</b>{page_txt}'
                    f'<br><span style="color:#CBD5E1">{s["preview"]}</span></div>'
                )
            src_items = "".join(src_parts)
            sources_html = f"""
            <details style="margin-top:10px;cursor:pointer;">
                <summary style="color:#F59E0B;font-size:12px;font-weight:600;">
                    ⊙ SUMBER DATA & DASAR HUKUM
                </summary>
                <div style="margin-top:8px;">{src_items}</div>
            </details>"""
        st.markdown(f"""
        <div class="ai-row">
            <div class="ai-avatar">{LOGO_AVATAR}</div>
            <div class="ai-bubble">{content}{sources_html}</div>
        </div>
        """, unsafe_allow_html=True)

# ── Quick Action Chips ────────────────────────────────────────────────────────
st.markdown('<div style="margin:8px 0 4px;"></div>', unsafe_allow_html=True)
chips = [
    ("💰 Hitung Pajak", "Saya bergaji Rp 9 juta/bulan status TK/0, berapa PPh 21 saya?"),
    ("📈 Info Saham", "Berapa harga saham BBCA sekarang?"),
    ("💱 Kurs Hari Ini", "Berapa kurs USD ke IDR sekarang?"),
    ("📊 Analisis Portfolio", "Apa rekomendasi alokasi portfolio untuk pemula?"),
]
cols = st.columns(len(chips))
for i, (label, prompt) in enumerate(chips):
    with cols[i]:
        if st.button(label, key=f"chip_{i}", use_container_width=True):
            st.session_state.pending_prompt = prompt
            st.rerun()

# ── Chat Input ────────────────────────────────────────────────────────────────
pending = st.session_state.pop("pending_prompt", "")
user_input = st.chat_input("Tanya soal pajak, investasi, keuangan...")
query = user_input or pending

if query:
    if not api_key:
        st.error("⚠️ Masukkan Gemini API Key terlebih dahulu di menu **⚙️ Pengaturan** di sidebar.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": query})

    with st.spinner("NusaArtha AI sedang berpikir..."):
        try:
            if st.session_state.mode == "rag":
                if not st.session_state.db_loaded or st.session_state.rag_chain is None:
                    resp = "⚠️ Knowledge base belum dimuat. Buka menu **Pengaturan** → klik **▶ Muat KB**."
                    sources = []
                else:
                    # rag_chain sekarang mengembalikan (answer, sources)
                    resp, sources = st.session_state.rag_chain(query)
                st.session_state.messages.append({"role": "assistant", "content": resp, "sources": sources})
            else:
                from gemini_agent import create_finance_agent, chat_with_function_calling
                if st.session_state.gemini_client is None:
                    st.session_state.gemini_client = create_finance_agent(api_key)
                resp, updated = chat_with_function_calling(
                    st.session_state.gemini_client, query, st.session_state.gemini_history)
                st.session_state.gemini_history = updated
                st.session_state.messages.append({"role": "assistant", "content": resp, "sources": []})
        except Exception as e:
            st.session_state.messages.append({"role": "assistant", "content": f"Error: {e}", "sources": []})

    st.rerun()
