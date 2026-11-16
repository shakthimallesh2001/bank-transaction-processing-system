
import logging

import pandas as pd
import pytest

from app.processor import (
    setup_loggers,
    read_transaction_file,
    process_file,
    process_all_files
)


# Test 1: Read CSV file
def test_read_csv_file(tmp_path):

    file_path = tmp_path / "Bank-1404-Transaction.csv"

    df = pd.DataFrame({
        "Transaction ID": ["TXN001"],
        "Transaction Date": ["02-04-2025"],
        "Description": ["Grocery Store"],
        "Amount": [-2450],
        "Account Reference": ["ACC-1404"]
    })

    df.to_csv(file_path, index=False)

    result = read_transaction_file(file_path)

    assert len(result) == 1
    assert result.iloc[0]["Transaction ID"] == "TXN001"


# Test 2: Read Excel file
def test_read_excel_file(tmp_path):

    file_path = tmp_path / "Bank-1404-Transaction.xlsx"

    df = pd.DataFrame({
        "Transaction ID": ["TXN001"],
        "Transaction Date": ["02-04-2025"],
        "Description": ["Grocery Store"],
        "Amount": [-2450],
        "Account Reference": ["ACC-1404"]
    })

    df.to_excel(file_path, index=False)

    result = read_transaction_file(file_path)

    assert len(result) == 1
    assert result.iloc[0]["Transaction ID"] == "TXN001"


# Test 3: Reject unsupported file format
def test_unsupported_file_format():

    with pytest.raises(ValueError):
        read_transaction_file("transactions.txt")


# Test 4: Detect duplicate transactions
def test_duplicate_transactions(tmp_path, capsys):

    file_path = tmp_path / "Bank-1404-Duplicate.csv"
    output_folder = tmp_path / "reports"
    output_folder.mkdir()

    df = pd.DataFrame({
        "Transaction ID": ["TXN001", "TXN002", "TXN001"],
        "Transaction Date": ["02-04-2025", "05-04-2025", "02-04-2025"],
        "Description": ["Grocery", "Salary", "Grocery"],
        "Amount": [-2450, 45000, -2450],
        "Account Reference": ["ACC-1404", "ACC-1404", "ACC-1404"]
    })

    df.to_csv(file_path, index=False)

    logger = logging.getLogger("test_processor_duplicates")

    process_file(str(file_path), str(output_folder), logger)

    report_path = output_folder / "Bank-1404-Duplicate-duplicates.csv"

    assert report_path.exists()

    report = pd.read_csv(report_path)

    assert len(report) == 2

    captured = capsys.readouterr()

    assert "Duplicate Transactions Found" in captured.out


# Test 5: Handle invalid transaction file
def test_invalid_transaction_file(tmp_path, capsys):

    file_path = tmp_path / "Bank-1404-Error.csv"
    output_folder = tmp_path / "reports"
    output_folder.mkdir()

    file_path.write_text(
        "This is not a valid transaction file",
        encoding="utf-8"
    )

    logger = logging.getLogger("test_processor_invalid")

    process_file(str(file_path), str(output_folder), logger)

    captured = capsys.readouterr()

    assert "Error processing" in captured.out


# Test 6: Skip file without four-digit number
def test_skip_file_without_number(tmp_path, capsys):

    file_path = tmp_path / "Bank-Transaction.csv"
    output_folder = tmp_path / "reports"
    output_folder.mkdir()

    df = pd.DataFrame({
        "Transaction ID": ["TXN001"],
        "Transaction Date": ["02-04-2025"],
        "Description": ["Grocery"],
        "Amount": [-2450],
        "Account Reference": ["ACC-1404"]
    })

    df.to_csv(file_path, index=False)

    logger = logging.getLogger("test_processor_skip")

    process_file(str(file_path), str(output_folder), logger)

    captured = capsys.readouterr()

    assert "No four-digit number found" in captured.out


# Test 7: Raise error when input folder is missing
def test_missing_input_folder(tmp_path):

    missing_folder = tmp_path / "missing_input"

    with pytest.raises(FileNotFoundError):
        process_all_files(
            input_folder=str(missing_folder),
            output_folder=str(tmp_path / "reports"),
            log_folder=str(tmp_path / "logs")
        )


# Test 8: Create separate bank and credit log folders
def test_setup_loggers(tmp_path):

    bank_logger, credit_logger = setup_loggers(
        str(tmp_path / "logs")
    )

    assert bank_logger.name == "bank"
    assert credit_logger.name == "credit"

    assert (tmp_path / "logs" / "bank").is_dir()
    assert (tmp_path / "logs" / "credit").is_dir()
