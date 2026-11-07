"""停車場資料的載入與基本整理。"""

from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = [
    "行政區",
    "臨時停車處所",
    "可提供小型車停車位",
    "地址",
]


def load_parking_data(file_path: Path) -> pd.DataFrame:
    """讀取 CSV，確認必要欄位存在並將車位數轉為整數。"""
    data = pd.read_csv(file_path, encoding="utf-8-sig")
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in data.columns]
    if missing_columns:
        raise ValueError(f"資料檔缺少必要欄位：{', '.join(missing_columns)}")

    data["可提供小型車停車位"] = pd.to_numeric(
        data["可提供小型車停車位"], errors="coerce"
    ).fillna(0).astype(int)
    return data
