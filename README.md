# GX_Project

### Prerequisites

1. Python 3.x
2. MSSQL Server

### Dependencies

```
pip install pymssql SQLAlchemy great_expectations python-dotenv
```

### Installation

1. Set up MSSQL "AdventureWorks2012" database locally
2. Create user in MSSQL to connect from Python  
3. Install Microsoft ODBC driver for SQL
4. Clone the repository to your local machine

```
git clone
https://github.com/HannaTsyhan/GX_Project.git
```

Create .env file in the root project directory with your MSSQL user credentials

```
USERID=your_user
PASSWORD=your_user_password
```

### Running tests:

To execute run main.py  
