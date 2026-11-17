
import os
from io import BytesIO
from decimal import Decimal

import pandas as pd

from fastapi import (
    FastAPI,
    File,
    HTTPException,
    UploadFile,
    Depends
)

from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.processor import process_uploaded_dataframe
from app.database import get_db
from app.models import Transaction, ProcessingHistory


app = FastAPI(
    title="Bank Transaction Processing System API",
    description="API for validating and processing bank transaction files.",
    version="1.0.0"
)


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Home endpoint
@app.get("/")
def home():
    return {
        "message": "Welcome to Bank Transaction Processing System API",
        "status": "Running"
    }


# Health check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "Bank Transaction Processing System"
    }


# Get all transactions
@app.get("/transactions")
def get_transactions(db: Session = Depends(get_db)):

    transactions = (
        db.query(Transaction)
        .order_by(Transaction.id.desc())
        .all()
    )

    return [
        {
            "id": transaction.id,
            "transaction_id": transaction.transaction_id,
            "transaction_date": transaction.transaction_date,
            "description": transaction.description,
            "amount": transaction.amount,
            "account_reference": transaction.account_reference,
            "source_file": transaction.source_file,
            "is_duplicate": transaction.is_duplicate
        }
        for transaction in transactions
    ]


# Get processing history
@app.get("/processing-history")
def get_processing_history(db: Session = Depends(get_db)):

    history_records = (
        db.query(ProcessingHistory)
        .order_by(ProcessingHistory.id.desc())
        .all()
    )

    return [
        {
            "id": record.id,
            "file_name": record.file_name,
            "uploaded_at": record.uploaded_at,
            "total_transactions": record.total_transactions,
            "duplicate_transactions": record.duplicate_transactions,
            "status": record.status,
            "message": record.message
        }
        for record in history_records
    ]


# Upload and process transaction file
@app.post("/upload")
async def upload_transaction_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file selected."
        )

    file_name = os.path.basename(file.filename)

    try:

        contents = await file.read()

        if not contents:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty."
            )

        file_data = BytesIO(contents)

        # Read CSV or Excel file
        if file_name.lower().endswith(".csv"):
            df = pd.read_csv(file_data)

        elif file_name.lower().endswith((".xlsx", ".xls")):
            df = pd.read_excel(file_data)

        else:
            raise HTTPException(
                status_code=400,
                detail="Only CSV and Excel files are supported."
            )

        # Process uploaded data
        result = process_uploaded_dataframe(
            df=df,
            file_name=file_name
        )

        # Identify duplicate transactions
        duplicate_mask = df.duplicated(
            subset=["Transaction ID"],
            keep=False
        )

        # Prepare transactions for PostgreSQL
        transactions = []

        for index, row in df.iterrows():

            if row[
                [
                    "Transaction ID",
                    "Transaction Date",
                    "Description",
                    "Amount",
                    "Account Reference"
                ]
            ].isna().any():

                raise ValueError(
                    "Transaction file contains missing required values."
                )

            transaction = Transaction(
                transaction_id=str(row["Transaction ID"]),

                transaction_date=pd.to_datetime(
                    row["Transaction Date"],
                    dayfirst=True
                ).date(),

                description=str(row["Description"]),

                amount=Decimal(str(row["Amount"])),

                account_reference=str(row["Account Reference"]),

                source_file=file_name,

                is_duplicate=bool(duplicate_mask.iloc[index])
            )

            transactions.append(transaction)

        # Save transactions
        db.add_all(transactions)

        # Save successful processing history
        history = ProcessingHistory(
            file_name=file_name,
            total_transactions=result["total_transactions"],
            duplicate_transactions=result["duplicate_transactions"],
            status="Success",
            message="File processed and saved successfully."
        )

        db.add(history)

        db.commit()

        return {
            "status": "success",
            "message": "File uploaded, processed and saved to database successfully.",
            "file_name": file_name,
            "stored_transactions": len(transactions),
            **result
        }

    except HTTPException as error:

        db.rollback()

        # Record failed upload
        try:

            history = ProcessingHistory(
                file_name=file_name,
                status="Failed",
                message=str(error.detail)
            )

            db.add(history)
            db.commit()

        except Exception:
            db.rollback()

        raise

    except Exception as error:

        db.rollback()

        # Record failed upload
        try:

            history = ProcessingHistory(
                file_name=file_name,
                status="Failed",
                message=str(error)
            )

            db.add(history)
            db.commit()

        except Exception:
            db.rollback()

        raise HTTPException(
            status_code=400,
            detail=f"Unable to process file: {str(error)}"
        )

    finally:
        await file.close()
