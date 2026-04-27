import streamlit as st
import pandas as pd
import requests
import json
import folium
from streamlit_folium import st_folium
from datetime import datetime

# ─── Page Config ────────────────────────────────────────────────
st.set_page_config(
    page_title="台灣一週天氣預報",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ─────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;500;700&display=swap');

* { font-family: 'Noto Sans TC', sans-serif; }

.main { background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%); }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
}

.weather-card {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 16px;
    padding: 20px;
    margin: 8px 0;
    transition: transform 0.2s, box-shadow 0.2s;
}
.weather-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}

.metric-value {
    font-size: 2.4rem;
    font-weight: 700;
    background: linear-gradient(135deg, #f093fb, #f5576c);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.metric-value.temp-high {
    background: linear-gradient(135deg, #ff6b6b, #ee5a24);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.metric-value.temp-low {
    background: linear-gradient(135deg, #74b9ff, #0984e3);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.metric-value.rain {
    background: linear-gradient(135deg, #a29bfe, #6c5ce7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.metric-label {
    font-size: 0.9rem;
    color: rgba(255,255,255,0.6);
    margin-bottom: 4px;
}

.region-header {
    font-size: 1.6rem;
    font-weight: 700;
    color: #fff;
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 2px solid rgba(255,255,255,0.15);
}

.header-container {
    text-align: center;
    padding: 20px 0 10px 0;
}
.header-container h1 {
    font-size: 2.2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 4px;
}
.header-container p {
    color: rgba(255,255,255,0.5);
    font-size: 0.95rem;
}

.weather-icon { font-size: 2rem; }

.time-badge {
    display: inline-block;
    background: rgba(102, 126, 234, 0.25);
    color: #a8b5ff;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.78rem;
    margin: 2px;
}
</style>
""", unsafe_allow_html=True)

# ─── Constants ──────────────────────────────────────────────────
API_KEY = 'CWA-77A0C3C8-E800-4830-996A-190BE56C4EF1'
GEOJSON_URL = 'https://raw.githubusercontent.com/g0v/twgeojson/master/json/twCounty2010.geo.json'

# Region grouping for Taiwan weather regions
REGION_MAP = {
    '北部': ['臺北市', '新北市', '基隆市', '桃園市', '新竹市', '新竹縣'],
    '中部': ['臺中市', '苗栗縣', '彰化縣', '南投縣', '雲林縣'],
    '南部': ['臺南市', '高雄市', '嘉義市', '嘉義縣', '屏東縣'],
    '東北部': ['宜蘭縣'],
    '東部': ['花蓮縣'],
    '東南部': ['臺東縣'],
}

# County center coordinates (lat, lon) for map markers
COUNTY_COORDS = {
    '臺北市': (25.033, 121.565), '新北市': (25.012, 121.465),
    '基隆市': (25.128, 121.739), '桃園市': (24.994, 121.301),
    '新竹市': (24.804, 120.969), '新竹縣': (24.839, 121.004),
    '宜蘭縣': (24.702, 121.738), '臺中市': (24.148, 120.674),
    '苗栗縣': (24.560, 120.821), '彰化縣': (24.052, 120.516),
    '南投縣': (23.961, 120.685), '雲林縣': (23.709, 120.432),
    '臺南市': (22.999, 120.227), '高雄市': (22.627, 120.301),
    '嘉義市': (23.480, 120.449), '嘉義縣': (23.452, 120.255),
    '屏東縣': (22.552, 120.549), '花蓮縣': (23.991, 121.601),
    '臺東縣': (22.757, 121.144), '澎湖縣': (23.571, 119.579),
    '金門縣': (24.449, 118.377), '連江縣': (26.160, 119.950),
}

# Name mapping (GeoJSON uses 台 while API uses 臺)
NAME_MAP = {
    '台北市': '臺北市', '台中市': '臺中市', '台南市': '臺南市',
    '台東縣': '臺東縣',
}

def get_weather_icon(desc):
    """Return emoji based on weather description."""
    if not desc:
        return '🌤️'
    if '雨' in desc and '雷' in desc:
        return '⛈️'
    if '雨' in desc:
        return '🌧️'
    if '陰' in desc:
        return '☁️'
    if '雲' in desc:
        return '⛅'
    if '晴' in desc:
        return '☀️'
    if '霧' in desc:
        return '🌫️'
    return '🌤️'

def temp_to_color(temp, min_t=10, max_t=38):
    """Map temperature to a color for the map."""
    try:
        t = float(temp)
    except (ValueError, TypeError):
        return '#888888'
    ratio = max(0, min(1, (t - min_t) / (max_t - min_t)))
    if ratio < 0.25:
        r, g, b = 66, 133, 244   # cool blue
    elif ratio < 0.5:
        r, g, b = 52, 211, 153   # green
    elif ratio < 0.75:
        r, g, b = 251, 191, 36   # warm yellow
    else:
        r, g, b = 239, 68, 68    # hot red
    return f'#{r:02x}{g:02x}{b:02x}'

# ─── Data Fetching ──────────────────────────────────────────────
import sqlite3

@st.cache_data(ttl=1800)
def fetch_weather():
    """Fetch one-week weather forecast from SQLite Database."""
    try:
        conn = sqlite3.connect('weather_data.db')
        query = '''
            SELECT 
                location AS Location,
                element AS Element,
                start_time AS StartTime,
                end_time AS EndTime,
                value AS Value
            FROM weather_forecast
        '''
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        # We no longer have the raw JSON from the API, so we provide a placeholder
        raw_json = '{"source": "SQLite DB", "message": "Data loaded from local database weather_data.db"}'
        return df, raw_json
    except Exception as e:
        st.error(f"無法讀取資料庫: {e}")
        return pd.DataFrame(), "{}"

@st.cache_data(ttl=86400)
def fetch_geojson():
    """Fetch Taiwan county GeoJSON."""
    resp = requests.get(GEOJSON_URL)
    return resp.json()

# ─── Main App ───────────────────────────────────────────────────
def main():
    # Header
    st.markdown("""
    <div class="header-container">
        <h1>🌤️ 台灣一週天氣預報儀表板</h1>
        <p>資料來源：中央氣象署 CWA Open Data API</p>
    </div>
    """, unsafe_allow_html=True)

    # Fetch data
    with st.spinner('正在從中央氣象署取得資料...'):
        df, raw_json = fetch_weather()
        geojson = fetch_geojson()

    # ── Sidebar ──────────────────────────────────────────────
    with st.sidebar:
        st.markdown("### ⚙️ 控制面板")

        # Time period selection
        time_options = sorted(df['StartTime'].unique())
        time_labels = []
        for t in time_options:
            try:
                dt = datetime.fromisoformat(t)
                time_labels.append(dt.strftime('%m/%d %H:%M'))
            except:
                time_labels.append(t)

        selected_idx = st.select_slider(
            "📅 選擇時間段",
            options=list(range(len(time_options))),
            format_func=lambda i: time_labels[i] if i < len(time_labels) else '',
            value=0,
        )
        selected_time = time_options[selected_idx]

        st.markdown("---")

        # Region filter
        region_choice = st.multiselect(
            "🗺️ 選擇地區",
            options=list(REGION_MAP.keys()),
            default=list(REGION_MAP.keys()),
        )

        st.markdown("---")

        # Display element
        display_element = st.radio(
            "🌡️ 地圖顯示指標",
            options=['最高溫度', '最低溫度', '12小時降雨機率'],
            index=0,
        )

        st.markdown("---")

        # Show JSON toggle
        show_json = st.checkbox("📄 顯示原始 JSON", value=False)

    # Filter data by selected time
    df_time = df[df['StartTime'] == selected_time]

    # Get selected counties
    selected_counties = []
    for region in region_choice:
        selected_counties.extend(REGION_MAP.get(region, []))

    # ── Map (full width) ─────────────────────────────────────
    st.markdown("#### 🗺️ 互動式台灣天氣地圖")

    m = folium.Map(
        location=[23.7, 120.9],
        zoom_start=7,
        tiles='CartoDB dark_matter',
        control_scale=True,
    )

    # Build lookup for current values per county
    county_values = {}
    for _, row in df_time[df_time['Element'] == display_element].iterrows():
        county_values[row['Location']] = row['Value']

    county_wx = {}
    for _, row in df_time[df_time['Element'] == '天氣現象'].iterrows():
        county_wx[row['Location']] = row['Value']

    county_max = {}
    for _, row in df_time[df_time['Element'] == '最高溫度'].iterrows():
        county_max[row['Location']] = row['Value']

    county_min = {}
    for _, row in df_time[df_time['Element'] == '最低溫度'].iterrows():
        county_min[row['Location']] = row['Value']

    county_pop = {}
    for _, row in df_time[df_time['Element'] == '12小時降雨機率'].iterrows():
        county_pop[row['Location']] = row['Value']

    # Style function for choropleth
    def style_function(feature):
        county_name = feature['properties'].get('COUNTYNAME', '')
        mapped = NAME_MAP.get(county_name, county_name)
        val = county_values.get(mapped, None)
        if display_element in ['最高溫度', '最低溫度']:
            color = temp_to_color(val)
        else:
            try:
                pop = float(val)
                if pop < 30:
                    color = '#34d399'
                elif pop < 60:
                    color = '#fbbf24'
                else:
                    color = '#ef4444'
            except:
                color = '#888888'
        return {
            'fillColor': color,
            'color': 'rgba(255,255,255,0.3)',
            'weight': 1,
            'fillOpacity': 0.6,
        }

    def highlight_function(feature):
        return {
            'fillOpacity': 0.85,
            'weight': 3,
            'color': '#fff',
        }

    folium.GeoJson(
        geojson,
        style_function=style_function,
        highlight_function=highlight_function,
        tooltip=folium.GeoJsonTooltip(
            fields=['COUNTYNAME'],
            aliases=['縣市：'],
            style='background-color: rgba(0,0,0,0.8); color: white; border-radius: 8px; padding: 8px;',
        ),
    ).add_to(m)

    # Add text-label markers for selected counties
    for county in selected_counties:
        if county in COUNTY_COORDS:
            lat, lon = COUNTY_COORDS[county]
            max_t = county_max.get(county, '-')
            min_t = county_min.get(county, '-')
            pop = county_pop.get(county, '-')
            wx = county_wx.get(county, '')
            icon_emoji = get_weather_icon(wx)

            popup_html = f"""
            <div style="font-family:'Noto Sans TC',sans-serif;min-width:180px;padding:8px;">
                <h4 style="margin:0 0 8px 0;color:#333;border-bottom:2px solid #667eea;padding-bottom:4px;">{icon_emoji} {county}</h4>
                <table style="width:100%;font-size:13px;">
                    <tr><td>🌡️ 最高溫</td><td style="text-align:right;color:#e74c3c;font-weight:bold;">{max_t}°C</td></tr>
                    <tr><td>🌡️ 最低溫</td><td style="text-align:right;color:#3498db;font-weight:bold;">{min_t}°C</td></tr>
                    <tr><td>🌧️ 降雨機率</td><td style="text-align:right;color:#8e44ad;font-weight:bold;">{pop}%</td></tr>
                    <tr><td>🌤️ 天氣</td><td style="text-align:right;">{wx}</td></tr>
                </table>
            </div>"""

            try:
                t_val = float(max_t)
                temp_color = '#ff6b6b' if t_val >= 33 else '#ffa502' if t_val >= 28 else '#2ed573' if t_val >= 22 else '#70a1ff'
            except:
                temp_color = '#dfe6e9'

            label_html = f"""
            <div style="font-family:'Noto Sans TC',Arial,sans-serif;font-size:11px;font-weight:700;color:#fff;text-align:center;text-shadow:0 1px 4px rgba(0,0,0,0.9),0 0 8px rgba(0,0,0,0.6);line-height:1.35;white-space:nowrap;pointer-events:auto;">
                <div>{county}</div>
                <div style="color:{temp_color};font-size:13px;">{max_t}°</div>
            </div>"""

            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(popup_html, max_width=250),
                icon=folium.DivIcon(html=label_html, icon_size=(80, 36), icon_anchor=(40, 18), class_name='county-label'),
            ).add_to(m)

    st_folium(m, width=None, height=500, returned_objects=[])

    # Legend
    if display_element in ['最高溫度', '最低溫度']:
        st.markdown("""
        <div style="display:flex;align-items:center;gap:8px;margin-top:8px;justify-content:center;">
            <span style="color:rgba(255,255,255,0.5);font-size:0.8rem;">溫度圖例：</span>
            <span style="background:#4285f4;width:20px;height:12px;border-radius:3px;display:inline-block;"></span><span style="color:#aaa;font-size:0.75rem;">≤17°C</span>
            <span style="background:#34d399;width:20px;height:12px;border-radius:3px;display:inline-block;"></span><span style="color:#aaa;font-size:0.75rem;">18-24°C</span>
            <span style="background:#fbbf24;width:20px;height:12px;border-radius:3px;display:inline-block;"></span><span style="color:#aaa;font-size:0.75rem;">25-31°C</span>
            <span style="background:#ef4444;width:20px;height:12px;border-radius:3px;display:inline-block;"></span><span style="color:#aaa;font-size:0.75rem;">≥32°C</span>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="display:flex;align-items:center;gap:8px;margin-top:8px;justify-content:center;">
            <span style="color:rgba(255,255,255,0.5);font-size:0.8rem;">降雨機率圖例：</span>
            <span style="background:#34d399;width:20px;height:12px;border-radius:3px;display:inline-block;"></span><span style="color:#aaa;font-size:0.75rem;">&lt;30%</span>
            <span style="background:#fbbf24;width:20px;height:12px;border-radius:3px;display:inline-block;"></span><span style="color:#aaa;font-size:0.75rem;">30-60%</span>
            <span style="background:#ef4444;width:20px;height:12px;border-radius:3px;display:inline-block;"></span><span style="color:#aaa;font-size:0.75rem;">&gt;60%</span>
        </div>""", unsafe_allow_html=True)

    # ── Region Tables: 3-col × 2-row grid ────────────────────
    st.markdown("---")
    st.markdown("#### 📊 各地區天氣概況")
    try:
        dt_display = datetime.fromisoformat(selected_time)
        st.markdown(f'<div class="time-badge">🕐 {dt_display.strftime("%Y/%m/%d %H:%M")}</div>', unsafe_allow_html=True)
    except:
        pass

    import streamlit.components.v1 as components

    def render_region_table(region_name, counties):
        """Render a single region table using components.html."""
        rows_html = ""
        for county in counties:
            wx = county_wx.get(county, '-')
            max_t = county_max.get(county, '-')
            min_t = county_min.get(county, '-')
            pop = county_pop.get(county, '-')
            icon = get_weather_icon(wx)
            rows_html += f'''<tr style="border-bottom:1px solid rgba(255,255,255,0.06);">
                <td style="padding:8px 10px;font-weight:700;font-size:0.95rem;color:#fff;white-space:nowrap;"><span style="font-size:1.2rem;vertical-align:middle;margin-right:4px;">{icon}</span>{county}</td>
                <td style="padding:8px 6px;color:rgba(255,255,255,0.6);font-size:0.8rem;">{wx}</td>
                <td style="padding:8px 6px;text-align:center;font-weight:700;font-size:1rem;color:#ff6b6b;">{max_t}°</td>
                <td style="padding:8px 6px;text-align:center;font-weight:700;font-size:1rem;color:#74b9ff;">{min_t}°</td>
                <td style="padding:8px 6px;text-align:center;font-weight:700;font-size:1rem;color:#a29bfe;">{pop}%</td>
            </tr>'''

        table_height = max(150, 90 + len(counties) * 46)
        components.html(f"""<html><head>
            <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;700&display=swap" rel="stylesheet">
            </head><body style="margin:0;padding:0;background:transparent;font-family:'Noto Sans TC',Arial,sans-serif;">
            <div style="background:rgba(30,30,60,0.95);border-radius:10px;border:1px solid rgba(255,255,255,0.1);overflow:hidden;">
                <div style="background:rgba(102,126,234,0.2);padding:8px 12px;font-size:0.95rem;font-weight:700;color:#a8b5ff;">📍 {region_name}地區</div>
                <table style="width:100%;border-collapse:collapse;">
                    <thead><tr style="background:rgba(255,255,255,0.06);">
                        <th style="padding:6px 10px;text-align:left;color:rgba(255,255,255,0.4);font-size:0.72rem;font-weight:500;">地名</th>
                        <th style="padding:6px 6px;text-align:left;color:rgba(255,255,255,0.4);font-size:0.72rem;font-weight:500;">天氣</th>
                        <th style="padding:6px 6px;text-align:center;color:rgba(255,255,255,0.4);font-size:0.72rem;font-weight:500;">🔺最高</th>
                        <th style="padding:6px 6px;text-align:center;color:rgba(255,255,255,0.4);font-size:0.72rem;font-weight:500;">🔻最低</th>
                        <th style="padding:6px 6px;text-align:center;color:rgba(255,255,255,0.4);font-size:0.72rem;font-weight:500;">🌧降雨</th>
                    </tr></thead>
                    <tbody>{rows_html}</tbody>
                </table>
            </div></body></html>""", height=table_height)

    # Row 1: 北部 | 中部 | 南部
    active_regions = [r for r in ['北部', '中部', '南部'] if r in region_choice]
    if active_regions:
        cols = st.columns(len(active_regions))
        for i, region_name in enumerate(active_regions):
            with cols[i]:
                render_region_table(region_name, REGION_MAP[region_name])

    # Row 2: 東北部 | 東部 | 東南部
    active_regions2 = [r for r in ['東北部', '東部', '東南部'] if r in region_choice]
    if active_regions2:
        cols2 = st.columns(len(active_regions2))
        for i, region_name in enumerate(active_regions2):
            with cols2[i]:
                render_region_table(region_name, REGION_MAP[region_name])

    # ── Raw JSON ─────────────────────────────────────────────
    if show_json:
        st.markdown("---")
        st.markdown("#### 📄 原始 JSON 輸出 (json.dumps)")
        st.code(raw_json[:5000] + "\n... (truncated)", language='json')

    # ── Data Table ───────────────────────────────────────────
    st.markdown("---")
    st.markdown("#### 📋 完整資料表")
    df_display = df_time[df_time['Location'].isin(selected_counties)]
    st.dataframe(
        df_display,
        use_container_width=True,
        height=400,
    )

    # ── Line Charts ──────────────────────────────────────────
    st.markdown("---")
    st.markdown("#### 📈 各地區溫度趨勢折線圖")

    # Prepare data for charts
    df_chart = df[df['Element'].isin(['最高溫度', '最低溫度'])].copy()
    # Ensure proper datetime format (remove timezone info for plotting if needed, or keep it)
    df_chart['StartTime'] = pd.to_datetime(df_chart['StartTime'], errors='coerce')
    df_chart['Value'] = pd.to_numeric(df_chart['Value'], errors='coerce')
    
    # Map county to region
    county_to_region = {}
    for r, c_list in REGION_MAP.items():
        for c in c_list:
            county_to_region[c] = r
            
    df_chart['Region'] = df_chart['Location'].map(county_to_region)
    df_chart = df_chart.dropna(subset=['Region', 'Value', 'StartTime'])
    
    # Aggregate to get average temperature per region
    df_agg = df_chart.groupby(['Region', 'StartTime', 'Element'])['Value'].mean().reset_index()
    
    all_active_regions = [r for r in ['北部', '中部', '南部', '東北部', '東部', '東南部'] if r in region_choice]
    
    if all_active_regions:
        for i in range(0, len(all_active_regions), 2):
            cols_chart = st.columns(2)
            for j in range(2):
                if i + j < len(all_active_regions):
                    reg_name = all_active_regions[i + j]
                    with cols_chart[j]:
                        st.markdown(f"**{reg_name}地區 平均溫度**")
                        df_r = df_agg[df_agg['Region'] == reg_name]
                        if not df_r.empty:
                            df_pivot = df_r.pivot(index='StartTime', columns='Element', values='Value')
                            # Ensure specific column order for colors
                            if '最高溫度' in df_pivot.columns and '最低溫度' in df_pivot.columns:
                                df_pivot = df_pivot[['最高溫度', '最低溫度']]
                                colors = ["#ff6b6b", "#74b9ff"]
                            elif '最高溫度' in df_pivot.columns:
                                df_pivot = df_pivot[['最高溫度']]
                                colors = ["#ff6b6b"]
                            elif '最低溫度' in df_pivot.columns:
                                df_pivot = df_pivot[['最低溫度']]
                                colors = ["#74b9ff"]
                            else:
                                colors = None
                                
                            st.line_chart(df_pivot, color=colors)

if __name__ == '__main__':
    main()