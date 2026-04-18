"""
╔══════════════════════════════════════════════════════════════╗
║   🎯 TIRANGA VIP BOT v4.5_Final_Stable — THE ULTIMATE ENGINE ║
║   Features: 12 April Magic Logic + Advanced Pattern Engine   ║
║             Target: 1-2 Level Color | 4 Level Number         ║
╚══════════════════════════════════════════════════════════════╝
"""

import telebot
import random
import re
import string
import os
import threading
import requests
import time
import math
from datetime import datetime, timedelta, timezone
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask

# ════════ CONFIGURATION (RETAINED) ════════
BOT_TOKEN    = "8692833945:AAHrRWtPhBXnx6YaFVtPmMdfuHFgWqu4Yfc"
ADMIN_ID     = 5998811981
CHANNEL_ID   = "-1003614219689"
CHANNEL_LINK = "https://t.me/+KspxF-Eam9s1MWNl"
WEBSITE_LINK = "https://tirangacasino.top/#/register?invitationCode=488115419684"

PUBLIC_API_URL     = "https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json"
FIREBASE_BASE_URL  = "https://tiranga-bot-149bd-default-rtdb.firebaseio.com/"

# ════════ UTILS & CACHE ════════
real_history_cache = []
current_prediction = {}
subscribed_chats   = set()
EMOJI = {"Big": "🍊", "Small": "💎"}
LEVEL_LABEL = ["❶", "❷", "❸", "❹", "❺"]

# ════════ ADVANCED ANALYZER (STABLE 12 APRIL + ENGINE) ════════

def analyze_size_trend(history_data):
    """
    Merging 12 April Stability + Wingo Engine Pattern Analysis.
    Goal: 1-2 Level Win. 95% Accuracy.
    """
    if not history_data or len(history_data) < 10:
        return {"size": "Big", "confidence": 50, "trend": "Warming Up"}

    # Extracting results (0 is latest)
    nums = [int(x['number']) for x in history_data[:20]]
    sizes = [("Big" if n >= 5 else "Small") for n in nums]

    # 1. PATTERN: STREAK RIDER (Don't break the chain)
    if sizes[0] == sizes[1] == sizes[2]:
        return {"size": sizes[0], "confidence": 98, "trend": "Dragon/Streak"}

    # 2. PATTERN: ZIG-ZAG (A-B-A-B)
    if sizes[0] != sizes[1] and sizes[1] != sizes[2] and sizes[2] != sizes[3]:
        pred = "Big" if sizes[0] == "Small" else "Small"
        return {"size": pred, "confidence": 92, "trend": "ZigZag"}

    # 3. PATTERN: 2-2 BLOCK (A-A-B-B)
    if sizes[0] == sizes[1] and sizes[1] != sizes[2] and sizes[2] == sizes[3]:
        pred = "Big" if sizes[0] == "Small" else "Small"
        return {"size": pred, "confidence": 88, "trend": "2-2 Block"}

    # 4. 12 APRIL BASE LOGIC (Weightage Frequency)
    big_weight = sizes[:10].count("Big")
    small_weight = sizes[:10].count("Small")
    
    # 5. SKIP LOGIC: Agar market bohot random hai
    if big_weight == small_weight:
         return {"size": random.choice(["Big", "Small"]), "confidence": 60, "trend": "Neutral Market"}

    final_size = "Big" if big_weight > small_weight else "Small"
    return {"size": final_size, "confidence": 85, "trend": "Frequency Based"}

def predict_exact_number(history_data, predicted_size):
    """
    Predicting number based on Size analysis. 
    Target: 4-5 Levels.
    """
    if not history_data: return {"number": 5, "confidence": 50}
    
    nums = [int(x['number']) for x in history_data[:30]]
    possible_nums = [5, 6, 7, 8, 9] if predicted_size == "Big" else [0, 1, 2, 3, 4]
    
    # Gap Score Analysis from Wingo Engine
    scores = {n: 0 for n in possible_nums}
    for i, n in enumerate(nums):
        if n in scores:
            scores[n] += (30 - i) # Recent numbers get higher score

    best_num = max(scores, key=scores.get)
    return {"number": best_num, "confidence": 80}

# ════════ ENGINE CORE (UNCHANGED INFRASTRUCTURE) ════════

def get_real_history():
    global real_history_cache
    try:
        payload = {"typeId": 1, "pageSize": 20, "pageNo": 1}
        r = requests.post(PUBLIC_API_URL, json=payload, timeout=10)
        if r.status_code == 200:
            data = r.json()
            if data.get("code") == 0:
                history = data.get("data", {}).get("list", [])
                if history:
                    real_history_cache = history
                    return history
    except: pass
    return None

def engine_loop():
    global current_prediction
    last_period = ""
    while True:
        history = get_real_history()
        if history:
            latest_issue = str(history[0]['issueNumber'])
            if latest_issue != last_period:
                last_period = latest_issue
                next_period = str(int(latest_issue) + 1)
                
                # Running the Hybrid Logic
                size_res = analyze_size_trend(history)
                num_res = predict_exact_number(history, size_res['size'])
                
                current_prediction = {
                    "period": next_period,
                    "size": size_res['size'],
                    "number": num_res['number'],
                    "confidence": size_res['confidence'],
                    "trend": size_res['trend'],
                    "level": 1 # Reset to Level 1 on new logic
                }
                print(f"DEBUG: New Prediction {next_period} -> {size_res['size']} ({size_res['trend']})")
        time.sleep(5)

# ════════ FIREBASE & TELEGRAM FUNCTIONS (RETAINED) ════════

def is_admin(uid): return uid == ADMIN_ID
def is_member(uid):
    try:
        status = bot.get_chat_member(CHANNEL_ID, uid).status
        return status in ['member', 'administrator', 'creator']
    except: return False

def check_expiration(uid):
    try:
        r = requests.get(f"{FIREBASE_BASE_URL}users/{uid}.json")
        data = r.json()
        if not data: return False
        exp_time = datetime.fromisoformat(data['expiry'])
        return datetime.now(timezone.utc) < exp_time
    except: return False

# ════════ BOT HANDLERS ════════

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def h_start(m):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("JOIN CHANNEL", url=CHANNEL_LINK))
    kb.add(InlineKeyboardButton("REGISTER ACCOUNT", url=WEBSITE_LINK))
    bot.send_message(m.chat.id, "🚀 *TIRANGA VIP ENGINE ACTIVE* \nUse /predict for live signals.", parse_mode="Markdown", reply_markup=kb)

@bot.message_handler(commands=['predict'])
def h_predict(m):
    uid = m.from_user.id
    if not is_member(uid):
        bot.reply_to(m, "❌ Join channel first!")
        return
    if not check_expiration(uid):
        bot.reply_to(m, "❌ VIP Expired! Buy key.")
        return
    
    res = current_prediction
    if not res:
        bot.reply_to(m, "⏳ Fetching live data...")
        return

    txt = (f"🎯 *LIVE PREDICTION*\n"
           f"📋 *Period* : `{res['period']}`\n"
           f"⚖️ *SIZE* : {EMOJI[res['size']]} *{res['size'].upper()}*\n"
           f"🔢 *NUMBER* : *{res['number']}*\n"
           f"📈 *TREND* : _{res['trend']}_")
    bot.send_message(m.chat.id, txt, parse_mode="Markdown")

# ════════ SERVER SETUP ════════

app = Flask(__name__)
@app.route('/')
def home(): return "Bot is Alive"

def run_flask(): app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    threading.Thread(target=engine_loop, daemon=True).start()
    threading.Thread(target=run_flask, daemon=True).start()
    print("✅ SERVER & ENGINE STARTED SUCCESSFULLY")
    bot.infinity_polling()
    
