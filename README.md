# Bank Transaction Processing System

A Python-based application that processes bank and credit transaction files in CSV and Excel formats.

## Features

- Reads CSV and Excel transaction files.
- Validates required transaction columns.
- Detects duplicate transactions using Transaction ID.
- Generates separate duplicate reports.
- Handles invalid files without stopping the entire process.
- Maintains separate bank and credit log files.
- Includes automated tests using pytest.

## Technologies Used

- Python 3.12
- Pandas
- OpenPyXL
- Pytest
- Git and GitHub

## Project Structure

```text
bank-transaction-processing-system/
│
├── app/
│   ├── processor.py
│   └── validator.py
│
├── tests/
│   ├── test_processor.py
│   └── test_validator.py
│
├── main.py
├── requirements.txt
├── pytest.ini
└── .gitignore
```

## Installation

Clone the repository:

```bash
git clone https://github.com/shakthimallesh2001/bank-transaction-processing-system.git
```

Navigate into the project:

```bash
cd bank-transaction-processing-system
```

Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Usage

Create an `input_file` folder in the project directory and place your transaction CSV or Excel files inside it.

Run the application:

```bash
python main.py
```

## Running Tests

```bash
python -m pytest -v
```

**Test Results:** 10 tests passed.

## Future Enhancements

- FastAPI backend integration
- PostgreSQL database integration
- Web-based transaction dashboard
- Transaction upload API
- Processing history and downloadable reports

## Author

**Shakthi D**

GitHub: https://github.com/shakthimallesh2001
