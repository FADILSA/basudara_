import asyncio
from telethon import TelegramClient
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# === CONFIG ===
API_ID = 22224672   # ganti dengan API ID dari my.telegram.org
API_HASH = "ab86915fd2f484b55855f66dd3d7cecc"  # ganti API HASH
SESSION_NAME = "sidompul.session"  # session Telethon (harus login dulu)
BOT_TOKEN = "8209743796:AAEjJnZ0AvLiqU9nfZJrY5R2ju2OE0NbBxc"      # Token dari BotFather
SIDOMPUL_USERNAME = "dompetpulsabot"   # username bot Sidompul
XL_NUMBER = "087722590788"         # nomor XL disimpan di sini
INTER_DELAY = 5                    # delay antar pesan

# Telethon client
tele_client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# === Fungsi cek kuota ke Sidompul ===
async def cek_sidompul():
    async with tele_client:
        # 1. Kirim /start
        await tele_client.send_message(SIDOMPUL_USERNAME, "🔢Cek Nomor")
        await asyncio.sleep(INTER_DELAY)

        # 2. Klik menu 🔍 Cek Nomor
        msgs = await tele_client.get_messages(SIDOMPUL_USERNAME, limit=1)
        if msgs:
            try:
                await msgs[0].click(text="Detail Nomor")
            except Exception as e:
                return f"Gagal klik tombol: {e}"
        else:
            return "Tidak ada balasan setelah /start"
        await asyncio.sleep(1)

        # 3. Kirim nomor XL otomatis
        await tele_client.send_message(SIDOMPUL_USERNAME, XL_NUMBER)
        await asyncio.sleep(1)

        # 4. Ambil beberapa balasan terakhir
        replies = await tele_client.get_messages(SIDOMPUL_USERNAME, limit=5)
        for r in replies:
            if r.text and "Umur Kartu" in r.text:
                return r.text

        # fallback kalau ga ketemu
        return "Tidak ada detail kuota ditemukan"
# === Handler Bot Telegram ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Ketik /kuota untuk cek kuota XL otomatis.")

async def kuota(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Sedang cek kuota, tunggu sebentar...")
    try:
        hasil = await cek_sidompul()
    except Exception as e:
        hasil = f"Error: {e}"
    await update.message.reply_text(f"\n\n{hasil}")

# === Main ===
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("kuota", kuota))

    print("Bot berjalan... coba ketik /kuota di Telegram.")
    app.run_polling()

if __name__ == "__main__":
    main()

