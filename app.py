import streamlit as st
import pandas as pd

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="학생 별점 관리",
    page_icon="🎓",
    layout="wide"
)

# 2. 제목 및 설명
st.title("🎓 학생 별점 관리 보드")
st.markdown("학생들의 **이름**, **나이**, 그리고 **별점**을 한눈에 확인하세요.")
st.markdown("---")

# 3. 데이터 준비 (세션 스테이트를 사용하여 데이터 유지)
# 초기 데이터가 없다면 생성합니다.
if 'student_data' not in st.session_state:
    data = {
        '이름': ['김철수', '이영희', '박민수', '최지우', '정수현'],
        '나이': [14, 15, 14, 16, 15],
        '별점': [3, 5, 4, 5, 2]
    }
    st.session_state.student_data = pd.DataFrame(data)

# 4. 사이드바: 새로운 학생 추가 기능
with st.sidebar:
    st.header("📝 학생 추가하기")
    new_name = st.text_input("이름")
    new_age = st.number_input("나이", min_value=7, max_value=20, value=14)
    new_rating = st.slider("별점", 1, 5, 3)
    
    if st.button("추가"):
        new_row = pd.DataFrame({'이름': [new_name], '나이': [new_age], '별점': [new_rating]})
        st.session_state.student_data = pd.concat([st.session_state.student_data, new_row], ignore_index=True)
        st.success(f"{new_name} 학생이 추가되었습니다!")

# 5. 메인 화면: 데이터 표시
# 원본 데이터를 복사하여 시각화용 컬럼을 만듭니다.
display_df = st.session_state.student_data.copy()

# 숫자 별점을 '⭐' 문자열로 변환하는 함수
def make_stars(score):
    return "⭐" * int(score)

display_df['별점 시각화'] = display_df['별점'].apply(make_stars)

# 6. 데이터프레임 출력 (컬럼 설정 활용)
st.subheader("📊 학생 목록")

st.dataframe(
    display_df,
    column_config={
        "이름": st.column_config.TextColumn("학생 이름", width="medium"),
        "나이": st.column_config.NumberColumn("나이", format="%d세"),
        "별점": st.column_config.NumberColumn(
            "점수 (1-5)",
            help="숫자로 된 점수입니다.",
            min_value=1,
            max_value=5,
        ),
        "별점 시각화": st.column_config.TextColumn(
            "평가 (별점)",
            help="별점으로 시각화된 결과입니다.",
            width="medium"
        ),
    },
    use_container_width=True,
    hide_index=True
)

# 7. 통계 요약 (선택 사항)
st.markdown("---")
avg_score = display_df['별점'].mean()
st.metric(label="전체 학생 평균 별점", value=f"{avg_score:.1f}점")