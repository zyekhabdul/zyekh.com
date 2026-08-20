# [ BLUEPRINT ] Self-Hosted Sovereign Dynamic QRIS Engine & Omnichannel Architecture

Dokumen ini adalah spesifikasi arsitektur teknis untuk modul pembayaran mandiri (*self-hosted payment engine*) yang dihosting pada VPS `zyekh-ai-core`. Sistem ini menggantikan ketergantungan pada payment gateway pihak ketiga (seperti Pakasir) guna mengeliminasi risiko pembekuan saldo (*frozen funds*), biaya administrasi, dan penolakan produk digital/otomasi.

---

## 1. Arsitektur Topologi Sistem

```
┌─────────────────────────┐  ┌─────────────────────────┐  ┌─────────────────────────┐
│     Web Storefront      │  │      Bot Telegram       │  │      Bot WhatsApp       │
│  (zyekh.com/shop.zyekh) │  │     (bot-telegram)      │  │     (bot-whatsapp)      │
└────────────┬────────────┘  └────────────┬────────────┘  └────────────┬────────────┘
             │                            │                            │
             └────────────────────────────┼────────────────────────────┘
                                          │ (Internal REST / Socket)
                                          ▼
                     ┌──────────────────────────────────────────┐
                     │              zyekh-ai-core               │
                     │       (VPS Central Sovereign Hub)        │
                     ├──────────────────────────────────────────┤
                     │ • EMVCo ISO/IEC 18043 QRIS Generator     │
                     │ • Tag 54 & CRC16-CCITT Injection Engine  │
                     │ • Unique Code & Order State Pool         │
                     │ • Webhook Ingestor & Mutation Parser     │
                     │ • Multi-Channel Dispatch Adapter         │
                     └────────────────────┬─────────────────────┘
                                          │
                  ┌───────────────────────┴───────────────────────┐
                  ▼                                               ▼
     ┌────────────────────────┐                      ┌────────────────────────┐
     │   Bank / E-Wallet P2P  │                      │    Local Stock Vault   │
     │  (Direct to Merchant)  │                      │ (Tokens, Accounts, DB) │
     └────────────────────────┘                      └────────────────────────┘
```

---

## 2. Spesifikasi Standar EMVCo Dynamic QRIS

### A. Algoritma Injeksi Tag 54
Setiap string QRIS statis merchant (GoPay Usaha, Nobu, BCA, Dana Bisnis) memiliki struktur tag EMVCo terstandarisasi:
1. Menghapus 4 byte checksum terakhir (`6304XXXX`).
2. Menghapus tag `54` lama jika ada, atau menambahkan tag `54` baru:
   - Format: `54` + `panjang_string_nominal (2 digit)` + `nominal`.
   - Contoh untuk nominal Rp 25.104 -> `540525104`.
3. Menambahkan tag `58` (Country Code `ID`) jika belum ada.
4. Menambahkan prefix checksum `6304`.
5. Menghitung checksum `CRC16-CCITT (Polynomial 0x1021, Initial Value 0xFFFF)`.
6. Menggabungkan hasil hash 4 karakter heksadesimal kapital ke akhir string QRIS.

---

## 3. Alur Resolusi Pesanan (Order State Lifecycle)

1. **Request Checkout**: Client (Web, Telegram, WhatsApp) memanggil `POST /api/payment/create-qris` dengan payload:
   ```json
   {
     "amount": 25000,
     "channel": "telegram",
     "userId": "12345678",
     "items": ["cheatsheet_linux_pdf"]
   }
   ```
2. **Unique Code Allocation**: Sistem mengambil kode unik 3 digit (misal `104`), menetapkan `finalAmount = 25104`, status `PENDING`, dan TTL 15 menit.
3. **QR Code Rendering**: String QRIS dinamis dikonversi ke gambar PNG/Buffer dan dikirim langsung ke user.
4. **Mutation Match**:
   - Sumber mutasi (CekMutasi / Moota / Bank Daemon) menembak `POST /api/payment/webhook-mutation`.
   - Sistem mencocokkan `amount === 25104` dalam rentang waktu aktif.
   - Status pesanan berubah menjadi `PAID`.
5. **Auto-Dispatch**:
   - Jika channel `telegram`: Bot Telegram mengirim dokumen dari stock vault.
   - Jika channel `whatsapp`: Bot WhatsApp mengirim dokumen via Baileys socket.
   - Jika channel `web`: Memicu broadcast SSE/WebSocket agar browser langsung mengunduh file.

---

## 4. Keuntungan Strategis & Keamanan

- **Zero-Intermediary**: Dana 100% langsung masuk ke rekening pribadi/bisnis merchant secara instan.
- **Zero-Banning Risk**: Bebas dari risiko penutupan akun, pembekuan saldo, atau sensor jenis produk oleh payment gateway perantara.
- **Unified Omnichannel**: Satu backend `zyekh-ai-core` melayani seluruh frontend (Web, Telegram, WhatsApp, Mobile).
