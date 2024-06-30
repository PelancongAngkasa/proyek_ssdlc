import calendar
from datetime import datetime
import streamlit as st
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import database as db

pendapatans = ["Gaji", "Blog", "Pendapatan Lainnya"]
pengeluarans = ["Kos", "Pajak", "Makan", "Hiburan","Tabungan"]
mata_uang = "IDR"
judul = "Pencacatan Pendapatan dan Pengeluaran"
icon = ":money_with_wings:"
layout = "centered"

st.set_page_config(page_title=judul, page_icon=icon, layout=layout)
st.title(judul + " " + icon)

if 'name' in st.session_state:
    st.subheader(f"Selamat datang, {st.session_state['name']}!")

tahun = [datetime.today().year, datetime.today().year + 1]
bulan = list(calendar.month_name[1:]) 

def get_all_periods():
    items = db.fetch_all_periods()
    periods = [item["key"] for item in items]
    return periods

selected = option_menu(
    menu_title=None,
    options=["Masukkan Data", "Visualisasi Data"],
    icons=["pencil-fill", "bar-chart-fill"], 
    orientation="horizontal",
)
if selected == "Masukkan Data":
    st.header(f"Masukkan Data dengan {mata_uang}")
    with st.form("entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        col1.selectbox("Pilih Bulan:", bulan, key="bulan")
        col2.selectbox("Pilih Tahun:", tahun, key="tahun")

        with st.expander("Pemasukan"):
            for pendapatan in pendapatans:
                st.number_input(f"{pendapatan}:", min_value=0, format="%i", step=10, key=pendapatan)
        with st.expander("Pengeluaran"):
            for pengeluaran in pengeluarans:
                st.number_input(f"{pengeluaran}:", min_value=0, format="%i", step=10, key=pengeluaran)
        with st.expander("Catatan"):
            catatan = st.text_area("", placeholder="berikan catatan")
        
        submitted = st.form_submit_button("Simpan Data")
        if submitted:
            periode = str(st.session_state["tahun"]) + " " + str(st.session_state["bulan"])
            pendapatans = {pendapatan: st.session_state[pendapatan] for pendapatan in pendapatans}
            pengeluarans = {pengeluaran: st.session_state[pengeluaran] for pengeluaran in pengeluarans}
            #masukin ke database nanti
            if 'name' in st.session_state:
                name = st.session_state['name']
                db.insert_period(periode, pendapatans, pengeluarans, catatan)
                st.success("Data saved!")
            else:
                st.error("User not logged in. Please log in first.")


    #plot
    if selected == "Data Visualization":
        st.header("Data Visualization")
        with st.form("saved_periods"):
            if 'name' in st.session_state:
                name = st.session_state['name']
                period = st.selectbox("Select Period:", get_all_periods())
                submitted = st.form_submit_button("Plot Period")
                if submitted:
                    # Get data from database
                    periode_data = db.get_period(period)
                    Komentar = periode_data.get("catatan")
                    pengeluarans = periode_data.get("pengeluaran")
                    pendapatans = periode_data.get("pemasukan")

                    # Create metrics
                    total_income = sum(pendapatan.values())
                    total_expense = sum(pengeluarans.values())
                    remaining_budget = total_income - total_expense
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Total Pemasukan", f"{total_income} {mata_uang}")
                    col2.metric("Total Pengeluaran", f"{total_expense} {mata_uang}")
                    col3.metric("Sisa Budget", f"{remaining_budget} {mata_uang}")
                    st.text(f"Catatan: {catatan}")

                    # Create sankey chart
                    label = list(pendapatans.keys()) + ["Total Income"] + list(pengeluarans.keys())
                    source = list(range(len(pendapatans))) + [len(pendapatans)] * len(pengeluarans)
                    target = [len(pendapatans)] * len(pendapatans) + [label.index(pengeluaran) for pengeluaran in pengeluarans.keys()]
                    value = list(pendapatans.values()) + list(pengeluarans.values())

                    # Data to dict, dict to sankey
                    link = dict(source=source, target=target, value=value)
                    node = dict(label=label, pad=20, thickness=30, color="#E694FF")
                    data = go.Sankey(link=link, node=node)

                    # Plot it!
                    fig = go.Figure(data)
                    fig.update_layout(margin=dict(l=0, r=0, t=5, b=5))
                    st.plotly_chart(fig, use_container_width=True)  
            else:
                st.error("User not logged in. Please log in first.")