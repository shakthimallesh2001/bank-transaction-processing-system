
import os
import re
import pandas as pd
import logging

# ==========================================
# 1. CREATE REQUIRED FOLDERS
# ==========================================

os.makedirs("Log/bank", exist_ok=True)
os.makedirs("Log/credit", exist_ok=True)
os.makedirs("duplicate_reports", exist_ok=True)


# ==========================================
# 2. CONFIGURE BANK LOGGER
# ==========================================

bank_logger = logging.getLogger("bank")
bank_logger.setLevel(logging.INFO)

if not bank_logger.handlers:
    bank_handler = logging.FileHandler("Log/bank/bank.log")
    bank_logger.addHandler(bank_handler)


# ==========================================
# 3. CONFIGURE CREDIT LOGGER
# ==========================================

credit_logger = logging.getLogger("credit")
credit_logger.setLevel(logging.INFO)

if not credit_logger.handlers:
    credit_handler = logging.FileHandler("Log/credit/credit.log")
    credit_logger.addHandler(credit_handler)


# ==========================================
# 4. DEFINE INPUT AND OUTPUT FOLDERS
# ==========================================

folder_path = "input_file"
output_folder = "duplicate_reports"


# ==========================================
# 5. REQUIRED TRANSACTION COLUMNS
# ==========================================

required_columns = [
    "Transaction ID",
    "Transaction Date",
    "Description",
    "Amount",
    "Account Reference"
]


# ==========================================
# 6. GET ALL INPUT FILES
# ==========================================

files = os.listdir(folder_path)

print("Current working directory:", os.getcwd())
print("Files found:", files)


# ==========================================
# 7. PROCESS EACH FILE
# ==========================================

for file in files:

    file_path = os.path.join(folder_path, file)

    # Extract 4-digit number from filename
    match = re.search(r'\d{4}', file)

    if not match:
        continue

    number = match.group()

    # Identify bank or credit file
    if "bank" in file.lower():
        logger = bank_logger

    elif "credit" in file.lower():
        logger = credit_logger

    else:
        continue

    print("\n==========================================")
    print("File Name:", file)
    print("Extracted Number:", number)

    logger.info(f"Processing file: {file}")

    try:

        # ==========================================
        # 8. READ CSV OR EXCEL FILE
        # ==========================================

        if file.lower().endswith(".csv"):
            df = pd.read_csv(file_path)

        elif file.lower().endswith((".xlsx", ".xls")):
            df = pd.read_excel(file_path)

        else:
            print("Unsupported file format:", file)
            continue

        # ==========================================
        # 9. VALIDATE REQUIRED COLUMNS
        # ==========================================

        missing_columns = [
            column for column in required_columns
            if column not in df.columns
        ]

        if missing_columns:
            raise ValueError(
                f"Invalid transaction file. Missing columns: {missing_columns}"
            )

        print("File validation successful")

        # ==========================================
        # 10. FIND DUPLICATE TRANSACTIONS
        # ==========================================

        duplicates = df[
            df.duplicated(
                subset=["Transaction ID"],
                keep=False
            )
        ]

        if not duplicates.empty:

            print("\nDuplicate Transactions Found:")
            print(duplicates)

            # ==========================================
            # 11. SAVE DUPLICATES INTO CSV REPORT
            # ==========================================

            report_name = (
                os.path.splitext(file)[0] + "-duplicates.csv"
            )

            report_path = os.path.join(
                output_folder,
                report_name
            )

            duplicates.to_csv(
                report_path,
                index=False
            )

            print("\nDuplicate report saved:", report_path)

            logger.warning(
                f"Duplicate transactions found in {file}"
            )

        else:

            print("No Duplicate Transactions Found")

        # ==========================================
        # 12. DISPLAY FILE DATA
        # ==========================================

        print("\nFile Data:")
        print(df)

        logger.info(
            f"Successfully processed file: {file}"
        )

    except Exception as e:

        print(f"Error processing {file}: {e}")

        logger.exception(
            f"Error processing file {file}: {e}"
        )


# ==========================================
# 13. PROCESSING COMPLETED
# ==========================================

print("\n==========================================")
print("All files processed!")
print("Duplicate reports folder:", output_folder)
print("==========================================")
