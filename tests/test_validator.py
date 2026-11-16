
import pandas as pd
import pytest

from app.validator import validate_transaction_file


def test_valid_transaction_file():

    df = pd.DataFrame({
        "Transaction ID": ["TXN001"],
        "Transaction Date": ["02-04-2025"],
        "Description": ["Grocery Store"],
        "Amount": [-2450],
        "Account Reference": ["ACC-1404"]
    })

    assert validate_transaction_file(df) is True


def test_invalid_transaction_file():

    df = pd.DataFrame({
        "Transaction ID": ["TXN001"],
        "Description": ["Grocery Store"]
    })

    with pytest.raises(ValueError):
        validate_transaction_file(df)
