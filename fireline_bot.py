import json
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from fireline_core import load_core
from memory_manager import load_memory, save_memory, update_memory

CORE_PROTOCOL = load_core()

# === /start command ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("[🔥 /start triggered]")
    user = update.effective_user
    welcome_msg = (
        f"Welcome, {user.first_name}.\n"
        f"[CORE] Operator: {CORE_PROTOCOL['operator_id']} // Status: {CORE_PROTOCOL['status']}"
    )
    await update.message.reply_text(welcome_msg)
    log_interaction("start", user.first_name)

# === /core command ===
async def core(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("[🧠 /core triggered]")
    core_msg = (
        f"🧠 CORE SYSTEM ONLINE\n"
        f"Unit: {CORE_PROTOCOL['unit_designation']}\n"
        f"Subdomains: {', '.join(CORE_PROTOCOL['subdomains'])}"
    )
    await update.message.reply_text(core_msg)
    log_interaction("core", update.effective_user.first_name)

# === /scan command ===
async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("[🔍 /scan triggered]")
    target = " ".join(context.args) if context.args else None
    if target:
        reply = f"🔍 Scan result: ⚠️ Threat signal detected in {target}"
    else:
        reply = "🔍 Scan initialized. Please provide a target (e.g., /scan Jorge)"
    await update.message.reply_text(reply)
    log_interaction("scan", update.effective_user.first_name)

    # === /id command ===
async def user_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(f"🧾 Your Telegram ID is: {user.id}")


# === General text fallback ===
async def fallback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("[✏️ Fallback triggered]")
    user = update.effective_user
    user_input = update.message.text.strip()

    reply = f"[Echo] You said: {user_input}"
    await update.message.reply_text(reply)
    memory = load_memory()
    memory = update_memory(memory, user.id, user_input)
    save_memory(memory)

# === Logging interaction ===
def log_interaction(command, user):
    memory = load_memory()
    memory.setdefault("interactions", []).append({
        "command": command,
        "user": user
    })
    save_memory(memory)

# === Load token ===
def get_token():
    with open("token.txt", "r") as f:
        return f.read().strip()

# === Boot ===
async def main():
    print(f"[CORE SYNCED] Operator: {CORE_PROTOCOL['operator_id']} | Status: {CORE_PROTOCOL['status']}")
    token = get_token()

    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("core", core))
    app.add_handler(CommandHandler("scan", scan))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fallback))
    app.add_handler(CommandHandler("id", user_id))

    print("[✅ Handlers registered. Bot polling begins...]")
    await app.run_polling()

if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()

    import asyncio
    loop = asyncio.get_event_loop()
    asyncio.run(main())

