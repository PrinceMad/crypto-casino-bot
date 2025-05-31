import os
import random
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OWNER_WALLET = os.getenv("OWNER_WALLET")

bot = Bot(token=TOKEN)

jackpot_entries = []

def pick_winner():
    if not jackpot_entries:
        return None
    return random.choice(jackpot_entries)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Velkommen til CryptoCasino 🎰\nBruk /jackpot for å bli med i trekningen.")

async def jackpot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    address = context.args[0] if context.args else None
    if not address or not address.startswith("0x"):
        await update.message.reply_text("Skriv inn din wallet-adresse slik: /jackpot 0xD1Nwallet...")
        return
    jackpot_entries.append((user.username, address))
    await update.message.reply_text(f"{user.first_name} er med i jackpot! 🤑\nVi trekker vinner senere.")

async def draw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    winner = pick_winner()
    if winner:
        await update.message.reply_text(f"🎉 Vinneren er @{winner[0]} med adresse {winner[1]}! Gratulerer!")
    else:
        await update.message.reply_text("Ingen deltakere ennå. Bruk /jackpot for å bli med!")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("jackpot", jackpot))
app.add_handler(CommandHandler("draw", draw))

app.run_polling()
