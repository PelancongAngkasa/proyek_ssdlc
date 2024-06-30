import streamlit as st
import database as db

# Fungsi untuk login
def login():
    st.title("Login")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            user = db.get_user(username, password)
            if user:
                st.session_state['logged_in'] = True
                st.session_state['name'] = user['name']
                st.session_state['username'] = user['username']
                st.success(f"Selamat Datang, {user['name']}!")
            else:
                st.error("Invalid username or password")

# Fungsi untuk registrasi pengguna baru
def register():
    st.title("Register")
    with st.form("register_form"):
        username = st.text_input("Username")
        name = st.text_input("Name")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Register")
        
        if submit:
            result, msg = db.insert_user(username, name, password)
            if result:
                st.success("Akun sukses terdaftar!")
            else:
                st.error(f"Error: {msg}")

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if st.session_state['logged_in']:
    st.write("Mengalihkan ke Halaman Utama...")
    st.switch_page('main')
    st.stop()
else:
    selected = st.sidebar.selectbox("Pilih Opsi", ["Login", "Register"])

    if selected == "Login":
        login()
    elif selected == "Register":
        register()
