import streamlit as st
import pandas as pd
import plotly.express as px

# 엑셀 파일 불러오기
df = pd.read_excel("테스트파일.xlsx")

st.title("📦 물류센터 출고 관리 대시보드")

# 날짜 필터
st.sidebar.header("필터")
selected_date = st.sidebar.date_input("출고일자 기준", pd.to_datetime(df['출고일자']).max())
df['출고일자'] = pd.to_datetime(df['출고일자'], errors='coerce')
filtered_df = df[df['출고일자'] == pd.to_datetime(selected_date)]

# 제품군 선택
product_groups = df['제품군'].dropna().unique()
selected_group = st.sidebar.multiselect("제품군 선택", product_groups, default=product_groups)
filtered_df = filtered_df[filtered_df['제품군'].isin(selected_group)]

# 출하형태 선택
ship_types = df['출하형태명'].dropna().unique()
selected_ship_type = st.sidebar.multiselect("출하형태명 선택", ship_types, default=ship_types)
filtered_df = filtered_df[filtered_df['출하형태명'].isin(selected_ship_type)]

# 메인 테이블
st.subheader("출고 리스트")
st.dataframe(filtered_df)

# 요약 지표
total_qty = filtered_df['출하수량'].sum()
total_amount = filtered_df['원화금액'].sum()
st.metric("총 출하수량", f"{total_qty:,}")
st.metric("총 출고금액", f"₩ {total_amount:,.0f}")

# 제품군별 출고 금액 차트
st.subheader("제품군별 출고 금액")
if not filtered_df.empty:
    group_chart = filtered_df.groupby('제품군')['원화금액'].sum().reset_index()
    fig = px.bar(group_chart, x='제품군', y='원화금액', text='원화금액', color='제품군')
    st.plotly_chart(fig)

# CSV 다운로드
st.subheader("출고 데이터 다운로드")
st.download_button(
    label="CSV 다운로드",
    data=filtered_df.to_csv(index=False).encode('utf-8-sig'),
    file_name='출고리스트_다운로드.csv',
    mime='text/csv'
)
