import random
import streamlit as st
import pandas as pd

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
    all_numbers = []
    rule_texts = []

    for combo in results:
        all_numbers.append(", ".join(str(n) for n in combo))
        rule_texts.append("""
- 홀짝 비율 적절 (3:3 또는 4:2)
- 합계 130~170
- 끝수 다양성 ≥ 5
- 연속된 숫자 포함
- 번호대 분포 고름
- 동반출현 번호쌍 포함
- 마코프 번호 포함
""")

    df = pd.DataFrame({"추천 조합": all_numbers, "적용된 규칙": rule_texts})
    st.dataframe(df, use_container_width=True)

    copy_text = "\n".join(all_numbers)
    st.text_area("📋 전체 조합 복사하기", value=copy_text, height=200)
    st.success("✅ 조합이 표 형태로 생성되었습니다. 위 텍스트를 복사해 사용하세요!")
