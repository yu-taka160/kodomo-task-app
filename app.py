import streamlit as st
from dotenv import load_dotenv
import os
import requests
import random
import time
import re

ua = st.session_state.get("_browser") or st.session_state.get("_user_agent") or ""
is_mobile = bool(re.search("Mobile|Android|iPhone|iPad", ua))

# PC用キャラセット
pc_animals = ["🐰", "🐣", "🐧"]

# スマホ用キャラセット
mobile_animals = ["🐹", "🐶", "🐷"]

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
        
        .block-container {
            border-top: none !important;
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
        
        /* チェック欄にうっすら枠をつける */
        div[role="checkbox"] {
            border: 2px solid #d9d9d9 !important;
            border-radius: 4px !important;
            background-color: white !important;
        }

        /* 入力欄の枠を復活させる */
        div[data-testid="stTextInput"] input {
            border: 1px solid #d9d9d9 !important;
            border-radius: 4px !important;
            background-color: white !important;
        }
          
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
#     アプリ本体
# =========================
st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
st.markdown("<h1 style='color:#FF8C00;'>こどもタスクチェックアプリ</h1>", unsafe_allow_html=True)

st.markdown("""
<style>
/* PC用キャラ（デフォルト） */
.animal-char::before {
    content: "🐰";
    font-size: 50px;
}

/* スマホだけキャラを上書き */
@media screen and (max-width: 600px) {
    .animal-char::before {
        content: "🐹";   /* ← スマホ用キャラ */
        font-size: 40px;
    }
}
</style>
""", unsafe_allow_html=True)

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
 
        row1 = ''.join(["<span class='emoji-frame'></span>" for _ in range(row1_count)])
        row2 = ''.join(["<span class='emoji-frame'></span>" for _ in range(row2_count)])
        row3 = ''.join(["<span class='emoji-frame'></span>" for _ in range(row3_count)])
        
        placeholder.markdown(
            f"""
            <div style='display:flex; align-items:center; color:green;'>{row1}</div>
            <div style='display:flex; align-items:center; color:green;'>{row2}</div>
            <div style='display:flex; align-items:center; color:green;'>{row3}</div>
            """,
            unsafe_allow_html=True
        )

st.markdown("""
<style>
/* チェック欄の枠を復活させる */
div[role="checkbox"] > div {
    border: 2px solid #d9d9d9 !important;
    border-radius: 4px !important;
    background-color: white !important;
}

/* チェック欄の枠を確実に復活させる（最終版） */
div[role="checkbox"]::before {
    content: "";
    display: block;
    width: 20px;
    height: 20px;
    border: 2px solid #d9d9d9 !important;
    border-radius: 4px;
    background-color: white;
}

/* ヘッダーの黒線・影を完全に消す */
header[data-testid="stHeader"],
header[data-testid="stHeader"] > div,
header[data-testid="stHeader"] * {
    box-shadow: none !important;
    border-bottom: none !important;
}

/* ヘッダー以外の上部に影がある場合の対策 */
section[data-testid="stSidebar"] {
    box-shadow: none !important;
    border-right: none !important;
}

div[data-testid="stAppViewContainer"] {
    box-shadow: none !important;
    border-top: none !important;
}

body, div[data-testid="stAppViewContainer"] {
    background-color: #fff8e6 !important;  /* アイボリー */
}

/* 黒線の最上位の親を消す */
[data-testid="stAppViewContainer"] > div:first-child {
    border-bottom: none !important;
    box-shadow: none !important;
}

/* Streamlit 固定ヘッダーを背景色と同化させる */
header[data-testid="stHeader"] {
    background-color: #FFF8E7 !important;
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
            background-color: white;  /* 枠は白のまま */
            border: 1px solid transparent;  /* ← 黒線の原因を消す */            
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
