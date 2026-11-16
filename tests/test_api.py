
from fastapi.testclient import TestClient

from app.api import app


client = TestClient(app)


# Test 1: Home endpoint
def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "Running"


# Test 2: Health endpoint
def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


# Test 3: Valid CSV upload
def test_valid_csv_upload():
    csv_content = (
        "Transaction ID,Transaction Date,Description,Amount,Account Reference\n"
        "TXN001,02-04-2025,Grocery Store,-2450,ACC-1404\n"
        "TXN002,03-04-2025,Shopping,-1500,ACC-1404\n"
    )

    response = client.post(
        "/upload",
        files={
            "file": (
                "Bank-1404-Transaction.csv",
                csv_content,
                "text/csv"
            )
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert data["total_transactions"] == 2
    assert data["duplicate_transactions"] == 0
    assert data["unique_transaction_ids"] == 2
    assert data["non_duplicate_transactions"] == 2


# Test 4: Duplicate transaction detection
def test_duplicate_csv_upload():
    csv_content = (
        "Transaction ID,Transaction Date,Description,Amount,Account Reference\n"
        "TXN001,02-04-2025,Grocery Store,-2450,ACC-1404\n"
        "TXN001,02-04-2025,Grocery Store,-2450,ACC-1404\n"
        "TXN002,03-04-2025,Shopping,-1500,ACC-1404\n"
    )

    response = client.post(
        "/upload",
        files={
            "file": (
                "Bank-1404-Duplicate.csv",
                csv_content,
                "text/csv"
            )
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_transactions"] == 3
    assert data["duplicate_transactions"] == 2
    assert data["unique_transaction_ids"] == 2
    assert data["non_duplicate_transactions"] == 1


# Test 5: Invalid CSV upload
def test_invalid_csv_upload():
    csv_content = "Name,City\nShakthi,Chennai\n"

    response = client.post(
        "/upload",
        files={
            "file": (
                "Bank-1404-Error.csv",
                csv_content,
                "text/csv"
            )
        }
    )

    assert response.status_code == 400
    assert "Missing columns" in response.json()["detail"]


# Test 6: Unsupported file format
def test_unsupported_file_upload():
    response = client.post(
        "/upload",
        files={
            "file": (
                "transactions.txt",
                "Some transaction data",
                "text/plain"
            )
        }
    )

    assert response.status_code == 400
    assert "Only CSV and Excel files are supported" in response.json()["detail"]
