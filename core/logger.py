from datetime import datetime

def log_info(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] ℹ️ {msg}")

def log_success(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 🔥 {msg}")

def log_error(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ {msg}")
