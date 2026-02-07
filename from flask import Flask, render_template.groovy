from flask import Flask, render_template, request
import folium
import pandas as pd
import os

app = Flask(__name__)

# تحميل البيانات
df = pd.read_csv('pharmacies.csv')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/map')
def generate_map():
    # الحصول على معايير الفلترة من طلب المستخدم
    city = request.args.get('city', '')
    status = request.args.get('status', '')
    format_type = request.args.get('format', '')
    
    # فلترة البيانات
    filtered_df = df.copy()
    
    if city:
        filtered_df = filtered_df[filtered_df['City'] == city]
    if status:
        filtered_df = filtered_df[filtered_df['Status'] == status]
    if format_type:
        filtered_df = filtered_df[filtered_df['Format'] == format_type]
    
    # إنشاء الخريطة
    m = folium.Map(
        location=[26.4, 50.1],  # إحداثيات الدمام
        zoom_start=10,
        tiles='OpenStreetMap'
    )
    
    # إضافة العلامات على الخريطة
    for idx, row in filtered_df.iterrows():
        popup_text = f"""
        <b>Store Code:</b> {row['StoreCode']}<br>
        <b>City:</b> {row['City']}<br>
        <b>Format:</b> {row['Format']}<br>
        <b>Status:</b> {row['Status']}<br>
        <b>Area Manager:</b> {row['Area_manager']}<br>
        <b>Growth Phase:</b> {row['Growth_Phase']}
        """
        
        folium.Marker(
            location=[row['lat'], row['lon']],
            popup=folium.Popup(popup_text, max_width=300),
            tooltip=row['StoreCode'],
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)
    
    # حفظ الخريطة
    m.save('templates/map.html')
    return 'Map generated successfully'

if __name__ == '__main__':
    app.run(debug=True)
