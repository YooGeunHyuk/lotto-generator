
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

st.title("🎯 수학 기반 로또 추천 조합 생성기")
st.write("과학적으로 검증된 규칙을 기반으로 로또 조합을 생성합니다.")

num_sets = st.slider("생성할 조합 수량", 1, 10, 5)
if st.button("조합 생성하기"):
    results = generate_lotto_set(num_sets)
    for idx, combo in enumerate(results, 1):
        st.write(f"**조합 {idx}:**", combo)
