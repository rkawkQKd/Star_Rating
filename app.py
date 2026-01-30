import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(
    page_title="학생 점수 관리 (수정 모드)",
    page_icon="✏️",
    layout="wide"
)

st.title("✏️ 학생 점수 관리 및 수정")
st.markdown("표의 내용을 **마우스로 클릭**하여 바로 수정해보세요. 별점이 자동으로 바뀝니다!")
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

# 4. 사이드바: 학생 추가 (기존 기능 유지)
with st.sidebar:
    st.header("➕ 학생 추가")
    new_name = st.text_input("이름")
    new_age = st.number_input("나이", 7, 20, 14)
    new_score = st.number_input("점수", 0.0, 10.0, 5.0, 0.1)
    
    if st.button("추가하기"):
        if new_name:
            new_row = pd.DataFrame({'이름': [new_name], '나이': [new_age], '점수': [new_score]})
            st.session_state.student_data = pd.concat([st.session_state.student_data, new_row], ignore_index=True)
            st.success("추가되었습니다!")
            st.rerun() # 데이터 추가 후 화면 즉시 새로고침

# 5. 메인 화면: 데이터 편집기 (핵심 기능!)
st.subheader("📋 학생 명단 (직접 수정 가능)")

# 현재 데이터에 '별점 미리보기' 컬럼을 잠시 붙여서 보여줍니다.
# (원본 데이터에는 저장하지 않고 보여주기용으로만 씁니다)
display_df = st.session_state.student_data.copy()
display_df['별점 시각화'] = display_df['점수'].apply(make_stars)

# st.data_editor를 사용하여 데이터를 표시하고 수정을 허용합니다.
edited_df = st.data_editor(
    display_df,
    column_config={
        "이름": st.column_config.TextColumn("학생 이름", width="medium"),
        "나이": st.column_config.NumberColumn("나이", format="%d세"),
        "점수": st.column_config.NumberColumn(
            "점수 (클릭해서 수정)",
            help="점수를 수정하면 별점이 바뀝니다.",
            min_value=0,
            max_value=10,
            step=0.1,
            format="%.1f"
        ),
        "별점 시각화": st.column_config.TextColumn(
            "현재 별점 (자동)",
            disabled=True # 이 컬럼은 수정 불가능하게 막음 (자동 계산되므로)
        )
    },
    use_container_width=True,
    num_rows="dynamic", # 행 추가/삭제 기능 활성화
    hide_index=True
)

# 6. 수정된 데이터 저장 로직
# 사용자가 편집기에서 무언가를 수정하면 edited_df가 바뀝니다.
# '별점 시각화'는 저장할 필요가 없으므로 제거하고 원본 데이터(이름, 나이, 점수)만 세션에 업데이트합니다.

# 데이터가 변경되었는지 확인 (간단히 비교)
is_changed = not edited_df.drop(columns=['별점 시각화']).equals(st.session_state.student_data)

if is_changed:
    # 별점 시각화 컬럼을 제외하고 저장
    st.session_state.student_data = edited_df.drop(columns=['별점 시각화'])
    st.rerun() # 변경 즉시 화면을 새로고침하여 별점 업데이트 반영

# 7. 통계
st.markdown("---")
avg = st.session_state.student_data['점수'].mean()
st.metric("전체 평균 점수", f"{avg:.1f}점")
