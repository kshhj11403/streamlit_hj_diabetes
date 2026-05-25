import streamlit as st
import pandas as pd
import joblib
import os

# =========================================
# ⚖️ 페이지 설정
# =========================================
st.set_page_config(
    page_title="당뇨 재판소",
    page_icon="⚖️",
    layout="centered"
)

# =========================================
# 🎨 도트 재판소 CSS
# =========================================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

html, body, [class*="css"]{
    background-color:#1c1c1c;
    color:white;
    font-family:'Press Start 2P', cursive;
}

/* 전체 여백 */
.block-container{
    padding-top:2rem;
}

/* 메인 타이틀 */
.main-title{
    text-align:center;
    font-size:34px;
    color:#ffcc00;
    line-height:1.6;
    text-shadow:
        4px 4px 0px black;
    margin-bottom:20px;
}

/* 부제목 */
.sub-title{
    background:#2a2a2a;
    border:4px solid #ffcc00;
    padding:20px;
    line-height:1.9;
    text-align:center;
    margin-bottom:30px;
    box-shadow:8px 8px 0px black;
}

/* 입력 박스 */
.pixel-box{
    background:#2a2a2a;
    border:4px solid white;
    padding:20px;
    margin-bottom:20px;
    box-shadow:8px 8px 0px black;
}

/* 입력창 */
div[data-baseweb="input"] input{
    background:#121212;
    color:#00ff99;
    border:3px solid white;
    border-radius:0px;
    font-family:'Press Start 2P', cursive;
}

/* 버튼 */
.stButton > button{
    background:#8b0000;
    color:white;
    border:4px solid white;
    border-radius:0px;
    height:85px;
    font-size:18px;
    font-family:'Press Start 2P', cursive;
    box-shadow:8px 8px 0px black;
    transition:0.1s;
}

.stButton > button:hover{
    transform:translate(3px,3px);
    box-shadow:3px 3px 0px black;
}

/* 판결문 */
.verdict-guilty{
    background:#4a1010;
    border:4px solid #ff4444;
    padding:30px;
    line-height:2;
    box-shadow:10px 10px 0px black;
    margin-top:20px;
}

.verdict-safe{
    background:#103b22;
    border:4px solid #00ff99;
    padding:30px;
    line-height:2;
    box-shadow:10px 10px 0px black;
    margin-top:20px;
}

/* 깜빡임 */
@keyframes blink{
    50%{
        opacity:0.7;
    }
}

.blink{
    animation:blink 1s infinite;
}

/* 제목 */
h1,h2,h3{
    color:#ffcc00 !important;
}

/* 성공/경고 */
.stSuccess{
    border:4px solid #00ff99;
}

.stWarning{
    border:4px solid #ffcc00;
}

.stError{
    border:4px solid #ff4444;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# 📂 모델 로딩
# =========================================
current_dir = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(current_dir, "diabetes_model.pkl")
scaler_path = os.path.join(current_dir, "diabetes_scaler.pkl")

FEATURE_COLUMNS = [
    '임신',
    '혈당',
    '혈압',
    '피부두께',
    '인슐린',
    'BMI',
    '당뇨내력지수',
    '나이',
    '비만상태',
    '고령',
    '신체위험점수',
    '유전연령지수'
]

try:

    scaler = joblib.load(scaler_path)
    model = joblib.load(model_path)

    st.toast("⚖️ 재판관 입장 완료", icon="🔔")

except Exception as e:

    st.error(f"재판 준비 실패: {e}")
    st.stop()

# =========================================
# ⚖️ 제목
# =========================================
st.markdown("""
<div class="main-title">
⚖️ 당뇨 재판소 ⚖️
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="sub-title">
혈관 상태에 대한 심리를 시작합니다.<br><br>
모든 수치는 재판 기록으로 보관됩니다.
</div>
""", unsafe_allow_html=True)

# =========================================
# 입력 UI
# =========================================
st.markdown('<div class="pixel-box">', unsafe_allow_html=True)

st.subheader("📜 피고인 기록")

col1, col2 = st.columns(2)

with col1:

    preg = st.number_input(
        "임신 횟수",
        0, 20, 1
    )

    glucose = st.number_input(
        "혈당 수치",
        0, 300, 120
    )

    bp = st.number_input(
        "혈압",
        0, 200, 70
    )

    skin = st.number_input(
        "피부두께",
        0, 100, 20
    )

with col2:

    insulin = st.number_input(
        "인슐린 수치",
        0, 900, 80
    )

    bmi = st.number_input(
        "BMI",
        0.0, 70.0, 30.0
    )

    dpf = st.number_input(
        "당뇨내력",
        0.0, 3.0, 0.4
    )

    age = st.number_input(
        "나이",
        0, 120, 30
    )

st.markdown("</div>", unsafe_allow_html=True)

# =========================================
# 경고 문구
# =========================================
if glucose >= 150:
    st.warning("⚠️ 법원이 높은 혈당 수치를 확인했습니다.")

if bmi >= 35:
    st.error("🚨 체중 관련 위험 요소가 감지되었습니다.")

# =========================================
# 판결 버튼
# =========================================
if st.button("⚖️ 판결 선고"):

    input_df = pd.DataFrame([{
        '임신': preg,
        '혈당': glucose,
        '혈압': bp,
        '피부두께': skin,
        '인슐린': insulin,
        'BMI': bmi,
        '당뇨내력지수': dpf,
        '나이': age
    }])

    # 파생 변수
    input_df['비만상태'] = (
        input_df['BMI'] >= 35
    ).astype(int)

    input_df['고령'] = (
        input_df['나이'] >= 60
    ).astype(int)

    input_df['신체위험점수'] = (
        input_df['혈당']
        + input_df['혈압']
        + input_df['BMI']
    )

    input_df['유전연령지수'] = (
        input_df['당뇨내력지수']
        * input_df['나이']
    )

    input_df = input_df[FEATURE_COLUMNS]

    try:

        scaled_data = scaler.transform(input_df)

        prediction = model.predict(scaled_data)[0]

        probability = (
            model.predict_proba(scaled_data)[0][1]
            * 100
        )

        st.write("")

        # =====================================
        # 🚨 유죄 판결
        # =====================================
        if prediction == 1:

            st.markdown(f"""
            <div class="verdict-guilty blink">

            <h2>⚖️ 유죄 판결 ⚖️</h2>

            <br>

            법원은 제출된 혈관 기록과
            췌장 상태를 종합적으로 검토한 결과,

            피고인에게서 상당한 수준의
            당뇨 위험 요소가 존재한다고 판단하였습니다.

            <br><br>

            🚨 위험도:
            {probability:.1f}%

            <br><br>

            현재 혈당 관리와 생활 습관에 대한
            즉각적인 주의가 필요합니다.

            <br><br>

            본 법정은 피고인에게
            건강 검진을 강력히 권고합니다.

            </div>
            """, unsafe_allow_html=True)

        # =====================================
        # 🌿 정상 판결
        # =====================================
        else:

            st.markdown(f"""
            <div class="verdict-safe">

            <h2>⚖️ 정상 판결 ⚖️</h2>

            <br>

            법원은 제출된 건강 기록을 검토한 결과,

            현재 상태에서는 당뇨 위험도가
            비교적 안정적인 수준이라고 판단하였습니다.

            <br><br>

            🌿 위험도:
            {probability:.1f}%

            <br><br>

            다만 지속적인 건강 관리와
            생활 습관 유지는 필요합니다.

            <br><br>

            본 법정은 피고인의 건강한 생활을 응원합니다.

            </div>
            """, unsafe_allow_html=True)

    except Exception as e:

        st.error(f"""
⚠️ 재판 진행 중 오류 발생

에러 내용:
{e}

학습 데이터 컬럼과
현재 입력 컬럼이 일치하는지 확인하십시오.
""")