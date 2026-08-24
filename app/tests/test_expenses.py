from fastapi.testclient import TestClient
from typing import Any
import pytest

EXPENSE_DATA = {
    "amount": 15.50,
    "category": "Courses",
    "description": "Pain et lait",
}

def create_expense(client: TestClient, data: dict[str, Any] = EXPENSE_DATA,) -> dict[str, Any]:
    response = client.post("/expenses/", json=data)

    assert response.status_code == 201

    return response.json()

def test_health_check(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_expense(client: TestClient) -> None:
    response = client.post("/expenses/", json=EXPENSE_DATA)
    assert response.status_code == 201

    expense = response.json()
    assert expense["amount"] == 15.50
    assert expense["category"] == "Courses"
    assert expense["description"] == "Pain et lait"


def test_list_all_expenses(client: TestClient) -> None:
    created_expense = create_expense(client)

    response = client.get("/expenses/")
    assert response.status_code == 200

    expenses = response.json()
    assert len(expenses) == 1
    assert expenses[0]["id"] == created_expense["id"]

def test_list_all_expenses_by_category(client: TestClient) -> None:
    created_expense = create_expense(client, {
        "amount": 50.0,
        "category": "Loisirs",
        "description": "Cinéma",
    })

    response = client.get("/expenses/", params={"category": "Loisirs"},)
    assert response.status_code == 200

    expenses = response.json()
    assert len(expenses) == 1
    assert expenses[0]["id"] == created_expense["id"]
    assert expenses[0]["category"] == "Loisirs"


def test_get_expense(client: TestClient) -> None:
    created_expense = create_expense(client)
    expense_id = created_expense["id"]

    response = client.get(f"/expenses/{expense_id}")
    assert response.status_code == 200

    expense = response.json()

    assert expense["id"] == expense_id
    assert expense["amount"] == 15.50
    assert expense["category"] == "Courses"

def test_get_expense_not_found(client: TestClient) -> None:
    expense_id = 999999
    reponse = client.get(f"/expenses/{expense_id}")
    assert reponse.status_code == 404

def test_update_expense(client: TestClient) -> None:
    created_expense = create_expense(client)
    expense_id = created_expense["id"]

    updated_data = {
        "amount": 10.50,
        "category": "Courses",
        "description": "lait",
    }
    response = client.put(f"/expenses/{expense_id}", json=updated_data)
    assert response.status_code == 200

    expense = response.json()
    assert expense["id"] == expense_id
    assert expense["amount"] == 10.50
    assert expense["description"] == "lait"

def test_update_expense_not_found(client: TestClient) -> None:
    expense_id = 999999
    updated_data = {
        "amount": 10.50,
        "category": "Courses",
        "description": "lait",
    }
    response = client.put(f"/expenses/{expense_id}", json=updated_data)
    assert response.status_code == 404

def test_delete_expense(client: TestClient) -> None:
    created_expense = create_expense(client)
    expense_id = created_expense["id"]

    reponse = client.delete(f"/expenses/{expense_id}")
    assert reponse.status_code == 204

def test_delete_expense_not_found(client: TestClient) -> None:
    expense_id = 999999
    response = client.delete(f"/expenses/{expense_id}")
    assert response.status_code == 404

@pytest.mark.parametrize("invalid_fields", [
    {"amount": -13},
    {"amount": 0},
    {"category": "a"},
    {"description": ""},
    {"amount": -13, "category": "a"},         
    {"amount": 0, "description": ""},
],
    ids=[
        "negative_amount",
        "zero_amount",
        "category_too_short",
        "empty_description",
        "negative_amount_and_short_category",
        "zero_amount_and_empty_description",
    ],)
def test_create_expense_invalid_data(client: TestClient, invalid_fields) -> None:
    data = {**EXPENSE_DATA, **invalid_fields}
    response = client.post("/expenses/", json=data)
    assert response.status_code == 422
