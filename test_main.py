
from fastapi.testclient import TestClient
import pytest


from main import api, books

client = TestClient(api)

@pytest.fixture(autouse=True)
def clear_books():
    """
    Ensure test isolation: clear the shared books list before each test.
    """
    books.clear()
    yield
    books.clear()

def test_get_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json() == {"Message": "Welcome to the Book Management System"}

def test_get_books_empty():
    r = client.get("/book")
    assert r.status_code == 200
    assert r.json() == []

def test_add_book():
    payload = {"id": 1, "name": "Book One", "description": "Desc", "isAvailable": True}
    r = client.post("/book", json=payload)
    assert r.status_code == 200
    assert r.json() == [payload]

def test_add_book_validation_error():
    
    payload = {"id": 2, "description": "No name", "isAvailable": False}
    r = client.post("/book", json=payload)
    assert r.status_code == 422

def test_update_book_success():
    payload = {"id": 1, "name": "Book One", "description": "Desc", "isAvailable": True}
    client.post("/book", json=payload)

    updated = {"id": 1, "name": "Updated", "description": "New desc", "isAvailable": False}
    r = client.put("/book/1", json=updated)
    assert r.status_code == 200
    assert r.json() == updated

    r2 = client.get("/book")
    assert r2.status_code == 200
    assert r2.json() == [updated]

def test_update_book_not_found():
    updated = {"id": 999, "name": "Nope", "description": "None", "isAvailable": False}
    r = client.put("/book/999", json=updated)
    assert r.status_code == 200
    assert r.json() == {"error": "Book Not Found"}

def test_delete_book_success():
    payload = {"id": 1, "name": "Book One", "description": "Desc", "isAvailable": True}
    client.post("/book", json=payload)

    r = client.delete("/book/1")
    assert r.status_code == 200
    assert r.json() == payload
    
    r2 = client.get("/book")
    assert r2.status_code == 200
    assert r2.json() == []

def test_delete_book_not_found():
    r = client.delete("/book/999")
    assert r.status_code == 200
    assert r.json() == {"error": "Book not found, deletion failed"}
