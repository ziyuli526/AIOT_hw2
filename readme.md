網址連結 : https://aiothw2-jlmzzouezytxwjwg9wv5b7.streamlit.app/

<img width="1200" height="600" alt="image" src="https://github.com/user-attachments/assets/8bdfad0c-fc38-40c5-9a5f-2d4126e66c10" />


下拉式選單:

<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/c84df526-3ac3-4f0a-9760-3e8293adc77b" />


表格:

<img width="840" height="500" alt="image" src="https://github.com/user-attachments/assets/f4ef6eb1-45ea-40b4-bba8-750b6abea62a" />



折線圖:

<img width="460" height="460" alt="image" src="https://github.com/user-attachments/assets/1f3518bf-9c4a-4bc2-adb8-32621d20e8fb" />


氣溫資料存到資料庫:

<img width="480" height="335" alt="image" src="https://github.com/user-attachments/assets/eab8f8b6-affd-4d99-9251-009fb2b6947e" />
<img width="480" height="328" alt="image" src="https://github.com/user-attachments/assets/05729149-42b5-4bfa-87dc-a81c908dc81e" />

 json.dumps 觀察提取的資料:程式執行後顯示
 <img width="480" height="445" alt="image" src="https://github.com/user-attachments/assets/9227589a-8f20-47be-9f41-d78ed97cb839" />


 # 🌤️ 台灣一週天氣預報儀表板

本專案使用 **Streamlit** 建立互動式網頁儀表板，將中央氣象署（CWA）的一週天氣資料進行整理、分析與視覺化呈現，提供直觀且高互動性的天氣查詢平台。

---

## 📌 專案簡介

本系統整合天氣開放資料，透過資料處理與視覺化技術，實現：

* 🗺️ 台灣互動式天氣地圖
* 📊 各地區天氣統整
* 📈 溫度趨勢分析
* 📋 完整資料查詢
* 🎛️ 即時篩選控制（時間 / 地區 / 指標）

目標是將原始資料轉換為**易讀、即時、可互動的資訊平台**。

---

## 🖥️ 系統畫面展示

### 🗺️ 互動式天氣地圖

![Image](https://images.openai.com/static-rsc-4/w9FyPaxn_CbTXXlu7AOQM_dHNIOlSsvzyyPoqM_4QzRQI71BRmRTJ19AuiMvDU4xpmS_MjK8Rkn7QezPpudGrVLCcMy4YWBgPib6oMOJR2cftkf5QQjAUGf_19VvsmTYsrPbqqoQjsXR4Gq0IU1dXWWqh_YZbXYdklQ3uO0_USF0BDLUJeKMJkcRQ42frAcc?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/6gy0T8KXTmAVPJTn8KPqrgOdEZdiVstfvqKVfj2o17lhj1o0pR5qT3tx8c6jtNx-sxY2W3iCckC95UPJwLpAzTXxg4icJbWlaGFTenadB0eeKFuJWT9hK4b0JUrPRa3s_oTFeh89iQyz897GS6zDpSMHl1fklys3PQC1sc6WjEvaWJpTxdzlJPhmuxe6IHkP?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/2dcBmge6ec1XNnbGx4_GdhLxVaM4B3faug2k7S_9hiH3nvhXdJ6UZD24g6Qeq_u1xTqsJn2LeQU-ZdNKm97WxJsJZTBeD1Vv6iO75JnJIhCu9oWHg9WmXBKtHXXx2bKPlLyeayv4Igsl0FVAJGBq05EpVifwJanAsDHLf9kVdEljG_nHFJp_ZjmdmTui2DuV?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/svyDXRki4oWdqMKKmYjknV1DdTg8Bg3M9h9Som4STt5dhfOGjQeWvon5Yl68tmHYrGMq7MeG7UG_2YicUiQ_QYbQ7GYYu6Lyf2UEkwDmx6_FfyVr-9i_0Si6vUEyieEK_Xdqk2PeJZqHaO_Eadx_DBBOijFCux8xDV4dWAvnTQqXEJq5Q85_Cbcol_0JJEZQ?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/7IXYhf1wU_QI-2tcxxcUcyB1I-CHiByJhTG90ZZ64vYjwS_WRGkkc2p8HuXZ_UCxnUzcjwRrhnhpYTWuEYOiSMDMDStaefbrcgGJf2blsL1fThyG0GoUGRenzxTl4t7FfHrg4-r2jPL26QAvdxRLfrW1ebdwBzIiHreaIbnj37gDU1bq-R77GUjgS7kDApiF?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/q1dqijkfJGULzOvo5NkcYoaRC-H0aSPqJSewKEAhD8m4Dp1_U3ZtRyFFmVJz4PncSiI9xQIH69fO3A_t65bFgUQyqbwDSroDUcjuimWAv-gYRQ48uKsUUiWdYCGCELN18MaYceL5WPEJ5-66Gi1R5q3t_lAJcHBX1pBrLY6cUj7DKg4xx0LGPYMcD8BlRfQa?purpose=fullsize)

* 根據溫度或降雨機率進行顏色分層
* 滑鼠懸停顯示各縣市資訊
* 動態標記溫度與天氣狀況

---

### 📊 地區天氣統整


* 依北部 / 中部 / 南部 / 東部分類
* 顯示：

  * 天氣狀況
  * 最高 / 最低溫
  * 降雨機率

---

### 📈 溫度趨勢分析


* 各地區平均溫度變化
* 支援多時間點比較
* 視覺化氣候趨勢

---

## 🛠️ 技術架構

* **前端框架**：Streamlit
* **資料處理**：Pandas
* **資料庫**：SQLite
* **地圖視覺化**：Folium
* **資料來源**：中央氣象署（CWA）Open Data API

---

## 📂 專案結構

```text
weather-dashboard/
│
├── dashboard.py          # 主程式（Streamlit 網頁）
├── fetch_weather.py      # 抓取與整理天氣資料
├── weather_data.db       # SQLite 資料庫
├── weather_data.csv      # 原始資料備份
├── requirements.txt      # 套件需求
└── README.md
```

---

## ⚙️ 系統功能

### 🗺️ 地圖視覺化

* 溫度 / 降雨機率顏色映射
* GeoJSON 台灣地圖
* 即時資訊提示

### 📊 資料分析

* 多維度篩選（時間 / 地區 / 指標）
* 區域整合分析

### 📈 趨勢圖

* 溫度變化折線圖
* 區域平均統計

### 📋 資料展示

* 完整資料表格查詢
* 支援滾動與排序

---

## 🚀 執行方式

### 1️⃣ 安裝套件

```bash
pip install -r requirements.txt
```

---

### 2️⃣ 取得資料（選擇性）

```bash
python fetch_weather.py
```

---

### 3️⃣ 啟動網頁

```bash
streamlit run dashboard.py
```

---

## 🌐 部署方式（Streamlit Cloud）

1. 將專案上傳至 GitHub
2. 進入 Streamlit Community Cloud
3. 設定：

   * Repository：你的 repo
   * Main file：`dashboard.py`
4. 點擊 Deploy

---

## 📊 資料來源

* 台灣中央氣象署（CWA）
* 一週天氣預報資料集
* https://opendata.cwa.gov.tw/

---

## ⚠️ 注意事項

* 系統資料來自本地 `weather_data.db`
* 不會自動更新，需執行 `fetch_weather.py`
* API Key 建議使用安全方式儲存（如 Streamlit Secrets）

---

## 🔮 未來擴充

* 🔄 自動更新資料（排程）
* 📱 行動裝置優化
* 🌏 多語系支援
* 🤖 AI 天氣建議（穿搭 / 出遊）

---

## 👤 作者

黎子瑜
國立中興大學 資訊工程學系

---

## ⭐ 專案價值

本專案展示了從「資料擷取 → 清理 → 儲存 → 視覺化 → 部署」的完整流程，
具備實務應用與資料工程基礎能力，適合作為：

* 📌 課程專題
* 📌 實習作品集
* 📌 技術展示專案

---


 
 
