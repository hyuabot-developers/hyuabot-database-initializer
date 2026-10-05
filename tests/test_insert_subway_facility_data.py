import pytest

from scripts.subway_station_facility import parse_subway_station_facilities


def test_empty_facility_csv_is_a_valid_seed(tmp_path):
    csv_path = tmp_path / "facility.csv"
    csv_path.write_text(
        "station_id,facility_type,sort_order,exit_no,from_place,to_place,"
        "description_korean,description_english,source\n",
        encoding="utf-8",
    )
    assert parse_subway_station_facilities(csv_path) == []


def test_facility_csv_rejects_an_unexpected_header(tmp_path):
    csv_path = tmp_path / "facility.csv"
    csv_path.write_text("station_id,facility_type\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Unexpected subway station facility CSV columns"):
        parse_subway_station_facilities(csv_path)
