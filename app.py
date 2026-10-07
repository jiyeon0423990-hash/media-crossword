import streamlit as st

st.set_page_config(
    page_title="광고와 홍보물 핵심 개념 퍼즐",
    page_icon="🧩",
    layout="centered"
)

# =========================================================
# 1. 문제 데이터
# =========================================================

WORDS = {
    1: {
        "answer": "고정관념",
        "initial": "ㄱㅈㄱㄴ",
        "clue": "특정 집단이나 대상에 대해 굳어져 있는 생각이나 이미지",
        "cells": ["r1c2", "r1c3", "r1c4", "r1c5"],
    },
    2: {
        "answer": "정보",
        "initial": "ㅈㅂ",
        "clue": "어떤 사실이나 내용을 사람들에게 알려 주는 것",
        "cells": ["r1c3", "r2c3"],
    },
    3: {
        "answer": "관점",
        "initial": "ㄱㅈ",
        "clue": "제작자가 어떤 대상을 바라보는 생각이나 입장",
        "cells": ["r1c4", "r2c4"],
    },
    4: {
        "answer": "선택",
        "initial": "ㅅㅌ",
        "clue": "제작자가 특정 문구나 이미지를 골라 사용하는 것",
        "cells": ["r4c2", "r4c3"],
    },
    5: {
        "answer": "배제",
        "initial": "ㅂㅈ",
        "clue": "제작자가 어떤 문구나 이미지를 포함하지 않는 것",
        "cells": ["r4c6", "r4c7"],
    },
    6: {
        "answer": "설득",
        "initial": "ㅅㄷ",
        "clue": "보는 이의 생각이나 행동을 바꾸도록 하는 것",
        "cells": ["r6c4", "r6c5"],
    },
    7: {
        "answer": "의도",
        "initial": "ㅇㄷ",
        "clue": "제작자가 광고나 홍보물을 만든 목적이나 까닭",
        "cells": ["r8c2", "r8c3"],
    },
    8: {
        "answer": "재현",
        "initial": "ㅈㅎ",
        "clue": "현실을 특정한 방식으로 다시 보여 주는 것",
        "cells": ["r8c6", "r8c7"],
    },
}

# =========================================================
# 2. 각 퍼즐 칸의 정답 만들기
# =========================================================

CELL_ANSWERS = {}

for _, data in WORDS.items():
    for cell_id, char in zip(data["cells"], data["answer"]):
        if cell_id in CELL_ANSWERS:
            assert CELL_ANSWERS[cell_id] == char
        else:
            CELL_ANSWERS[cell_id] = char

# =========================================================
# 3. 세션 상태 초기화
# =========================================================

if "checked" not in st.session_state:
    st.session_state.checked = False

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "cell_results" not in st.session_state:
    st.session_state.cell_results = {}

if "word_results" not in st.session_state:
    st.session_state.word_results = {}

for cell_id in CELL_ANSWERS:
    if cell_id not in st.session_state:
        st.session_state[cell_id] = ""

# =========================================================
# 4. 스타일
# =========================================================

st.markdown(
    """
    <style>
    .block-container {
        max-width: 850px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .main-title {
        text-align: center;
        font-size: 2rem;
        font-weight: 800;
        margin-bottom: 6px;
    }

    .subtitle {
        text-align: center;
        color: #555;
        margin-bottom: 25px;
    }

    .clue-card {
        padding: 12px 15px;
        margin: 7px 0;
        border: 1px solid #dddddd;
        border-radius: 10px;
        background: #fafafa;
        line-height: 1.7;
    }

    .hint-box {
        border-radius: 10px;
        padding: 10px 14px;
        margin-top: 6px;
        margin-bottom: 10px;
        background: #fff4cf;
        border: 1px solid #e7c75d;
        font-weight: 700;
    }

    .correct-word {
        color: #188038;
        font-weight: 700;
    }

    .wrong-word {
        color: #d93025;
        font-weight: 700;
    }

    .score-card {
        text-align: center;
        margin-top: 20px;
        padding: 20px;
        border: 1px solid #dce3ef;
        border-radius: 15px;
        background: #f6f8fc;
    }

    div[data-testid="stTextInput"] input {
        text-align: center;
        font-size: 1.35rem;
        font-weight: 800;
        height: 48px;
        padding: 0 !important;
        border: 2px solid #555;
        border-radius: 5px;
    }

    .blank-cell {
        height: 48px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# 5. 채점 이후 칸 색상
# =========================================================

if st.session_state.checked:
    css = "<style>"

    for cell_id, is_correct in st.session_state.cell_results.items():
        if is_correct:
            css += f"""
            div[data-testid="stTextInput"]:has(
                input[aria-label="{cell_id}"]
            ) input {{
                background-color: #e6f4ea !important;
                border: 3px solid #188038 !important;
            }}
            """
        else:
            css += f"""
            div[data-testid="stTextInput"]:has(
                input[aria-label="{cell_id}"]
            ) input {{
                background-color: #fce8e6 !important;
                border: 3px solid #d93025 !important;
                color: #d93025 !important;
            }}
            """

    css += "</style>"
    st.markdown(css, unsafe_allow_html=True)

# =========================================================
# 6. 제목
# =========================================================

st.markdown(
    """
    <div class="main-title">
        🧩 광고와 홍보물 핵심 개념 십자말풀이
    </div>

    <div class="subtitle">
        힌트를 읽고 네모 칸에 한 글자씩 입력하세요.
    </div>
    """,
    unsafe_allow_html=True,
)

st.info(
    "📌 맞춤법까지 정확해야 정답입니다. "
    "채점 후 틀린 글자만 빨간색으로 표시됩니다."
)

# =========================================================
# 7. 문제 힌트
# =========================================================

st.subheader("🔎 낱말 힌트")

for num, data in WORDS.items():
    st.markdown(
        f"""
        <div class="clue-card">
        <b>{num}.</b> {data["clue"]}
        <span style="color:#777;">
        ({len(data["answer"])}글자)
        </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if (
        st.session_state.checked
        and not st.session_state.word_results.get(num, False)
    ):
        st.markdown(
            f"""
            <div class="hint-box">
            💡 재도전 힌트 : {data["initial"]}
            </div>
            """,
            unsafe_allow_html=True,
        )

st.divider()

# =========================================================
# 8. 퍼즐판
# =========================================================

GRID = [
    [None, "r1c2", "r1c3", "r1c4", "r1c5", None, None, None],
    [None, None, "r2c3", "r2c4", None, None, None, None],
    [None] * 8,
    [None, "r4c2", "r4c3", None, None, "r4c6", "r4c7", None],
    [None] * 8,
    [None, None, None, "r6c4", "r6c5", None, None, None],
    [None] * 8,
    [None, "r8c2", "r8c3", None, None, "r8c6", "r8c7", None],
]

st.subheader("✏️ 퍼즐판")
st.caption("① 고정관념과 ② 정보, ③ 관점은 서로 글자가 교차합니다.")

# =========================================================
# 9. 퍼즐판 출력
# =========================================================

for row in GRID:
    cols = st.columns(8, gap="small")

    for col, cell_id in zip(cols, row):
        with col:
            if cell_id is None:
                st.markdown(
                    '<div class="blank-cell"></div>',
                    unsafe_allow_html=True,
                )
            else:
                st.text_input(
                    cell_id,
                    key=cell_id,
                    max_chars=1,
                    label_visibility="collapsed",
                )

# =========================================================
# 10. 채점
# =========================================================

def grade():
    cell_results = {}

    for cell_id, correct_char in CELL_ANSWERS.items():
        student_char = st.session_state[cell_id].strip()
        cell_results[cell_id] = student_char == correct_char

    word_results = {}

    for num, data in WORDS.items():
        student_word = "".join(
            st.session_state[cell].strip()
            for cell in data["cells"]
        )
        word_results[num] = student_word == data["answer"]

    st.session_state.cell_results = cell_results
    st.session_state.word_results = word_results
    st.session_state.attempts += 1
    st.session_state.checked = True

# =========================================================
# 11. 초기화
# =========================================================

def reset_game():
    for cell_id in CELL_ANSWERS:
        st.session_state[cell_id] = ""

    st.session_state.checked = False
    st.session_state.attempts = 0
    st.session_state.cell_results = {}
    st.session_state.word_results = {}

# =========================================================
# 12. 버튼
# =========================================================

st.write("")

button_col1, button_col2 = st.columns(2)

with button_col1:
    if st.button(
        "✅ 채점하기",
        type="primary",
        use_container_width=True,
    ):
        grade()
        st.rerun()

with button_col2:
    if st.button(
        "🔄 처음부터 다시 하기",
        use_container_width=True,
    ):
        reset_game()
        st.rerun()

# =========================================================
# 13. 결과
# =========================================================

if st.session_state.checked:
    correct_words = sum(st.session_state.word_results.values())
    total_words = len(WORDS)
    score = round(correct_words / total_words * 100)

    st.markdown(
        f"""
        <div class="score-card">
        <h2>{correct_words} / {total_words} 정답</h2>
        <h3>{score}점</h3>
        <p>현재 {st.session_state.attempts}번째 도전입니다.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    for num in WORDS:
        if st.session_state.word_results[num]:
            st.markdown(
                f"""
                <span class="correct-word">
                ✅ {num}번 정답!
                </span>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <span class="wrong-word">
                ❌ {num}번에서 빨간색 칸을 다시 살펴보세요.
                </span>
                """,
                unsafe_allow_html=True,
            )

    st.write("")

    if correct_words == total_words:
        st.balloons()
        st.success(
            "🎉 모두 맞았습니다! "
            "광고와 홍보물을 분석하는 핵심 개념을 잘 이해했어요."
        )
    else:
        st.warning(
            "🔴 빨간색 칸은 틀린 글자입니다. "
            "초성 힌트를 참고해서 수정한 뒤 "
            "다시 「채점하기」를 눌러 보세요."
        )
