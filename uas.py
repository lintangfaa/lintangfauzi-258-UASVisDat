# import library yang sudah diinstall sebelumnya
import pandas as pd # untuk load data
# import plotly.express as px  # untuk proses pembuatan grafik
import streamlit as st # untuk menjalankan program

# setting website page (judul, logo, layout)
st.set_page_config(page_title="Sales Dashboard", page_icon=":traffic_light:", layout="wide")

# ---- MAINPAGE ----
st.title(":car: Data Penindakan Pelanggaran Lalu Lintas dan Angkutan Jalan Tahun 2021")
st.markdown("#") # pembuatan garis pembatas

# proses pembacaan dataset
df = pd.read_excel(
    io="dataset.xlsx", # nama file dataset
    engine="openpyxl",
    sheet_name="Data",  # nama worksheet yang digunakan
    usecols="A:I",
    nrows=43,
)

# pembuatan sidebar untuk fitur filtering
st.sidebar.header("Please Filter Here:")
wilayah = st.sidebar.multiselect(
    "Pilih Wilayah:",
    options=df["Wilayah"].unique(),
    default=df["Wilayah"].unique()
)

bulan = st.sidebar.multiselect(
    "Pilih Bulan:",
    options=df["Bulan"].unique(),
    default=df["Bulan"].unique(),
)


# penerapan fitur filter kedalam query
df_selection = df.query(
    "Wilayah == @wilayah & Bulan == @bulan"
)

st.dataframe(df_selection) # menampilkan dataset

st.markdown("""---""")

# ---- MAINPAGE ----
st.title(":bar_chart: Dashboard Data")
st.markdown("##")

# TOP KPI's
bap_tilang = int(df_selection["BAP_Tilang"].sum())
derek = int(df_selection["Penderekan"].sum())
left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total BAP Tilang :")
    st.subheader(f"{bap_tilang:,}")
with middle_column:
    st.subheader("Total Penderekan :")
    st.subheader(f"{derek}")

st.markdown("""---""")

# BAP TILANG BY WILAYAH [BAR CHART]
tilang_wilayah = (df_selection.groupby(by=["Wilayah"]).sum()[["BAP_Tilang"]])
fig_tilang = px.bar(
    tilang_wilayah,
    x=tilang_wilayah.index,
    y="BAP_Tilang",
    title="<b>BAP Tilang by Wilayah</b>",
    color_discrete_sequence=["#0083B8"] * len(tilang_wilayah),
    template="plotly_white",
)
fig_tilang.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

df_tilang = pd.read_excel(
    io="dataset.xlsx", # nama file dataset
    engine="openpyxl",
    sheet_name="Data",  # nama worksheet yang digunakan
    usecols="A:K",
    nrows=43,
)

df_select = df_tilang.query(
    "Wilayah == @wilayah & Bulan == @bulan"
)

# --- PLOT PIE CHART
pie_chart = px.pie(df_select,
                title='<b>Total Penderekan tiap Bulan</b>',
                values='Count',
                names='Bulan')


left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_tilang, use_container_width=True)
right_column.plotly_chart(pie_chart, use_container_width=True)

# --- LINE CHART
line_chart = px.line(df_select, x="Wilayah", y="OCP2_Total", title='<b>Total OCP Roda 2 tiap Wilayah</b>')

left_column2, right_column2 = st.columns(2)
left_column.plotly_chart(line_chart, use_container_width=True)
