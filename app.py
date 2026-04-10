import streamlit as st
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

import pandas as pd
import plotly.express as px
import base64

# ---------------- BACKGROUND FUNCTION ---------------- #
def set_bg(image_file):
    with open(image_file, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()

    st.markdown(f"""
    <style>
    header {{visibility: hidden;}}
    footer {{visibility: hidden;}}

    .block-container {{
        padding-top: 0rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }}

    .stApp {{
        background-image: linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.75)),
        url("data:image/jpeg;base64,{encoded}");
        background-size: 100% 100%;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: white;
    }}

    section[data-testid="stSidebar"] {{
        background: rgba(0,0,0,0.9);
        color: white;
    }}

    .card {{
        background: rgba(255,255,255,0.08);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 0 20px rgba(0,255,255,0.4);
        text-align: center;
        transition: 0.3s;
    }}

    .card:hover {{
        transform: scale(1.05);
        box-shadow: 0 0 25px cyan;
    }}

    .title {{
        font-size: 50px;
        font-weight: bold;
        text-align: center;
        color: #00FFFF;
    }}

    .subtext {{
        text-align: center;
        color: #CCCCCC;
        margin-bottom: 20px;
    }}
    </style>
    """, unsafe_allow_html=True)

set_bg("bg1.jpg")

# ---------------- LOAD DATA ---------------- #
df = pd.read_csv("uac_dataset.csv")
df['Date'] = pd.to_datetime(df['Date'])

cols = [
    'Children in CBP custody',
    'Children in HHS Care',
    'Children transferred out of CBP custody',
    'Children discharged from HHS Care'
]

for col in cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df.fillna(0, inplace=True)

# ---------------- METRICS ---------------- #
df['Total_Load'] = df['Children in CBP custody'] + df['Children in HHS Care']
df['Net_Intake'] = df['Children transferred out of CBP custody'] - df['Children discharged from HHS Care']
df['Backlog'] = df['Net_Intake'].cumsum()

df['Care_Load_Growth'] = df['Total_Load'].pct_change() * 100
df['Intake_Discharge_Gap'] = df['Net_Intake']
threshold = df['Total_Load'].mean()
df['High_Stress'] = df['Total_Load'] > threshold

# ---------------- SIDEBAR ---------------- #

st.sidebar.markdown("---")
st.sidebar.subheader(" About Project")
st.sidebar.write("A smart analytics dashboard for tracking UAC system load and capacity. It helps identify trends, monitor performance, and predict system pressure.")

st.sidebar.markdown("---")
st.sidebar.subheader(" Insights")
st.sidebar.write("• Detect overload periods")
st.sidebar.write("• Monitor intake vs discharge")
st.sidebar.write("• Forecast future demand")

# ---------------- TITLE ---------------- #
st.markdown('<div class="title">UAC System Capacity & Care Load</div>', unsafe_allow_html=True)
st.markdown('<div class="subtext">Monitoring system load using analytics & AI</div>', unsafe_allow_html=True)

# ---------------- KPI ---------------- #
st.subheader(" KPI Summary")

col1, col2, col3 = st.columns(3)

col1.markdown(f'<div class="card"><h3>Total Load</h3><h1 style="color:#00FFFF;">{int(df["Total_Load"].mean())}</h1></div>', unsafe_allow_html=True)
col2.markdown(f'<div class="card"><h3>Net Intake</h3><h1 style="color:#FFA500;">{int(df["Net_Intake"].mean())}</h1></div>', unsafe_allow_html=True)
col3.markdown(f'<div class="card"><h3>Backlog</h3><h1 style="color:#FF4B4B;">{int(df["Backlog"].iloc[-1])}</h1></div>', unsafe_allow_html=True)

# ---------------- GRAPHS ---------------- #

# 1️⃣ Total Load
st.markdown("###  System Load Overview")

c1, c2 = st.columns(2)
with c1:
    load_start = st.date_input("Start Date", df['Date'].min(), key="load_start")
with c2:
    load_end = st.date_input("End Date", df['Date'].max(), key="load_end")

df1 = df[(df['Date'] >= pd.to_datetime(load_start)) & (df['Date'] <= pd.to_datetime(load_end))]

fig1 = px.line(df1, x='Date', y='Total_Load', color_discrete_sequence=["#00FFFF"])
fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white')
st.plotly_chart(fig1, use_container_width=True)

if st.checkbox("Show Data for Total Load"):
    st.dataframe(df1[['Date', 'Total_Load']].head(20), use_container_width=True)

# 2️⃣ Net Intake
st.markdown("### Net Intake Trend")

c1, c2 = st.columns(2)
with c1:
    ni_start = st.date_input("Start Date", df['Date'].min(), key="ni_start")
with c2:
    ni_end = st.date_input("End Date", df['Date'].max(), key="ni_end")

df2 = df[(df['Date'] >= pd.to_datetime(ni_start)) & (df['Date'] <= pd.to_datetime(ni_end))]

fig2 = px.line(df2, x='Date', y='Net_Intake', color_discrete_sequence=["#FFA500"])
fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white')
st.plotly_chart(fig2, use_container_width=True)

if st.checkbox("Show Data for Net Intake"):
    st.dataframe(df2[['Date', 'Net_Intake']].head(20), use_container_width=True)

# 3️⃣ Backlog
st.markdown("### Backlog Growth")

c1, c2 = st.columns(2)
with c1:
    b_start = st.date_input("Start Date", df['Date'].min(), key="b_start")
with c2:
    b_end = st.date_input("End Date", df['Date'].max(), key="b_end")

df3 = df[(df['Date'] >= pd.to_datetime(b_start)) & (df['Date'] <= pd.to_datetime(b_end))]

fig3 = px.line(df3, x='Date', y='Backlog', color_discrete_sequence=["#FF4B4B"])
fig3.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white')
st.plotly_chart(fig3, use_container_width=True)

if st.checkbox("Show Data for Backlog"):
    st.dataframe(df3[['Date', 'Backlog']].head(20), use_container_width=True)

# 4️⃣ Growth
st.markdown("### Care Load Growth Rate (%)")

c1, c2 = st.columns(2)
with c1:
    g_start = st.date_input("Start Date", df['Date'].min(), key="g_start")
with c2:
    g_end = st.date_input("End Date", df['Date'].max(), key="g_end")

df4 = df[(df['Date'] >= pd.to_datetime(g_start)) & (df['Date'] <= pd.to_datetime(g_end))]

fig4 = px.line(df4, x='Date', y='Care_Load_Growth', color_discrete_sequence=["#00FF7F"])
fig4.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white')
st.plotly_chart(fig4, use_container_width=True)

if st.checkbox("Show Data for Growth"):
    st.dataframe(df4[['Date', 'Care_Load_Growth']].head(20), use_container_width=True)

# 5️⃣ Gap
st.markdown("### Intake vs Discharge Gap")

c1, c2 = st.columns(2)
with c1:
    gap_start = st.date_input("Start Date", df['Date'].min(), key="gap_start")
with c2:
    gap_end = st.date_input("End Date", df['Date'].max(), key="gap_end")

df5 = df[(df['Date'] >= pd.to_datetime(gap_start)) & (df['Date'] <= pd.to_datetime(gap_end))]

fig5 = px.line(df5, x='Date', y='Intake_Discharge_Gap', color_discrete_sequence=["#FFD700"])
fig5.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white')
st.plotly_chart(fig5, use_container_width=True)

if st.checkbox("Show Data for Gap"):
    st.dataframe(df5[['Date', 'Intake_Discharge_Gap']].head(20), use_container_width=True)

# 6️⃣ Stress
st.markdown("### High Load Stress Indicator")

c1, c2 = st.columns(2)
with c1:
    s_start = st.date_input("Start Date", df['Date'].min(), key="s_start")
with c2:
    s_end = st.date_input("End Date", df['Date'].max(), key="s_end")

df6 = df[(df['Date'] >= pd.to_datetime(s_start)) & (df['Date'] <= pd.to_datetime(s_end))]

fig6 = px.scatter(df6, x='Date', y='Total_Load', color='High_Stress',
                  color_discrete_map={True: 'red', False: 'green'})
fig6.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white')
st.plotly_chart(fig6, use_container_width=True)

if st.checkbox("Show Data for Stress"):
    st.dataframe(df6[['Date', 'Total_Load', 'High_Stress']].head(20), use_container_width=True)

# ---------------- TABLE ---------------- #
st.subheader("📋 Data Preview")
st.dataframe(df.head(10))
