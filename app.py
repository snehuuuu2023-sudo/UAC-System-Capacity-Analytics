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

    /* REMOVE HEADER + WHITE SPACE */
    header {{visibility: hidden;}}
    footer {{visibility: hidden;}}

    .block-container {{
        padding-top: 0rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }}

    .main {{
        max-width: 100%;
    }}

    /* BACKGROUND FIX (NO ZOOM ISSUE) */
    .stApp {{
        background-image: linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.75)),
        url("data:image/jpeg;base64,{encoded}");
        background-size: 100% 100%;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: white;
    }}

    /* SIDEBAR */
    section[data-testid="stSidebar"] {{
        background: rgba(0,0,0,0.9);
        color : white;
    }}

    /* KPI CARDS */
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

    /* TITLE */
    .title {{
        font-size: 50px;
        font-weight: bold;
        text-align: center;
        color: #00FFFF;
        font-family: 'Poppins', sans-serif;
        letter-spacing: 1px;
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

# ---------------- SIDEBAR ---------------- #
st.sidebar.title("⚙️ Filters")

start_date = st.sidebar.date_input("Start Date", df['Date'].min())
end_date = st.sidebar.date_input("End Date", df['Date'].max())

metric = st.sidebar.selectbox("Select Metric", ["Total_Load", "Net_Intake", "Backlog"])
time_granularity = st.sidebar.selectbox("Time Granularity", ["Daily", "Monthly"])

st.sidebar.markdown("---")
st.sidebar.subheader("📊 About Project")
st.sidebar.write("A smart analytics dashboard for tracking UAC system load and capacity. It helps identify trends, monitor performance, and predict system pressure.")

st.sidebar.markdown("---")
st.sidebar.subheader("📌 Insights")
st.sidebar.write("• Detect overload periods")
st.sidebar.write("• Monitor intake vs discharge")
st.sidebar.write("• Forecast future demand")

# ---------------- FILTER DATA ---------------- #
df = df[(df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))]

# ---------------- TITLE ---------------- #
st.markdown('<div class="title">UAC System Capacity & Care Load </div>', unsafe_allow_html=True)
st.markdown('<div class="subtext">Monitoring system load, intake balance, and capacity stress using analytics & AI</div>', unsafe_allow_html=True)

# ---------------- KPI ---------------- #
st.subheader("📊 KPI Summary")

col1, col2, col3 = st.columns(3)

col1.markdown(f'<div class="card"><h3>Total Load</h3><h1 style="color:#00FFFF;">{int(df["Total_Load"].mean())}</h1></div>', unsafe_allow_html=True)
col2.markdown(f'<div class="card"><h3>Net Intake</h3><h1 style="color:#FFA500;">{int(df["Net_Intake"].mean())}</h1></div>', unsafe_allow_html=True)
col3.markdown(f'<div class="card"><h3>Backlog</h3><h1 style="color:#FF4B4B;">{int(df["Backlog"].iloc[-1])}</h1></div>', unsafe_allow_html=True)

# ---------------- GRAPHS ---------------- #
st.subheader("📈 System Load Overview")

fig1 = px.line(df, x='Date', y='Total_Load', color_discrete_sequence=["#00FFFF"])
fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white')
st.plotly_chart(fig1, use_container_width=True)

# 👉 Toggle Table
if st.checkbox("Show Data for Total Load"):
    st.dataframe(df[['Date', 'Total_Load']].head(20), use_container_width=True)

st.subheader("📊 Net Intake Trend")

fig2 = px.line(df, x='Date', y='Net_Intake', color_discrete_sequence=["#FFA500"])
fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white')
st.plotly_chart(fig2, use_container_width=True)

if st.checkbox("Show Data for Net Intake"):
    st.dataframe(df[['Date', 'Net_Intake']].head(20), use_container_width=True)

st.subheader("🚨 Backlog Growth")

fig3 = px.line(df, x='Date', y='Backlog', color_discrete_sequence=["#FF4B4B"])
fig3.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white')
st.plotly_chart(fig3, use_container_width=True)

if st.checkbox("Show Data for Backlog"):
    st.dataframe(df[['Date', 'Backlog']].head(20), use_container_width=True)

# ---------------- TABLE ---------------- #
st.subheader("📋 Data Preview")

st.dataframe(df.head(10))