"""Optional Streamlit chat interface: streamlit run src/app.py"""

import streamlit as st

from src.agent import Agent


st.set_page_config(page_title="Agentic AI Assistant", page_icon="🤖", layout="centered")
st.title("🤖 الوكيل الذكي العملي")
st.caption("تخطيط + أدوات آمنة + ذاكرة محلية + Gemini اختياري")

if "agent" not in st.session_state:
    st.session_state.agent = Agent()
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("اكتب طلبك..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        result = st.session_state.agent.run(prompt)
        st.markdown(result.answer)
        with st.expander("تفاصيل التنفيذ"):
            st.json({"steps": result.steps, "used_llm": result.used_llm})
    st.session_state.messages.append({"role": "assistant", "content": result.answer})

with st.sidebar:
    if st.button("مسح الذاكرة"):
        st.session_state.agent.memory.clear()
        st.session_state.messages = []
        st.rerun()
