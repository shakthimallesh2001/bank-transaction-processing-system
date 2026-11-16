
import os
from io import BytesIO

import pandas as pd
from fastapi import FastAPI, File, HTTPException, UploadFile

from app.processor import process_uploaded_dataframe


app = FastAPI(
    title="Bank Transaction Processing System API",
    description="API for validating and processing bank transaction files.",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to Bank Transaction Processing System API",
        "status": "Running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "Bank Transaction Processing System"
    }


@app.post("/upload")
async def upload_transaction_file(file: UploadFile = File(...)):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file selected."
        )

    file_name = os.path.basename(file.filename)
    file_extension = file_name.lower()

    try:
        contents = await file.read()

        if not contents:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty."
            )

        file_data = BytesIO(contents)

        if file_extension.endswith(".csv"):
            df = pd.read_csv(file_data)

        elif file_extension.endswith((".xlsx", ".xls")):
            df = pd.read_excel(file_data)

        else:
            raise HTTPException(
                status_code=400,
                detail="Only CSV and Excel files are supported."
            )

        # Process uploaded data using existing processor
        result = process_uploaded_dataframe(
            df=df,
            file_name=file_name
        )

        return {
            "status": "success",
            "message": "File uploaded and processed successfully.",
            "file_name": file_name,
            **result
        }

    except HTTPException:
        raise

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=f"Unable to process file: {str(error)}"
        )

    finally:
        await file.close()
