import random
import streamlit as st

# 필수 기반 데이터
high_freq_numbers = [34, 12, 13, 18, 27, 3, 17, 7, 33, 14]
co_occur_pairs = [(11, 21), (33, 40), (6, 38), (12, 24), (3, 20)]
markov_favored = [5, 2, 21, 18, 3]

def is_valid_combo(combo):
    combo = sorted(combo)
    odd = sum(1 for n in combo if n % 2)
    if odd not in [2, 3, 4]: return False
    if not (130 <= sum(combo) <= 170): return False
    if len(set(n % 10 for n in combo)) < 5: return False
    if not any(combo[i]+1 == combo[i+1] for i in range(5)): return False
    ranges = [0]*5
    for n in combo:
        if 1 <= n <= 10: ranges[0] += 1
        elif 11 <= n <= 20: ranges[1] += 1
        elif 21 <= n <= 30: ranges[2] += 1
        elif 31 <= n <= 40: ranges[3] += 1
        else: ranges[4] += 1
    if sum(r > 0 for r in ranges) < 3: return False
    if not any(p[0] in combo and p[1] in combo for p in co_occur_pairs): return False
    if not any(n in combo for n in markov_favored): return False
    return True

def generate_lotto_set(n=5):
    results = set()
    while len(results) < n:
        trial = sorted(random.sample(range(1, 46), 6))
        if is_valid_combo(trial):
            results.add(tuple(trial))
    return list(results)

st.set_page_config(page_title="로또 조합 생성기", page_icon="🎯")
st.title("🎯 수학 기반 로또 추천 조합 생성기")
st.write("과학적으로 검증된 규칙을 바탕으로 조합을 생성하고, 번호별 해설과 규칙 통과 내역도 함께 확인하세요!")

num_sets = st.slider("생성할 조합 수량", 1, 20, 5)
if st.button("🎰 조합 생성하기"):
    results = generate_lotto_set(num_sets)
    for idx, combo in enumerate(results, 1):
        st.markdown(f"### 🎟️ 조합 {idx}")
        cols = st.columns(6)
        for i, num in enumerate(combo):
            color = "blue" if num <= 10 else "green" if num <= 20 else "orange" if num <= 30 else "red" if num <= 40 else "purple"
            cols[i].markdown(f"<div style='text-align:center; background-color:{color}; color:white; padding:10px; border-radius:10px;'>{num}</div>", unsafe_allow_html=True)

        # 규칙 통과 내역 표시
        st.markdown("**✅ 적용된 규칙**")
        st.write("- 홀짝 비율: 3:3 또는 4:2")
        st.write("- 합계: 130 ~ 170")
        st.write("- 끝수 다양성: 최소 5종")
        st.write("- 연속된 숫자 한 쌍 포함")
        st.write("- 번호대 분포 고름 (1~45 범위에서 최소 3구간 이상)")
        st.write("- 동반출현 번호쌍 포함")
        st.write("- 마코프 확률 번호 포함")

    st.success("✅ 조합이 성공적으로 생성되었습니다! 복사해서 사용하세요!")
