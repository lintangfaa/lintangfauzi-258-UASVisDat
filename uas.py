import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import numpy as np

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
# Streamlit page configuration 
st.set_page_config(page_title="Dashboard", page_icon=":bar_chart:", layout="wide")

st.title(":traffic_light: Penindakan Pelanggaran Lalu Lintas dan Angkutan Jalan Tahun 2021 Bulan Januari-Juli")
st.subheader("by : Istianah Retna Ningtyas Handayani - 1900018276 - UAS -VDATA - C")
st.markdown("#")

# ---- READ EXCEL ----
df = pd.read_excel(
    io="data_penindakan_pelanggaran_lalu_lintas_dan_angkutan_jalan_tahun_2021.xlsx",
    engine="openpyxl",
   sheet_name="Sheet1",
    usecols="A:J",
    nrows=43,
)

#==================Sidebar====================

st.sidebar.header("Silahkan Filter Data Disini :")

Bulan = st.sidebar.multiselect(
    "Filter Bulan:",
    options=df["bulan"].unique(),
    default=df["bulan"].unique(),
)

Wilayah = st.sidebar.multiselect(
    "Filter Wilayah:",
    options=df["wilayah"].unique(),
    default=df["wilayah"].unique(),
)

df_selection = df.query(
    " bulan ==@Bulan & wilayah ==@Wilayah"
)

st.markdown("#")


# TOP KPI's
BAP_Tilang = int(df_selection["BAP_tilang"].sum())
Penderekan = int(df_selection["Penderekan"].sum())
Rata_rata_BAP_Tilang = int(df_selection["BAP_tilang"].mean())

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total BAP Tilang :oncoming_police_car:")
    st.subheader(f"{BAP_Tilang:,}")
with middle_column:
    st.subheader("Total Penderekan  :police_car:")
    st.subheader(f"{Penderekan:,}")
with right_column:
    st.subheader("Rata-Rata BAP Tilang :bar_chart:")
    st.subheader(f"{Rata_rata_BAP_Tilang}")

st.markdown("#")
st.dataframe(df_selection) # view dataframe on page

#------------------------------ Visualisasi yang lain ---------------------------


pie_chart = px.pie(df,
                    title="<b>BAP Tilang Perbulan</b>",
                    values= 'BAP_tilang',
                    names= 'bulan')

st.plotly_chart(pie_chart)

# ================================================================================

data_penindakan_pelanggaran_lalu_lintas = (
    df_selection.groupby(by=["wilayah"]).sum()[["BAP_tilang"]].sort_values(by="BAP_tilang")
)
fig_pelanggaran_lalu_lintas = px.bar(
    data_penindakan_pelanggaran_lalu_lintas,
    x="BAP_tilang",
    y=data_penindakan_pelanggaran_lalu_lintas.index,
    orientation="h",
    title="<b>BAP Tilang Berdasarkan Wilayah</b>",
    color_discrete_sequence=["#0083B8"] * len(data_penindakan_pelanggaran_lalu_lintas),
    template="plotly_white",
)
fig_pelanggaran_lalu_lintas.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

st.plotly_chart(fig_pelanggaran_lalu_lintas, use_container_width=True)

# ================================================================================
st.text("Grafik Garis Berdasarkan Kriteria BAP Tilang, Penderekan dan Stop Operasi ")

chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['BAP_tilang', 'Penderekan', 'stop_operasi'])

st.line_chart(chart_data)


# ================================================================================
databar_chart_pelanggaran_lalu_lintas = (
    df_selection.groupby(by=["bulan"]).sum()[["Penderekan"]].sort_values(by="Penderekan")
)
bar_chart = px.bar(databar_chart_pelanggaran_lalu_lintas,
                    x=databar_chart_pelanggaran_lalu_lintas.index,
                    y='Penderekan',
                    text='penderekan',
                    title="<b>Penderekan Berdasarkan Bulan</b>",
                    color_discrete_sequence = ['#F63366']*len(databar_chart_pelanggaran_lalu_lintas),
                    template='plotly_white')
st.plotly_chart(bar_chart)

