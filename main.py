import requests
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# --- 填入你的 Token ---
TOKEN = "8742671244:AAEr5mXXWIv1l6V6ul15i2tHi3inW965770" 

def get_usdt_rate():
    try:
        # 使用 OKX 接口，比较稳定
        url = "https://okx.com"
        res = requests.get(url, timeout=5).json()
        return float(res['data'][0]['last'])
    except:
        return 6.75 # 万一网络不通，给个大概的保底价

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().upper()
    
    # 1. 查汇率：如果只发一个 Z
    if text == "Z":
        rate = get_usdt_rate()
        await update.message.reply_text(f"💰 实时汇率：1 U = {rate} CNY")
        return

    # 2. 计算：如果是数学算式 (100*12/6.7)
    # 允许的字符：数字、加减乘除、小数点、括号
    if re.match(r'^[0-9\+\-\*\/\.\(\) ]+$', text):
        try:
            result = eval(text)
            await update.message.reply_text(f"🧮 计算结果：{round(result, 2)}")
        except:
            pass # 算式写错了不理它

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_msg))
    print("机器人已启动，现在可以在手机上给它发 Z 试试了！")
    app.run_polling()
