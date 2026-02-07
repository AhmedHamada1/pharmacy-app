import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# تحميل البيانات
df = pd.read_csv('pharmacies.csv')

st.set_page_config(page_title="خريطة الصيدليات", layout="wide")

st.title("🗺️ خريطة الصيدليات")
st.markdown("---")

# ==================== الفلاتر المتقدمة ====================
st.subheader("🔍 الفلاتر")

col1, col2, col3, col4 = st.columns(4)

# فلتر المدينة (متعدد)
with col1:
    city_options = list(df['City'].unique())
    select_all_city = st.checkbox("✓ اختر كل المدن", value=False, key="city_all")
    if select_all_city:
        cities = city_options
    else:
        cities = st.multiselect("المدينة:", city_options, default=city_options[:1])

# فلتر الحالة (متعدد)
with col2:
    status_options = list(df['Status'].unique())
    select_all_status = st.checkbox("✓ اختر كل الحالات", value=False, key="status_all")
    if select_all_status:
        statuses = status_options
    else:
        statuses = st.multiselect("الحالة:", status_options, default=status_options[:1])

# فلتر النوع (متعدد)
with col3:
    format_options = list(df['Format'].unique())
    select_all_format = st.checkbox("✓ اختر كل الأنواع", value=False, key="format_all")
    if select_all_format:
        formats = format_options
    else:
        formats = st.multiselect("النوع:", format_options, default=format_options[:1])

# فلتر StoreCode (متعدد)
with col4:
    storecode_options = list(df['StoreCode'].unique())
    select_all_store = st.checkbox("✓ اختر كل الصيدليات", value=False, key="store_all")
    if select_all_store:
        storecodes = storecode_options
    else:
        storecodes = st.multiselect("رمز الصيدلية:", storecode_options, default=storecode_options[:5])

# ==================== فلترة البيانات ====================
filtered_df = df.copy()

if cities:
    filtered_df = filtered_df[filtered_df['City'].isin(cities)]
if statuses:
    filtered_df = filtered_df[filtered_df['Status'].isin(statuses)]
if formats:
    filtered_df = filtered_df[filtered_df['Format'].isin(formats)]
if storecodes:
    filtered_df = filtered_df[filtered_df['StoreCode'].isin(storecodes)]

# ==================== إنشاء الخريطة ====================
st.markdown("---")
st.subheader("🗺️ الخريطة")

m = folium.Map(location=[26.4, 50.1], zoom_start=10, tiles='OpenStreetMap')

for idx, row in filtered_df.iterrows():
    folium.Marker(
        location=[row['lat'], row['lon']],
        popup=f"<b>{row['StoreCode']}</b><br>{row['City']}<br>{row['Status']}<br>{row['Format']}",
        tooltip=row['StoreCode']
    ).add_to(m)

st_folium(m, width=1200, height=600)

# ==================== الإحصائيات ====================
st.markdown("---")
st.subheader("📊 الإحصائيات")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📍 عدد الصيدليات", len(filtered_df))

with col2:
    st.metric("🏙️ المدن المختارة", len(cities) if cities else 0)

with col3:
    st.metric("✅ الحالات المختارة", len(statuses) if statuses else 0)

with col4:
    st.metric("📋 الأنواع المختارة", len(formats) if formats else 0)

# ==================== عرض الجدول مع فلتر إضافي ====================
st.markdown("---")
st.subheader("📋 تفاصيل الصيدليات")

# خيار فلتر إضافي بحث حر
search_text = st.text_input("🔎 ابحث عن نص في الجدول:", "")

if search_text:
    filtered_df = filtered_df[
        filtered_df.astype(str).apply(lambda x: x.str.contains(search_text, case=False)).any(axis=1)
    ]

# عرض الجدول
st.dataframe(filtered_df, use_container_width=True, height=500)

# خيار تحميل البيانات كـ CSV
st.download_button(
    label="📥 تحميل البيانات (CSV)",
    data=filtered_df.to_csv(index=False),
    file_name="pharmacies_filtered.csv",
    mime="text/csv"
)
