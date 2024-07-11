import mariadb
import hashlib

def create_connection():
    return mariadb.connect(
        user="root",
        password="",
        host="localhost",
        port=3306,
        database="proyek_ssdlc"
    )

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def insert_period(name, periode, pemasukan, pengeluaran, catatan):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO periods (name, periode, pemasukan, pengeluaran, catatan) VALUES (?, ?, ?, ?, ?)",
            (name, periode, pemasukan, pengeluaran, catatan)
        )
        conn.commit()
        return cursor.rowcount
    except mariadb.Error as e:
        return f"Error: {e}"
    finally:
        cursor.close()
        conn.close()
        
def update_period(name, periode, pemasukan, pengeluaran, catatan):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE periods SET pemasukan = ?, pengeluaran = ?, catatan = ? WHERE name = ? AND periode = ?",
            (pemasukan, pengeluaran, catatan, name, periode)
        )
        conn.commit()
        return cursor.rowcount, 
    except mariadb.Error as e:
        return f"Error: {e}"
    finally:
        cursor.close()
        conn.close()

def delete_period(name, periode):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM periods WHERE name = ? AND periode = ?", (name, periode))
        conn.commit()
        return cursor.rowcount, 
    except mariadb.Error as e:
        return f"Error: {e}"
    finally:
        cursor.close()
        conn.close()

def insert_user(username, name, password):
    hashed_password = hash_password(password)
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, name, password) VALUES (?, ?, ?)",
            (username, name, hashed_password)
        )
        conn.commit()
        return cursor.rowcount, 
    except mariadb.Error as e:
        return f"Error: {e}"
    finally:
        cursor.close()
        conn.close()

def get_user(username, password):
    hashed_password = hash_password(password)
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
        result = cursor.fetchone()
        if result:
            columns = [desc[0] for desc in cursor.description]
            return dict(zip(columns, result))
        return None
    except mariadb.Error as e:
        return f"Error: {e}"
    finally:
        cursor.close()
        conn.close()

def fetch_all_periods(name):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT periode FROM periods WHERE name = ?", (name,))
        results = cursor.fetchall()
        return results
    except mariadb.Error as e:
        return f"Error: {e}"
    finally:
        cursor.close()
        conn.close()

def fetch_all_expenditures(name):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT periode, pengeluaran FROM periods WHERE name = ?", (name,))
        results = cursor.fetchall()
        return [{"periode": result[0], "pengeluaran": result[1]} for result in results]
    except mariadb.Error as e:
        return f"Error: {e}"
    finally:
        cursor.close()
        conn.close()

def get_period(name, period):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM periods WHERE name = ? AND periode = ?", (name, period))
        result = cursor.fetchone()
        if result:
            columns = [desc[0] for desc in cursor.description]
            return dict(zip(columns, result))
        return None
    except mariadb.Error as e:
        return f"Error: {e}"
    finally:
        cursor.close()
        conn.close()

def insert_user(username, name, password):
    hashed_password = hash_password(password)
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, name, password) VALUES (?, ?, ?)",
            (username, name, hashed_password)
        )
        conn.commit()
        return cursor.rowcount, 
    except mariadb.Error as e:
        return f"Error: {e}"
    finally:
        cursor.close()
        conn.close()

def get_user(username, password):
    hashed_password = hash_password(password)
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
        result = cursor.fetchone()
        if result:
            columns = [desc[0] for desc in cursor.description]
            return dict(zip(columns, result))
        return None
    except mariadb.Error as e:
        return f"Error: {e}"
    finally:
        cursor.close()
        conn.close()
