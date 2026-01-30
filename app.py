import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(
    page_title="학생 성적 관리부",
    page_icon="🏫",
    layout="wide"
)

st.title("🏫 학생 성적 관리부")
st.markdown("학생의 **학년**과 **반** 정보도 함께 관리할 수 있습니다.")
st.markdown("---")

# 2. 데이터 준비 (컬럼 추가됨)
if 'student_data' not in st.session_state:
    data = {
        '학년': [2, 3, 2, 1],
        '반': [1, 5, 3, 2],
        '번호': [15, 7, 20, 3], # (선택사항) 출석번호도 있으면 좋겠지만 일단 제외
        '이름': ['김철수', '이영희', '박민수', '최지우'],
        '나이': [15, 16, 15, 14],
        '점수': [3, 9, 7, 5] 
    }
    st.session_state.student_data = pd.DataFrame(data)

# 3. 별점 생성 함수
def make_stars(score):
    star_count = int(score)
    if star_count > 10:
        return "⭐" * 10 + " (MAX)"
    return "⭐" * star_count

# 4. 사이드바: 학생 추가 (입력창 추가됨)
with st.sidebar:
    st.header("➕ 학생 등록")
    
    # [추가됨] 학년, 반 입력
    col1, col2 = st.columns(2) # 입력창을 두 줄로 나누어 예쁘게 배치
    with col1:
        new_grade = st.number_input("학년", min_value=1, max_value=6, value=1, step=1)
    with col2:
        new_class = st.number_input("반", min_value=1, max_value=20, value=1, step=1)

    new_name = st.text_input("이름")
    new_age = st.number_input("나이", min_value=7, max_value=20, value=14)
    
    new_score = st.number_input(
        "점수 (0~10)", 
        min_value=0, 
        max_value=10, 
        value=5, 
        step=1
    )
    
    if st.button("등록하기"):
        if new_name:
            new_row = pd.DataFrame({
                '학년': [new_grade],
                '반': [new_class],
                '이름': [new_name], 
                '나이': [new_age], 
                '점수': [new_score]
            })
            st.session_state.student_data = pd.concat([st.session_state.student_data, new_row], ignore_index=True)
            st.success(f"{new_grade}학년 {new_class}반 {new_name} 학생 등록 완료!")
            st.rerun()

# 5. 메인 화면: 데이터 편집기
st.subheader("📋 학급 명단")

# 정렬 및 인덱스 정리
display_df = st.session_state.student_data.copy()
display_df['별점 시각화'] = display_df['점수'].apply(make_stars)
display_df.index = range(1, len(display_df) + 1)

edited_df = st.data_editor(
    display_df,
    column_config={
        "_index": st.column_config.NumberColumn("No.", disabled=True),
        
        # [추가됨] 학년, 반 컬럼 설정
        "학년": st.column_config.NumberColumn(
            "학년", 
            format="%d학년", 
            step=1, 
            width="small"
        ),
        "반": st.column_config.NumberColumn(
            "반", 
            format="%d반", 
            step=1, 
            width="small"
        ),
        
        "이름": st.column_config.TextColumn("이름", width="medium"),
        "나이": st.column_config.NumberColumn("나이", format="%d세"),
        "점수": st.column_config.NumberColumn(
            "점수",
            min_value=0,
            max_value=10,
            step=1,
            format="%d점"
        ),
        "별점 시각화": st.column_config.TextColumn(
            "평가",
            disabled=True,
            width="medium"
        )
    },
    use_container_width=True,
    num_rows="dynamic",
    hide_index=False
)

# 6. 저장 로직
data_to_save = edited_df.drop(columns=['별점 시각화'])

if not data_to_save.reset_index(drop=True).equals(st.session_state.student_data.reset_index(drop=True)):
    st.session_state.student_data = data_to_save.reset_index(drop=True)
    st.rerun()

# 7. 통계 (반별 평균 등 응용 가능)
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    avg = st.session_state.student_data['점수'].mean()
    st.metric("전체 평균 점수", f"{avg:.1f}점")
with col2:
    count = len(st.session_state.student_data)
    st.metric("총 학생 수", f"{count}명")
