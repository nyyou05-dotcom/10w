import streamlit as st
import pandas as pd
import numpy as np

# 보드게임 데이터
data = {
    "게임 이름": ["광기의 저택", "엘드리치 호러", "아컴 호러", "블리츠", "클루", "데드 오브 윈터"],
    "카테고리": ["협력, 테마", "협력, 테마", "협력, 테마", "카드, 경쟁", "추리, 경쟁, 심리", "테마, 협력, 좀비, 경쟁"],
    "난이도": ["어려움", "매우 어려움", "매우 어려움", "쉬움", "보통", "매우 어려움"],
    "추천 인원수": [5, 6, 6, 2, 4, 4],
    "별점": [4, 5, 5, 4, 5, 4],
    "플레이 횟수": [2, 4, 2, 1, 1, 1]
}

df = pd.DataFrame(data)

# 제목
st.title("🎲 나의 보드게임 대시보드")

st.write("내가 플레이한 보드게임을 정리하고, 조건에 맞는 게임을 추천하는 대시보드입니다.")

# 보드게임 통계
st.header("보드게임 통계")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("등록된 게임", len(df))

with col2:
    st.metric("평균 별점", round(df["별점"].mean(), 1))

with col3:
    st.metric("총 플레이 횟수", df["플레이 횟수"].sum())

# 보드게임 검색
st.header("보드게임 검색")

category = st.selectbox(
    "카테고리를 선택하세요",
    ["전체", "테마", "좀비", "심리", "추리", "협력", "카드", "경쟁"]
)

difficulty = st.selectbox(
    "난이도를 선택하세요",
    ["전체", "쉬움", "보통", "어려움", "매우 어려움"]
)

people = st.slider("플레이 인원수를 선택하세요", 2, 8, 4)

# 선택한 조건에 따라 데이터 변경
filtered_df = df.copy()

if category != "전체":
    filtered_df = filtered_df[filtered_df["카테고리"] == category]

if difficulty != "전체":
    filtered_df = filtered_df[filtered_df["난이도"] == difficulty]

filtered_df = filtered_df[filtered_df["추천 인원수"] == people]

st.subheader("검색 결과")

if len(filtered_df) > 0:
    st.write("조건에 맞는 보드게임은", len(filtered_df), "개입니다.")
    st.dataframe(filtered_df)
else:
    st.warning("조건에 맞는 보드게임이 없습니다.")

# 보드게임 추천
st.header("보드게임 추천")

if len(filtered_df) > 0:
    recommended = filtered_df.sort_values("별점", ascending=False)
    best_game = recommended.iloc[0]

    st.success("추천 게임: " + best_game["게임 이름"])
    st.write("카테고리:", best_game["카테고리"])
    st.write("난이도:", best_game["난이도"])
    st.write("별점:", "⭐" * int(best_game["별점"]))
else:
    st.write("추천할 게임이 없습니다.")

# 차트
st.header("보드게임 분석")

st.subheader("카테고리별 게임 수")
category_count = df["카테고리"].value_counts()
st.bar_chart(category_count)

st.subheader("게임별 플레이 횟수")
play_count = df.set_index("게임 이름")["플레이 횟수"]
st.bar_chart(play_count)

# 전체 데이터
st.header("전체 보드게임 목록")
st.dataframe(df)
