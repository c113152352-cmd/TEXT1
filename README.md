# TEXT1｜高雄市停車場查詢系統

選修課小型專題：使用 Python、Streamlit 與 Pandas 製作的高雄市停車場資料查詢工具。

## 功能

- 依處所名稱或地址搜尋停車場。
- 依行政區及最低小型車位數篩選資料。
- 顯示符合條件的處所數、車位總數與行政區數。
- 以長條圖比較各行政區的小型車位總數。
- 查看停車場清單，並下載目前篩選結果為 CSV。

## 資料來源

- 資料集名稱：停車場資訊
- 提供機關：高雄市政府交通局
- 用途：提供高雄市轄內各行政區停車場資訊。
- 官方資料集頁面：[高雄市政府資料開放平台－停車場資訊](https://data.kcg.gov.tw/DataSet/Detail/a35d8a8f-557f-4fc7-bf21-f5b2afa99f8c)
- 官方頁面標示下載格式：CSV、JSON。
- 系統使用欄位：行政區、臨時停車處所、可提供小型車停車位、地址（原始檔另含 Seq）。
- 本專案附帶 `parking_lots.csv`，是從使用者提供的下載檔複製而來；此檔案有 121 筆資料。資料會隨資料來源更新，請以官方平台及附帶檔案的實際內容為準。

## 啟動方式

請先安裝 Python 3.9 或更新版本。於本資料夾開啟終端機後執行：

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Streamlit 啟動後會在瀏覽器開啟本機頁面。停止程式可在終端機按 `Ctrl+C`。

## 專案檔案

- `app.py`：程式入口，啟動 Streamlit 畫面。
- `text1/data_loader.py`：讀取 CSV、檢查欄位並整理車位數。
- `text1/parking_service.py`：處理關鍵字、行政區、最低車位數篩選及行政區統計。
- `text1/ui.py`：顯示查詢條件、指標、圖表、清單與下載功能。
- `text1/__init__.py`：讓 Python 將 `text1` 識別為模組套件。
- `parking_lots.csv`：資料集 CSV 原始資料副本（UTF-8 with BOM）。
- `requirements.txt`：必要 Python 套件。
- `README.md`：專題說明及操作方式。

資料處理和查詢邏輯已從畫面拆開，方便之後分別修改或增加功能；目前仍維持精簡的 Python 套件結構，沒有額外資料庫或服務。
