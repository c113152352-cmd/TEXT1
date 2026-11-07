"""停車場搜尋、篩選與統計邏輯。"""

import pandas as pd


DISTRICT_COLUMN = "行政區"
NAME_COLUMN = "臨時停車處所"
SPOTS_COLUMN = "可提供小型車停車位"
ADDRESS_COLUMN = "地址"
DISPLAY_COLUMNS = [DISTRICT_COLUMN, NAME_COLUMN, SPOTS_COLUMN, ADDRESS_COLUMN]


def filter_parking_data(
    data: pd.DataFrame,
    keyword: str = "",
    districts: list[str] | None = None,
    min_spots: int = 0,
) -> pd.DataFrame:
    """依行政區、最低車位數及處所/地址關鍵字篩選。"""
    filtered = data.copy()
    if districts is not None:
        filtered = filtered[filtered[DISTRICT_COLUMN].isin(districts)]

    filtered = filtered[filtered[SPOTS_COLUMN] >= min_spots]
    search_text = keyword.strip()
    if search_text:
        matches_name = filtered[NAME_COLUMN].fillna("").str.contains(
            search_text, case=False, regex=False
        )
        matches_address = filtered[ADDRESS_COLUMN].fillna("").str.contains(
            search_text, case=False, regex=False
        )
        filtered = filtered[matches_name | matches_address]

    return filtered


def get_district_capacity(data: pd.DataFrame) -> pd.Series:
    """計算每個行政區符合條件的車位總數，並由多至少排序。"""
    return data.groupby(DISTRICT_COLUMN)[SPOTS_COLUMN].sum().sort_values(ascending=False)
