import streamlit as st
from openai import OpenAI

st.title("AI 聊天助手")

client = OpenAI(
    api_key=st.secrets["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com",
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "你是一个友好、简洁的中文 AI 助手。"
        }
    ]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.write(message["content"])

user_input = st.chat_input("请输入消息")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=st.session_state.messages
        )
        ai_reply = response.choices[0].message.content
    except Exception as error:
        ai_reply = f"调用失败：{error}"

    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_reply
    })

    st.rerun()