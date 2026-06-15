import requests
import time
from flask import Flask
from threading import Thread

# --- إعدادات البوت ---
TOKEN = 'ا8852086212:AAEZuLMYSR6j0hEvw-wmlDNyEdBzu-m2YgQ'
CHANNEL_ID = '@ffffq0'

# --- كود الـ Flask للحفاظ على البوت مستيقظاً ---
app = Flask('')

@app.route('/')
def home():
    return "البوت يعمل الآن!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- دالة جلب السعر ---
def get_ton_price():
    # نستخدم CoinGecko لأنه أكثر استقراراً في الاستضافات المجانية
    url = "https://api.coingecko.com/api/v3/simple/price?ids=the-open-network&vs_currencies=usd"
    response = requests.get(url).json()
    return response['the-open-network']['usd']

# --- دالة إرسال الرسالة ---
def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {'chat_id': CHANNEL_ID, 'text': text}
    requests.post(url, data=params)

# --- تشغيل البوت ---
keep_alive()

print("البوت بدأ بالعمل...")

while True:
    try:
        price = get_ton_price()
        message = f" {price} $"
        send_message(message)
        print(f"تم إرسال السعر: {price}")
    except Exception as e:
        print(f"خطأ في الاتصال: {e}")
    
    # تحديث كل 5 دقائق (300 ثانية) لتجنب الحظر من الموقع
    time.sleep(300)
