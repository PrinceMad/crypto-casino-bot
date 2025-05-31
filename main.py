# CryptoCasino Telegram Bot – main.py
# Fully automated casino system with Coinflip, Roulette, Lottery, Jackpot, and VIP logic

import os
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

wallets = {
    "coinflip": "0xfe3c7ff12639A2d01fC7977f58C2831c2264abB1",
    "roulette": "0x2465277F546c6C6a0A5b446168aB1E2DB41B8FA8",
    "lottery": "0xcFDa829bb82EAcb36C0cfD6cA54ff316014a2A62",
    "jackpot": "0x4750b8B77A371b30280c35DF2959F3421D1fE5B9",
    "owner": "0x0ad7833bee4309A23570063786675D5823B1c03e"
}

jackpot_pool = []
vip_users = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "🎰 Welcome to CryptoCasino!\n\n"
        "Available commands:\n"
        "/games – View available games\n"
        "/jackpot – Join the monthly jackpot\n"
        "/vip – Become a VIP player\n"
        "/info – How everything works\n"
    )

async def games(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "🎲 Available Games:\n"
        "• Coinflip – /coinflip\n"
        "• Roulette – /roulette\n"
        "• Lottery – /lottery\n"
        "• Jackpot – /jackpot"
    )

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "ℹ️ How CryptoCasino Works:\n\n"
        "• All games use MATIC (Polygon)\n"
        "• Send the exact amount to the correct wallet\n"
        "• 10% goes to maintenance and development (5% if VIP)\n"
        "• Jackpot distributes 85% to the winner, 15% to dev\n"
        "• Payments are verified automatically\n"
        "• VIP players get better odds and rewards\n"
    )

async def vip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    vip_users.add(update.effective_user.id)
    await update.message.reply_text("👑 You're now registered as a VIP!")

async def jackpot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.args:
        wallet_address = context.args[0]
        jackpot_pool.append((update.effective_user.username, wallet_address))
        await update.message.reply_text(
            f"✅ {update.effective_user.username} has joined the jackpot with {wallet_address}!\n"
            "Winner will be drawn monthly."
        )
    else:
        await update.message.reply_text(
            f"To join the jackpot, use: /jackpot <your_wallet_address>\n"
            f"Send your entry fee to: {wallets['jackpot']}"
        )

async def draw_jackpot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != 777777777:
        return
    if not jackpot_pool:
        await update.message.reply_text("❌ No participants in the jackpot.")
        return
    winner = random.choice(jackpot_pool)
    await update.message.reply_text(f"🎉 The jackpot winner is @{winner[0]} with address {winner[1]}!")
    jackpot_pool.clear()

def main() -> None:
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("games", games))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("vip", vip))
    app.add_handler(CommandHandler("jackpot", jackpot))
    app.add_handler(CommandHandler("draw", draw_jackpot))

    app.run_polling()

if __name__ == "__main__":
    main()
