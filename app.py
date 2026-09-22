import streamlit as st
from dotenv import load_dotenv
import os
import requests
import random
import time
from streamlit_js_eval import streamlit_js_eval 

# 画面幅を取得
width = streamlit_js_eval(js_expressions="window.innerWidth")

if width is None:
    width = 800

load_dotenv()

endpoint = os.getenv("AZURE_LANGUAGE_ENDPOINT")
key = os.getenv("AZURE_LANGUAGE_KEY")
region = os.getenv("AZURE_LANGUAGE_REGION")

def analyze_sentiment(text):
    url = f"{endpoint}/text/analytics/v3.1/sentiment"

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }

    payload = {
        "documents": [
            {"id": "1", "language": "ja", "text": text}
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    result = response.json()

    return result["documents"][0]["sentiment"]

# =========================
#         CSS
# =========================
st.markdown(
    """
    <style>

        /* 背景（アイボリー） */
        .stApp, .block-container {
            background-color: #FFF8E7;
        }

        /* 入力欄ラベル */
        .stTextInput > label {
            color: black !important;
        }

        /* 追加ボタン：白 → 押したとき赤 */
        .stButton > button {
            background-color: white !important;
            color: black !important;
            border: 1px solid #ccc !important;
        }
        .stButton > button:active {
            background-color: red !important;
            color: white !important;
        }

        /* タイトル・見出し（オレンジ） */
        h1, h3 {
            color: #FF8C00 !important;
        }

        /* タスク文字を黒にする */
        div[data-testid="stCheckbox"] label {
            color: black !important;
        }

        /* チェック前の□を白にする */
        div[data-testid="stCheckbox"] div[role="checkbox"] {
            background-color: white !important;
            border: 2px solid #666 !important;
            box-shadow: none !important;
        }

        /* メッセージ（明るい緑） */
        .message-green {
            color: #7CFF7C !important;
            font-weight: bold;
            font-size: 28px !important;
        }

        /* progress-text 以外は小さいまま（サイズ指定なし） */
        div[data-testid="stMarkdown"] p:not(.progress-text) {
            color: black !important;
        }

        /* progress-text を大きくする（進捗表示用） */
        .progress-text {
            font-size: 28px !important;
            font-weight: bold;
        }

        /* 100%のときだけ赤文字を強制する */
        .progress-text[style*="color:red"] {
            color: red !important;
        }

        /* 絵文字のサイズ（PC用） */
        .emoji-frame {
            font-size: 60px;
        }
  
        /* スマホ（画面幅600px以下）のときだけ適用 */
        @media (max-width: 600px) {
            div[data-testid="stMarkdown"] .message-green {
                font-size: 20px !important;
                line-height: 1.2 !important;
            }
            .progress-text {
                font-size: 20px !important;
            }
            .emoji-frame {
                font-size: 28px !important;
            }
        }

        header, .css-1dp5vir {
            border: none !important;
            box-shadow: none !important;
        }
        
        div[role="checkbox"] {
            background-color: white !important;
            border: 2px solid #666 !important;
        }
        
        div[data-testid="stProgress"] div {
            background-color: white !important;
        }
        
        div[data-testid="stProgress"] div > div {
            background-color: red !important;
        }
        
        input {
            border: 1px solid #ccc !important;
            background-color: white !important;
            color: black !important;
        }

        /* ヘッダーの黒い線・影を消す（Emotion CSS） */
        .css-1dp5vir, .css-1avcm0n {
            box-shadow: none !important;
            border-bottom: none !important;
        }
        
        /* 入力欄の黒枠を消す */
        div[data-testid="stTextInput"] > div > div {
            border: 1px solid #ccc !important;
            background-color: white !important;
            box-shadow: none !important;
        }
        
         /* チェックボックスの黒枠を消す（Emotion CSS） */
        .css-1p0v0p6, .css-16idsys {
            background-color: white !important;
            border: 2px solid #666 !important;
            box-shadow: none !important;
        }
            
        
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
#     アプリ本体
# =========================

st.title("こどもタスクチェックアプリ")

# --- タスクを保存するための session_state ---
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# --- タスク追加フォーム ---
new_task = st.text_input(
    "タスク(やること)を入力してください",
    key="task_input",
    autocomplete="off"
)

if st.button("ついかボタン"):
    if new_task:
        st.session_state.tasks.append({"name": new_task, "done": False})
        st.rerun()

# --- タスク一覧表示 ---
st.subheader("きょうのミッション")

messages = [
    "できたね！すごい！",
    "えらい！そのちょうし！",
    "ひとつクリアしたよ！"
]

for i, task in enumerate(st.session_state.tasks):
    checked = st.checkbox(task["name"], key=f"task_{i}")

    if checked and not task["done"]:
        task["done"] = True

        done_count = sum(1 for t in st.session_state.tasks if t["done"])
        remaining = len(st.session_state.tasks) - done_count
        
        # PC用キャラセット
        pc_animals = ["🐰", "🐣", "🐧"]
        
        # スマホ用キャラセット
        mobile_animals = ["🐹", "🐷", "🐶"]

        # 画面幅でスマホ判定（新しい width を使う）
        if width < 600:
            char = random.choice(mobile_animals)
        else:
            char = random.choice(pc_animals)
        
        dance = {
            "🐰": ["🐰", "✨", "🐰", "💫", "🐰"],
            "🐣": ["🐣", "💫", "🐣", "✨", "🐣"],
            "🐧": ["🐧", "✨", "🐧", "💫", "🐧"],
            "🐹": ["🐹", "✨", "🐹", "💫", "🐹"],
            "🐷": ["🐷", "💫", "🐷", "✨", "🐷"],
            "🐶": ["🐶", "✨", "🐶", "💫", "🐶"]
        }

        if remaining == 0:
            message = "ミッションかんりょう✌"
        elif remaining == 1:
            message = "あとすこしでコンプリート！レッツゴー！"
        else:
            message = random.choice(messages)

        st.markdown(
            f"""
            <div style='display:flex; align-items:center;'>
                <span class='message-green' style='font-size:35px; margin-left:8px;'>「{message}」</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        placeholder = st.empty()
        frames = dance[char]

        for frame in frames:
            row1_count = min(done_count, 12)
            row2_count = min(max(done_count - 12, 0), 12)
            row3_count = max(done_count - 24, 0)

            row1 = ''.join([f"<span class='emoji-frame'>{frame}</span>" for _ in range(row1_count)])
            row2 = ''.join([f"<span class='emoji-frame'>{frame}</span>" for _ in range(row2_count)])
            row3 = ''.join([f"<span class='emoji-frame'>{frame}</span>" for _ in range(row3_count)])

            placeholder.markdown(
                f"""
                <div style='display:flex; align-items:center; color:green;'>{row1}</div>
                <div style='display:flex; align-items:center; color:green;'>{row2}</div>
                <div style='display:flex; align-items:center; color:green;'>{row3}</div>
                """,
                unsafe_allow_html=True
            )

            time.sleep(0.3)

st.markdown("""
<style>
/* チェック欄の黒い□を白くする（枠は消す） */
.st-emotion-cache-x5jhx8 {
    background-color: white !important;
    border: none !important;
    box-shadow: none !important;
}

/* 上部の黒い線を消す */
header[data-testid="stHeader"],
header[data-testid="stHeader"] > div {
    box-shadow: none !important;
    border-bottom: none !important;
}
</style>
""", unsafe_allow_html=True)

# --- 1日の達成率 ---
total = len(st.session_state.tasks)
done = sum(1 for t in st.session_state.tasks if t["done"])

if total > 0:
    rate = done / total
    st.subheader("きょうの　たっせいりつ")

    percent = int(rate * 100)

    st.markdown(
        f"""
        <div style="
            width: 100%;
            height: 20px;
            background-color: white;
            border: 1px solid #ccc;
            border-radius: 5px;
            overflow: hidden;
            margin-bottom: 10px;
        ">
            <div style="
                width: {percent}%;
                height: 100%;
                background-color: red;
            "></div>
        </div>
        """,
        unsafe_allow_html=True
    )
    # ここがあなたの希望どおりの表示
    if percent == 100:
        st.markdown(
            f"<p class='progress-text' style='color:red;'>👏👏{percent}%できたよ！👏👏</p>",
            unsafe_allow_html=True
        )

    else:
        st.markdown(
            f"<p class='progress-text' style='color:black;'>{percent}%できたよ！</p>",
            unsafe_allow_html=True
        )

else:
    st.write("まだミッションがないよ")
