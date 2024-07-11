import calendar
from datetime import datetime
import streamlit as st
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import database as db

pendapatans = ["Gaji", "Blog", "Pendapatan Lainnya"]
pengeluarans = ["Kos", "Pajak", "Makan", "Hiburan", "Tabungan"]
mata_uang = "IDR"
judul = "Pencatatan Pendapatan dan Pengeluaran"
icon = ":money_with_wings:"
layout = "centered"

st.set_page_config(page_title=judul, page_icon=icon, layout=layout)
st.title(judul + " " + icon)

if 'name' in st.session_state:
    st.subheader(f"Selamat datang, {st.session_state['name']}!")

tahun = [datetime.today().year, datetime.today().year + 1]
bulan = list(calendar.month_name[1:])

def get_all_periods():
    if 'name' in st.session_state:
        items = db.fetch_all_periods(st.session_state['name'])
        if isinstance(items, list):
            periods = [item[0] for item in items]
            return periods
    return []

def get_all_expenditures():
    if 'name' in st.session_state:
        items = db.fetch_all_expenditures(st.session_state['name'])
        if isinstance(items, list):
            return items
    return []

with st.sidebar:
    selected = option_menu(
        menu_title=None,
        options=["Dashboard", "Masukkan Data", "Visualisasi Data", "Edit Data", "Hapus Data"],
        icons=["graph-up-arrow","box-arrow-right", "bar-chart-fill", "pencil-fill", "trash"], 
        orientation="vertical",
    )

    if 'logged_in' in st.session_state and st.session_state['logged_in']:
        if st.button("Log Out"):
            st.session_state['logged_in'] = False
            st.session_state.pop('name', None)
            st.session_state.pop('username', None)
            st.success("Logged out successfully!")
            st.page_link("login.py")
    else:
        st.write("Please log in to access these pages.")

# Redirect to login page if not logged in
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("Please log in to access this page.")
    st.stop()

if selected == "Dashboard":
    st.header("Dashboard")
    expenditures = get_all_expenditures()
    if expenditures:
        labels = [item['periode'] for item in expenditures]
        values = [item['pengeluaran'] for item in expenditures]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=labels,
            y=values,
            mode='lines+markers',
            name='Pengeluaran',
            line=dict(color='#1f77b4', width=2),
            marker=dict(size=8)
        ))

        fig.update_layout(
            title="Performa Pengeluaran",
            xaxis_title="Periode",
            yaxis_title=f"Jumlah ({mata_uang})",
            margin=dict(l=0, r=0, t=40, b=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No data available")

if selected == "Masukkan Data":
    st.header(f"Masukkan Data dengan {mata_uang}")
    with st.form("entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        bulan = col1.selectbox("Pilih Bulan:", bulan, key="bulan")
        tahun = col2.selectbox("Pilih Tahun:", tahun, key="tahun")

        total_pemasukan = 0
        total_pengeluaran = 0

        with st.expander("Pemasukan"):
            for pendapatan in pendapatans:
                total_pemasukan += st.number_input(f"{pendapatan}:", min_value=0, format="%i", step=1000000, key=pendapatan)
        with st.expander("Pengeluaran"):
            for pengeluaran in pengeluarans:
                total_pengeluaran += st.number_input(f"{pengeluaran}:", min_value=0, format="%i", step=1000000, key=pengeluaran)
        with st.expander("Catatan"):
            catatan = st.text_area("", placeholder="berikan catatan")
        
        submitted = st.form_submit_button("Simpan Data")
        if submitted:
            periode = str(st.session_state["tahun"]) + "_" + str(st.session_state["bulan"])
            name = st.session_state['name']
            db.insert_period(name, periode, total_pemasukan, total_pengeluaran, catatan)
            st.success("Data saved!")

if selected == "Edit Data":
    st.header("Edit Data Keuangan")
    periods = get_all_periods()
    if periods:
        period_to_edit = st.selectbox("Pilih Periode untuk Diedit:", periods)
        periode_data = db.get_period(st.session_state['name'], period_to_edit)
        if periode_data:
            with st.form("update_form", clear_on_submit=True):
                catatan = periode_data.get("catatan")
                total_pengeluaran = periode_data.get("pengeluaran")
                total_pemasukan = periode_data.get("pemasukan")

                total_pemasukan = st.number_input("Total Pemasukan", value=periode_data["pemasukan"], min_value=0, step=1000000)
                total_pengeluaran = st.number_input("Total Pengeluaran", value=periode_data["pengeluaran"], min_value=0, step=1000000)
                catatan = st.text_area("Catatan", value=periode_data["catatan"])
                
                submitted = st.form_submit_button("Perbarui Data")
                if submitted:
                    db.update_period(st.session_state['name'], period_to_edit, total_pemasukan, total_pengeluaran, catatan)
                    st.success("Data berhasil diperbarui!")
    else:
        st.write("Tidak ada data yang tersedia untuk diedit.")

if selected == "Hapus Data":
    st.header("Hapus Data Keuangan")
    periods = get_all_periods()
    if periods:
        period_to_delete = st.selectbox("Pilih Periode untuk Dihapus:", periods)
        if st.button("Hapus"):
            db.delete_period(st.session_state['name'], period_to_delete)
            st.success("Data berhasil dihapus!")
    else:
        st.write("Tidak ada data yang tersedia untuk dihapus.")

if selected == "Visualisasi Data":
    st.header("Grafik Data")
    with st.form("saved_periods"):
        name = st.session_state['name']
        period = st.selectbox("Select Period:", get_all_periods())
        submitted = st.form_submit_button("Tampilkan Grafik")
        if submitted:
            periode_data = db.get_period(name, period)
            if isinstance(periode_data, dict):
                catatan = periode_data.get("catatan")
                total_pengeluaran = periode_data.get("pengeluaran")
                total_pemasukan = periode_data.get("pemasukan")

                
                total_pengeluaran = int(total_pengeluaran)
                total_pemasukan = int(total_pemasukan)
               

                remaining_budget = total_pemasukan - total_pengeluaran
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Pemasukan", f"{total_pemasukan} {mata_uang}")
                col2.metric("Total Pengeluaran", f"{total_pengeluaran} {mata_uang}")
                col3.metric("Sisa Budget", f"{remaining_budget} {mata_uang}")
                st.text(f"Catatan: {catatan}")

                labels = ["Total Pemasukan", "Total Pengeluaran"]
                values = [total_pemasukan, total_pengeluaran]
                
                # Create Line Chart
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=labels,
                    y=values,
                    name='Pemasukan dan Pengeluaran',
                    marker_color='#1f77b4'
                ))
                
                fig.update_layout(
                    title="Pemasukan dan Pengeluaran",
                    xaxis_title="Kategori",
                    yaxis_title=f"Jumlah ({mata_uang})",
                    margin=dict(l=0, r=0, t=40, b=20)
                )
                
                st.plotly_chart(fig, use_container_width=True)
