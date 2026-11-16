
import os
import re
import logging
import pandas as pd

from app.validator import validate_transaction_file


# 1. Configure loggers
def setup_loggers(log_folder="Log"):

    os.makedirs(os.path.join(log_folder, "bank"), exist_ok=True)
    os.makedirs(os.path.join(log_folder, "credit"), exist_ok=True)

    bank_logger = logging.getLogger("bank")
    bank_logger.setLevel(logging.INFO)
    bank_logger.propagate = False

    credit_logger = logging.getLogger("credit")
    credit_logger.setLevel(logging.INFO)
    credit_logger.propagate = False

    if not bank_logger.handlers:
        bank_handler = logging.FileHandler(
            os.path.join(log_folder, "bank", "bank.log"),
            encoding="utf-8"
        )
        bank_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s"
            )
        )
        bank_logger.addHandler(bank_handler)

    if not credit_logger.handlers:
        credit_handler = logging.FileHandler(
            os.path.join(log_folder, "credit", "credit.log"),
            encoding="utf-8"
        )
        credit_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s"
            )
        )
        credit_logger.addHandler(credit_handler)

    return bank_logger, credit_logger


# 2. Read transaction files
def read_transaction_file(file_path):

    if file_path.lower().endswith(".csv"):
        return pd.read_csv(file_path)

    elif file_path.lower().endswith((".xlsx", ".xls")):
        return pd.read_excel(file_path)

    else:
        raise ValueError("Unsupported file format")


# 3. Process an individual file
def process_file(file_path, output_folder, logger):

    file_name = os.path.basename(file_path)

    logger.info(f"Processing file: {file_name}")

    print("\n==========================================")
    print("File Name:", file_name)

    try:
        match = re.search(r"\d{4}", file_name)

        if not match:
            print("No four-digit number found. Skipping file.")
            return

        number = match.group()
        print("Extracted Number:", number)

        df = read_transaction_file(file_path)

        validate_transaction_file(df)

        print("File validation successful")

        duplicates = df[
            df.duplicated(
                subset=["Transaction ID"],
                keep=False
            )
        ]

        if not duplicates.empty:

            print("\nDuplicate Transactions Found:")
            print(duplicates)

            report_name = (
                os.path.splitext(file_name)[0] + "-duplicates.csv"
            )

            report_path = os.path.join(
                output_folder,
                report_name
            )

            duplicates.to_csv(report_path, index=False)

            print("\nDuplicate report saved:", report_path)

            logger.warning(
                f"Duplicate transactions found in {file_name}"
            )

        else:
            print("No Duplicate Transactions Found")

        print("\nFile Data:")
        print(df)

        logger.info(
            f"Successfully processed file: {file_name}"
        )

    except Exception as error:

        print(f"Error processing {file_name}: {error}")

        logger.exception(
            f"Error processing file {file_name}: {error}"
        )


# 4. Process all transaction files
def process_all_files(
    input_folder="input_file",
    output_folder="duplicate_reports",
    log_folder="Log"
):

    os.makedirs(output_folder, exist_ok=True)

    bank_logger, credit_logger = setup_loggers(log_folder)

    if not os.path.isdir(input_folder):
        raise FileNotFoundError(
            f"Input folder not found: {input_folder}"
        )

    files = os.listdir(input_folder)

    print("Current working directory:", os.getcwd())
    print("Files found:", files)

    for file in files:

        file_path = os.path.join(input_folder, file)

        if not os.path.isfile(file_path):
            continue

        if "bank" in file.lower():
            logger = bank_logger

        elif "credit" in file.lower():
            logger = credit_logger

        else:
            continue

        process_file(file_path, output_folder, logger)

    print("\n==========================================")
    print("All files processed!")
    print("Duplicate reports folder:", output_folder)
    print("==========================================")
