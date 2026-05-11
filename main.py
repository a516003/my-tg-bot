import os
import requests
import re
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# --- 1. 这里的网页部分是给 Koyeb 检查身体用的，不能删 ---
app = Flask('')
@app.route('/')
def home():
    return "Bot is running!"

def run():
    # Koyeb 默认使用 8080 端口
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- 2. 机器人逻辑 ---
TOKEN = "8742671244:AAEr5mXXWIv1l6V6ul15i2tHi3inW965770"

def get_okx_rate():
    try:
        url = "https://okx.com"
        res = requests.get(url, timeout=5).json()
        return float(res['data'][0]['idxPrice'])
    except:
        return 6.76

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    text = update.message.text.strip().upper()
    if text == "Z":
        rate = get_okx_rate()
        await update.message.reply_text(f"📊 欧意 C2C 参考价：\n1 USDT = {rate} CNY")
    elif re.match(r'^[0-9\+\-\*\/\.\(\) ]+$', text):
        try:
            res = eval(text)
            await update.message.reply_text(f"🧮 计算结果：{round(res, 2)}")
        except: pass

if __name__ == '__main__':
    keep_alive()  # 启动防休眠网页
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_msg))
    print("Bot started...")
    application.run_polling()
