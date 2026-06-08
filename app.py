from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

import streamlit as st


# =========================
# 基本設定
# =========================

APP_DIR = Path(__file__).resolve().parent
DATA_DIR = APP_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
CSV_PATH = DATA_DIR / "responses.csv"

SHOW_SPECIFIC_NAMES = True

VERSION_LABEL = "具体名あり版" if SHOW_SPECIFIC_NAMES else "具体名なし版"

YES_NO = ["はい", "いいえ"]

FIRST_USE_OPTIONS = [
    "1週間以内",
    "1週間超〜1か月以内",
    "1か月超〜3か月以内",
    "3か月超〜1年以内",
    "1年より前",
]

FREQUENCY_OPTIONS = [
    "ほぼ毎日",
    "週に2〜3回",
    "週に1回程度",
    "月に数回",
    "1回だけ",
]

PURPOSE_ITEMS: List[Tuple[str, str]] = [
    ("purpose_search", "調べもの・わからないことを聞く"),
    ("purpose_life_advice", "生活の相談をする（予定・手続きなど）"),
    ("purpose_health_medical_info", "健康・医療に関する情報を調べる"),
    ("purpose_shopping_travel", "買い物、旅行・外出の相談をする"),
    ("purpose_writing", "文章の作成・修正をする（メール等）"),
    ("purpose_summary_translation", "要約・翻訳をする"),
    ("purpose_hobby", "趣味・娯楽に使う（料理、園芸等）"),
    ("purpose_image_creation", "画像やイラストを作成する"),
]

REASON_ITEMS: List[Tuple[str, str]] = [
    ("reason_no_need", "必要性を感じない"),
    ("reason_dont_know_use", "何に使えるか分からない"),
    ("reason_dont_know_how", "使い方が分からない"),
    ("reason_no_device_or_internet", "スマートフォン・パソコン・インターネット環境が十分でない"),
    ("reason_cost_anxiety", "料金がかかるのが不安"),
    ("reason_privacy_anxiety", "個人情報やプライバシーが不安"),
    ("reason_wrong_info_anxiety", "間違った情報が出るのが不安"),
    ("reason_fraud_abuse_anxiety", "詐欺や悪用が不安"),
    ("reason_no_people_around", "家族や周囲に使っている人がいない"),
    ("reason_prefer_asking_people", "人に聞く方がよい"),
    ("reason_input_operation_difficult", "文字入力や画面操作が難しい"),
    ("reason_no_particular_reason", "特に理由はない"),
]


# =========================
# 画面設定
# =========================

st.set_page_config(
    page_title="生成AI追加質問票",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
    /* レイアウト全体 */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    /* サイドバーを非表示 */
    [data-testid="collapsedControl"] { display: none; }

    /* フォームタイトル行 */
    .form-title-row {
        border: 2px solid #334155;
        border-bottom: none;
        background: #F8FAFC;
        padding: 10px 16px;
        font-size: 26px;
        font-weight: 800;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    /* バージョンラベル（非表示） */
    .version-label {
        display: none;
    }

    /* フォーム本体 */
    .form-body {
        border: 2px solid #334155;
        border-top: none;
        padding: 18px 28px 28px 28px;
        background: white;
    }

    /* 説明文ボックス */
    .explanation-box {
        background: #E8F7FB;
        border: 1.5px solid #7DD3FC;
        padding: 16px 20px;
        font-size: 20px;
        line-height: 1.65;
        margin-bottom: 22px;
        border-radius: 4px;
    }

    /* 質問文 */
    .question-text {
        font-size: 21px;
        line-height: 1.7;
        font-weight: 600;
        margin-top: 18px;
        margin-bottom: 10px;
    }

    /* 分岐注記（緑） */
    .branch-note {
        color: #15803D;
        font-size: 20px;
        font-weight: 800;
        margin: 18px 0 12px 0;
        padding: 6px 0;
        border-top: 1px solid #BBF7D0;
    }

    /* 赤い注記 */
    .red-note {
        color: #DC2626;
        font-size: 17px;
        font-weight: 600;
        margin-top: 6px;
        margin-bottom: 14px;
    }

    /* 項目テキスト（はい/いいえ行） */
    .item-text {
        font-size: 19px;
        line-height: 1.55;
        padding-top: 6px;
        padding-bottom: 6px;
    }

    /* 区切り線 */
    .divider {
        border: none;
        border-top: 1.5px solid #CBD5E1;
        margin: 18px 0;
    }

    /* 通常ボタン（水色） */
    div.stButton > button {
        min-height: 46px;
        font-size: 17px;
        border-radius: 4px;
        background-color: #BFEAF5;
        border: 1.5px solid #67C5DF;
        color: #1F2937;
        font-weight: 600;
        transition: background-color 0.15s;
    }

    div.stButton > button:hover {
        background-color: #93D9EF;
        border-color: #38B2CC;
    }

    /* 選択済みボタン（緑・primary） */
    div.stButton > button[kind="primary"] {
        background-color: #15803D !important;
        border: 1.5px solid #15803D !important;
        color: white !important;
    }

    div.stButton > button[kind="primary"]:hover {
        background-color: #166534 !important;
    }

    /* 保存エリア */
    .save-area {
        background: #F8FAFC;
        border: 1.5px solid #CBD5E1;
        padding: 18px 22px;
        margin-top: 24px;
        border-radius: 6px;
    }

    /* はい/いいえ 行のゼブラ縞 */
    .item-row-odd  { background: #F8FAFC; }
    .item-row-even { background: #FFFFFF; }
</style>
""",
    unsafe_allow_html=True,
)


# =========================
# 状態管理
# =========================

def init_state() -> None:
    defaults = {
        "q1_experience": None,
        "q2_first_use_timing": None,
        "q3_use_frequency": None,
        "submitted": False,
        "last_saved_json": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    for code, _ in PURPOSE_ITEMS:
        if code not in st.session_state:
            st.session_state[code] = None

    for code, _ in REASON_ITEMS:
        if code not in st.session_state:
            st.session_state[code] = None


def reset_all() -> None:
    keys_to_clear = [
        "q1_experience",
        "q2_first_use_timing",
        "q3_use_frequency",
        "submitted",
        "last_saved_json",
    ]

    keys_to_clear += [code for code, _ in PURPOSE_ITEMS]
    keys_to_clear += [code for code, _ in REASON_ITEMS]

    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]

    st.rerun()


init_state()


# =========================
# UI部品
# =========================

def choice_buttons(
    key: str,
    options: List[str],
    columns_per_row: int | None = None,
) -> None:
    """単一選択ボタン。選択済みは緑で強調する。"""
    if columns_per_row is None:
        columns_per_row = len(options)

    rows = [
        options[i : i + columns_per_row]
        for i in range(0, len(options), columns_per_row)
    ]

    for row_index, row_options in enumerate(rows):
        cols = st.columns(len(row_options))
        for col_index, option in enumerate(row_options):
            selected = st.session_state.get(key) == option
            button_label = f"✓ {option}" if selected else option
            button_type = "primary" if selected else "secondary"

            with cols[col_index]:
                if st.button(
                    button_label,
                    key=f"btn_{key}_{row_index}_{col_index}",
                    use_container_width=True,
                    type=button_type,
                ):
                    st.session_state[key] = option
                    st.rerun()


def yes_no_row(key: str, text: str, number: int | None = None, stripe: bool = False) -> None:
    """1項目ごとの「はい／いいえ」選択行。"""
    row_class = "item-row-odd" if stripe else "item-row-even"
    prefix = f"{number}. " if number is not None else "・"

    cols = st.columns([5.5, 1.35, 1.35])

    with cols[0]:
        st.markdown(
            f"<div class='item-text {row_class}'>{prefix}{text}</div>",
            unsafe_allow_html=True,
        )

    for idx, answer in enumerate(YES_NO):
        selected = st.session_state.get(key) == answer
        button_label = f"✓ {answer}" if selected else answer
        button_type = "primary" if selected else "secondary"

        with cols[idx + 1]:
            if st.button(
                button_label,
                key=f"btn_{key}_{answer}",
                use_container_width=True,
                type=button_type,
            ):
                st.session_state[key] = answer
                st.rerun()


def divider() -> None:
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)


# =========================
# データ保存
# =========================

def get_missing_fields() -> List[str]:
    missing: List[str] = []

    q1 = st.session_state.get("q1_experience")

    if q1 not in YES_NO:
        missing.append("Q1：生成AIの利用経験")
        return missing

    if q1 == "はい":
        if not st.session_state.get("q2_first_use_timing"):
            missing.append("Q2：はじめて使った時期")

        if not st.session_state.get("q3_use_frequency"):
            missing.append("Q3：利用頻度")

        for idx, (code, label) in enumerate(PURPOSE_ITEMS, start=1):
            if st.session_state.get(code) not in YES_NO:
                missing.append(f"Q4-{idx}：{label}")

    elif q1 == "いいえ":
        for idx, (code, label) in enumerate(REASON_ITEMS, start=1):
            if st.session_state.get(code) not in YES_NO:
                missing.append(f"Q2-{idx}：{label}")

    return missing


def build_response_row() -> Dict[str, str]:
    q1 = st.session_state.get("q1_experience")

    row: Dict[str, str] = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "questionnaire_version": VERSION_LABEL,
        "q1_experience": q1 or "",
        "q2_first_use_timing": "",
        "q3_use_frequency": "",
    }

    for code, _ in PURPOSE_ITEMS:
        row[code] = ""

    for code, _ in REASON_ITEMS:
        row[code] = ""

    if q1 == "はい":
        row["q2_first_use_timing"] = st.session_state.get("q2_first_use_timing") or ""
        row["q3_use_frequency"] = st.session_state.get("q3_use_frequency") or ""

        for code, _ in PURPOSE_ITEMS:
            row[code] = st.session_state.get(code) or ""

    elif q1 == "いいえ":
        for code, _ in REASON_ITEMS:
            row[code] = st.session_state.get(code) or ""

    return row


def save_response(row: Dict[str, str]) -> None:
    file_exists = CSV_PATH.exists() and CSV_PATH.stat().st_size > 0

    with CSV_PATH.open("a", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(row.keys()))

        if not file_exists:
            writer.writeheader()

        writer.writerow(row)


# =========================
# メインレイアウト
# =========================

# フォームタイトル
st.markdown(
    f"""
<div class="form-title-row">
    <div>生成AIの利用について</div>
    <div class="version-label">{VERSION_LABEL}</div>
</div>
""",
    unsafe_allow_html=True,
)

# フォーム本体開始
st.markdown("<div class='form-body'>", unsafe_allow_html=True)

# ──────────────────────────────
# 説明文
# ──────────────────────────────
if SHOW_SPECIFIC_NAMES:
    explanation = (
        "生成AIとは、ChatGPT、Geminiなどのように、話しかけたり文字を入力したりすると、"
        "文章・画像・要約・アイデアなどを作って返すサービスで、"
        "スマートフォン、タブレットなどで使うものです。"
    )
else:
    explanation = (
        "生成AIとは、話しかけたり文字を入力したりすると、"
        "文章・画像・要約・アイデアなどを作って返すAIサービスで、"
        "スマートフォン、タブレットなどで使うものです。"
    )

st.markdown(
    f"<div class='explanation-box'>{explanation}</div>",
    unsafe_allow_html=True,
)

# ──────────────────────────────
# Q1
# ──────────────────────────────
st.markdown(
    "<div class='question-text'>1. これまでに1回でも、生成AIを使ったことがありますか。</div>",
    unsafe_allow_html=True,
)
choice_buttons("q1_experience", YES_NO, columns_per_row=2)

q1 = st.session_state.get("q1_experience")

# ──────────────────────────────
# Q1「はい」分岐
# ──────────────────────────────
if q1 == "はい":
    divider()

    st.markdown(
        "<div class='branch-note'>【1で「はい」と答えた方におたずねします】</div>",
        unsafe_allow_html=True,
    )

    # Q2
    st.markdown(
        "<div class='question-text'>2. はじめて使ったのは、いつごろですか。</div>",
        unsafe_allow_html=True,
    )
    choice_buttons("q2_first_use_timing", FIRST_USE_OPTIONS, columns_per_row=5)

    # Q3
    st.markdown(
        "<div class='question-text'>3. はじめて使った時から、どのくらいの頻度でこれまで使いましたか。</div>",
        unsafe_allow_html=True,
    )
    choice_buttons("q3_use_frequency", FREQUENCY_OPTIONS, columns_per_row=5)

    # Q4
    st.markdown(
        """<div class='question-text'>
4. 生成AIを、以下のことに使ったことがありますか。<br>
それぞれについて、「はい」または「いいえ」を選んでください。
</div>""",
        unsafe_allow_html=True,
    )

    for idx, (code, label) in enumerate(PURPOSE_ITEMS, start=1):
        yes_no_row(code, label, number=idx, stripe=(idx % 2 == 0))

# ──────────────────────────────
# Q1「いいえ」分岐
# ──────────────────────────────
elif q1 == "いいえ":
    divider()

    st.markdown(
        "<div class='red-note'>※ 1で「いいえ」と答えた方は、2〜4の質問は表示されません。</div>",
        unsafe_allow_html=True,
    )

    # Q5（表示上は「2.」）
    st.markdown(
        """<div class='question-text'>
2. 生成AIを使っていない理由についておたずねします。<br>
それぞれについて、「はい」または「いいえ」を選んでください。
</div>""",
        unsafe_allow_html=True,
    )

    for idx, (code, label) in enumerate(REASON_ITEMS, start=1):
        yes_no_row(code, label, number=idx, stripe=(idx % 2 == 0))

else:
    st.info("まず、1の質問で「はい」または「いいえ」を選んでください。")

st.markdown("</div>", unsafe_allow_html=True)  # .form-body 閉じ


# =========================
# 保存エリア
# =========================

st.markdown("<div class='save-area'>", unsafe_allow_html=True)

missing_fields = get_missing_fields()

if missing_fields:
    st.warning("⚠️ 未回答の項目があります。すべて回答してから保存してください。")
    with st.expander("未回答項目を確認する", expanded=False):
        for item in missing_fields:
            st.write(f"・{item}")

    st.button("回答を保存する", disabled=True, use_container_width=True)

else:
    if st.button("✔ 回答を保存する", type="primary", use_container_width=True):
        response_row = build_response_row()
        save_response(response_row)

        st.session_state["submitted"] = True
        st.session_state["last_saved_json"] = json.dumps(
            response_row,
            ensure_ascii=False,
            indent=2,
        )

        st.success("✅ 回答を保存しました。")

if st.session_state.get("submitted") and st.session_state.get("last_saved_json"):
    st.download_button(
        label="この回答をJSONでダウンロード",
        data=st.session_state["last_saved_json"],
        file_name="genai_questionnaire.json",
        mime="application/json",
        use_container_width=True,
    )

    if st.button("▶ 次の対象者の入力へ進む", use_container_width=True):
        reset_all()

st.markdown("</div>", unsafe_allow_html=True)  # .save-area 閉じ


# =========================
# 開発確認用（本番では削除可）
# =========================

with st.expander("現在の回答状況を確認する（開発用）", expanded=False):
    st.json(build_response_row())
