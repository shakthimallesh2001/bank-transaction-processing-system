
# 🏦 Bank Transaction Processing System

A Python-based Bank Transaction Processing System that validates, processes, and manages bank transaction files using **FastAPI, PostgreSQL, Pandas, and a web-based dashboard**.

The application supports CSV and Excel uploads, transaction validation, duplicate detection, database storage, processing history, and transaction reporting.

## 🚀 Features

- **Transaction File Upload:** Upload CSV and Excel transaction files.
- **Data Validation:** Validate required transaction columns and data.
- **Duplicate Detection:** Identify duplicate transactions using Transaction ID.
- **Duplicate Reports:** Generate downloadable duplicate transaction reports.
- **PostgreSQL Integration:** Store processed transactions in a relational database.
- **REST API:** Manage transaction uploads and retrieve transaction records using FastAPI.
- **Dashboard:** View transaction statistics and recent transactions.
- **Transaction History:** View previously processed transactions.
- **Processing History:** Track successful and failed file uploads.
- **Logging:** Maintain separate bank and credit transaction logs.
- **Automated Testing:** Verify application functionality using pytest.

## 📸 Application Screenshots

### Dashboard

![Bank Transaction Processing Dashboard](screenshots/dashboard.png)

### Processing History

![Transaction Processing History](screenshots/processing-history.png)

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.12 | Backend development |
| FastAPI | REST API development |
| Pandas | Data processing and analysis |
| PostgreSQL | Database management |
| SQLAlchemy | Database ORM |
| OpenPyXL | Excel file handling |
| HTML, CSS, JavaScript | Frontend dashboard |
| Pytest | Automated testing |
| Git & GitHub | Version control |

## 📂 Project Structure

```text
bank-transaction-processing-system/
│
├── app/
│   ├── __init__.py
│   ├── api.py
│   ├── database.py
│   ├── models.py
│   ├── processor.py
│   └── validator.py
│
├── frontend/
│   └── index.html
│
├── tests/
│   ├── test_api.py
│   ├── test_processor.py
│   └── test_validator.py
│
├── screenshots/
│   ├── dashboard.png
│   └── processing-history.png
│
├── input_file/
├── duplicate_reports/
├── Log/
│
├── main.py
├── pytest.ini
├── requirements.txt
└── .gitignore
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/shakthimallesh2001/bank-transaction-processing-system.git
```

### 2. Navigate to the project directory

```bash
cd bank-transaction-processing-system
```

### 3. Create a virtual environment

```powershell
python -m venv .venv
```

### 4. Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
python -m pip install -r requirements.txt
```

## 🗄️ Database Configuration

This project uses PostgreSQL.

1. Install PostgreSQL.
2. Create a database named `bank_transactions`.
3. Create a `.env` file in the project root directory.
4. Configure your database connection:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=bank_transactions
DB_USER=postgres
DB_PASSWORD=your_postgres_password
```

Replace the password with your own PostgreSQL password.

**Security:** Never upload your `.env` file or database credentials to GitHub.

## ▶️ Running the Application

### Start the FastAPI backend

```bash
uvicorn app.api:app --reload
```

Backend URL:

http://127.0.0.1:8000

### Access API documentation

FastAPI provides interactive API documentation through Swagger UI:

http://127.0.0.1:8000/docs

### Start the frontend dashboard

Open another terminal and run:

```bash
python -m http.server 5500
```

Open the dashboard:

http://127.0.0.1:5500/frontend/

### Run the original file-processing application

Place transaction files inside the `input_file` directory and execute:

```bash
python main.py
```

## 🔗 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Check API status |
| GET | `/health` | Health check |
| POST | `/upload` | Upload and process transaction files |
| GET | `/transactions` | Retrieve transaction records |
| GET | `/processing-history` | Retrieve processing history |

## 🧪 Running Automated Tests

Run the complete test suite:

```bash
python -m pytest -v
```

### Test Results

**22 tests passed successfully.**

The automated tests cover:

- API endpoints
- CSV file uploads
- Duplicate transaction detection
- Database storage
- File validation
- Processing history
- Transaction processing

## 🏗️ Application Architecture

The application consists of three main layers:

1. **Frontend:** Web dashboard built using HTML, CSS, and JavaScript.
2. **Backend:** FastAPI application responsible for file uploads, validation, and processing.
3. **Database:** PostgreSQL database managed through SQLAlchemy.

## 🔮 Future Enhancements

- Cloud deployment
- User authentication and authorization
- Advanced transaction analytics
- Improved error monitoring
- Real-time processing notifications

## 👩‍💻 Author

**Shakthi D**

GitHub: https://github.com/shakthimallesh2001

---

⭐ If you find this project interesting, feel free to explore the repository!
