import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

st.set_page_config(layout="wide")
st.title("🗺️ Pharmacy Locations Map")

# اقرأ الداتا
df = pd.read_csv("pharmacies.csv")

# ===== فلاتر =====
col1, col2, col3 = st.columns(3)
with col1:
    head_list = ["All"] + sorted(df["HEAD"].dropna().unique().tolist())
    selected_head = st.selectbox("HEAD", head_list)
with col2:
    area_list = ["All"] + sorted(df["Area_manager"].dropna().unique().tolist())
    selected_area = st.selectbox("Area Manager", area_list)
with col3:
    supervisor_list = ["All"] + sorted(df["Supervisor"].dropna().unique().tolist())
    selected_supervisor = st.selectbox("Supervisor", supervisor_list)

col4, col5, col6 = st.columns(3)
with col4:
    district_list = ["All"] + sorted(df["District"].dropna().unique().tolist())
    selected_district = st.selectbox("District", district_list)
with col5:
    main_city_list = ["All"] + sorted(df["Main_City"].dropna().unique().tolist())
    selected_main_city = st.selectbox("Main City", main_city_list)
with col6:
    city_list = ["All"] + sorted(df["City"].dropna().unique().tolist())
    selected_city = st.selectbox("City", city_list)

col7, col8, col9 = st.columns(3)
with col7:
    format_list = ["All"] + sorted(df["Format"].dropna().unique().tolist())
    selected_format = st.selectbox("Format", format_list)
with col8:
    growth_list = ["All"] + sorted(df["Growth_Phase"].dropna().unique().tolist())
    selected_growth = st.selectbox("Growth Phase", growth_list)
with col9:
    status_list = ["All"] + sorted(df["Status"].dropna().unique().tolist())
    selected_status = st.selectbox("Status", status_list)

# ===== تطبيق الفلاتر =====
filtered_df = df.copy()
filters = {
    "HEAD": selected_head,
    "Area_manager": selected_area,
    "Supervisor": selected_supervisor,
    "District": selected_district,
    "Main_City": selected_main_city,
    "City": selected_city,
    "Format": selected_format,
    "Growth_Phase": selected_growth,
    "Status": selected_status
}
for col, val in filters.items():
    if val != "All":
        filtered_df = filtered_df[filtered_df[col] == val]

st.markdown(f"**📍 Locations found: {len(filtered_df)}**")

# ===== الخريطة =====
m = folium.Map(location=[23.8859, 45.0792], zoom_start=6)
cluster = MarkerCluster().add_to(m)

for _, row in filtered_df.iterrows():
    popup_html = f"""
    <b>Store:</b> {row['StoreCode']}<br>
    <b>HEAD:</b> {row['HEAD']}<br>
    <b>Area Manager:</b> {row['Area_manager']}<br>
    <b>Supervisor:</b> {row['Supervisor']}<br>
    <b>District:</b> {row['District']}<br>
    <b>Main City:</b> {row['Main_City']}<br>
    <b>City:</b> {row['City']}<br>
    <b>Format:</b> {row['Format']}<br>
    <b>Growth Phase:</b> {row['Growth_Phase']}<br>
    <b>Status:</b> {row['Status']}
    """

    folium.Marker(
        location=[row["lat"], row["lon"]],
        popup=popup_html,
        tooltip=row["StoreCode"]
    ).add_to(cluster)

st_folium(m, width=1200, height=600)
