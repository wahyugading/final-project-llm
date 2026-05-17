# gemini_agent.py
# Gemini Agent dengan Function Calling — diadaptasi dari salinan_dari_gemini_part_2_avpn_it_data.py
# Menggunakan google-genai SDK (bukan LangChain) untuk Function Calling otomatis

from google import genai
from google.genai import types
from tools import ALL_TOOLS, get_exchange_rate, convert_currency, get_stock_info, calculate_pph21, calculate_investment_tax

# ─────────────────────────────────────────────
# System Instruction untuk Finance Agent
# (mengikuti pola dari notebook contoh)
# ─────────────────────────────────────────────

FINANCE_AGENT_INSTRUCTION = """Kamu adalah **Finance Copilot**, asisten keuangan AI pribadi untuk pengguna Indonesia.

Kamu memiliki akses ke tool-tool berikut yang harus kamu gunakan saat diperlukan:

1. **get_exchange_rate(from_currency, to_currency)** — Dapatkan kurs mata uang real-time
2. **convert_currency(amount, from_currency, to_currency)** — Konversi jumlah uang antar mata uang
3. **get_stock_info(ticker)** — Info harga saham IDX (BBCA, BBRI, BMRI, dll.)
4. **calculate_pph21(gaji_bruto, status)** — Hitung PPh 21 TER bulanan
5. **calculate_investment_tax(jenis_investasi, jumlah, jenis_transaksi)** — Hitung pajak investasi

**Kapan menggunakan tool:**
- Pertanyaan tentang kurs → gunakan get_exchange_rate atau convert_currency
- Pertanyaan tentang harga saham → gunakan get_stock_info
- Pertanyaan "berapa PPh 21 saya?" → gunakan calculate_pph21
- Pertanyaan pajak saham/crypto/reksadana → gunakan calculate_investment_tax

**Gaya komunikasi:**
- Profesional tapi ramah, seperti financial advisor yang peduli
- Berikan penjelasan yang jelas dan mudah dipahami
- Sertakan disclaimer untuk pertanyaan pajak/investasi yang kompleks
- Jawab dalam bahasa Indonesia

**Disclaimer wajib:**
Selalu ingatkan bahwa kamu adalah alat edukasi, bukan konsultan pajak/investasi berlisensi."""


def create_finance_agent(api_key: str):
    """
    Buat Gemini client untuk Function Calling.
    Mengikuti pola dari salinan_dari_gemini_part_2_avpn_it_data.py.
    """
    client = genai.Client(api_key=api_key)
    return client


def chat_with_function_calling(
    client,
    user_message: str,
    chat_history: list,
    model_id: str = "gemini-2.5-flash",
) -> tuple[str, list]:
    """
    Kirim pesan ke Gemini dengan dukungan Function Calling otomatis.
    Mengikuti pola dari salinan_dari_gemini_part_2_avpn_it_data.py.

    Args:
        client: Gemini client
        user_message: Pertanyaan dari user
        chat_history: Riwayat percakapan (list of dict)
        model_id: ID model Gemini yang digunakan

    Returns:
        (response_text, updated_history)
    """
    # Konfigurasi chat dengan tools dan system instruction
    # Persis seperti pola di notebook: client.chats.create(model=MODEL_ID, config={...})
    chat_config = types.GenerateContentConfig(
        system_instruction=FINANCE_AGENT_INSTRUCTION,
        tools=ALL_TOOLS,  # Automatic Function Calling
        temperature=0.2,
        top_p=0.95,
        top_k=20,
    )

    # Buat chat baru dengan history yang ada
    # Konversi format history dari Streamlit ke format Gemini
    gemini_history = []
    for msg in chat_history:
        role = msg["role"]
        content = msg["content"]
        gemini_history.append(
            types.Content(
                role=role,
                parts=[types.Part(text=content)],
            )
        )

    chat = client.chats.create(
        model=model_id,
        config=chat_config,
        history=gemini_history,
    )

    # Kirim pesan — SDK otomatis handle function calling loop
    response = chat.send_message(user_message)

    # Tambah ke history
    chat_history.append({"role": "user", "content": user_message})
    chat_history.append({"role": "model", "content": response.text})

    return response.text, chat_history


def count_tokens(client, text: str, model_id: str = "gemini-2.5-flash") -> int:
    """Hitung jumlah token untuk teks tertentu (seperti di notebook)."""
    try:
        result = client.models.count_tokens(model=model_id, contents=text)
        return result.total_tokens
    except Exception:
        return 0
