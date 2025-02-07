import pyodbc
import os

# 📌 SQL Server Connection Settings
DB_SERVER = os.getenv("DB_SERVER", "localhost")
DB_NAME = os.getenv("DB_NAME", "GovalyltdDatabase")
DB_USER = os.getenv("DB_USER", "sa")
DB_PASSWORD = os.getenv("DB_PASSWORD", "MahinSQL12@")

# 📌 Function to Connect to SQL Server
def get_db_connection():
    try:
        conn = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={DB_SERVER};"
            f"DATABASE={DB_NAME};"
            f"UID={DB_USER};"
            f"PWD={DB_PASSWORD}",
            timeout=5
        )
        print("✅ Connected to SQL Server!")
        return conn
    except pyodbc.Error as e:
        print(f"❌ Connection failed: {e}")
        return None

# 📌 Create Orders Table
def setup_db():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Orders' AND xtype='U')
            CREATE TABLE Orders (
                id INT IDENTITY(1,1) PRIMARY KEY,
                consignment_id NVARCHAR(50) NOT NULL UNIQUE,
                order_id NVARCHAR(10),
                status NVARCHAR(100),
                status_on_slug NVARCHAR(20),
                time DATETIME 
            )
        """)
        conn.commit()
        conn.close()
        print("✅ Database setup complete!")
    else:
        print("❌ Database setup failed!")


