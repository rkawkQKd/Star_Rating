import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(
    page_title="학생 점수 관리",
    page_icon="✏️",
    layout="wide"
)

st.title("✏️ 학생 점수 관리")
st.markdown("학생 번호가 **1번**부터 시작합니다.")
st.markdown("---")

# 2. 데이터 준비
if 'student_data' not in st.session_state:
    data = {
        '이름': ['김철수', '이영희', '박민수', '최지우'],
        '나이': [14, 15, 14, 16],
        '점수': [3.5, 9.0, 7.2, 5.0]
    }
    st.session_state.student_data = pd.DataFrame(data)

# 3. 별점 생성 함수
def make_stars(score):
    try:
        star_count = int(score)
        if star_count > 10:
            return "⭐" * 10 + " (MAX)"
        return "⭐" * star_count
    except:
        return ""

# 4. 사이드바: 학생 추가
with st.sidebar:
    st.header("➕ 학생 추가")
    new_name = st.text_input("이름")
    new_age = st.number_input("나이", 7, 20, 14)
    new_score = st.number_input("점수", 0.0, 10.0, 5.0, 0.1)
    
    if st.button("추가하기"):
        if new_name:
            new_row = pd.DataFrame({'이름': [new_name], '나이': [new_age], '점수': [new_score]})
            # concat을 할 때 ignore_index=True로 하면 내부적으로는 다시 0부터 인덱싱이 됩니다.
            st.session_state.student_data = pd.concat([st.session_state.student_data, new_row], ignore_index=True)
            st.success("추가되었습니다!")
            st.rerun()

# 5. 메인 화면: 데이터 편집기
st.subheader("📋 학생 명단")

# [중요] 보여줄 데이터를 복사한 뒤, 인덱스(번호)를 1부터 강제로 다시 매깁니다.
display_df = st.session_state.student_data.copy()
display_df['별점 시각화'] = display_df['점수'].apply(make_stars)

# 인덱스를 1, 2, 3... 으로 설정 (데이터 개수만큼 범위를 만듦)
display_df.index = range(1, len(display_df) + 1)

edited_df = st.data_editor(
    display_df,
    column_config={
        # [중요] _index는 인덱스 컬럼을 의미합니다. 이름을 "번호"로 바꿉니다.
        "_index": st.column_config.NumberColumn("번호", disabled=True), 
        "이름": st.column_config.TextColumn("학생 이름", width="medium"),
        "나이": st.column_config.NumberColumn("나이", format="%d세"),
        "점수": st.column_config.NumberColumn(
            "점수 (수정 가능)",
            min_value=0,
            max_value=10,
            step=0.1,
            format="%.1f"
        ),
        "별점 시각화": st.column_config.TextColumn(
            "별점 (자동)",
            disabled=True
        )
    },
    use_container_width=True,
    num_rows="dynamic",
    hide_index=False # 인덱스(번호)를 숨기지 않고 보여줍니다.
)

# 6. 저장 로직
# 인덱스는 보여주기용으로 바꿨으므로, 내용 비교를 위해 '별점 시각화'만 빼고 비교합니다.
# 저장할 때는 다시 reset_index를 해서 0부터 시작하는 깔끔한 상태로 저장합니다.

# 현재 보여지는 데이터(edited_df)에서 별점 컬럼 제거
data_to_save = edited_df.drop(columns=['별점 시각화'])

# 데이터가 변경되었는지 확인 (값만 비교)
# reset_index(drop
