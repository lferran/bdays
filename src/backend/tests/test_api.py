from bdays.api import BirthdaySchema
import json


def test_create_and_get_birthday(client):
    payload = {
        "name": "John Doe",
        "year": 1991,
        "month": 11,
        "day": 12,
    }
    response = client.post("/bday", data=json.dumps(payload))
    assert response.status_code == 200
    resp_body = response.json()

    bday_id = resp_body["id"]
    assert bday_id
    assert resp_body["name"] == payload["name"]
    assert resp_body["year"] == payload["year"]
    assert resp_body["day"] == payload["day"]
    assert resp_body["month"] == payload["month"]

    # now get it
    response = client.get(f"bday/{bday_id}")
    assert response.status_code == 200
    resp_body = response.json()
    assert resp_body["id"] == bday_id
    assert resp_body["name"] == payload["name"]
    assert resp_body["year"] == payload["year"]
    assert resp_body["day"] == payload["day"]
    assert resp_body["month"] == payload["month"]


def test_list_birthdays(client):
    to_create = [
        BirthdaySchema(name=f"Foo{i}", year=1991, day=12, month=12) for i in range(20)
    ]
    for bday in to_create:
        response = client.post("/bday", data=json.dumps(bday.dict()))
        assert response.status_code == 200

    # now get the list of bdays
    response = client.get("/bdays/list")

    assert response.status_code == 200
    resp_body = response.json()
    assert isinstance(resp_body, list)
    assert len(resp_body) == 10

    # Check sorted by id
    assert [b["id"] for b in resp_body] == list(range(1, 11))

    # Check pagination
    offset = None
    total_bdays = []
    while True:
        payload = {
            "limit": 2
        }
        if offset is not None:
            payload["offset"] = offset

        response = client.get("/bdays/list", data=json.dumps(payload))
        resp_content = response.json()
        if len(resp_content) == 0:
            break
        else:
            total_bdays.extend(resp_content)
            offset = resp_content[-1]["id"]
    assert len(total_bdays) == 20
    assert [b["id"] for b in total_bdays] == list(range(1, 21))


def test_search_birthdays(client):
    to_create = BirthdaySchema(name="John", surname="Doe", year=1991, day=12, month=12)
    response = client.post("/bday", data=json.dumps(to_create.dict()))
    assert response.status_code == 200

    # now search bdays
    for term in ("john", "doe", "john doe", "JoHn", "DoE"):
        response = client.get(f"/bdays/search?term={term}")
        assert response.status_code == 200
        resp_body = response.json()
        assert isinstance(resp_body, list)
        assert len(resp_body) == 1
