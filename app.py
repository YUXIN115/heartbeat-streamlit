
import streamlit as st
import numpy as np
import pandas as pd
import time
from datetime import datetime

st.set_page_config(page_title="心跳包", layout="wide")
st.title("❤️ 心跳包实时数据可视化")

st.sidebar.header("参数设置")
heart_rate = st.sidebar.slider("心率 BPM", 40, 180, 75)
noise = st.sidebar.slider("噪声", 0.0, 3.0, 0.5)
speed = st.sidebar.slider("更新间隔秒", 0.1, 1.0, 0.2)

if "data" not in st.session_state:
    st.session_state.data = []

def heartbeat(t, bpm, noise):
    f = bpm / 60
    v = np.sin(2 * np.pi * f * t)
    v += 0.5 * np.sin(4 * np.pi * f * t)
    v += noise * np.random.randn()
    return v

chart = st.empty()
metric = st.empty()

while True:
    t = time.time()
    now = datetime.now()
    val = heartbeat(t, heart_rate, noise)

    st.session_state.data.append({
        "time": now,
        "value": val
    })

    if len(st.session_state.data) > 100:
        st.session_state.data.pop(0)

    df = pd.DataFrame(st.session_state.data)

    with chart.container():
        st.subheader("📈 心跳波形")
        st.line_chart(df, x="time", y="value")

    with metric.container():
        c1, c2 = st.columns(2)
        c1.metric("当前值", round(val, 2))
        c2.metric("数据点数", len(df))

    time.sleep(speed)