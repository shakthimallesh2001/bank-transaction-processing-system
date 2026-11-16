
# ==========================================
# TRANSACTION FILE VALIDATOR
# ==========================================

REQUIRED_COLUMNS = [
    "Transaction ID",
    "Transaction Date",
    "Description",
    "Amount",
    "Account Reference"
]


def validate_transaction_file(df):
    """
    Validate whether a transaction DataFrame
    contains all required columns.
    """

    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Invalid transaction file. Missing columns: {missing_columns}"
        )

    return True
