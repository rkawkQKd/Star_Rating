import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(
    page_title="학생 별점 관리",
    page_icon="⭐",
    layout="wide"
)

st.title("⭐ 학생 별점 관리 (정수 입력)")
st.markdown("점수는 **0점부터 10점까지 정수**로만 입력할 수 있습니다.")
st.markdown("---")

# 2. 데이터 준비
if 'student_data' not in st.session_state:
    # 초기 데이터도 정수로 변경했습니다 (3.5 -> 3)
    data = {
        '이름': ['김철수', '이영희', '박민수', '최지우'],
        '나이': [14, 15, 14, 16],
        '점수': [3, 9, 7, 5] 
    }
    st.session_state.student_data = pd.DataFrame(data)

# 3. 별점 생성 함수
def make_stars(score):
    # 정수가 들어오므로 int() 변환이 자연스럽습니다.
    star_count = int(score)
    if star_count > 10:
        return "⭐" * 10 + " (MAX)"
    return "⭐" * star_count

# 4. 사이드바: 학생 추가
with st.sidebar:
    st.header("➕ 학생 추가")
    new_name = st.text_input("이름")
    new_age = st.number_input("나이", 7, 20, 14)
    
    # [수정됨] 정수 입력 설정
    # step=1로 설정하여 1단위로만 움직이게 함
    # value=5 (정수)
    new_score = st.number_input(
        "점수 (0~10)", 
        min_value=0, 
        max_value=10, 
        value=5, 
        step=1
    )
    
    if st.button("추가하기"):
        if new_name:
            new_row = pd.DataFrame({'이름': [new_name], '나이': [new_age], '점수': [new_score]})
            st.session_state.student_data = pd.concat([st.session_state.student_data, new_row], ignore_index=True)
            st.success("추가되었습니다!")
            st.rerun()

# 5. 메인 화면: 데이터 편집기
st.subheader("📋 학생 명단")

# 번호를 1부터 보여주기 위한 처리
display_df = st.session_state.student_data.copy()
display_df['별점 시각화'] = display_df['점수'].apply(make_stars)
display_df.index = range(1, len(display_df) + 1)

edited_df = st.data_editor(
    display_df,
    column_config={
        "_index": st.column_config.NumberColumn("번호", disabled=True),
        "이름": st.column_config.TextColumn("학생 이름", width="medium"),
        "나이": st.column_config.NumberColumn("나이", format="%d세"),
        
        # [수정됨] 점수 컬럼 설정
        "점수": st.column_config.NumberColumn(
            "점수 (정수)",
            min_value=0,
            max_value=10,
            step=1,          # 1점 단위로 변경
            format="%d점"    # 소수점 없이 정수로 표시
        ),
        "별점 시각화": st.column_config.TextColumn(
            "별점 (자동)",
            disabled=True
        )
    },
    use_container_width=True,
    num_rows="dynamic",
    hide_index=False
)

# 6. 저장 로직
data_to_save = edited_df.drop(columns=['별점 시각화'])

# 인덱스 리셋 후 비교 및 저장
if not data_to_save.reset_index(drop=True).equals(st.session_state.student_data.reset_index(drop=True)):
    st.session_state.student_data = data_to_save.reset_index(drop=True)
    st.rerun()

# 7. 통계
st.markdown("---")
avg = st.session_state.student_data['점수'].mean()
# 평균은 소수점이 나올 수 있으므로 %.1f 유지
st.metric("전체 평균 점수", f"{avg:.1f}점")
