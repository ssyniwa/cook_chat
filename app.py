import streamlit as st
import google.generativeai as genai

# API設定
genai.configure(api_key="AIzaSyDroxlJ2EaGjfRTNYUtFB6po0sCKSPUBgo")
model = genai.GenerativeModel('gemini-3.1-flash-light')

# ページ設定
st.set_page_config(page_title="異界美食クラブ", page_icon="🍲")

# --- セッション管理 ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "username" not in st.session_state:
    st.session_state.username = None

# --- ログイン画面 ---
if not st.session_state.username:
    st.title("Welcome to 異界美食クラブ 🍲")
    name = st.text_input("ハンター名を入力して入室してください")
    if st.button("入室する"):
        if name:
            st.session_state.username = name
            st.rerun()
    st.stop()

# --- チャット画面 ---
st.title(f"異界美食クラブへようこそ、{st.session_state.username}さん！")
st.sidebar.write(f"ログイン中: {st.session_state.username}")

# 料理人AIの役割定義
system_prompt = """
あなたは伝説の「異界料理人」です。ユーザーが異界の奇妙な食材を持ってきます。
あなたはそれを、未知のスパイスや調理法を使って、最高級の料理に仕上げるレシピを提案してください。
口調は少し傲慢だが、料理には情熱的なプロの料理人として振る舞ってください。
"""

# 過去の会話を表示
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ユーザー入力
if prompt := st.chat_input("異界の食材を提案してください..."):
    # ユーザー発言を保存・表示
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gemini API呼び出し
    with st.chat_message("assistant"):
        full_prompt = system_prompt + f"\n食材: {prompt}"
        response = model.generate_content(full_prompt)
        st.markdown(response.text)
    
    # AIの回答を保存
    st.session_state.messages.append({"role": "assistant", "content": response.text})
