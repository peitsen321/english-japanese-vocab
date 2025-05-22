# Filename: app.py


import os
import streamlit as st
import pandas as pd
import random
from dotenv import load_dotenv
from openai import OpenAI
from openai import OpenAIError
import pandas as pd
import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


# -------------------------
# 頁面設定
# -------------------------
st.set_page_config(page_title="多語言學習小工具", layout="wide")


st.markdown("""
<style>
body, .main {
    background-color: #FFE5B4;  /* 淡橘色背景 */
}
h1, h2, h3, p, div, span {
    color: #4B2E00;
}
div.stButton > button:first-child {
    background-color: #F18F49;  /* 中藍色按鈕 */
    color: white;
    font-weight: 800;
    border-radius: 8px;
    padding: 8px 20px;
    transition: background-color 0.3s ease;
}
div.stButton > button:hover {
    background-color: #1C86EE;
}
</style>
""", unsafe_allow_html=True)



# Load .env 裡的 API KEY
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 初始化 OpenAI 客戶端（新版官方用法）
client = OpenAI(api_key=OPENAI_API_KEY)

# -------------------------

# i18n 多語介面設定
# -------------------------
LANGUAGES = {
    "English": {
        "select_interface": "Select Interface Language",
        "select_word_lang": "Select the language of the word you want to look up",
        "select_explain_lang": "Select the language in which the word will be explained",
        "input_word": "Enter the word to look up",
        "lookup": "Look up word",
        "dictionary": "Dictionary",
        "quiz": "Vocabulary Quiz",
        "feedback": "Feedback",
        "learned_words": "Vocabulary learned",
        "explanation_example": "Explanation and example:",
        "feedback_prompt": "Please leave your feedback or suggestion:",
        "submit_feedback": "Submit Feedback",
        "thank_feedback": "Thank you for your feedback!",
        "error_api": "Error in API call, please try again later.",
        "title": "Vocabulary Quiz",
        "select_test": "Select Test Type",
        "select_level": "Select Level",
        "select_lang": "Interface Language",
        "select_exp_lang": "Select Option Language",
        "start_test": "Start Quiz",
        "submit": "Submit Answer",
        "score": "Your score is",
        "question": "Question",
        "choose_answer": "Please choose the correct explanation",
        "restart": "Restart",
        "next": "Next",
        "start_prompt": "Please press 'Start Quiz' to begin.",
        "correct": "correct!!",
        "incorrect": "Incorrect! The answer is ： ",
        "your_answer": "your answer is ",
        "Continue": "Continue：",
    },
    "日本語": {
        "select_interface": "インターフェース言語を選択してください",
        "select_word_lang": "調べる単語の言語を選択してください",
        "select_explain_lang": "単語の説明の言語を選択してください",
        "input_word": "調べたい単語を入力してください",
        "lookup": "単語を調べる",
        "dictionary": "辞書",
        "quiz": "単語クイズ",
        "feedback": "フィードバック",
        "explanation_example": "説明と例文：",
        "learned_words": "これまでに調べた単語",
        "feedback_prompt": "フィードバックやご意見をお願いします：",
        "submit_feedback": "送信",
        "thank_feedback": "フィードバックありがとうございます！",
        "error_api": "API呼び出しにエラーが発生しました。後でもう一度お試しください。",
        "title": "単語クイズ",
        "select_test": "テスト種類を選択",
        "select_level": "レベルを選択",
        "select_lang": "インターフェース言語",
        "select_exp_lang": "選択肢の言語を選択",
        "start_test": "テスト開始",
        "submit": "回答送信",
        "score": "あなたのスコアは",
        "question": "問題",
        "choose_answer": "正しい説明を選んでください",
        "restart": "再開する",
        "next": "次へ",
        "start_prompt": "「テスト開始」を押してクイズを始めてください。",
        "correct": "正解です！",
        "incorrect": "不正解です。正しい答えは：",
        "your_answer": "あなたの答え：",
        "Continue": "次へ：",


    },
    "中文": {
        "select_interface": "選擇介面語言",
        "select_word_lang": "選擇要查找的單字語言",
        "select_explain_lang": "選擇單字解釋的語言",
        "input_word": "輸入要查詢的單字",
        "lookup": "查詢單字",
        "dictionary": "字典",
        "quiz": "單字小考",
        "feedback": "回饋",
        "explanation_example": "解釋與例句：",
        "learned_words": "已學習清單",
        "feedback_prompt": "請留下您的回饋或建議：",
        "submit_feedback": "送出回饋",
        "thank_feedback": "感謝您的回饋！",
        "error_api": "API呼叫失敗，請稍後再試。",
        "title": "單字小測驗",
        "select_test": "選擇測驗種類",
        "select_level": "選擇等級",
        "select_lang": "介面語言",
        "select_exp_lang": "選擇選項的語言",
        "start_test": "開始測驗",
        "submit": "送出答案",
        "score": "你的分數是",
        "question": "題目",
        "choose_answer": "請選擇正確解釋",
        "restart": "重新開始",
        "next": "下一題",
        "start_prompt": "請按「開始測驗」開始答題。",
        "correct": "答對了！",
        "incorrect": "答錯了，正確答案是：",
        "your_answer": "你的答案：",
        "Continue": "繼續：",


    }
}
# -------------------------
# 讀取單字CSV檔 (這個檔案需事先準備放同目錄)
# -------------------------


if "interface_lang" not in st.session_state:
    st.title("🌟 Welcome!")
    st.markdown("Please select your preferred interface language:")

    selected_lang = st.radio("🌐 Language", list(LANGUAGES.keys()))

    if st.button("Confirm"):
        st.session_state.interface_lang = selected_lang
        st.rerun()
    st.stop()
else:
    # 讓使用者可以隨時從 sidebar 更改語言
    selected_lang = st.sidebar.selectbox(
        "🌏 Select Interface Language / インターフェース言語 / 選擇介面語言",
        list(LANGUAGES.keys()),
        index=list(LANGUAGES.keys()).index(st.session_state.interface_lang)
    )

    # 如果選擇有變化，更新 session_state 並重新執行
    if selected_lang != st.session_state.interface_lang:
        st.session_state.interface_lang = selected_lang
        st.rerun()

    interface_lang = st.session_state.interface_lang
    text = LANGUAGES[interface_lang]


# -------------------------
# 主選單
# -------------------------
menu = st.sidebar.radio("🔍 Menu / メニュー / 選單", [text["dictionary"], text["quiz"], text["feedback"]])


# -------------------------
# 字典功能
# -------------------------
def dictionary_module():
    st.header(text["dictionary"])

    word_lang = st.selectbox(text["select_word_lang"], ["English", "日本語", "中文"])
    explain_lang = st.selectbox(text["select_explain_lang"], ["English", "日本語", "中文"])

    lookup_word = st.text_input(text["input_word"])

    if "learned_words" not in st.session_state:
        st.session_state.learned_words = []

    if st.button(text["lookup"]):
        if lookup_word.strip() == "":
            st.warning("⚠️ 請輸入單字")
            return

        # 呼叫 OpenAI 產生解釋與例句
        prompt = f"請用{explain_lang}解釋以下{word_lang}單字，並造一個例句:\n單字: {lookup_word}"
        try:
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            result = completion.choices[0].message.content
            st.markdown(f"### {text['explanation_example']}\n{result}")
            if lookup_word not in st.session_state.learned_words:
                st.session_state.learned_words.append(lookup_word)
        except OpenAIError as e:
            st.error(text["error_api"])
            st.error(f"Details: {str(e)}")

    if st.session_state.learned_words:
        st.markdown(f"### {text['learned_words']}")
        for w in st.session_state.learned_words:
            st.write(w)


# -------------------------
# 單字小考功能
# -------------------------


# 假設 words_df 是你已經有的 DataFrame，包含欄位：word, language, meaning, example


# 範例題庫，實際可擴充


# 範例題庫
word_data = {
    "TOEIC": {
        "220": [ # 最基礎單字，生活常見詞
            {"word": "apple", "explanations": {"中文": "蘋果", "English": "apple", "日本語": "りんご"}},
            {"word": "book", "explanations": {"中文": "書", "English": "book", "日本語": "本"}},
            {"word": "car", "explanations": {"中文": "汽車", "English": "car", "日本語": "車"}},
            {"word": "dog", "explanations": {"中文": "狗", "English": "dog", "日本語": "犬"}},
            {"word": "pen", "explanations": {"中文": "筆", "English": "pen", "日本語": "ペン"}},
            {"word": "bag", "explanations": {"中文": "包包", "English": "bag", "日本語": "かばん"}},
            {"word": "cat", "explanations": {"中文": "貓", "English": "cat", "日本語": "猫"}},
            {"word": "milk", "explanations": {"中文": "牛奶", "English": "milk", "日本語": "ミルク"}},
            {"word": "chair", "explanations": {"中文": "椅子", "English": "chair", "日本語": "いす"}},
            {"word": "table", "explanations": {"中文": "桌子", "English": "table", "日本語": "テーブル"}},
            {"word": "phone", "explanations": {"中文": "電話", "English": "phone", "日本語": "電話"}},
            {"word": "hat", "explanations": {"中文": "帽子", "English": "hat", "日本語": "帽子"}},
            {"word": "water", "explanations": {"中文": "水", "English": "water", "日本語": "水"}},
            {"word": "shoes", "explanations": {"中文": "鞋子", "English": "shoes", "日本語": "くつ"}},
            {"word": "door", "explanations": {"中文": "門", "English": "door", "日本語": "ドア"}},

        ],
        "470": [  # 日常生活、工作相關較常見詞彙
        {"word": "window", "explanations": {"中文": "窗戶", "English": "window", "日本語": "窓"}},
        {"word": "computer", "explanations": {"中文": "電腦", "English": "computer", "日本語": "コンピューター"}},
        {"word": "river", "explanations": {"中文": "河流", "English": "river", "日本語": "川"}},
        {"word": "mountain", "explanations": {"中文": "山", "English": "mountain", "日本語": "山"}},
        {"word": "school", "explanations": {"中文": "學校", "English": "school", "日本語": "学校"}},
        {"word": "teacher", "explanations": {"中文": "老師", "English": "teacher", "日本語": "先生"}},
        {"word": "student", "explanations": {"中文": "學生", "English": "student", "日本語": "学生"}},
        {"word": "music", "explanations": {"中文": "音樂", "English": "music", "日本語": "音楽"}},
        {"word": "movie", "explanations": {"中文": "電影", "English": "movie", "日本語": "映画"}},
        {"word": "restaurant", "explanations": {"中文": "餐廳", "English": "restaurant", "日本語": "レストラン"}},
        {"word": "hotel", "explanations": {"中文": "旅館", "English": "hotel", "日本語": "ホテル"}},
        {"word": "airport", "explanations": {"中文": "機場", "English": "airport", "日本語": "空港"}},
        {"word": "train", "explanations": {"中文": "火車", "English": "train", "日本語": "電車"}},
        {"word": "bus", "explanations": {"中文": "公車", "English": "bus", "日本語": "バス"}},
        {"word": "ticket", "explanations": {"中文": "票", "English": "ticket", "日本語": "切符"}},
        ],

        "730": [  # 商務、工作相關詞彙，較抽象
        {"word": "economy", "explanations": {"中文": "經濟", "English": "economy", "日本語": "経済"}},
        {"word": "investment", "explanations": {"中文": "投資", "English": "investment", "日本語": "投資"}},
        {"word": "marketing", "explanations": {"中文": "行銷", "English": "marketing", "日本語": "マーケティング"}},
        {"word": "management", "explanations": {"中文": "管理", "English": "management", "日本語": "マネジメント"}},
        {"word": "strategy", "explanations": {"中文": "策略", "English": "strategy", "日本語": "戦略"}},
        {"word": "analysis", "explanations": {"中文": "分析", "English": "analysis", "日本語": "分析"}},
        {"word": "finance", "explanations": {"中文": "財務", "English": "finance", "日本語": "財務"}},
        {"word": "budget", "explanations": {"中文": "預算", "English": "budget", "日本語": "予算"}},
        {"word": "project", "explanations": {"中文": "專案", "English": "project", "日本語": "プロジェクト"}},
        {"word": "performance", "explanations": {"中文": "表現", "English": "performance", "日本語": "パフォーマンス"}},
        {"word": "report", "explanations": {"中文": "報告", "English": "report", "日本語": "レポート"}},
        {"word": "deadline", "explanations": {"中文": "截止期限", "English": "deadline", "日本語": "締め切り"}},
        {"word": "contract", "explanations": {"中文": "合約", "English": "contract", "日本語": "契約"}},
        {"word": "meeting", "explanations": {"中文": "會議", "English": "meeting", "日本語": "会議"}},
        {"word": "presentation", "explanations": {"中文": "報告演說", "English": "presentation", "日本語": "プレゼンテーション"}},
        ],
        "860": [  # 進階商務與正式文書詞彙
        {"word": "negotiation", "explanations": {"中文": "談判", "English": "negotiation", "日本語": "交渉"}},
        {"word": "agreement", "explanations": {"中文": "協議", "English": "agreement", "日本語": "合意"}},
        {"word": "legislation", "explanations": {"中文": "立法", "English": "legislation", "日本語": "立法"}},
        {"word": "compliance", "explanations": {"中文": "遵從", "English": "compliance", "日本語": "遵守"}},
        {"word": "regulation", "explanations": {"中文": "規定", "English": "regulation", "日本語": "規則"}},
        {"word": "revenue", "explanations": {"中文": "收入", "English": "revenue", "日本語": "収益"}},
        {"word": "expense", "explanations": {"中文": "費用", "English": "expense", "日本語": "費用"}},
        {"word": "audit", "explanations": {"中文": "審計", "English": "audit", "日本語": "監査"}},
        {"word": "liability", "explanations": {"中文": "負債", "English": "liability", "日本語": "負債"}},
        {"word": "equity", "explanations": {"中文": "股本", "English": "equity", "日本語": "株式資本"}},
        {"word": "dividend", "explanations": {"中文": "股利", "English": "dividend", "日本語": "配当"}},
        {"word": "merger", "explanations": {"中文": "合併", "English": "merger", "日本語": "合併"}},
        {"word": "acquisition", "explanations": {"中文": "收購", "English": "acquisition", "日本語": "買収"}},
        {"word": "subsidiary", "explanations": {"中文": "子公司", "English": "subsidiary", "日本語": "子会社"}},
        {"word": "shareholder", "explanations": {"中文": "股東", "English": "shareholder", "日本語": "株主"}},
        ],
        "990": [  # 頂尖高級詞彙，適合最高分段考試與精準表達
        {"word": "sustainable", "explanations": {"中文": "可持續的", "English": "sustainable", "日本語": "持続可能な"}},
        {"word": "entrepreneur", "explanations": {"中文": "企業家", "English": "entrepreneur", "日本語": "起業家"}},
        {"word": "philanthropy", "explanations": {"中文": "慈善", "English": "philanthropy", "日本語": "慈善活動"}},
        {"word": "disruption", "explanations": {"中文": "中斷，顛覆", "English": "disruption", "日本語": "混乱"}},
        {"word": "innovation", "explanations": {"中文": "創新", "English": "innovation", "日本語": "革新"}},
        {"word": "synergy", "explanations": {"中文": "協同效應", "English": "synergy", "日本語": "相乗効果"}},
        {"word": "benchmark", "explanations": {"中文": "基準", "English": "benchmark", "日本語": "ベンチマーク"}},
        {"word": "comprehensive", "explanations": {"中文": "全面的", "English": "comprehensive", "日本語": "包括的な"}},
        {"word": "confidentiality", "explanations": {"中文": "機密性", "English": "confidentiality", "日本語": "機密性"}},
        {"word": "intellectual", "explanations": {"中文": "知識的", "English": "intellectual", "日本語": "知的な"}},
        {"word": "jurisdiction", "explanations": {"中文": "司法管轄權", "English": "jurisdiction", "日本語": "管轄権"}},
        {"word": "liability", "explanations": {"中文": "法律責任", "English": "liability", "日本語": "責任"}},
        {"word": "proprietary", "explanations": {"中文": "專有的", "English": "proprietary", "日本語": "専有の"}},
        {"word": "restructuring", "explanations": {"中文": "重組", "English": "restructuring", "日本語": "再構築"}},
        {"word": "volatility", "explanations": {"中文": "波動性", "English": "volatility", "日本語": "変動性"}},
        ],
    },

    "JLPT": {
    "N5": [
        {"word": "猫", "explanations": {"中文": "貓", "English": "cat", "日本語": "ねこ"}},
        {"word": "犬", "explanations": {"中文": "狗", "English": "dog", "日本語": "いぬ"}},
        {"word": "水", "explanations": {"中文": "水", "English": "water", "日本語": "みず"}},
        {"word": "学校", "explanations": {"中文": "學校", "English": "school", "日本語": "がっこう"}},
        {"word": "先生", "explanations": {"中文": "老師", "English": "teacher", "日本語": "せんせい"}},
        {"word": "本", "explanations": {"中文": "書", "English": "book", "日本語": "ほん"}},
        {"word": "車", "explanations": {"中文": "車子", "English": "car", "日本語": "くるま"}},
        {"word": "友達", "explanations": {"中文": "朋友", "English": "friend", "日本語": "ともだち"}},
        {"word": "食べる", "explanations": {"中文": "吃", "English": "eat", "日本語": "たべる"}},
        {"word": "飲む", "explanations": {"中文": "喝", "English": "drink", "日本語": "のむ"}},
        {"word": "見る", "explanations": {"中文": "看", "English": "see", "日本語": "みる"}},
        {"word": "行く", "explanations": {"中文": "去", "English": "go", "日本語": "いく"}},
        {"word": "来る", "explanations": {"中文": "來", "English": "come", "日本語": "くる"}},
        {"word": "家", "explanations": {"中文": "家", "English": "house", "日本語": "いえ"}},
        {"word": "時々", "explanations": {"中文": "有時候", "English": "sometimes", "日本語": "ときどき"}}
    ],
    "N4": [
        {"word": "運動", "explanations": {"中文": "運動", "English": "exercise", "日本語": "うんどう"}},
        {"word": "勉強", "explanations": {"中文": "學習", "English": "study", "日本語": "べんきょう"}},
        {"word": "旅行", "explanations": {"中文": "旅行", "English": "travel", "日本語": "りょこう"}},
        {"word": "天気", "explanations": {"中文": "天氣", "English": "weather", "日本語": "てんき"}},
        {"word": "仕事", "explanations": {"中文": "工作", "English": "work", "日本語": "しごと"}},
        {"word": "病院", "explanations": {"中文": "醫院", "English": "hospital", "日本語": "びょういん"}},
        {"word": "休み", "explanations": {"中文": "休息、假日", "English": "holiday/rest", "日本語": "やすみ"}},
        {"word": "教室", "explanations": {"中文": "教室", "English": "classroom", "日本語": "きょうしつ"}},
        {"word": "新聞", "explanations": {"中文": "報紙", "English": "newspaper", "日本語": "しんぶん"}},
        {"word": "試験", "explanations": {"中文": "考試", "English": "exam", "日本語": "しけん"}},
        {"word": "図書館", "explanations": {"中文": "圖書館", "English": "library", "日本語": "としょかん"}},
        {"word": "飲み物", "explanations": {"中文": "飲料", "English": "drink/beverage", "日本語": "のみもの"}},
        {"word": "勉強する", "explanations": {"中文": "學習（動詞）", "English": "to study", "日本語": "べんきょうする"}},
        {"word": "旅行する", "explanations": {"中文": "旅行（動詞）", "English": "to travel", "日本語": "りょこうする"}},
        {"word": "忘れる", "explanations": {"中文": "忘記", "English": "to forget", "日本語": "わすれる"}}
    ],
    "N3": [
        {"word": "感情", "explanations": {"中文": "感情", "English": "emotion", "日本語": "かんじょう"}},
        {"word": "経験", "explanations": {"中文": "經驗", "English": "experience", "日本語": "けいけん"}},
        {"word": "意見", "explanations": {"中文": "意見", "English": "opinion", "日本語": "いけん"}},
        {"word": "解決", "explanations": {"中文": "解決", "English": "solution", "日本語": "かいけつ"}},
        {"word": "努力", "explanations": {"中文": "努力", "English": "effort", "日本語": "どりょく"}},
        {"word": "経済", "explanations": {"中文": "經濟", "English": "economy", "日本語": "けいざい"}},
        {"word": "報告", "explanations": {"中文": "報告", "English": "report", "日本語": "ほうこく"}},
        {"word": "社会", "explanations": {"中文": "社會", "English": "society", "日本語": "しゃかい"}},
        {"word": "意味", "explanations": {"中文": "意思", "English": "meaning", "日本語": "いみ"}},
        {"word": "注意", "explanations": {"中文": "注意", "English": "attention", "日本語": "ちゅうい"}},
        {"word": "結果", "explanations": {"中文": "結果", "English": "result", "日本語": "けっか"}},
        {"word": "条件", "explanations": {"中文": "條件", "English": "condition", "日本語": "じょうけん"}},
        {"word": "成功", "explanations": {"中文": "成功", "English": "success", "日本語": "せいこう"}},
        {"word": "情報", "explanations": {"中文": "資訊", "English": "information", "日本語": "じょうほう"}},
        {"word": "理解", "explanations": {"中文": "理解", "English": "understanding", "日本語": "りかい"}}
    ],
    "N2": [
        {"word": "挑戦", "explanations": {"中文": "挑戰", "English": "challenge", "日本語": "ちょうせん"}},
        {"word": "成果", "explanations": {"中文": "成果", "English": "achievement", "日本語": "せいか"}},
        {"word": "発展", "explanations": {"中文": "發展", "English": "development", "日本語": "はってん"}},
        {"word": "証明", "explanations": {"中文": "證明", "English": "proof", "日本語": "しょうめい"}},
        {"word": "協力", "explanations": {"中文": "合作", "English": "cooperation", "日本語": "きょうりょく"}},
        {"word": "尊敬", "explanations": {"中文": "尊敬", "English": "respect", "日本語": "そんけい"}},
        {"word": "期待", "explanations": {"中文": "期待", "English": "expectation", "日本語": "きたい"}},
        {"word": "反対", "explanations": {"中文": "反對", "English": "opposition", "日本語": "はんたい"}},
        {"word": "報告書", "explanations": {"中文": "報告書", "English": "report document", "日本語": "ほうこくしょ"}},
        {"word": "責任", "explanations": {"中文": "責任", "English": "responsibility", "日本語": "せきにん"}},
        {"word": "提案", "explanations": {"中文": "提案", "English": "proposal", "日本語": "ていあん"}},
        {"word": "結果", "explanations": {"中文": "結果", "English": "result", "日本語": "けっか"}},
        {"word": "理解", "explanations": {"中文": "理解", "English": "understanding", "日本語": "りかい"}},
        {"word": "成長", "explanations": {"中文": "成長", "English": "growth", "日本語": "せいちょう"}},
        {"word": "影響", "explanations": {"中文": "影響", "English": "influence", "日本語": "えいきょう"}}
    ],
    "N1": [
        {"word": "曖昧", "explanations": {"中文": "模糊", "English": "ambiguous", "日本語": "あいまい"}},
        {"word": "依存", "explanations": {"中文": "依賴", "English": "dependence", "日本語": "いぞん"}},
        {"word": "崩壊", "explanations": {"中文": "崩潰", "English": "collapse", "日本語": "ほうかい"}},
        {"word": "矛盾", "explanations": {"中文": "矛盾", "English": "contradiction", "日本語": "むじゅん"}},
        {"word": "妥協", "explanations": {"中文": "妥協", "English": "compromise", "日本語": "だきょう"}},
        {"word": "希薄", "explanations": {"中文": "稀薄", "English": "thin, weak", "日本語": "きはく"}},
        {"word": "冗談", "explanations": {"中文": "玩笑", "English": "joke", "日本語": "じょうだん"}},
        {"word": "洞察", "explanations": {"中文": "洞察", "English": "insight", "日本語": "どうさつ"}},
        {"word": "諮問", "explanations": {"中文": "諮詢", "English": "consultation", "日本語": "しもん"}},
        {"word": "圧迫", "explanations": {"中文": "壓迫", "English": "pressure", "日本語": "あっぱく"}},
        {"word": "促進", "explanations": {"中文": "促進", "English": "promotion", "日本語": "そくしん"}},
        {"word": "洗練", "explanations": {"中文": "洗練", "English": "refinement", "日本語": "せんれん"}},
        {"word": "持続", "explanations": {"中文": "持續", "English": "continuation", "日本語": "じぞく"}},
        {"word": "排除", "explanations": {"中文": "排除", "English": "elimination", "日本語": "はいじょ"}},
        {"word": "調和", "explanations": {"中文": "調和", "English": "harmony", "日本語": "ちょうわ"}}
    ]
  },

    "TOCFL": {
    "A1": [
        {"word": "你好", "explanations": {"中文": "你好", "English": "hello", "日本語": "こんにちは"}},
        {"word": "謝謝", "explanations": {"中文": "謝謝", "English": "thank you", "日本語": "ありがとう"}},
        {"word": "是", "explanations": {"中文": "是", "English": "yes", "日本語": "はい"}},
        {"word": "不是", "explanations": {"中文": "不是", "English": "no", "日本語": "いいえ"}},
        {"word": "我", "explanations": {"中文": "我", "English": "I/me", "日本語": "私"}},
        {"word": "你", "explanations": {"中文": "你", "English": "you", "日本語": "あなた"}},
        {"word": "他", "explanations": {"中文": "他", "English": "he/him", "日本語": "彼"}},
        {"word": "吃", "explanations": {"中文": "吃", "English": "eat", "日本語": "食べる"}},
        {"word": "喝", "explanations": {"中文": "喝", "English": "drink", "日本語": "飲む"}},
        {"word": "家", "explanations": {"中文": "家", "English": "home", "日本語": "家"}},
        {"word": "學校", "explanations": {"中文": "學校", "English": "school", "日本語": "学校"}},
        {"word": "水", "explanations": {"中文": "水", "English": "water", "日本語": "水"}},
        {"word": "書", "explanations": {"中文": "書", "English": "book", "日本語": "本"}},
        {"word": "朋友", "explanations": {"中文": "朋友", "English": "friend", "日本語": "友達"}},
        {"word": "快樂", "explanations": {"中文": "快樂", "English": "happy", "日本語": "嬉しい"}}
    ],
    "A2": [
        {"word": "早上", "explanations": {"中文": "早上", "English": "morning", "日本語": "朝"}},
        {"word": "晚上", "explanations": {"中文": "晚上", "English": "evening", "日本語": "晩"}},
        {"word": "工作", "explanations": {"中文": "工作", "English": "work", "日本語": "仕事"}},
        {"word": "學習", "explanations": {"中文": "學習", "English": "study", "日本語": "勉強"}},
        {"word": "老師", "explanations": {"中文": "老師", "English": "teacher", "日本語": "先生"}},
        {"word": "學生", "explanations": {"中文": "學生", "English": "student", "日本語": "学生"}},
        {"word": "天氣", "explanations": {"中文": "天氣", "English": "weather", "日本語": "天気"}},
        {"word": "買", "explanations": {"中文": "買", "English": "buy", "日本語": "買う"}},
        {"word": "賣", "explanations": {"中文": "賣", "English": "sell", "日本語": "売る"}},
        {"word": "朋友", "explanations": {"中文": "朋友", "English": "friend", "日本語": "友達"}},
        {"word": "家人", "explanations": {"中文": "家人", "English": "family", "日本語": "家族"}},
        {"word": "衣服", "explanations": {"中文": "衣服", "English": "clothes", "日本語": "服"}},
        {"word": "電影", "explanations": {"中文": "電影", "English": "movie", "日本語": "映画"}},
        {"word": "音樂", "explanations": {"中文": "音樂", "English": "music", "日本語": "音楽"}},
        {"word": "公園", "explanations": {"中文": "公園", "English": "park", "日本語": "公園"}}
    ],
    "B1": [
        {"word": "經濟", "explanations": {"中文": "經濟", "English": "economy", "日本語": "経済"}},
        {"word": "文化", "explanations": {"中文": "文化", "English": "culture", "日本語": "文化"}},
        {"word": "政治", "explanations": {"中文": "政治", "English": "politics", "日本語": "政治"}},
        {"word": "環境", "explanations": {"中文": "環境", "English": "environment", "日本語": "環境"}},
        {"word": "社會", "explanations": {"中文": "社會", "English": "society", "日本語": "社会"}},
        {"word": "科技", "explanations": {"中文": "科技", "English": "technology", "日本語": "技術"}},
        {"word": "教育", "explanations": {"中文": "教育", "English": "education", "日本語": "教育"}},
        {"word": "法律", "explanations": {"中文": "法律", "English": "law", "日本語": "法律"}},
        {"word": "健康", "explanations": {"中文": "健康", "English": "health", "日本語": "健康"}},
        {"word": "新聞", "explanations": {"中文": "新聞", "English": "news", "日本語": "ニュース"}},
        {"word": "經驗", "explanations": {"中文": "經驗", "English": "experience", "日本語": "経験"}},
        {"word": "藝術", "explanations": {"中文": "藝術", "English": "art", "日本語": "芸術"}},
        {"word": "旅遊", "explanations": {"中文": "旅遊", "English": "travel", "日本語": "旅行"}},
        {"word": "心理", "explanations": {"中文": "心理", "English": "psychology", "日本語": "心理学"}},
        {"word": "經營", "explanations": {"中文": "經營", "English": "management", "日本語": "経営"}}
    ],
    "B2": [
        {"word": "國際", "explanations": {"中文": "國際", "English": "international", "日本語": "国際"}},
        {"word": "責任", "explanations": {"中文": "責任", "English": "responsibility", "日本語": "責任"}},
        {"word": "創新", "explanations": {"中文": "創新", "English": "innovation", "日本語": "革新"}},
        {"word": "策略", "explanations": {"中文": "策略", "English": "strategy", "日本語": "戦略"}},
        {"word": "經濟學", "explanations": {"中文": "經濟學", "English": "economics", "日本語": "経済学"}},
        {"word": "投資", "explanations": {"中文": "投資", "English": "investment", "日本語": "投資"}},
        {"word": "管理", "explanations": {"中文": "管理", "English": "management", "日本語": "管理"}},
        {"word": "技術", "explanations": {"中文": "技術", "English": "technology", "日本語": "技術"}},
        {"word": "法律", "explanations": {"中文": "法律", "English": "law", "日本語": "法律"}},
        {"word": "市場", "explanations": {"中文": "市場", "English": "market", "日本語": "市場"}},
        {"word": "發展", "explanations": {"中文": "發展", "English": "development", "日本語": "発展"}},
        {"word": "經驗", "explanations": {"中文": "經驗", "English": "experience", "日本語": "経験"}},
        {"word": "創業", "explanations": {"中文": "創業", "English": "startup", "日本語": "起業"}},
        {"word": "交流", "explanations": {"中文": "交流", "English": "exchange", "日本語": "交流"}},
        {"word": "全球化", "explanations": {"中文": "全球化", "English": "globalization", "日本語": "グローバル化"}}
    ],
    "C1": [
        {"word": "哲學", "explanations": {"中文": "哲學", "English": "philosophy", "日本語": "哲学"}},
        {"word": "社會學", "explanations": {"中文": "社會學", "English": "sociology", "日本語": "社会学"}},
        {"word": "心理學", "explanations": {"中文": "心理學", "English": "psychology", "日本語": "心理学"}},
        {"word": "政治學", "explanations": {"中文": "政治學", "English": "political science", "日本語": "政治学"}},
        {"word": "文學", "explanations": {"中文": "文學", "English": "literature", "日本語": "文学"}},
        {"word": "經濟政策", "explanations": {"中文": "經濟政策", "English": "economic policy", "日本語": "経済政策"}},
        {"word": "國際關係", "explanations": {"中文": "國際關係", "English": "international relations", "日本語": "国際関係"}},
        {"word": "文化研究", "explanations": {"中文": "文化研究", "English": "cultural studies", "日本語": "文化研究"}},
        {"word": "法學", "explanations": {"中文": "法學", "English": "law studies", "日本語": "法学"}},
        {"word": "環境保護", "explanations": {"中文": "環境保護", "English": "environmental protection", "日本語": "環境保護"}},
        {"word": "技術創新", "explanations": {"中文": "技術創新", "English": "technological innovation", "日本語": "技術革新"}},
        {"word": "經濟發展", "explanations": {"中文": "經濟發展", "English": "economic development", "日本語": "経済発展"}},
        {"word": "社會變遷", "explanations": {"中文": "社會變遷", "English": "social change", "日本語": "社会変遷"}},
        {"word": "政治制度", "explanations": {"中文": "政治制度", "English": "political system", "日本語": "政治制度"}},
        {"word": "文化多樣性", "explanations": {"中文": "文化多樣性", "English": "cultural diversity", "日本語": "文化多様性"}}
    ],
    "C2": [
        {"word": "跨文化溝通", "explanations": {"中文": "跨文化溝通", "English": "cross-cultural communication", "日本語": "異文化コミュニケーション"}},
        {"word": "全球經濟", "explanations": {"中文": "全球經濟", "English": "global economy", "日本語": "グローバル経済"}},
        {"word": "環境永續", "explanations": {"中文": "環境永續", "English": "environmental sustainability", "日本語": "環境持続可能性"}},
        {"word": "社會正義", "explanations": {"中文": "社會正義", "English": "social justice", "日本語": "社会正義"}},
        {"word": "經濟全球化", "explanations": {"中文": "經濟全球化", "English": "economic globalization", "日本語": "経済のグローバル化"}},
        {"word": "政治哲學", "explanations": {"中文": "政治哲學", "English": "political philosophy", "日本語": "政治哲学"}},
        {"word": "文化身份", "explanations": {"中文": "文化身份", "English": "cultural identity", "日本語": "文化的アイデンティティ"}},
        {"word": "科技倫理", "explanations": {"中文": "科技倫理", "English": "technology ethics", "日本語": "技術倫理"}},
        {"word": "社會動力學", "explanations": {"中文": "社會動力學", "English": "social dynamics", "日本語": "社会力学"}},
        {"word": "國際合作", "explanations": {"中文": "國際合作", "English": "international cooperation", "日本語": "国際協力"}},
        {"word": "政治經濟學", "explanations": {"中文": "政治經濟學", "English": "political economy", "日本語": "政治経済学"}},
        {"word": "文化衝突", "explanations": {"中文": "文化衝突", "English": "cultural conflict", "日本語": "文化衝突"}},
        {"word": "經濟危機", "explanations": {"中文": "經濟危機", "English": "economic crisis", "日本語": "経済危機"}},
        {"word": "法律制度", "explanations": {"中文": "法律制度", "English": "legal system", "日本語": "法制度"}},
        {"word": "全球治理", "explanations": {"中文": "全球治理", "English": "global governance", "日本語": "グローバルガバナンス"}}
    ]
 },
}





def quiz_module():
    if "quiz_index" not in st.session_state:
        st.session_state.quiz_index = 0
        st.session_state.score = 0
        st.session_state.quiz_words = []
        st.session_state.selected_answer = None
        st.session_state.answered = False
        st.session_state.choices = []

    test_type = st.selectbox(text["select_test"], ["TOEIC", "JLPT", "TOCFL"])
    level_options = list(word_data[test_type].keys())
    level = st.selectbox(text["select_level"], level_options)
    explanation_lang = st.selectbox(text["select_exp_lang"], ["中文", "English", "日本語"])

    if st.button(text["start_test"]):
        pool = word_data[test_type][level]
        if len(pool) < 5:
            st.warning(text.get("error_pool_short", "題庫不足，請選擇其他等級或測驗種類。"))
            return
        st.session_state.quiz_words = random.sample(pool, 5)
        st.session_state.quiz_index = 0
        st.session_state.score = 0
        st.session_state.selected_answer = None
        st.session_state.answered = False
        st.session_state.choices = []

    if st.session_state.quiz_words and st.session_state.quiz_index < len(st.session_state.quiz_words):
        index = st.session_state.quiz_index
        q = st.session_state.quiz_words[index]
        correct = q["explanations"][explanation_lang]

        st.write(f"{text['question']} {index + 1}： **{q['word']}**")

        if len(st.session_state.choices) <= index:
            pool = word_data[test_type][level]
            wrong_options = [w["explanations"][explanation_lang] for w in pool if w["word"] != q["word"]]
            wrong_choices = random.sample(wrong_options, min(3, len(wrong_options)))
            choices = wrong_choices + [correct]
            random.shuffle(choices)
            st.session_state.choices.append(choices)

        choices = st.session_state.choices[index]
        select_key = f"select_{index}_{q['word']}"

        # 選項框禁用，已答題就不能改
        selected = st.selectbox(text["choose_answer"], choices, key=select_key, disabled=st.session_state.answered)

        # 按鈕顯示邏輯：用 container 包裹，避免衝突
        btn_container = st.container()

        btn_label = "Continue"

        if st.button(btn_label):
            if not st.session_state.answered:
                # 第一次按，當作提交，判斷答對錯
                st.session_state.selected_answer = selected
                st.session_state.answered = True

                if selected == correct:
                    st.success(text.get("correct", "答對了！"))
                    st.session_state.score += 1
                else:
                    st.error(f"{text.get('incorrect', '答錯了，正確答案是：')}{correct}")
                st.write(f"{text.get('your_answer', '你的答案：')}{selected}")

            else:
                # 第二次按，進入下一題
                st.session_state.quiz_index += 1
                st.session_state.selected_answer = None
                st.session_state.answered = False
                st.rerun()  # 重新載入，顯示下一題


    elif st.session_state.quiz_words and st.session_state.quiz_index >= len(st.session_state.quiz_words):

        st.success(f"{text['score']}：{st.session_state.score} / {len(st.session_state.quiz_words)}")

        st.write(text["start_prompt"])


    else:

        st.write(text["start_prompt"])



# -------------------------
# 反饋功能
# -------------------------
import streamlit as st
import sqlite3

# -------------------------
# 初始化資料庫，建立回饋表
# -------------------------
def init_db():
    conn = sqlite3.connect("feedback.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS feedbacks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# -------------------------
# 將回饋寫入資料庫
# -------------------------
def save_feedback_to_db(feedback_text):
    conn = sqlite3.connect("feedback.db")
    c = conn.cursor()
    c.execute("INSERT INTO feedbacks (content) VALUES (?)", (feedback_text,))
    conn.commit()
    conn.close()

# -------------------------
# 回饋功能模組
# -------------------------
def feedback_module():
    st.header(text["feedback"])

    if "feedback_submitted" not in st.session_state:
        st.session_state.feedback_submitted = False

    feedback_input = st.text_area(text["feedback_prompt"])

    if st.button(text["submit_feedback"]):
        if feedback_input.strip() == "":
            st.warning("⚠️ 請輸入內容")
        else:
            save_feedback_to_db(feedback_input)
            st.session_state.feedback_submitted = True

    if st.session_state.feedback_submitted:
        st.success(text["thank_feedback"])

# -------------------------
# 主程式入口
# -------------------------
if __name__ == "__main__":
    init_db()  # 啟動時建立資料表

    # 假設你有個選單 menu，這裡示範如何呼叫
    menu = st.sidebar.selectbox("選單", [text["dictionary"], text["quiz"], text["feedback"]])

    if menu == text["dictionary"]:
        dictionary_module()
    elif menu == text["quiz"]:
        quiz_module()
    elif menu == text["feedback"]:
        feedback_module()
