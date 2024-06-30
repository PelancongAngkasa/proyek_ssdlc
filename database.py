import mariadb
import hashlib

# Koneksi ke database MariaDB
conn = mariadb.connect(
    user="root",
    password="",
    host="localhost",
    port=3306,
    database="proyek_ssdlc"
)

# Membuat cursor untuk mengeksekusi query
cursor = conn.cursor()

def hash_password(password):
    """Hashes a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def insert_period(name, period, incomes, expenses, comment):
    """Mengembalikan laporan setelah berhasil membuat catatan, jika gagal akan mengembalikan error"""
    try:
        cursor.execute("INSERT INTO periods (name, periode, pemasukan, pengeluaran, catatan) VALUES (?, ?, ?, ?, ?)", 
                       (name, period, incomes, expenses, comment))
        conn.commit()
        return cursor.rowcount, "Insert successful"
    except mariadb.Error as e:
        return f"Error: {e}"

def fetch_all_periods():
    """Mengembalikan dict dari semua periode"""
    try:
        cursor.execute("SELECT * FROM periods")
        results = cursor.fetchall()
        return results
    except mariadb.Error as e:
        return f"Error: {e}"

def get_period(period):
    """Jika tidak ditemukan, fungsi akan mengembalikan None"""
    try:
        cursor.execute("SELECT * FROM periods WHERE periode = ?", (period,))
        result = cursor.fetchone()
        return result
    except mariadb.Error as e:
        return f"Error: {e}"

def insert_user(username, name, password):
    hashed_password = hash_password(password)
    try:
        cursor.execute("INSERT INTO users (username, name, password) VALUES (?, ?, ?)", 
                       (username, name, hashed_password))
        conn.commit()
        return cursor.rowcount, "Insert successful"
    except mariadb.Error as e:
        return f"Error: {e}"

def get_user(username, password):
    hashed_password = hash_password(password)
    try:
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
        result = cursor.fetchone()
        if result:
            return {
                "username": result[0],
                "name": result[1]
            }
        return None
    except mariadb.Error as e:
        return f"Error: {e}"

def update_user(username, updates):
    # Assume 'updates' is a dict of columns to update
    query = "UPDATE users SET "
    query += ", ".join([f"{key} = ?" for key in updates.keys()])
    query += " WHERE username = ?"
    params = list(updates.values()) + [username]
    
    try:
        cursor.execute(query, params)
        conn.commit()
        return cursor.rowcount, "Update successful"
    except mariadb.Error as e:
        return f"Error: {e}"

def delete_user(username):
    try:
        cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        conn.commit()
        return cursor.rowcount, "Delete successful"
    except mariadb.Error as e:
        return f"Error: {e}"
