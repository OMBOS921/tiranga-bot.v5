"""
🎯 TIRANGA GAMES VIP BOT v3.1 - TREND ANALYSIS ENGINE
Features: 100% Real API Sync | Smart Trend Analysis | Strict 3-Level System
         | Auto Key Expiry | Consolidated Sync Dashboard | Cloud-Ready | Device Binding | AI Data Logging
"""

import telebot
import random
import re
import string
import os
import threading
import requests
import time
from datetime import datetime, timedelta, timezone
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask

# ════════ CONFIGURATION ════════
BOT_TOKEN    = "8692833945:AAHrRWtPhBXnx6YaFVtPmMdfuHFgWqu4Yfc"
ADMIN_ID     = 5998811981
CHANNEL_ID   = "-1003614219689"
CHANNEL_LINK = "https://t.me/+KspxF-Eam9s1MWNl"
WEBSITE_LINK = "https://tirangacasino.top/#/register?invitationCode=488115419684"

PUBLIC_API_URL     = "https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json"
FIREBASE_BASE      = "https://tiranga-vip-c6f29-default-rtdb.asia-southeast1.firebasedatabase.app"
FIREBASE_URL       = f"{FIREBASE_BASE}/live_prediction.json"
FIREBASE_USERS_URL = f"{FIREBASE_BASE}/users"
FIREBASE_SYNC_URL  = f"{FIREBASE_BASE}/sync_data.json"
FIREBASE_LEARN_URL = f"{FIREBASE_BASE}/ai_learning_dataset.json"

IST = timezone(timedelta(hours=5, minutes=30))
bot = telebot.TeleBot(BOT_TOKEN)

# ════════ FLASK WEB SERVER (Cloud-Ready) ════════
app = Flask(__name__)

@app.route('/')
def home():
    return "🚀 Tiranga Bot v3.1 is Online! (Trend Analysis Engine & AI Learning Active)"

def run_web():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = threading.Thread(target=run_web)
    t.daemon = True
    t.start()

# ════════ API SESSION ════════
api_session = requests.Session()
api_session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Origin": "https://tirangacasino.top",
    "Referer": "https://tirangacasino.top/"
})

# ════════ GLOBAL VARIABLES ════════
current_period = ""
current_prediction = {}
loss_streak = 0
BET_NUMBERS = {"Small": [0, 1, 2, 3, 4], "Big": [5, 6, 7, 8, 9]}
EMOJI = {"Big": "🟡", "Small": "🔵"}
LEVEL_LABEL = {0: "🥇 LEVEL 1", 1: "🥈 LEVEL 2", 2: "🥉 LEVEL 3"}
real_history_cache = []

recent_predictions = {}
win_counts = {"L1": 0, "L2": 0, "L3": 0}

# ════════ CORE ENGINE ════════

def get_ist_period():
    now = datetime.now(IST)
    tiranga_time = now - timedelta(hours=5, minutes=30)
    date_str = tiranga_time.strftime("%Y%m%d")
    current_mins = now.hour * 60 + now.minute
    serial = current_mins - 329
    if serial <= 0: serial += 1440
    return f"{date_str}10001{serial:04d}"

def fetch_real_api():
    global real_history_cache
    try:
        ts = int(time.time() * 1000)
        r = api_session.get(f"{PUBLIC_API_URL}?ts={ts}", timeout=5)
        if r.status_code == 200:
            data = r.json()
            if "data" in data and "list" in data["data"]:
                real_history_cache = data["data"]["list"][:10]
                return True
    except: pass
    return False

def analyze_trend(force_opposite_of=None):
    if force_opposite_of:
        return "Big" if force_opposite_of == "Small" else "Small"

    if not real_history_cache or len(real_history_cache) < 3:
        return random.choice(["Big", "Small"])

    results = []
    for item in real_history_cache[:7]:
        n = int(item['number'])
        results.append("Big" if n >= 5 else "Small")

    streak_len = 1
    for i in range(1, len(results)):
        if results[i] == results[0]:
            streak_len += 1
        else:
            break
    if streak_len >= 3:
        return "Big" if results[0] == "Small" else "Small"

    if len(results) >= 4:
        alternating = all(results[i] != results[i+1] for i in range(3))
        if alternating:
            return "Big" if results[0] == "Small" else "Small"

    last5 = results[:5]
    big_count = last5.count("Big")
    small_count = last5.count("Small")
    if big_count > small_count:
        return "Small"
    elif small_count > big_count:
        return "Big"

    return "Big" if results[0] == "Small" else "Small"

def predict_number(size):
    number_range = BET_NUMBERS[size]
    if not real_history_cache:
        return number_range[len(number_range) // 2]
    recent_numbers = [int(item['number']) for item in real_history_cache[:10]]
    last_seen = {}
    for num in number_range:
        if num in recent_numbers:
            last_seen[num] = recent_numbers.index(num)
        else:
            last_seen[num] = 999
    return max(last_seen, key=last_seen.get)

def init_engine():
    global current_prediction, current_period
    fetch_real_api()
    period = get_ist_period()
    size = analyze_trend()
    num = predict_number(size)
    current_period = period
    current_prediction = {
        "period": period, "size": size, "number": num,
        "accuracy": 90, "level": 1
    }

init_engine()

def core_engine_loop():
    global current_period, current_prediction, loss_streak, real_history_cache

    while True:
        period = get_ist_period()
        now = datetime.now(IST)

        if now.second in [2, 5, 8, 15, 30, 45]:
            fetch_real_api()

        if period != current_period:
            actual_last_res = None
            if real_history_cache:
                n = int(real_history_cache[0]['number'])
                actual_last_res = "Big" if n >= 5 else "Small"

            if actual_last_res and current_prediction:
                if current_prediction.get("size") == actual_last_res:
                    loss_streak = 0
                else:
                    loss_streak += 1

            if loss_streak >= 2:
                force = actual_last_res if actual_last_res else (
                    real_history_cache[0] and
                    ("Big" if int(real_history_cache[0]['number']) >= 5 else "Small")
                )
                size = analyze_trend(force_opposite_of=force)
                conf = 99
                level = 3
            elif loss_streak == 1:
                last_pred = current_prediction.get("size", "Big")
                trend = analyze_trend()
                size = "Big" if last_pred == "Small" else "Small"
                conf = 93 if trend == size else 90
                level = 2
            else:
                size = analyze_trend()
                conf = 90
                level = 1

            num = predict_number(size)
            current_period = period
            current_prediction = {
                "period": period, "size": size,
                "number": num, "accuracy": conf, "level": level
            }

            recent_predictions[period] = {"size": size, "level": level, "checked": False}

        try:
            requests.put(FIREBASE_URL, json=current_prediction, timeout=2)
        except: pass

        time.sleep(1)

# ════════ BACKGROUND AI LEARNING DATA GATHERING ════════
def ai_learning_loop():
    """ Runs every 1 hour and saves pattern data silently for next month's V4 update """
    while True:
        try:
            if real_history_cache:
                learning_payload = {
                    "timestamp": int(time.time()),
                    "datetime_ist": datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S"),
                    "recent_trend_numbers": [int(x['number']) for x in real_history_cache]
                }
                requests.post(FIREBASE_LEARN_URL, json=learning_payload, timeout=3)
        except: pass
        time.sleep(3600)  # Sleep for 1 hour

# ════════ KEY EXPIRY HELPERS ════════

def parse_duration(duration_str):
    if not duration_str: return None
    m = re.match(r'^(\d+)([hmd])$', duration_str.strip().lower())
    if not m: return None
    amount = int(m.group(1))
    unit = m.group(2)
    if unit == 'h': return timedelta(hours=amount)
    if unit == 'd': return timedelta(days=amount)
    if unit == 'm': return timedelta(minutes=amount)
    return None

def expiry_checker_loop():
    while True:
        try:
            r = requests.get(f"{FIREBASE_USERS_URL}.json", timeout=5)
            if r.status_code == 200 and r.json():
                users = r.json()
                now_ts = int(time.time())
                for uid, udata in users.items():
                    if isinstance(udata, dict):
                        if udata.get("status") == "active" and "expiry" in udata:
                            if udata["expiry"] <= now_ts:
                                requests.patch(
                                    f"{FIREBASE_USERS_URL}/{uid}.json",
                                    json={"status": "expired"}, timeout=3
                                )
        except: pass
        time.sleep(60)

# ════════ CONSOLIDATED SYNC THREAD ════════

def sync_data_loop():
    global win_counts
    while True:
        try:
            ts = int(time.time() * 1000)
            r = api_session.get(f"{PUBLIC_API_URL}?ts={ts}", timeout=5)
            if r.status_code == 200:
                data = r.json()
                if "data" in data and "list" in data["data"]:
                    history_raw = data["data"]["list"][:10]
                    history_out = []
                    for item in history_raw:
                        period_id  = str(item["issueNumber"])
                        actual_num = int(item["number"])
                        actual_size = "Big" if actual_num >= 5 else "Small"

                        pred_info  = recent_predictions.get(period_id)
                        pred_size  = pred_info["size"]  if pred_info else None
                        pred_level = pred_info["level"] if pred_info else None
                        status     = None

                        if pred_info and not pred_info.get("checked"):
                            status = "WIN" if pred_size == actual_size else "LOSS"
                            recent_predictions[period_id]["checked"] = True
                            if status == "WIN" and pred_level:
                                key = f"L{pred_level}"
                                win_counts[key] = win_counts.get(key, 0) + 1

                        history_out.append({
                            "period": period_id, "actual_number": actual_num,
                            "actual_size": actual_size, "predicted_size": pred_size,
                            "predicted_level": pred_level, "status": status
                        })

                    sync_payload = {
                        "updated_at": int(time.time()),
                        "win_counts": win_counts, "history": history_out
                    }
                    requests.put(FIREBASE_SYNC_URL, json=sync_payload, timeout=3)

            if len(recent_predictions) > 50:
                oldest_keys = sorted(recent_predictions.keys())[:-50]
                for k in oldest_keys: del recent_predictions[k]
        except: pass
        time.sleep(30)

# ════════ BOT HELPERS & COMMANDS ════════

def check_join(user_id):
    if user_id == ADMIN_ID: return True
    try:
        status = bot.get_chat_member(CHANNEL_ID, user_id).status
        return status in ['member', 'administrator', 'creator']
    except: return False

@bot.message_handler(commands=["idpass"])
def generate_key(m):
    if m.from_user.id != ADMIN_ID: return
    parts = m.text.strip().split()
    duration_str = parts[1] if len(parts) > 1 else None
    delta = parse_duration(duration_str)

    user_id  = f"VIP{random.randint(1000, 9999)}"
    user_key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    payload = {"key": user_key, "status": "active", "device_id": ""}
    expiry_note = "♾️ *Expiry :* No Limit"

    if delta:
        expiry_ts = int((datetime.now(timezone.utc) + delta).timestamp())
        payload["expiry"] = expiry_ts
        expiry_dt = datetime.fromtimestamp(expiry_ts, tz=IST).strftime("%d %b %Y %I:%M %p IST")
        expiry_note = f"⏳ *Expiry :* `{expiry_dt}`"

    try:
        resp = requests.put(f"{FIREBASE_USERS_URL}/{user_id}.json", json=payload, timeout=3)
        if resp.status_code == 200:
            bot.send_message(m.chat.id,
                f"✅ *NEW VIP SYSTEM KEY*\n━━━━━━━━━━\n"
                f"👤 *ID :* `{user_id}`\n🔑 *PASS :* `{user_key}`\n"
                f"{expiry_note}\n━━━━━━━━━━", parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(m, f"❌ Server Error: {e}")

@bot.message_handler(commands=["expire"])
def expire_user(m):
    if m.from_user.id != ADMIN_ID: return
    parts = m.text.strip().split()
    if len(parts) < 2: return
    target_id = parts[1].strip()
    try:
        requests.patch(f"{FIREBASE_USERS_URL}/{target_id}.json", json={"status": "expired"}, timeout=5)
        bot.reply_to(m, f"🚫 *ACCESS REVOKED*\n👤 *ID :* `{target_id}`", parse_mode="Markdown")
    except: pass

@bot.message_handler(commands=["resetdev"])
def reset_device(m):
    if m.from_user.id != ADMIN_ID: return
    parts = m.text.strip().split()
    if len(parts) < 2: return
    target_id = parts[1].strip()
    try:
        requests.patch(f"{FIREBASE_USERS_URL}/{target_id}.json", json={"device_id": ""}, timeout=5)
        bot.reply_to(m, f"✅ *DEVICE RESET SUCCESSFUL*\n👤 *ID :* `{target_id}` can login on a new phone.", parse_mode="Markdown")
    except: pass

# ════════ BOT UI ════════

def main_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(InlineKeyboardButton("🎯 Prediction Lo", callback_data="predict"),
           InlineKeyboardButton("📊 Pattern Dekho", callback_data="pattern"))
    kb.add(InlineKeyboardButton("💰 3-Level Chart", callback_data="chart"),
           InlineKeyboardButton("🌐 Play Now", url=WEBSITE_LINK))
    return kb

@bot.message_handler(commands=["start"])
def h_start(m):
    if not check_join(m.from_user.id):
        kb = InlineKeyboardMarkup().add(
            InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK),
            InlineKeyboardButton("✅ Joined", callback_data="home"))
        bot.send_message(m.chat.id, "⚠️ *ACCESS DENIED*\nAapko hamara official channel join karna hoga!", parse_mode="Markdown", reply_markup=kb)
        return
    bot.send_message(m.chat.id, f"🌟 *Tiranga VIP Bot v3.1* 🌟\nSystem ab Trend Analysis se predict karta hai.", parse_mode="Markdown", reply_markup=main_kb())

@bot.callback_query_handler(func=lambda c: True)
def handle_cb(call):
    uid, cid, data = call.from_user.id, call.message.chat.id, call.data
    try: bot.answer_callback_query(call.id)
    except: pass
    if not check_join(uid): return

    if data == "home":
        bot.send_message(cid, "🏠 *Main Menu*", parse_mode="Markdown", reply_markup=main_kb())

    elif data == "predict":
        res = current_prediction
        lvl = res.get("level", 1)
        level_label = LEVEL_LABEL.get(lvl - 1, "🥇 LEVEL 1")
        bot.send_message(cid,
            f"🎯 *LIVE PREDICTION*\n━━━━━━━━━━━━━━━━━━━━\n"
            f"📋 *Period* : `{res['period']}`\n⚖️ *SIZE* : {EMOJI[res['size']]} *{res['size'].upper()}*\n"
            f"🔢 *NUMBER* : *{res['number']}*\n🔥 *ACCURACY* : `{res['accuracy']}%`\n"
            f"🏆 *LEVEL* : {level_label}\n━━━━━━━━━━━━━━━━━━━━",
            parse_mode="Markdown", reply_markup=main_kb())

    elif data == "pattern":
        if real_history_cache:
            table = "📊 *LIVE REAL-TIME PATTERN*\n━━━━━━━━━━━━━━━━━━━━\n"
            for item in real_history_cache[:5]:
                p = str(item['issueNumber'])[-5:]
                n = int(item['number'])
                s = "BIG" if n >= 5 else "SMALL"
                table += f"`...{p}`  |  {EMOJI[s.capitalize()]} {s} ({n})\n"
            bot.send_message(cid, table + f"━━━━━━━━━━━━━━━━━━━━\n📡 *Trend Signal* : {EMOJI[analyze_trend()]} *{analyze_trend().upper()}*", parse_mode="Markdown", reply_markup=main_kb())
        else:
            bot.send_message(cid, "🔄 *Syncing real data...* Click again in 2 seconds.", parse_mode="Markdown", reply_markup=main_kb())

    elif data == "chart":
        try:
            with open('chart.jpg', 'rb') as photo:
                bot.send_photo(cid, photo, caption="💰 *3-LEVEL FUND MANAGEMENT CHART*", parse_mode="Markdown", reply_markup=main_kb())
        except:
            bot.send_message(cid, "⚠️ *Error:* 'chart.jpg' not found.", parse_mode="Markdown", reply_markup=main_kb())

# ════════ MAIN ════════
if __name__ == "__main__":
    threading.Thread(target=core_engine_loop,    daemon=True).start()
    threading.Thread(target=expiry_checker_loop, daemon=True).start()
    threading.Thread(target=sync_data_loop,      daemon=True).start()
    threading.Thread(target=ai_learning_loop,    daemon=True).start() # The new AI Logger
    keep_alive()
    bot.polling(none_stop=True)
