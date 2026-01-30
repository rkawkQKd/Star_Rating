import streamlit as st
import pandas as pd

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="학생 점수 관리",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 학생 점수 관리 보드")
st.markdown("5점 만점이 아닌, **자유로운 점수(소수점 포함)**를 입력해 보세요.")
st.markdown("---")

# 2. 데이터 준비
if 'student_data' not in st.session_state:
    data = {
        '이름': ['김철수', '이영희', '박민수', '최지우'],
        '나이': [14, 15, 14, 16],
        '점수': [3.5, 9.0, 7.2, 5.0]  # 소수점 점수 예시
    }
    st.session_state.student_data = pd.DataFrame(data)

# 3. 사이드바: 입력 방식 변경 (핵심 수정 부분)
with st.sidebar:
    st.header("📝 학생 추가하기")
    new_name = st.text_input("이름")
    new_age = st.number_input("나이", min_value=7, max_value=20, value=14)
    
    # [수정됨] 슬라이더 대신 숫자 입력창 사용
    # step=0.1로 설정하여 소수점 입력 가능
    # max_value를 10.0으로 설정 (원하시면 100.0으로 바꾸거나 지워서 무제한으로 가능)
    new_rating = st.number_input(
        "점수 입력", 
        min_value=0.0, 
        max_value=10.0, 
        value=5.0, 
        step=0.1,
        format="%.1f"
    )
    
    if st.button("추가"):
        # 입력값이 비어있지 않을 때만 추가
        if new_name:
            new_row = pd.DataFrame({'이름': [new_name], '나이': [new_age], '점수': [new_rating]})
            st.session_state.student_data = pd.concat([st.session_state.student_data, new_row], ignore_index=True)
            st.success(f"{new_name} 학생 (점수: {new_rating}점) 추가 완료!")
        else:
            st.warning("이름을 입력해주세요.")

# 4. 메인 화면: 데이터 표시
display_df = st.session_state.student_data.copy()

# [수정됨] 점수에 따라 별 개수 보여주기 (소수점은 내림 처리, 예: 4.8 -> 별 4개)
# 점수가 10점이 넘어가면 별이 너무 많아지므로, 최대 10개까지만 보여주도록 제한합니다.
def make_stars(score):
    star_count = int(score) 
    # 별이 너무 길어지는 것을 방지 (최대 10개)
    if star_count > 10: 
        return "⭐" * 10 + " (만점 초과!)"
    return "⭐" * star_count

display_df['별점 시각화'] = display_df['점수'].apply(make_stars)

st.subheader("📊 학생 성적표")

st.dataframe(
    display_df,
    column_config={
        "이름": st.column_config.TextColumn("학생 이름", width="medium"),
        "나이": st.column_config.NumberColumn("나이", format="%d세"),
        "점수": st.column_config.NumberColumn(
            "점수",
            help="자유롭게 입력된 점수입니다.",
            format="%.1f 점" # 소수점 첫째자리까지 표시
        ),
        "별점 시각화": st.column_config.TextColumn(
            "평가 (시각화)",
            width="medium"
        ),
    },
    use_container_width=True,
    hide_index=True
)

# 5. 통계
st.markdown("---")
avg_score = display_df['점수'].mean()
st.metric(label="전체 평균 점수", value=f"{avg_score:.2f}점")
