# tools.py
# Function Calling Tools — diadaptasi dari salinan_dari_gemini_part_2_avpn_it_data.py
# Tools ini akan dipanggil secara otomatis oleh Gemini lewat Automatic Function Calling

import requests
import json
from datetime import datetime


# ─────────────────────────────────────────────
# TOOL 1: Kurs Mata Uang Real-Time
# ─────────────────────────────────────────────

def get_exchange_rate(from_currency: str, to_currency: str) -> str:
    """
    Mendapatkan kurs tukar mata uang real-time.

    Args:
        from_currency: Kode mata uang asal, contoh: 'USD', 'EUR', 'SGD', 'JPY'
        to_currency: Kode mata uang tujuan, contoh: 'IDR', 'USD'

    Returns:
        String berisi kurs tukar terkini dan informasi konversi.
    """
    try:
        from_currency = from_currency.upper().strip()
        to_currency = to_currency.upper().strip()

        # Menggunakan API gratis exchangerate-api
        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()
            rate = data["rates"].get(to_currency)
            if rate:
                updated = data.get("date", "N/A")
                return (
                    f"Kurs {from_currency}/{to_currency}: {rate:,.4f}\n"
                    f"Artinya: 1 {from_currency} = Rp {rate:,.2f} {to_currency}\n"
                    f"Update terakhir: {updated}"
                )
            else:
                return f"Mata uang '{to_currency}' tidak ditemukan."
        else:
            # Fallback: gunakan data statis sebagai ilustrasi
            fallback_rates = {
                ("USD", "IDR"): 15740,
                ("EUR", "IDR"): 17020,
                ("SGD", "IDR"): 11650,
                ("JPY", "IDR"): 103,
                ("GBP", "IDR"): 19850,
                ("MYR", "IDR"): 3360,
            }
            rate = fallback_rates.get((from_currency, to_currency))
            if rate:
                return (
                    f"Kurs {from_currency}/{to_currency} (estimasi): {rate:,}\n"
                    f"1 {from_currency} ≈ Rp {rate:,} {to_currency}\n"
                    f"[Data estimasi — koneksi API tidak tersedia]"
                )
            return f"Tidak dapat mengambil kurs {from_currency}/{to_currency}."
    except Exception as e:
        return f"Error mengambil kurs: {str(e)}"


def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """
    Mengonversi sejumlah uang dari satu mata uang ke mata uang lain.

    Args:
        amount: Jumlah uang yang akan dikonversi (angka positif)
        from_currency: Kode mata uang asal, contoh: 'USD', 'EUR'
        to_currency: Kode mata uang tujuan, contoh: 'IDR'

    Returns:
        String berisi hasil konversi mata uang.
    """
    try:
        from_currency = from_currency.upper().strip()
        to_currency = to_currency.upper().strip()

        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()
            rate = data["rates"].get(to_currency)
            if rate:
                result = amount * rate
                return (
                    f"Konversi: {amount:,.2f} {from_currency} = {result:,.2f} {to_currency}\n"
                    f"Kurs saat ini: 1 {from_currency} = {rate:,.4f} {to_currency}"
                )
            return f"Mata uang '{to_currency}' tidak ditemukan."
        else:
            # Fallback static rates
            fallback_rates = {"USD": 15740, "EUR": 17020, "SGD": 11650, "JPY": 103}
            rate = fallback_rates.get(from_currency, 15000)
            result = amount * rate
            return (
                f"Konversi estimasi: {amount:,.2f} {from_currency} ≈ Rp {result:,.0f}\n"
                f"[Data estimasi — kurs aktual mungkin berbeda]"
            )
    except Exception as e:
        return f"Error konversi: {str(e)}"


# ─────────────────────────────────────────────
# TOOL 2: Informasi Saham IDX
# ─────────────────────────────────────────────

def get_stock_info(ticker: str) -> str:
    """
    Mendapatkan informasi harga saham dari Bursa Efek Indonesia (IDX).
    Bisa digunakan untuk saham seperti BBCA, BBRI, BMRI, TLKM, ASII, dll.

    Args:
        ticker: Kode saham IDX, contoh: 'BBCA', 'BBRI', 'TLKM', 'BMRI', 'UNVR'

    Returns:
        String berisi informasi harga saham terkini.
    """
    ticker = ticker.upper().strip()

    # Data saham IDX (estimasi — untuk demo, karena API IDX berbayar)
    # Dalam produksi bisa menggunakan Yahoo Finance (yfinance) atau IDX API
    sample_stocks = {
        "BBCA": {
            "name": "Bank Central Asia Tbk",
            "price": 9275,
            "change": +75,
            "change_pct": +0.82,
            "volume": "12.4M",
            "market_cap": "1.14T",
            "sector": "Perbankan",
        },
        "BBRI": {
            "name": "Bank Rakyat Indonesia Tbk",
            "price": 4210,
            "change": -30,
            "change_pct": -0.71,
            "volume": "45.2M",
            "market_cap": "636B",
            "sector": "Perbankan",
        },
        "BMRI": {
            "name": "Bank Mandiri Tbk",
            "price": 5525,
            "change": +25,
            "change_pct": +0.45,
            "volume": "28.1M",
            "market_cap": "516B",
            "sector": "Perbankan",
        },
        "TLKM": {
            "name": "Telekomunikasi Indonesia Tbk",
            "price": 2870,
            "change": -10,
            "change_pct": -0.35,
            "volume": "31.7M",
            "market_cap": "283B",
            "sector": "Telekomunikasi",
        },
        "ASII": {
            "name": "Astra International Tbk",
            "price": 4620,
            "change": +50,
            "change_pct": +1.09,
            "volume": "18.3M",
            "market_cap": "186B",
            "sector": "Otomotif",
        },
        "UNVR": {
            "name": "Unilever Indonesia Tbk",
            "price": 1810,
            "change": -15,
            "change_pct": -0.82,
            "volume": "5.6M",
            "market_cap": "69B",
            "sector": "Consumer Goods",
        },
        "GOTO": {
            "name": "GoTo Gojek Tokopedia Tbk",
            "price": 68,
            "change": +2,
            "change_pct": +3.03,
            "volume": "289M",
            "market_cap": "71B",
            "sector": "Teknologi",
        },
    }

    stock = sample_stocks.get(ticker)
    if stock:
        trend = "▲" if stock["change"] >= 0 else "▼"
        color_text = "naik" if stock["change"] >= 0 else "turun"
        return (
            f"📈 {ticker} — {stock['name']}\n"
            f"Harga: Rp {stock['price']:,}\n"
            f"Perubahan: {trend} Rp {abs(stock['change']):,} ({color_text} {abs(stock['change_pct']):.2f}%)\n"
            f"Volume: {stock['volume']} lembar\n"
            f"Market Cap: Rp {stock['market_cap']}\n"
            f"Sektor: {stock['sector']}\n"
            f"[Data ilustrasi per {datetime.now().strftime('%d %B %Y')}]"
        )
    else:
        return (
            f"Saham '{ticker}' tidak ditemukan dalam database.\n"
            f"Saham yang tersedia: BBCA, BBRI, BMRI, TLKM, ASII, UNVR, GOTO.\n"
            f"Untuk data lengkap IDX, kunjungi: idx.co.id"
        )


# ─────────────────────────────────────────────
# TOOL 3: Kalkulator Pajak PPh 21
# ─────────────────────────────────────────────

def calculate_pph21(gaji_bruto: float, status: str = "TK/0") -> str:
    """
    Menghitung estimasi PPh 21 bulanan menggunakan tarif TER (Tarif Efektif Rata-rata)
    berdasarkan PMK 168 Tahun 2023 yang berlaku mulai 2024.

    Args:
        gaji_bruto: Gaji bruto bulanan dalam Rupiah (contoh: 9000000 untuk Rp 9 juta)
        status: Status PTKP, pilihan: 'TK/0', 'TK/1', 'TK/2', 'TK/3', 'K/0', 'K/1', 'K/2', 'K/3'
                TK = Tidak Kawin, K = Kawin, angka = jumlah tanggungan

    Returns:
        String berisi detail perhitungan PPh 21 TER bulanan.
    """
    status = status.upper().strip()

    # Tabel TER Bulanan (PMK 168/2023) — Kategori A (TK/0 s.d. TK/3 dan K/0)
    # Kategori B: K/1, K/2, K/3
    # Bracket: (batas_bawah, batas_atas, tarif_persen)

    ter_a = [  # TK/0, TK/1, TK/2, TK/3, K/0
        (0, 5_400_000, 0),
        (5_400_001, 5_650_000, 0.25),
        (5_650_001, 5_950_000, 0.5),
        (5_950_001, 6_300_000, 0.75),
        (6_300_001, 6_750_000, 1.0),
        (6_750_001, 7_500_000, 1.25),
        (7_500_001, 8_550_000, 1.5),
        (8_550_001, 9_650_000, 2.0),
        (9_650_001, 10_050_000, 2.5),
        (10_050_001, 10_350_000, 3.0),
        (10_350_001, 10_700_000, 3.5),
        (10_700_001, 11_050_000, 4.0),
        (11_050_001, 11_600_000, 4.5),
        (11_600_001, 12_500_000, 5.0),
        (12_500_001, 13_750_000, 5.5),
        (13_750_001, 15_100_000, 6.0),
        (15_100_001, 16_950_000, 7.0),
        (16_950_001, 19_750_000, 8.0),
        (19_750_001, 24_150_000, 9.0),
        (24_150_001, 26_450_000, 10.0),
        (26_450_001, 28_000_000, 11.0),
        (28_000_001, 30_050_000, 12.0),
        (30_050_001, 32_400_000, 13.0),
        (32_400_001, 35_400_000, 14.0),
        (35_400_001, 39_100_000, 15.0),
        (39_100_001, 43_850_000, 16.0),
        (43_850_001, 47_800_000, 17.0),
        (47_800_001, 51_400_000, 18.0),
        (51_400_001, 56_300_000, 19.0),
        (56_300_001, 62_200_000, 20.0),
        (62_200_001, 74_500_000, 21.0),
        (74_500_001, 86_000_000, 22.0),
        (86_000_001, 133_000_000, 23.0),
        (133_000_001, 173_000_000, 24.0),
        (173_000_001, 350_000_000, 25.0),
        (350_000_001, 900_000_000, 30.0),
        (900_000_001, float("inf"), 35.0),
    ]

    ter_b = [  # K/1, K/2, K/3
        (0, 6_200_000, 0),
        (6_200_001, 6_500_000, 0.25),
        (6_500_001, 6_850_000, 0.5),
        (6_850_001, 7_300_000, 0.75),
        (7_300_001, 9_200_000, 1.0),
        (9_200_001, 10_750_000, 1.5),
        (10_750_001, 11_250_000, 2.0),
        (11_250_001, 11_600_000, 2.5),
        (11_600_001, 12_600_000, 3.0),
        (12_600_001, 13_600_000, 4.0),
        (13_600_001, 14_950_000, 5.0),
        (14_950_001, 16_400_000, 6.0),
        (16_400_001, 18_450_000, 7.0),
        (18_450_001, 21_850_000, 8.0),
        (21_850_001, 26_000_000, 9.0),
        (26_000_001, float("inf"), 34.0),  # simplified
    ]

    use_b = status in ["K/1", "K/2", "K/3"]
    tabel = ter_b if use_b else ter_a

    tarif = 0.0
    for bawah, atas, t in tabel:
        if bawah <= gaji_bruto <= atas:
            tarif = t
            break

    pph_bulanan = gaji_bruto * (tarif / 100)
    gaji_neto = gaji_bruto - pph_bulanan

    return (
        f"=== Estimasi PPh 21 TER Bulanan ===\n"
        f"Status PTKP: {status}\n"
        f"Gaji Bruto: Rp {gaji_bruto:,.0f}\n"
        f"Tarif TER: {tarif:.2f}%\n"
        f"PPh 21 Dipotong: Rp {pph_bulanan:,.0f}\n"
        f"Gaji Take-Home: Rp {gaji_neto:,.0f}\n"
        f"─────────────────────────────────\n"
        f"Dasar hukum: PMK 168/2023 (berlaku Januari 2024)\n"
        f"⚠️ Ini adalah estimasi. PPh akhir tahun dihitung ulang dengan tarif Pasal 17."
    )


# ─────────────────────────────────────────────
# TOOL 4: Kalkulator Pajak Investasi
# ─────────────────────────────────────────────

def calculate_investment_tax(
    jenis_investasi: str, jumlah: float, jenis_transaksi: str = "jual"
) -> str:
    """
    Menghitung pajak atas transaksi investasi (saham, crypto, reksadana, obligasi).

    Args:
        jenis_investasi: Jenis aset: 'saham', 'crypto', 'reksadana', 'obligasi', 'dividen'
        jumlah: Nilai transaksi atau keuntungan dalam Rupiah
        jenis_transaksi: 'jual', 'beli', 'dividen', 'kupon'

    Returns:
        String berisi rincian pajak yang harus dibayar.
    """
    jenis = jenis_investasi.lower().strip()
    transaksi = jenis_transaksi.lower().strip()

    if jenis == "saham":
        if transaksi in ["jual", "beli"]:
            # PPh Final 0.1% dari nilai transaksi (bukan profit)
            pajak = jumlah * 0.001
            return (
                f"=== Pajak Saham — {transaksi.title()} ===\n"
                f"Nilai Transaksi: Rp {jumlah:,.0f}\n"
                f"PPh Final: 0.1% × Rp {jumlah:,.0f} = Rp {pajak:,.0f}\n"
                f"Dipotong otomatis oleh sekuritas saat transaksi.\n"
                f"Dasar: PP 41/1994 jo PP 55/2022"
            )
        elif transaksi == "dividen":
            pajak = jumlah * 0.10
            return (
                f"=== Pajak Dividen Saham ===\n"
                f"Dividen Diterima: Rp {jumlah:,.0f}\n"
                f"PPh Final Dividen: 10% = Rp {pajak:,.0f}\n"
                f"Dipotong emiten sebelum dividen diterima.\n"
                f"Dasar: PP 9/2021"
            )

    elif jenis == "crypto":
        # PPh 22 Final 0.1% untuk CEX (Bursa), 0.2% untuk non-bursa
        # Per PMK 68/2022 jo PMK 50/2025
        pajak_cex = jumlah * 0.001
        return (
            f"=== Pajak Crypto ===\n"
            f"Nilai Transaksi: Rp {jumlah:,.0f}\n"
            f"PPh 22 Final (via bursa OJK): 0.1% = Rp {pajak_cex:,.0f}\n"
            f"PPN (via bursa OJK): 0.11% = Rp {jumlah * 0.0011:,.0f}\n"
            f"Total dipotong platform: Rp {jumlah * 0.0021:,.0f}\n"
            f"Dipotong otomatis oleh platform (Indodax, Pintu, dll).\n"
            f"Dasar: PMK 50/2025"
        )

    elif jenis == "reksadana":
        pajak = jumlah * 0.10
        return (
            f"=== Pajak Reksadana ===\n"
            f"Capital Gain / Dividen: Rp {jumlah:,.0f}\n"
            f"PPh Final: 10% = Rp {pajak:,.0f}\n"
            f"Dipotong oleh Manajer Investasi saat pencairan.\n"
            f"Dasar: PP 55/2022"
        )

    elif jenis in ["obligasi", "obligasi"]:
        if transaksi == "kupon":
            pajak = jumlah * 0.10
            return (
                f"=== Pajak Kupon Obligasi ===\n"
                f"Kupon Diterima: Rp {jumlah:,.0f}\n"
                f"PPh Final Kupon: 10% = Rp {pajak:,.0f}\n"
                f"Dipotong otomatis saat kupon dibayar.\n"
                f"Dasar: PP 91/2021"
            )
        else:
            pajak = jumlah * 0.001
            return (
                f"=== Pajak Jual Obligasi ===\n"
                f"Nilai Transaksi: Rp {jumlah:,.0f}\n"
                f"PPh Final Capital Gain: 0.1% = Rp {pajak:,.0f}\n"
                f"Dasar: PP 91/2021"
            )

    return (
        f"Jenis investasi '{jenis_investasi}' belum dikenali.\n"
        f"Pilihan: saham, crypto, reksadana, obligasi"
    )


# ─────────────────────────────────────────────
# Daftar semua tools untuk Gemini Function Calling
# ─────────────────────────────────────────────

ALL_TOOLS = [
    get_exchange_rate,
    convert_currency,
    get_stock_info,
    calculate_pph21,
    calculate_investment_tax,
]
