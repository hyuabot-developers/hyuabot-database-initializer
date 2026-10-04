from scripts.shuttle import commute_route_seed_rows


def test_remaining_commute_routes_have_empty_descriptions():
    rows = commute_route_seed_rows()
    assert {row["route_name"] for row in rows} == {"1", "2", "3", "A", "B", "C"}
    assert all(row["route_description_korean"] == "" for row in rows)
    assert all(row["route_description_english"] == "" for row in rows)
