RESUME BUILDER SETUP INSTRUCTIONS
===============================

Prerequisites
------------
- Python 3.8 or higher
- MySQL 8.0 or higher
- Git

# Environment Setup

# Create and navigate to project directory
mkdir ResumeBuilder
cd ResumeBuilder

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt


2. MySQL Database Setup
---------------------
# Login to MySQL
mysql -u root -p

# Create database and user
CREATE DATABASE resumebuilder;
CREATE USER 'resumeuser'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON resumebuilder.* TO 'resumeuser'@'localhost';
FLUSH PRIVILEGES;


3. Environment Configuration
-------------------------
# Copy .env.template to .env
cp backend/.env.template backend/.env

# Edit .env with your values:
DB_HOST=localhost
DB_PORT=3306
DB_USER=resumeuser
DB_PASSWORD=your_password
DB_NAME=resumebuilder
OPENAI_API_KEY=your_openai_api_key
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
SECRET_KEY=your_secret_key


4. Database Initialization
------------------------
# Navigate to backend directory
cd backend

# Run database initialization script
python scripts/init_db.py


5. Database Migrations
-------------------
# Initialize alembic
alembic init migrations

# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Run migrations
alembic upgrade head


6. Running the Application
------------------------
# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000


7. Verification
-------------
1. Open your browser and go to: http://localhost:8000/docs
2. You should see the Swagger UI documentation
3. Test the health check endpoint: http://localhost:8000/api/v1/health


Project Structure
---------------
ResumeBuilder/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── middleware/
│   ├── scripts/
│   ├── migrations/
│   ├── tests/
│   ├── .env
│   ├── .env.template
│   ├── requirements.txt
│   └── alembic.ini
└── venv/


Common Issues and Solutions
-------------------------
1. MySQL Connection Issues:
   mysql -u root -p
   ALTER USER 'resumeuser'@'localhost' IDENTIFIED WITH mysql_native_password BY 'your_password';
   FLUSH PRIVILEGES;

2. Module Not Found Errors:
   pip install -e .

3. Permission Issues:
   sudo chmod -R 755 .


Development Commands
------------------
1. Running Tests:
   pytest

2. Code Style Checks:
   flake8

3. Code Formatting:
   black .

4. Updating Requirements:
   pip freeze > requirements.txt


Troubleshooting Tips
-------------------
1. Make sure MySQL service is running
2. Verify environment variables in .env file
3. Check database connection settings
4. Ensure all dependencies are installed
5. Verify Python version compatibility


Additional Resources
------------------
- FastAPI Documentation: https://fastapi.tiangolo.com/
- SQLAlchemy Documentation: https://docs.sqlalchemy.org/
- Alembic Documentation: https://alembic.sqlalchemy.org/
- MySQL Documentation: https://dev.mysql.com/doc/


Support
-------
For additional help or issues:
1. Check the project documentation
2. Submit an issue on GitHub
3. Contact the development team


Security Notes
-------------
1. Never commit .env file to version control
2. Regularly update dependencies
3. Use strong passwords
4. Keep MySQL and Python updated

END OF INSTRUCTIONS