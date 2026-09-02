import streamlit as st
import sqlite3
import hashlib
import random
import pandas as pd
import numpy as np
import plotly.express as px
import requests
from datetime import datetime, timedelta

try:
    from streamlit_autorefresh import st_autorefresh
except ImportError:
    st_autorefresh = None

# --- CONSTANTES Y CONFIGURACIONES ---
VIP_BADGE_B64 = "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAUDBAQEAwUEBAQFBQUGBwwIBwcHBw8LCwkMEQ8SEhEPERETFhwXExQaFRERGCEYGh0dHx8fExciJCIeJBweHx7/2wBDAQUFBQcGBw4ICA4eFBEUHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh7/wAARCADIAMgDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD4zNFJRQAuaKKKACiiigAozRQBQAUU4LmnCMmrUGwI8GjBqwsRParaYaj/CfyrVYeTFcrYNJg1c+zv/df+VNaBh/Cfyp/VpdguVcGjmp2iNMKEVm6TQXI80ZpxWmkVm4tDDNFJS0gCiiigA7UUUlAC0UU"

# Configuración de página de Streamlit
st.set_page_config(
    page_title="Alianza CryptoWallet v31",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

if st_autorefresh is not None:
    st_autorefresh(interval=10000, key="datarefresh") # Auto-refresh cada 10 segundos

# --- BASE DE DATOS Y CONFIGURACIÓN ---
def init_db():
    conn = sqlite3.connect("wallet_pro.db")
    cursor = conn.cursor()
    
    # 1. Tabla de usuarios
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        fullname TEXT,
        email TEXT,
        wallet_code TEXT UNIQUE,
        balance REAL DEFAULT 0.0,
        is_admin INTEGER DEFAULT 0,
        balance_cop REAL DEFAULT 0.0,
        is_vip INTEGER DEFAULT 0,
        nequi_number TEXT DEFAULT '',
        referred_by TEXT
    )
    """)
    
    # 2. Tabla de transacciones entre usuarios
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender_code TEXT,
        receiver_code TEXT,
        amount REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # 3. Tabla de configuraciones del token personalizado
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS token_settings (
        id INTEGER PRIMARY KEY DEFAULT 1,
        token_name TEXT DEFAULT 'SIAD',
        token_symbol TEXT DEFAULT 'SD',
        token_contract TEXT DEFAULT '0xC324649213ec1757190bc4b78bcD41Cc1545C264',
        token_price_usd REAL DEFAULT 0.50,
        nequi_number TEXT DEFAULT '3001234567'
    )
    """)
    
    # Asegurar que existan configuraciones iniciales
    cursor.execute("INSERT OR IGNORE INTO token_settings (id, token_name, token_symbol, token_contract, token_price_usd, nequi_number) VALUES (1, 'SIAD', 'SD', '0xC324649213ec1757190bc4b78bcD41Cc1545C264', 0.50, '3001234567')")
    
    # 4. Tabla de solicitudes de compra (Comprobantes)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS purchase_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_code TEXT,
        amount_cop REAL,
        amount_sd REAL,
        proof_image BLOB,
        status TEXT DEFAULT 'PENDING',
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # 5. Tabla de comisiones por referidos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS referral_rewards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        referrer_code TEXT,
        referred_code TEXT,
        purchase_id INTEGER,
        purchase_amount_sd REAL,
        reward_amount_sd REAL,
        status TEXT DEFAULT 'PENDING',
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # 6. Tabla de solicitudes de retiro (Withdrawals)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS withdrawal_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_code TEXT,
        amount_cop REAL,
        fee_cop REAL,
        net_cop REAL,
        nequi_number TEXT,
        receipt_image BLOB,
        status TEXT DEFAULT 'PENDING',
        fee_status TEXT DEFAULT 'UNCLAIMED',
        approved_at DATETIME,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 7. Tabla de notificaciones (Parche: Añadida para evitar OperationalError)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_code TEXT,
        message TEXT,
        status TEXT DEFAULT 'UNREAD',
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 8. Tabla de artículos de la tienda (Parche: Añadida para evitar OperationalError)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS store_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        description TEXT,
        price_sd REAL,
        item_type TEXT
    )
    """)

    # Insertar artículos por defecto para la tienda si está vacía
    cursor.execute("SELECT COUNT(*) FROM store_items")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
            INSERT INTO store_items (name, description, price_sd, item_type)
            VALUES (?, ?, ?, ?)
        """, [
            ("Membresía VIP Mensual", "Acceso a beneficios premium y tarifas cero en retiros.", 50.0, "MEMBERSHIP"),
            ("Soporte Prioritario", "Canal de soporte 24/7 directo con el equipo de la Alianza.", 15.0, "SERVICE"),
            ("Guía Crypto Alianza", "Ebook exclusivo sobre trading de tokens SD.", 10.0, "DIGITAL_GOOD")
        ])

    # 9. Tabla de compras de la tienda (Parche: Añadida para evitar OperationalError)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS store_purchases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_code TEXT,
        item_id INTEGER,
        price_sd REAL,
        status TEXT DEFAULT 'PENDING',
        code_delivered TEXT DEFAULT '',
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 10. Tabla de pagos móviles/mensajería (Parche: Añadida para evitar OperationalError)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movil_payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_code TEXT,
        payment_type TEXT,
        amount_sd REAL,
        amount_cop REAL,
        target_code TEXT,
        message TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Insertar administrador por defecto si no existe
    cursor.execute("SELECT 1 FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        hashed_admin_pw = hashlib.sha256("admin123".encode()).hexdigest()
        cursor.execute("""
            INSERT INTO users (username, password, fullname, email, wallet_code, balance, is_admin, balance_cop, is_vip, nequi_number)
            VALUES ('admin', ?, 'Administrador Principal', 'admin@alianza.com', '99999', 1000000.0, 1, 0.0, 1, '3001234567')
        """, (hashed_admin_pw,))
    
    conn.commit()
    conn.close()

init_db()

# --- FUNCIONES AUXILIARES DE BASE DE DATOS ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_db_connection():
    return sqlite3.connect("wallet_pro.db")

def generate_unique_wallet_code():
    conn = get_db_connection()
    cursor = conn.cursor()
    while True:
        code = str(random.randint(10000, 99999))
        cursor.execute("SELECT 1 FROM users WHERE wallet_code = ?", (code,))
        if not cursor.fetchone():
            conn.close()
            return code

def get_token_settings():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT token_name, token_symbol, token_contract, token_price_usd, nequi_number FROM token_settings WHERE id = 1")
    settings = cursor.fetchone()
    conn.close()
    if settings:
        return {
            "name": settings[0],
            "symbol": settings[1],
            "contract": settings[2],
            "price_usd": settings[3],
            "nequi_number": settings[4]
        }
    return {
        "name": "SIAD",
        "symbol": "SD",
        "contract": "0xC324649213ec1757190bc4b78bcD41Cc1545C264",
        "price_usd": 0.50,
        "nequi_number": "3001234567"
    }

def update_token_settings(name, symbol, contract, price_usd, nequi_number):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE token_settings
        SET token_name = ?, token_symbol = ?, token_contract = ?, token_price_usd = ?, nequi_number = ?
        WHERE id = 1
    """, (name, symbol, contract, price_usd, nequi_number))
    conn.commit()
    conn.close()

def update_store_item_price(item_id, price_sd, name, description):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE store_items
        SET price_sd = ?, name = ?, description = ?
        WHERE id = ?
    """, (price_sd, name, description, item_id))
    conn.commit()
    conn.close()
    return True

# --- GESTIÓN DE SOLICITUDES DE COMPRA ---
def submit_purchase_request(user_code, amount_cop, amount_sd, image_bytes):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO purchase_requests (user_code, amount_cop, amount_sd, proof_image, status)
        VALUES (?, ?, ?, ?, 'PENDING')
    """, (user_code, amount_cop, amount_sd, image_bytes))
    conn.commit()
    conn.close()

def get_pending_purchases():
    conn = get_db_connection()
    df = pd.read_sql_query("""
        SELECT p.id, p.user_code, p.amount_cop, p.amount_sd, p.proof_image, p.timestamp, u.fullname, u.username
        FROM purchase_requests p
        JOIN users u ON p.user_code = u.wallet_code
        WHERE p.status = 'PENDING'
        ORDER BY p.timestamp ASC
    """, conn)
    conn.close()
    return df

# --- GESTIÓN DE COMISIONES POR REFERIDOS ---
def get_pending_referral_rewards():
    conn = get_db_connection()
    df = pd.read_sql_query("""
        SELECT r.id, r.referrer_code, r.referred_code, r.purchase_amount_sd, r.reward_amount_sd, r.timestamp, u1.fullname as referrer_name, u2.fullname as referred_name
        FROM referral_rewards r
        JOIN users u1 ON r.referrer_code = u1.wallet_code
        JOIN users u2 ON r.referred_code = u2.wallet_code
        WHERE r.status = 'PENDING'
        ORDER BY r.timestamp ASC
    """, conn)
    conn.close()
    return df

def approve_referral_reward(reward_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT referrer_code, reward_amount_sd, referred_code FROM referral_rewards WHERE id = ?", (reward_id,))
    res = cursor.fetchone()
    if res:
        referrer_code, reward_amount_sd, referred_code = res
        cursor.execute("UPDATE referral_rewards SET status = 'APPROVED' WHERE id = ?", (reward_id,))
        # Aumentar saldo del referidor
        cursor.execute("UPDATE users SET balance = balance + ? WHERE wallet_code = ?", (reward_amount_sd, referrer_code))
        add_notification(referrer_code, f"¡Recibiste {reward_amount_sd} SD por recomendación del usuario {referred_code}!")
        conn.commit()
    conn.close()

def reject_referral_reward(reward_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE referral_rewards SET status = 'REJECTED' WHERE id = ?", (reward_id,))
    conn.commit()
    conn.close()
    return True

# --- SISTEMA DE NOTIFICACIONES ---
def add_notification(user_code, message):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notifications (user_code, message) VALUES (?, ?)", (user_code, message))
    conn.commit()
    conn.close()

def broadcast_notification(message):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT wallet_code FROM users WHERE is_admin = 0")
    users = cursor.fetchall()
    for user in users:
        user_code = user[0]
        cursor.execute("INSERT INTO notifications (user_code, message) VALUES (?, ?)", (user_code, message))
    conn.commit()
    conn.close()

def get_unread_notifications_count(user_code):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM notifications WHERE user_code = ? AND status = 'UNREAD'", (user_code,))
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_user_notifications(user_code):
    conn = get_db_connection()
    df = pd.read_sql_query("""
        SELECT id, message, status, timestamp
        FROM notifications
        WHERE user_code = ?
        ORDER BY timestamp DESC
    """, conn, params=(user_code,))
    conn.close()
    return df

def mark_notifications_as_read(user_code):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE notifications SET status = 'READ' WHERE user_code = ?", (user_code,))
    conn.commit()
    conn.close()

# --- FUNCIONES DE LA TIENDA ALIANZA (Parche: Lógica implementada y completada) ---
def get_user_purchases(user_code):
    conn = get_db_connection()
    df = pd.read_sql_query("""
        SELECT id, amount_cop, amount_sd, proof_image, status, timestamp as Fecha
        FROM purchase_requests
        WHERE user_code = ?
        ORDER BY timestamp DESC
    """, conn, params=(user_code,))
    conn.close()
    return df

def buy_store_item(user_code, item_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT price_sd, name FROM store_items WHERE id = ?", (item_id,))
    item = cursor.fetchone()
    if not item:
        conn.close()
        return False, "Artículo no encontrado."
    
    price_sd, name = item
    
    cursor.execute("SELECT balance FROM users WHERE wallet_code = ?", (user_code,))
    user_balance = cursor.fetchone()
    if not user_balance or user_balance[0] < price_sd:
        conn.close()
        return False, "Saldo de tokens SD insuficiente para realizar la compra."
    
    # Deducción y Registro de compra
    new_balance = user_balance[0] - price_sd
    cursor.execute("UPDATE users SET balance = ? WHERE wallet_code = ?", (new_balance, user_code))
    cursor.execute("""
        INSERT INTO store_purchases (user_code, item_id, price_sd, status)
        VALUES (?, ?, ?, 'PENDING')
    """, (user_code, item_id, price_sd))
    
    add_notification(user_code, f"Tu compra de '{name}' por {price_sd} SD ha sido enviada para aprobación.")
    conn.commit()
    conn.close()
    return True, f"¡Solicitud enviada! Tu saldo actual es de {new_balance:.2f} SD."

def deliver_store_purchase(purchase_id, code_delivered=""):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.user_code, p.item_id, p.price_sd, i.name, i.item_type
        FROM store_purchases p
        JOIN store_items i ON p.item_id = i.id
        WHERE p.id = ? AND p.status = 'PENDING'
    """, (purchase_id,))
    purchase = cursor.fetchone()
    if purchase:
        user_code, item_id, price_sd, item_name, item_type = purchase
        cursor.execute("""
            UPDATE store_purchases
            SET status = 'APPROVED', code_delivered = ?
            WHERE id = ?
        """, (code_delivered, purchase_id))
        
        # Si es membresía VIP, activarla automáticamente
        if item_type == "MEMBERSHIP":
            cursor.execute("UPDATE users SET is_vip = 1 WHERE wallet_code = ?", (user_code,))
        
        add_notification(user_code, f"¡Tu compra de '{item_name}' ha sido aprobada! Código/Detalle enviado: {code_delivered}")
        conn.commit()
        conn.close()
        return True, "Entrega aprobada con éxito."
    conn.close()
    return False, "No se encontró el artículo pendiente."

def reject_store_purchase(purchase_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.user_code, p.price_sd, i.name
        FROM store_purchases p
        JOIN store_items i ON p.item_id = i.id
        WHERE p.id = ? AND p.status = 'PENDING'
    """, (purchase_id,))
    purchase = cursor.fetchone()
    if purchase:
        user_code, price_sd, item_name = purchase
        cursor.execute("UPDATE store_purchases SET status = 'REJECTED' WHERE id = ?", (purchase_id,))
        cursor.execute("UPDATE users SET balance = balance + ? WHERE wallet_code = ?", (price_sd, user_code))
        add_notification(user_code, f"Tu compra de '{item_name}' fue rechazada. Se han reembolsado {price_sd} SD a tu saldo.")
        conn.commit()
        conn.close()
        return True, "Compra rechazada y reembolso emitido correctamente."
    conn.close()
    return False, "No se encontró la compra pendiente."

def get_pending_store_purchases():
    conn = get_db_connection()
    df = pd.read_sql_query("""
        SELECT p.id, p.user_code, p.item_id, p.price_sd, p.timestamp, i.name, i.item_type, u.fullname, u.username
        FROM store_purchases p
        JOIN store_items i ON p.item_id = i.id
        JOIN users u ON p.user_code = u.wallet_code
        WHERE p.status = 'PENDING'
        ORDER BY p.timestamp ASC
    """, conn)
    conn.close()
    return df

def get_user_store_purchases(user_code):
    conn = get_db_connection()
    df = pd.read_sql_query("""
        SELECT p.id, p.price_sd, p.status, p.code_delivered, p.timestamp, i.name, i.item_type
        FROM store_purchases p
        JOIN store_items i ON p.item_id = i.id
        WHERE p.user_code = ?
        ORDER BY p.timestamp DESC
    """, conn, params=(user_code,))
    conn.close()
    return df

# --- GESTIÓN DE DEPÓSITOS ---
def approve_purchase(request_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.user_code, p.amount_sd, p.amount_cop, u.fullname, u.referred_by
        FROM purchase_requests p
        JOIN users u ON p.user_code = u.wallet_code
        WHERE p.id = ? AND p.status = 'PENDING'
    """, (request_id,))
    req = cursor.fetchone()
    if req:
        user_code, amount_sd, amount_cop, fullname, referred_by = req
        cursor.execute("UPDATE purchase_requests SET status = 'APPROVED' WHERE id = ?", (request_id,))
        cursor.execute("UPDATE users SET balance = balance + ? WHERE wallet_code = ?", (amount_sd, user_code))
        add_notification(user_code, f"¡Tu depósito de ${amount_cop:,.2f} COP ({amount_sd} SD) ha sido aprobado!")
        
        # Procesar recompensa por referido si aplica
        if referred_by:
            # Buscar si el referidor existe
            cursor.execute("SELECT wallet_code FROM users WHERE wallet_code = ?", (referred_by,))
            if cursor.fetchone():
                reward_sd = amount_sd * 0.10 # 10% de comisión por referidos
                cursor.execute("""
                    INSERT INTO referral_rewards (referrer_code, referred_code, purchase_id, purchase_amount_sd, reward_amount_sd, status)
                    VALUES (?, ?, ?, ?, ?, 'PENDING')
                """, (referred_by, user_code, request_id, amount_sd, reward_sd))
        
        conn.commit()
    conn.close()

def reject_purchase(request_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_code, amount_sd, amount_cop FROM purchase_requests WHERE id = ?", (request_id,))
    req = cursor.fetchone()
    if req:
        user_code, amount_sd, amount_cop = req
        cursor.execute("UPDATE purchase_requests SET status = 'REJECTED' WHERE id = ?", (request_id,))
        add_notification(user_code, f"Tu depósito de ${amount_cop:,.2f} COP ({amount_sd} SD) ha sido rechazado tras revisar el comprobante.")
        conn.commit()
    conn.close()

def toggle_user_vip_manually(wallet_code, enable):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT fullname FROM users WHERE wallet_code = ?", (wallet_code,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        return False, "No se encontró ningún usuario con ese código de billetera."
    
    val = 1 if enable else 0
    cursor.execute("UPDATE users SET is_vip = ? WHERE wallet_code = ?", (val, wallet_code))
    add_notification(wallet_code, "Tu estatus VIP ha sido actualizado por un administrador.")
    conn.commit()
    conn.close()
    return True, f"Membresía VIP {'activada' if enable else 'desactivada'} para {user[0]}."

def approve_purchase_as_vip(request_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.user_code, p.amount_sd, p.amount_cop, u.fullname, u.referred_by
        FROM purchase_requests p
        JOIN users u ON p.user_code = u.wallet_code
        WHERE p.id = ? AND p.status = 'PENDING'
    """, (request_id,))
    req = cursor.fetchone()
    if req:
        user_code, amount_sd, amount_cop, fullname, referred_by = req
        cursor.execute("UPDATE purchase_requests SET status = 'APPROVED' WHERE id = ?", (request_id,))
        cursor.execute("UPDATE users SET balance = balance + ?, is_vip = 1 WHERE wallet_code = ?", (amount_sd, user_code))
        add_notification(user_code, f"¡Tu depósito VIP de ${amount_cop:,.2f} COP ({amount_sd} SD) fue aprobado!")
        conn.commit()
    conn.close()

# --- LLAMADOS A API Y CACHÉ ---
@st.cache_data(ttl=120)
def fetch_btc_price():
    try:
        response = requests.get("https://api.coinbase.com/v2/prices/BTC-USD/spot", timeout=2)
        if response.status_code == 200:
            data = response.json()
            return float(data['data']['amount'])
    except Exception:
        pass
    return 64320.50

@st.cache_data(ttl=10)
def fetch_sd_price_from_dexscreener():
    try:
        url = "https://api.dexscreener.com/latest/dex/tokens/0xC324649213ec1757190bc4b78bcD41Cc1545C264"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            if data and 'pairs' in data and data['pairs'] is not None and len(data['pairs']) > 0:
                pair = data['pairs'][0]
                price_usd = float(pair.get('priceUsd', 0.0))
                if price_usd > 0:
                    return price_usd
    except Exception:
        pass
    return None

@st.cache_data(ttl=120)
def fetch_usd_cop_rate():
    try:
        response = requests.get("https://economia.awesomeapi.com.br/json/last/USD-COP", timeout=2)
        if response.status_code == 200:
            data = response.json()
            return float(data['USDCOP']['bid'])
    except Exception:
        pass
    try:
        response = requests.get("https://open.er-api.com/v6/latest/USD", timeout=2)
        if response.status_code == 200:
            data = response.json()
            return float(data['rates']['COP'])
    except Exception:
        pass
    return 4150.00

@st.cache_data(ttl=600)
def get_btc_historical_data():
    try:
        response = requests.get("https://min-api.cryptocompare.com/data/v2/histoday?fsym=BTC&tsym=USD&limit=30", timeout=2)
        if response.status_code == 200:
            data = response.json()
            prices = data['Data']['Data']
            df = pd.DataFrame(prices)
            df['Fecha'] = pd.to_datetime(df['time'], unit='s')
            df['Precio (USD)'] = df['close']
            return df[['Fecha', 'Precio (USD)']]
    except Exception:
        pass
    dates = pd.date_range(end=datetime.now(), periods=30)
    np.random.seed(42)
    base = 61200
    prices = [base + i*160 + np.random.normal(0, 700) for i in range(30)]
    return pd.DataFrame({"Fecha": dates, "Precio (USD)": prices})

@st.cache_data(ttl=600)
def get_usd_cop_historical_data():
    try:
        response = requests.get("https://economia.awesomeapi.com.br/json/daily/USD-COP/30", timeout=2)
        if response.status_code == 200:
            data = response.json()
            rates = []
            dates = []
            for item in data:
                rates.append(float(item['bid']))
                timestamp = int(item['timestamp'])
                dates.append(pd.to_datetime(timestamp, unit='s'))
            df = pd.DataFrame({"Fecha": dates, "Tasa (COP)": rates})
            df = df.sort_values(by="Fecha").reset_index(drop=True)
            return df
    except Exception:
        pass
    dates = pd.date_range(end=datetime.now(), periods=30)
    np.random.seed(10)
    rates = [4150 - i*5 + np.random.normal(0, 25) for i in range(30)]
    return pd.DataFrame({"Fecha": dates, "Tasa (COP)": rates})

def get_custom_token_historical_data(current_price):
    dates = pd.date_range(end=datetime.now(), periods=30)
    np.random.seed(100)
    prices = []
    base = current_price * 0.75
    for i in range(29):
        pct_change = np.random.normal(0.008, 0.04)
        base = base * (1 + pct_change)
        prices.append(base)
    prices.append(current_price)
    return pd.DataFrame({"Fecha": dates, "Precio (USD)": prices})

# --- LÓGICA DE NEGOCIO ---
def register_user(username, password, fullname, email, referred_by=None):
    if not username or not password or not fullname or not email:
        return False, "Todos los campos obligatorios deben ser completados."
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_pw = hash_password(password)
    wallet_code = generate_unique_wallet_code()
    try:
        cursor.execute("""
            INSERT INTO users (username, password, fullname, email, wallet_code, balance, balance_cop, referred_by)
            VALUES (?, ?, ?, ?, ?, 0.0, 0.0, ?)
        """, (username, hashed_pw, fullname, email, wallet_code, referred_by))
        conn.commit()
        conn.close()
        return True, f"¡Registro exitoso! Tu código de billetera es {wallet_code}."
    except sqlite3.IntegrityError:
        conn.close()
        return False, "El nombre de usuario ya está registrado."

def login_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_pw = hash_password(password)
    cursor.execute("""
        SELECT id, username, fullname, email, wallet_code, balance, is_admin
        FROM users
        WHERE username = ? AND password = ?
    """, (username, hashed_pw))
    user = cursor.fetchone()
    conn.close()
    return user

def change_user_password(username, old_password, new_password):
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_old = hash_password(old_password)
    cursor.execute("SELECT 1 FROM users WHERE username = ? AND password = ?", (username, hashed_old))
    if not cursor.fetchone():
        conn.close()
        return False, "La contraseña actual es incorrecta."
    hashed_new = hash_password(new_password)
    cursor.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_new, username))
    conn.commit()
    conn.close()
    return True, "Contraseña cambiada exitosamente."

def send_points(sender_code, receiver_code, amount):
    if sender_code == receiver_code:
        return False, "No puedes enviarte puntos a ti mismo."
    if amount <= 0:
        return False, "El monto debe ser mayor a cero."
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT fullname FROM users WHERE wallet_code = ?", (receiver_code,))
    recv = cursor.fetchone()
    if not recv:
        conn.close()
        return False, "El código de billetera de destino no existe."
    
    cursor.execute("SELECT balance FROM users WHERE wallet_code = ?", (sender_code,))
    sender_bal = cursor.fetchone()[0]
    if sender_bal < amount:
        conn.close()
        return False, "Saldo de tokens SD insuficiente."
    
    cursor.execute("UPDATE users SET balance = balance - ? WHERE wallet_code = ?", (amount, sender_code))
    cursor.execute("UPDATE users SET balance = balance + ? WHERE wallet_code = ?", (amount, receiver_code))
    cursor.execute("""
        INSERT INTO transactions (sender_code, receiver_code, amount)
        VALUES (?, ?, ?)
    """, (sender_code, receiver_code, amount))
    
    add_notification(sender_code, f"Enviaste {amount} SD a {recv[0]} (Código: {receiver_code}).")
    add_notification(receiver_code, f"Recibiste {amount} SD de {sender_code}.")
    
    conn.commit()
    conn.close()
    return True, f"Transferencia exitosa de {amount} SD."

def get_user_balance(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance, wallet_code, balance_cop, is_vip FROM users WHERE username = ?", (username,))
    res = cursor.fetchone()
    conn.close()
    return res if res else (0.0, "", 0.0, 0)

def format_num(val):
    if val is None:
        return "0"
    try:
        val_f = float(val)
        if val_f.is_integer() or abs(val_f - round(val_f)) < 1e-9:
            return f"{int(round(val_f)):,}"
        formatted = f"{val_f:,.2f}"
        if '.' in formatted:
            formatted = formatted.rstrip('0').rstrip('.')
        return formatted
    except Exception:
        return str(val)

def update_user_balance_and_cop(user_code, balance_sd, balance_cop):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users SET balance = ?, balance_cop = ? WHERE wallet_code = ?
    """, (balance_sd, balance_cop, user_code))
    conn.commit()
    conn.close()

def get_user_nequi(wallet_code):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nequi_number FROM users WHERE wallet_code = ?", (wallet_code,))
    res = cursor.fetchone()
    conn.close()
    return res[0] if res and res[0] else ""

def update_user_nequi(wallet_code, nequi_number):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET nequi_number = ? WHERE wallet_code = ?", (nequi_number, wallet_code))
    conn.commit()
    conn.close()
    return True

def update_global_nequi(nequi_number):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE token_settings SET nequi_number = ? WHERE id = 1", (nequi_number,))
    cursor.execute("UPDATE users SET nequi_number = ? WHERE wallet_code = '99999'", (nequi_number,))
    conn.commit()
    conn.close()
    return True

# --- LÓGICA DE MENSAJERÍA Y MÓVILES ---
def pay_delivery_service(sender_code, driver_code, amount_sd, service_id=""):
    if sender_code == driver_code:
        return False, "No puedes pagarte un envío a ti mismo."
    if amount_sd <= 0:
        return False, "El monto del envío debe ser mayor a cero."
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM users WHERE wallet_code = ?", (sender_code,))
    sender_bal = cursor.fetchone()[0]
    if sender_bal < amount_sd:
        conn.close()
        return False, "Saldo de tokens SD insuficiente para pagar el servicio."
    
    cursor.execute("UPDATE users SET balance = balance - ? WHERE wallet_code = ?", (amount_sd, sender_code))
    cursor.execute("UPDATE users SET balance = balance + ? WHERE wallet_code = ?", (amount_sd, driver_code))
    cursor.execute("""
        INSERT INTO movil_payments (user_code, payment_type, amount_sd, amount_cop, target_code, message)
        VALUES (?, 'DELIVERY', ?, 0.0, ?, ?)
    """, (sender_code, amount_sd, driver_code, f"Servicio ID {service_id}"))
    
    add_notification(sender_code, f"Pagaste {amount_sd} SD al repartidor {driver_code}.")
    add_notification(driver_code, f"Recibiste {amount_sd} SD del cliente {sender_code} por envío.")
    
    conn.commit()
    conn.close()
    return True, "Pago de mensajería procesado."

def pay_weekly_fee(user_code, use_tokens=True, message=""):
    conn = get_db_connection()
    cursor = conn.cursor()
    fee_sd = 5.0
    fee_cop = 20000.0
    
    cursor.execute("SELECT balance, balance_cop FROM users WHERE wallet_code = ?", (user_code,))
    res = cursor.fetchone()
    if not res:
        conn.close()
        return False, "Usuario no encontrado."
    
    balance_sd, balance_cop = res
    if use_tokens:
        if balance_sd < fee_sd:
            conn.close()
            return False, "Saldo de tokens SD insuficiente para la cuota."
        cursor.execute("UPDATE users SET balance = balance - ? WHERE wallet_code = ?", (fee_sd, user_code))
    else:
        if balance_cop < fee_cop:
            conn.close()
            return False, "Saldo en pesos COP insuficiente para la cuota."
        cursor.execute("UPDATE users SET balance_cop = balance_cop - ? WHERE wallet_code = ?", (fee_cop, user_code))
        
    cursor.execute("""
        INSERT INTO movil_payments (user_code, payment_type, amount_sd, amount_cop, target_code, message)
        VALUES (?, 'WEEKLY_FEE', ?, ?, '99999', ?)
    """, (user_code, fee_sd if use_tokens else 0.0, 0.0 if use_tokens else fee_cop, message))
    
    add_notification(user_code, "Has pagado tu membresía semanal con éxito.")
    conn.commit()
    conn.close()
    return True, "Membresía semanal pagada exitosamente."

def get_movil_payments_history(user_code):
    conn = get_db_connection()
    df = pd.read_sql_query("""
        SELECT p.id, p.payment_type, p.amount_sd, p.amount_cop, p.target_code, p.timestamp, p.message, u1.fullname as customer_name, u2.fullname as driver_name
        FROM movil_payments p
        LEFT JOIN users u1 ON p.user_code = u1.wallet_code
        LEFT JOIN users u2 ON p.target_code = u2.wallet_code
        WHERE p.user_code = ? OR p.target_code = ?
        ORDER BY p.timestamp DESC
    """, conn, params=(user_code, user_code))
    conn.close()
    return df

def get_all_movil_payments():
    conn = get_db_connection()
    df = pd.read_sql_query("""
        SELECT p.id, p.payment_type, p.amount_sd, p.amount_cop, p.user_code, p.target_code, p.timestamp, p.message, u1.fullname as customer_name, u2.fullname as target_name
        FROM movil_payments p
        LEFT JOIN users u1 ON p.user_code = u1.wallet_code
        LEFT JOIN users u2 ON p.target_code = u2.wallet_code
        ORDER BY p.timestamp DESC
    """, conn)
    conn.close()
    return df

def get_transaction_history(wallet_code):
    conn = get_db_connection()
    df = pd.read_sql_query("""
        SELECT t.id, t.sender_code, t.receiver_code, t.amount, t.timestamp, u1.fullname as sender_name, u2.fullname as receiver_name
        FROM transactions t
        LEFT JOIN users u1 ON t.sender_code = u1.wallet_code
        LEFT JOIN users u2 ON t.receiver_code = u2.wallet_code
        WHERE t.sender_code = ? OR t.receiver_code = ?
        ORDER BY t.timestamp ASC
    """, conn, params=(wallet_code, wallet_code))
    conn.close()
    return df

# --- SWAPS Y RETIROS ---
def swap_sd_to_cop(user_code, amount_sd, rate_usd, usd_cop_rate):
    if amount_sd <= 0:
        return False, "La cantidad de SD debe ser mayor a cero."
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance, balance_cop FROM users WHERE wallet_code = ?", (user_code,))
    res = cursor.fetchone()
    if not res or res[0] < amount_sd:
        conn.close()
        return False, "Saldo de tokens SD insuficiente."
    
    amount_usd = amount_sd * rate_usd
    amount_cop = amount_usd * usd_cop_rate
    
    new_balance_sd = res[0] - amount_sd
    new_balance_cop = res[1] + amount_cop
    
    cursor.execute("""
        UPDATE users
        SET balance = ?, balance_cop = ?
        WHERE wallet_code = ?
    """, (new_balance_sd, new_balance_cop, user_code))
    
    add_notification(user_code, f"Intercambio exitoso: Vendiste {amount_sd} SD por ${amount_cop:,.2f} COP.")
    conn.commit()
    conn.close()
    return True, f"Intercambio exitoso. Recibiste ${amount_cop:,.2f} COP en tu saldo."

def submit_withdrawal_request(user_code, amount_cop, nequi_number):
    if amount_cop < 1000:
        return False, "El monto mínimo de retiro es de $1,000 COP."
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance_cop, is_vip FROM users WHERE wallet_code = ?", (user_code,))
    res = cursor.fetchone()
    if not res or res[0] < amount_cop:
        conn.close()
        return False, "Saldo en pesos (COP) insuficiente para procesar el retiro."
    
    # VIP no pagan comisión de retiro, cuentas normales pagan el 5%
    fee_pct = 0.0 if res[1] == 1 else 0.05
    fee_cop = amount_cop * fee_pct
    net_cop = amount_cop - fee_cop
    
    cursor.execute("UPDATE users SET balance_cop = balance_cop - ? WHERE wallet_code = ?", (amount_cop, user_code))
    cursor.execute("""
        INSERT INTO withdrawal_requests (user_code, amount_cop, fee_cop, net_cop, nequi_number, status)
        VALUES (?, ?, ?, ?, ?, 'PENDING')
    """, (user_code, amount_cop, fee_cop, net_cop, nequi_number))
    
    add_notification(user_code, f"Solicitud de retiro por ${amount_cop:,.2f} COP enviada. Neto a recibir en Nequi: ${net_cop:,.2f} COP.")
    conn.commit()
    conn.close()
    return True, f"Retiro enviado con éxito. Comisión aplicada: ${fee_cop:,.2f} COP."

def get_pending_withdrawals():
    conn = get_db_connection()
    df = pd.read_sql_query("""
        SELECT w.id, w.user_code, w.amount_cop, w.fee_cop, w.net_cop, w.nequi_number, w.timestamp, u.fullname, u.username
        FROM withdrawal_requests w
        JOIN users u ON w.user_code = u.wallet_code
        WHERE w.status = 'PENDING'
        ORDER BY w.timestamp ASC
    """, conn)
    conn.close()
    return df

def get_user_withdrawals(user_code):
    conn = get_db_connection()
    df = pd.read_sql_query("""
        SELECT id, amount_cop, fee_cop, net_cop, nequi_number, receipt_image, status, timestamp
        FROM withdrawal_requests
        WHERE user_code = ?
        ORDER BY timestamp DESC
    """, conn, params=(user_code,))
    conn.close()
    return df

def get_platform_fees_summary():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(fee_cop) FROM withdrawal_requests WHERE status = 'APPROVED'")
    total_fees = cursor.fetchone()[0] or 0.0
    cursor.execute("SELECT SUM(fee_cop) FROM withdrawal_requests WHERE status = 'APPROVED' AND fee_status = 'CLAIMED'")
    claimed_fees = cursor.fetchone()[0] or 0.0
    conn.close()
    return total_fees, total_fees - claimed_fees

def claim_platform_fees():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE withdrawal_requests SET fee_status = 'CLAIMED' WHERE status = 'APPROVED' AND fee_status = 'UNCLAIMED'")
    conn.commit()
    conn.close()
    return True

def get_approved_withdrawals_fees():
    conn = get_db_connection()
    df = pd.read_sql_query("""
        SELECT w.id, w.user_code, w.amount_cop, w.fee_cop, w.approved_at, w.fee_status, u.fullname
        FROM withdrawal_requests w
        JOIN users u ON w.user_code = u.wallet_code
        WHERE w.status = 'APPROVED'
        ORDER BY w.approved_at DESC
    """, conn)
    conn.close()
    return df

def approve_withdrawal(request_id, receipt_bytes):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_code, amount_cop, net_cop FROM withdrawal_requests WHERE id = ?", (request_id,))
    res = cursor.fetchone()
    if res:
        user_code, amount_cop, net_cop = res
        cursor.execute("""
            UPDATE withdrawal_requests
            SET status = 'APPROVED', receipt_image = ?, approved_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (receipt_bytes, request_id))
        add_notification(user_code, f"¡Tu retiro de ${amount_cop:,.2f} COP ha sido aprobado! Tu comprobante está listo.")
        conn.commit()
    conn.close()

def reject_withdrawal(request_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_code, amount_cop FROM withdrawal_requests WHERE id = ?", (request_id,))
    res = cursor.fetchone()
    if res:
        user_code, amount_cop = res
        cursor.execute("UPDATE withdrawal_requests SET status = 'REJECTED' WHERE id = ?", (request_id,))
        cursor.execute("UPDATE users SET balance_cop = balance_cop + ? WHERE wallet_code = ?", (amount_cop, user_code))
        add_notification(user_code, f"Tu retiro de ${amount_cop:,.2f} COP fue rechazado. Saldo reembolsado.")
        conn.commit()
    conn.close()

# --- INTERFAZ GRÁFICA DE STREAMLIT ---
# Estilo Premium: Negro Absoluto, Amarillo Dorado y Botones Verdes con Borde Dorado
st.markdown("""
<style>
    /* Ocultar elementos por defecto de Streamlit */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    .stDeployButton {display:none !important;}

    /* Fondo Negro Absoluto y Texto Blanco/Dorado */
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
    }
    
    /* Títulos Dorados */
    .golden-title {
        color: #FFD700;
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-weight: bold;
        text-shadow: 1px 1px 10px rgba(255, 215, 0, 0.3);
    }
    
    /* Botones Verdes con Bordes Dorados */
    div.stButton > button {
        background-color: #28a745 !important;
        color: #FFFFFF !important;
        border: 2px solid #FFD700 !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        padding: 0.5em 1.5em !important;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #218838 !important;
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.5) !important;
        transform: scale(1.02);
    }
</style>
""", unsafe_allow_html=True)

# Inicializar sesión
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.fullname = None
    st.session_state.email = None
    st.session_state.wallet_code = None
    st.session_state.is_admin = False

# Cargar cotizaciones y tokens
token = get_token_settings()
btc_price = fetch_btc_price()
usd_cop = fetch_usd_cop_rate()
live_sd_price = fetch_sd_price_from_dexscreener()

if live_sd_price is not None and live_sd_price > 0:
    token_price_usd = live_sd_price
    try:
        conn_sync = get_db_connection()
        cursor_sync = conn_sync.cursor()
        cursor_sync.execute("UPDATE token_settings SET token_price_usd = ? WHERE id = 1", (live_sd_price,))
        conn_sync.commit()
        conn_sync.close()
    except Exception:
        pass
else:
    token_price_usd = token['price_usd']

token_price_cop = token_price_usd * usd_cop

# --- FLUJO DE LA APLICACIÓN ---
if not st.session_state.logged_in:
    st.sidebar.title("🔐 Alianza CryptoWallet")
    menu = st.sidebar.selectbox("Seleccione una opción", ["Iniciar Sesión", "Registrarse"])
    
    st.markdown("<h1 class='golden-title' style='text-align: center;'>💼 Alianza CryptoWallet v31</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size:1.2em;'>El ecosistema digital seguro con token SIAD (SD) integrado.</p>", unsafe_allow_html=True)
    
    # Mostrar mercado público
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Bitcoin (BTC)", value=f"${format_num(btc_price)} USD", delta="+0.85%")
    col2.metric(label="Tasa de Cambio USD-COP", value=f"${format_num(usd_cop)} COP")
    col3.metric(label=f"Precio Token {token['name']} ({token['symbol']})", value=f"${format_num(token_price_usd)} USD", delta=f"${format_num(token_price_cop)} COP")

    if menu == "Iniciar Sesión":
        st.subheader("Accede a tu Billetera")
        username_inp = st.text_input("Usuario")
        password_inp = st.text_input("Contraseña", type="password")
        if st.button("Ingresar"):
            user = login_user(username_inp, password_inp)
            if user:
                st.session_state.logged_in = True
                st.session_state.user_id = user[0]
                st.session_state.username = user[1]
                st.session_state.fullname = user[2]
                st.session_state.email = user[3]
                st.session_state.wallet_code = user[4]
                st.session_state.is_admin = bool(user[6])
                st.success(f"¡Bienvenido, {user[2]}!")
                st.rerun()
            else:
                st.error("Credenciales incorrectas. Inténtalo de nuevo.")
                
    elif menu == "Registrarse":
        st.subheader("Crea tu cuenta gratis en 10 segundos")
        new_fullname = st.text_input("Nombre Completo")
        new_email = st.text_input("Correo Electrónico")
        new_username = st.text_input("Nombre de Usuario (Login)")
        new_password = st.text_input("Contraseña", type="password")
        referrer = st.text_input("Código de Referido (Opcional)")
        if st.button("Registrarse"):
            success, msg = register_user(new_username, new_password, new_fullname, new_email, referrer if referrer else None)
            if success:
                st.success(msg)
            else:
                st.error(msg)
else:
    # --- PANEL DE USUARIO CONECTADO ---
    st.sidebar.markdown(f"<h2 class='golden-title'>👋 {st.session_state.fullname}</h2>", unsafe_allow_html=True)
    st.sidebar.markdown(f"**Billetera ID (Código):** {st.session_state.wallet_code}")
    
    # Obtener estatus VIP y balances actualizados
    bal_sd, w_code, bal_cop, is_vip = get_db_connection().execute("SELECT balance, wallet_code, balance_cop, is_vip FROM users WHERE id = ?", (st.session_state.user_id,)).fetchone()
    
    if is_vip == 1:
        st.sidebar.markdown("### ⭐ VIP de la Alianza")
    
    # Menú de navegación
    if st.session_state.is_admin:
        nav = st.sidebar.selectbox("Panel Administrativo", ["Dashboard Admin", "Aprobar Depósitos", "Aprobar Retiros", "Tienda Admin", "Ajustes Billetera"])
    else:
        nav = st.sidebar.selectbox("Tu Billetera", ["Dashboard", "Enviar Token SD", "Tienda Alianza", "Retirar COP (Nequi)", "Historial", "Notificaciones"])

    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.logged_in = False
        st.rerun()

    # --- CONTENIDO DE CADA VISTA ---
    if nav == "Dashboard":
        st.markdown(f"<h1 class='golden-title'>Tu Billetera</h1>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Saldo en Tokens SD", value=f"{format_num(bal_sd)} {token['symbol']}")
        with col2:
            st.metric(label="Saldo en Pesos Colombianos (COP)", value=f"${format_num(bal_cop)} COP")
            
        st.subheader("Operaciones Rápidas")
        # Swap de SD a COP
        st.write("Intercambio de SD a COP")
        amount_swap = st.number_input("Cantidad de SD a vender", min_value=0.0, step=1.0)
        if st.button("Vender SD"):
            if amount_swap > 0:
                success, msg = swap_sd_to_cop(st.session_state.wallet_code, amount_swap, token_price_usd, usd_cop)
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
            else:
                st.warning("Escribe un monto válido.")

    elif nav == "Enviar Token SD":
        st.markdown(f"<h1 class='golden-title'>Enviar Tokens SD</h1>", unsafe_allow_html=True)
        target = st.text_input("Código de Billetera de Destino (5 dígitos)")
        amount_send = st.number_input("Monto en SD a transferir", min_value=0.0, step=1.0)
        if st.button("Enviar"):
            if len(target) == 5 and amount_send > 0:
                success, msg = send_points(st.session_state.wallet_code, target, amount_send)
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
            else:
                st.warning("Verifica que el código de destino tenga 5 dígitos y el monto sea mayor a cero.")

    elif nav == "Tienda Alianza":
        st.markdown(f"<h1 class='golden-title'>Tienda Alianza</h1>", unsafe_allow_html=True)
        # Mostrar catálogo
        conn = get_db_connection()
        items = pd.read_sql_query("SELECT id, name, description, price_sd FROM store_items", conn)
        conn.close()
        
        for idx, row in items.iterrows():
            with st.container():
                st.write(f"### {row['name']}")
                st.write(f"{row['description']}")
                st.write(f"**Precio:** {row['price_sd']} SD")
                if st.button(f"Adquirir {row['name']}", key=f"btn_{row['id']}"):
                    success, msg = buy_store_item(st.session_state.wallet_code, row['id'])
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)
                st.write("---")

    elif nav == "Retirar COP (Nequi)":
        st.markdown(f"<h1 class='golden-title'>Retiro a Nequi</h1>", unsafe_allow_html=True)
        st.info("Monto mínimo de retiro: $1,000 COP. Las cuentas VIP disfrutan de comisión cero. Las cuentas estándar tienen una comisión del 5%.")
        nequi_num = st.text_input("Número de Nequi", value=get_user_nequi(st.session_state.wallet_code))
        amount_ret = st.number_input("Cantidad de COP a retirar", min_value=0.0, step=1000.0)
        if st.button("Solicitar Retiro"):
            if len(nequi_num) >= 10 and amount_ret >= 1000:
                # Guardar el número de nequi del usuario
                update_user_nequi(st.session_state.wallet_code, nequi_num)
                success, msg = submit_withdrawal_request(st.session_state.wallet_code, amount_ret, nequi_num)
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
            else:
                st.error("Número de teléfono inválido o monto menor al mínimo.")

    elif nav == "Historial":
        st.markdown(f"<h1 class='golden-title'>Tu Actividad</h1>", unsafe_allow_html=True)
        st.subheader("Historial de Transferencias")
        txs = get_transaction_history(st.session_state.wallet_code)
        if len(txs) > 0:
            st.dataframe(txs[['sender_name', 'receiver_name', 'amount', 'timestamp']])
        else:
            st.info("No has realizado transferencias aún.")

    elif nav == "Notificaciones":
        st.markdown(f"<h1 class='golden-title'>Notificaciones</h1>", unsafe_allow_html=True)
        mark_notifications_as_read(st.session_state.wallet_code)
        notifs = get_user_notifications(st.session_state.wallet_code)
        if len(notifs) > 0:
            for idx, row in notifs.iterrows():
                st.write(f"🔔 **[{row['timestamp']}]** {row['message']}")
        else:
            st.info("No tienes notificaciones pendientes.")

    # --- PANEL ADMINISTRADOR (Vistas del Admin) ---
    elif nav == "Dashboard Admin":
        st.markdown(f"<h1 class='golden-title'>Consola de Administración</h1>", unsafe_allow_html=True)
        st.write("Estatus global de la plataforma.")
        total_f, pending_f = get_platform_fees_summary()
        st.metric(label="Comisiones de Plataforma por Retiros", value=f"${format_num(total_f)} COP", delta=f"${format_num(pending_f)} COP Disponibles para reclamo")
        if st.button("Reclamar Comisiones"):
            if pending_f > 0:
                claim_platform_fees()
                st.success("Comisiones reclamadas y agregadas a la cuenta madre.")
                st.rerun()
            else:
                st.error("No hay comisiones listas para reclamar.")

    elif nav == "Aprobar Depósitos":
        st.markdown(f"<h1 class='golden-title'>Aprobación de Depósitos</h1>", unsafe_allow_html=True)
        purchases = get_pending_purchases()
        if len(purchases) > 0:
            for idx, row in purchases.iterrows():
                st.write(f"**Usuario:** {row['fullname']} ({row['username']})")
                st.write(f"**COP Depositado:** ${format_num(row['amount_cop'])} COP")
                st.write(f"**SD a Recibir:** {row['amount_sd']} SD")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Aprobar Depósito", key=f"app_dep_{row['id']}"):
                        approve_purchase(row['id'])
                        st.success("Depósito aprobado.")
                        st.rerun()
                with col2:
                    if st.button("Rechazar Depósito", key=f"rej_dep_{row['id']}"):
                        reject_purchase(row['id'])
                        st.error("Depósito rechazado.")
                        st.rerun()
                st.write("---")
        else:
            st.info("No hay solicitudes de depósitos pendientes.")

    elif nav == "Aprobar Retiros":
        st.markdown(f"<h1 class='golden-title'>Aprobación de Retiros</h1>", unsafe_allow_html=True)
        withdrawals = get_pending_withdrawals()
        if len(withdrawals) > 0:
            for idx, row in withdrawals.iterrows():
                st.write(f"**Usuario:** {row['fullname']} ({row['username']})")
                st.write(f"**COP Solicitado:** ${format_num(row['amount_cop'])} COP")
                st.write(f"**Neto a Enviar:** ${format_num(row['net_cop'])} COP")
                st.write(f"**Nequi:** {row['nequi_number']}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Aprobar y Enviar", key=f"app_wit_{row['id']}"):
                        # En producción subirías un blob real de comprobante, aquí simulamos con vacío
                        approve_withdrawal(row['id'], b"comprobante_exito")
                        st.success("Retiro marcado como aprobado.")
                        st.rerun()
                with col2:
                    if st.button("Rechazar Retiro", key=f"rej_wit_{row['id']}"):
                        reject_withdrawal(row['id'])
                        st.error("Retiro rechazado. Saldo reembolsado.")
                        st.rerun()
                st.write("---")
        else:
            st.info("No hay retiros pendientes.")

    elif nav == "Tienda Admin":
        st.markdown(f"<h1 class='golden-title'>Administración de Tienda</h1>", unsafe_allow_html=True)
        st.subheader("Compras Pendientes de Clientes")
        purch_store = get_pending_store_purchases()
        if len(purch_store) > 0:
            for idx, row in purch_store.iterrows():
                st.write(f"**Cliente:** {row['fullname']} ({row['username']})")
                st.write(f"**Artículo:** {row['name']} ({row['item_type']})")
                st.write(f"**Precio Pagado:** {row['price_sd']} SD")
                
                code_deliv = st.text_input("Código de entrega (ej. Licencia, Enlace, etc.)", key=f"del_code_{row['id']}")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Completar Entrega", key=f"comp_del_{row['id']}"):
                        deliver_store_purchase(row['id'], code_deliv)
                        st.success("Artículo entregado exitosamente.")
                        st.rerun()
                with col2:
                    if st.button("Rechazar Compra", key=f"rej_store_{row['id']}"):
                        reject_store_purchase(row['id'])
                        st.error("Compra rechazada y reembolso ejecutado.")
                        st.rerun()
                st.write("---")
        else:
            st.info("No hay entregas pendientes en la tienda.")

    elif nav == "Ajustes Billetera":
        st.markdown(f"<h1 class='golden-title'>Ajustes del Sistema</h1>", unsafe_allow_html=True)
        st.subheader("Editar Datos del Token")
        new_tk_name = st.text_input("Nombre de Token", value=token['name'])
        new_tk_sym = st.text_input("Símbolo de Token", value=token['symbol'])
        new_tk_contr = st.text_input("Contrato Inteligente", value=token['contract'])
        new_tk_price = st.number_input("Precio USD (Si no hay DexScreener)", value=token['price_usd'], format="%.4f")
        new_global_nequi = st.text_input("Nequi Cuenta Madre Global", value=token['nequi_number'])
        
        if st.button("Guardar Configuración"):
            update_token_settings(new_tk_name, new_tk_sym, new_tk_contr, new_tk_price, new_global_nequi)
            update_global_nequi(new_global_nequi)
            st.success("Configuración del sistema actualizada correctamente.")
            st.rerun()
