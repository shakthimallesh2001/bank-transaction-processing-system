
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from fastapi.testclient import TestClient

from app.api import app
from app.database import Base, get_db
from app.models import Transaction


# Temporary SQLite database for API tests
test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)

Base.metadata.create_all(bind=test_engine)


# Override PostgreSQL database with temporary SQLite database
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


# Clear test database before every test
@pytest.fixture(autouse=True)
def clear_test_database():
    db = TestingSessionLocal()
    db.query(Transaction).delete()
    db.commit()
    db.close()


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


# Test 7: Verify transactions are stored in database
def test_transactions_saved_to_database():
    csv_content = (
        "Transaction ID,Transaction Date,Description,Amount,Account Reference\n"
        "TXN101,02-04-2025,Grocery Store,-2450,ACC-1404\n"
        "TXN102,03-04-2025,Shopping,-1500,ACC-1404\n"
    )

    response = client.post(
        "/upload",
        files={
            "file": (
                "Bank-1404-Storage.csv",
                csv_content,
                "text/csv"
            )
        }
    )

    assert response.status_code == 200
    assert response.json()["stored_transactions"] == 2

    db = TestingSessionLocal()

    try:
        transactions = db.query(Transaction).all()

        assert len(transactions) == 2
        assert transactions[0].transaction_id == "TXN101"
        assert transactions[1].transaction_id == "TXN102"
    finally:
        db.close()


# Test 8: Verify duplicate flags in database
def test_duplicate_flags_saved_to_database():
    csv_content = (
        "Transaction ID,Transaction Date,Description,Amount,Account Reference\n"
        "TXN201,02-04-2025,Grocery Store,-2450,ACC-1404\n"
        "TXN201,02-04-2025,Grocery Store,-2450,ACC-1404\n"
        "TXN202,03-04-2025,Shopping,-1500,ACC-1404\n"
    )

    response = client.post(
        "/upload",
        files={
            "file": (
                "Bank-1404-Database-Duplicate.csv",
                csv_content,
                "text/csv"
            )
        }
    )

    assert response.status_code == 200

    db = TestingSessionLocal()

    try:
        transactions = (
            db.query(Transaction)
            .order_by(Transaction.id)
            .all()
        )

        assert len(transactions) == 3
        assert transactions[0].is_duplicate is True
        assert transactions[1].is_duplicate is True
        assert transactions[2].is_duplicate is False
    finally:
        db.close()


# Test 9: Invalid file should not save transactions
def test_invalid_file_not_saved_to_database():
    csv_content = "Name,City\nTest,Chennai\n"

    response = client.post(
        "/upload",
        files={
            "file": (
                "Bank-1404-Invalid.csv",
                csv_content,
                "text/csv"
            )
        }
    )

    assert response.status_code == 400

    db = TestingSessionLocal()

    try:
        assert db.query(Transaction).count() == 0
    finally:
        db.close()
