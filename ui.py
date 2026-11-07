"""Streamlit 畫面與互動控制。"""

from pathlib import Path

import streamlit as st

from text1.data_loader import load_parking_data
from text1.parking_service import (
    DISPLAY_COLUMNS,
    DISTRICT_COLUMN,
    SPOTS_COLUMN,
    filter_parking_data,
    get_district_capacity,
)


DATA_FILE = Path(__file__).resolve().parent.parent / "parking_lots.csv"
DATASET_URL = "https://data.kcg.gov.tw/DataSet/Detail/a35d8a8f-557f-4fc7-bf21-f5b2afa99f8c"


@st.cache_data
def _get_parking_data(file_path: Path):
    return load_parking_data(file_path)


def run_app() -> None:
    """建立 Streamlit 查詢頁面。"""
    st.set_page_config(page_title="TEXT1｜高雄停車場查詢", page_icon="🅿️", layout="wide")
    st.title("🅿️ TEXT1｜高雄市停車場查詢")
    st.caption("依高雄市政府公開資料，搜尋停車處所並比較各行政區的車位數。")

    if not DATA_FILE.exists():
        st.error("找不到 parking_lots.csv，請將資料檔放在 app.py 同一個資料夾。")
        st.stop()

    try:
        data = _get_parking_data(DATA_FILE)
    except (OSError, ValueError) as error:
        st.error(f"讀取資料時發生問題：{error}")
        st.stop()

    with st.sidebar:
        st.header("查詢條件")
        keyword = st.text_input("關鍵字（處所或地址）", placeholder="例如：國中、三民路")
        districts = sorted(data[DISTRICT_COLUMN].dropna().unique().tolist())
        selected_districts = st.multiselect("行政區", districts, default=districts)
        min_spots = st.number_input(
            "最少小型車位數",
            min_value=0,
            max_value=int(data[SPOTS_COLUMN].max()),
            value=0,
        )

    filtered = filter_parking_data(
        data,
        keyword=keyword,
        districts=selected_districts,
        min_spots=int(min_spots),
    )

    left, middle, right = st.columns(3)
    left.metric("符合條件的停車處所", f"{len(filtered)} 處")
    middle.metric("符合條件的車位總數", f"{filtered[SPOTS_COLUMN].sum():,} 個")
    right.metric("涵蓋行政區", f"{filtered[DISTRICT_COLUMN].nunique()} 區")

    st.subheader("各行政區小型車位總數")
    if filtered.empty:
        st.info("沒有符合條件的資料，請調整左側篩選條件。")
    else:
        st.bar_chart(get_district_capacity(filtered))

    st.subheader("停車處所清單")
    st.dataframe(filtered[DISPLAY_COLUMNS], width="stretch", hide_index=True)
    st.download_button(
        "下載目前篩選結果（CSV）",
        data=filtered[DISPLAY_COLUMNS].to_csv(index=False, encoding="utf-8-sig"),
        file_name="kaohsiung_parking_filtered.csv",
        mime="text/csv",
    )

    with st.expander("資料來源與欄位說明"):
        st.markdown(
            f"資料集：**停車場資訊**（高雄市政府交通局）  \n"
            f"來源：[高雄市政府資料開放平台]({DATASET_URL})"
        )
        st.write(
            "資料提供高雄市各行政區停車場資訊；本系統使用行政區、臨時停車處所、"
            "可提供小型車停車位及地址欄位。"
        )
        st.caption(f"目前資料檔共 {len(data)} 筆；資料內容以專案附帶的下載檔為準。")
